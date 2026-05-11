"""Core runtime command handlers for .NeoN."""

from __future__ import annotations

import argparse
import json
import shutil
import sqlite3
from pathlib import Path

from neon.artifact import VERSION, canonical_bytes, read_json, utc_now, validate_artifact, write_json
from neon.cas import cas_path, cas_uri, parse_cas_uri, sha256_bytes, sha256_file
from neon.lifecycle import make_artifact, resolve_artifact_path, save_artifact
from neon.metrics import summarize_metrics
from neon.storage import connect, db_path, init_db, objects_root, require_vault_dirs, vault_root
from neon.topology import ancestry_chain, artifact_metrics, descendant_chain
from neon.verification import proof_packet_manifest, verify_artifact_file, verify_proof_packet


def object_path(digest: str) -> Path:
    return cas_path(objects_root(), digest)


def cmd_doctor(args: argparse.Namespace) -> None:
    checks = [
        ("vault", vault_root().exists()),
        ("database", db_path().exists()),
        ("artifacts", (vault_root() / "artifacts").is_dir()),
        ("exports", (vault_root() / "exports").is_dir()),
        ("objects", objects_root().is_dir()),
    ]
    ok = True
    for name, passed in checks:
        print(f"{'✓' if passed else '✗'} {name}")
        ok = ok and passed
    if not ok:
        raise SystemExit(1)
    print("doctor ok")


def cmd_init(args: argparse.Namespace) -> None:
    require_vault_dirs()
    conn = sqlite3.connect(db_path())
    init_db(conn)
    conn.close()
    identity = vault_root() / "identity.json"
    if not identity.exists():
        write_json(identity, {"neon_version": VERSION, "kind": "identity", "name": None})
    print(f"initialized {vault_root()}")


def cmd_register(args: argparse.Namespace) -> None:
    data = make_artifact(args.title, args.creator, args.type, args.statement)
    out, digest = save_artifact(data)
    print(data["artifact_id"])
    print(out)
    print(digest)


def cmd_derive(args: argparse.Namespace) -> None:
    parent_path = resolve_artifact_path(args.parent)
    parent = read_json(parent_path)
    parent_errors = validate_artifact(parent)
    if parent_errors:
        raise SystemExit("Parent artifact is invalid: " + "; ".join(parent_errors))

    data = make_artifact(args.title, args.creator, args.type, args.statement, [parent["artifact_id"]])
    out, digest = save_artifact(data)

    conn = connect()
    conn.execute(
        "INSERT INTO edges VALUES (?, ?, ?, ?)",
        (parent["artifact_id"], data["artifact_id"], "derived_from", utc_now()),
    )
    conn.commit()
    conn.close()

    print(data["artifact_id"])
    print(f"parent {parent['artifact_id']}")
    print(out)
    print(digest)


def cmd_validate(args: argparse.Namespace) -> None:
    ok, errors = verify_artifact_file(Path(args.artifact))
    print("VALID" if ok else "INVALID")
    if errors:
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    data = read_json(Path(args.artifact))
    print(data["artifact_id"])
    print(sha256_file(Path(args.artifact)))


def cmd_hash(args: argparse.Namespace) -> None:
    data = read_json(Path(args.artifact))
    print(sha256_bytes(canonical_bytes(data)))


def cmd_store(args: argparse.Namespace) -> None:
    data = read_json(Path(args.artifact))
    raw = canonical_bytes(data)
    digest = sha256_bytes(raw)

    out = object_path(digest)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)

    conn = connect()
    conn.execute(
        "INSERT OR REPLACE INTO cas_objects VALUES (?, ?, ?, ?)",
        (digest, cas_uri(digest), str(out), utc_now()),
    )
    conn.commit()
    conn.close()

    print(cas_uri(digest))
    print(out)


def cmd_fetch(args: argparse.Namespace) -> None:
    digest = parse_cas_uri(args.uri)
    path = object_path(digest)
    if not path.exists():
        raise SystemExit(f"Object not found: {args.uri}")
    if args.out:
        dest = Path(args.out)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
        print(dest)
        return
    print(path.read_text(encoding="utf-8"))


def cmd_export(args: argparse.Namespace) -> None:
    artifact = resolve_artifact_path(args.artifact)
    data = read_json(artifact)
    errors = validate_artifact(data)
    if errors:
        raise SystemExit("Cannot export invalid artifact: " + "; ".join(errors))

    digest = sha256_file(artifact)
    out = vault_root() / "exports" / f"{artifact.stem}-proof"
    out.mkdir(parents=True, exist_ok=True)
    shutil.copy2(artifact, out / "artifact.neon")

    manifest = proof_packet_manifest(
        version=VERSION,
        artifact_id=data["artifact_id"],
        artifact_sha256=digest,
        exported_at=utc_now(),
        parents=data["lineage"].get("parents", []),
    )

    write_json(out / "manifest.json", manifest)
    write_json(out / "lineage.json", data["lineage"])
    (out / "hashes.txt").write_text(f"{digest}  artifact.neon\n", encoding="utf-8")
    (out / "SUMMARY.md").write_text(
        f"# .NeoN Proof Packet\n\nArtifact: {data['title']}\n\nID: {data['artifact_id']}\n\nSHA-256: {digest}\n",
        encoding="utf-8",
    )
    write_json(out / "verification.json", {"status": "created", "artifact_sha256": digest, "checked_at": utc_now()})
    print(out)


def cmd_verify(args: argparse.Namespace) -> None:
    target = Path(args.target)
    if target.is_dir():
        ok = verify_proof_packet(target)
        print("verified" if ok else "failed")
        if not ok:
            raise SystemExit(1)
        return

    ok, errors = verify_artifact_file(target)
    print("verified" if ok else "failed")
    if errors:
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)


def cmd_graph(args: argparse.Namespace) -> None:
    data = read_json(resolve_artifact_path(args.artifact))
    parents = data["lineage"].get("parents", [])
    if args.format == "json":
        print(json.dumps({"artifact_id": data["artifact_id"], "parents": parents}, indent=2))
        return
    print("graph TD")
    node = data["artifact_id"].replace(".N/", "N_")
    if not parents:
        print(f"  {node}")
    for parent in parents:
        print(f"  {parent.replace('.N/', 'N_')} --> {node}")


def cmd_lineage(args: argparse.Namespace) -> None:
    start = Path(args.artifact)
    if not start.exists():
        start = resolve_artifact_path(args.artifact)
    chain = ancestry_chain(start, Path(args.root))
    if args.format == "json":
        print(json.dumps(chain, indent=2))
        return
    for index, item in enumerate(chain):
        prefix = "->" if index else "  "
        print(f"{prefix} {item['artifact_id']} | {item['title']}")


def cmd_descendants(args: argparse.Namespace) -> None:
    start = Path(args.artifact)
    if not start.exists():
        start = resolve_artifact_path(args.artifact)
    chain = descendant_chain(start, Path(args.root))
    if args.format == "json":
        print(json.dumps(chain, indent=2))
        return
    for item in chain:
        print(f"-> {item['artifact_id']} | {item['title']}")


def cmd_metrics(args: argparse.Namespace) -> None:
    start = Path(args.artifact)
    if not start.exists():
        start = resolve_artifact_path(args.artifact)
    metrics = artifact_metrics(start, Path(args.root))
    if args.format == "json":
        print(json.dumps({
            "artifact_id": metrics.artifact_id,
            "parent_count": metrics.parent_count,
            "child_count": metrics.child_count,
            "ancestor_count": metrics.ancestor_count,
            "descendant_count": metrics.descendant_count,
            "lineage_depth": metrics.lineage_depth,
            "continuity_vector": metrics.continuity_vector,
            "pressure_vector": metrics.pressure_vector,
            "derivation_ratio": metrics.derivation_ratio,
            "influence_ratio": metrics.influence_ratio,
        }, indent=2))
        return
    print(summarize_metrics(metrics))


def cmd_demo(args: argparse.Namespace) -> None:
    cmd_init(argparse.Namespace())

    root = make_artifact("Demo Creator Root", args.creator, "creator_identity", "Demo creator continuity root")
    root_path, _ = save_artifact(root)

    workflow = make_artifact("Demo Workflow", args.creator, "workflow", "Original reusable workflow", [root["artifact_id"]])
    workflow_path, _ = save_artifact(workflow)

    derived = make_artifact("Demo AI Assisted Workflow", args.creator, "workflow", "Workflow derived with AI assistance", [workflow["artifact_id"]])
    derived_path, _ = save_artifact(derived)

    cmd_store(argparse.Namespace(artifact=str(derived_path)))
    cmd_export(argparse.Namespace(artifact=str(derived_path)))
    proof_dir = vault_root() / "exports" / f"{derived_path.stem}-proof"
    cmd_verify(argparse.Namespace(target=str(proof_dir)))

    print("\nDemo continuity loop complete")
    print(f"root: {root_path}")
    print(f"workflow: {workflow_path}")
    print(f"derived: {derived_path}")
    print(f"proof: {proof_dir}")
    print("\nMetrics:")
    cmd_metrics(argparse.Namespace(artifact=str(derived_path), root=str(vault_root() / "artifacts"), format="text"))
    print("\nInspect:")
    print(f"neon lineage {derived_path} --root {vault_root() / 'artifacts'}")
    print(f"neon descendants {root_path} --root {vault_root() / 'artifacts'}")
    print(f"neon metrics {derived_path} --root {vault_root() / 'artifacts'}")
    print(f"neon graph {derived_path}")


def cmd_log(args: argparse.Namespace) -> None:
    data = read_json(resolve_artifact_path(args.artifact))
    print(data["title"])
    print(data["artifact_id"])
    print("parents", ", ".join(data["lineage"].get("parents", [])) or "none")
    for event in data["lineage"].get("events", []):
        print(f"- {event.get('event_type')} {event.get('created_at', '')}")


def cmd_list(args: argparse.Namespace) -> None:
    conn = connect()
    rows = conn.execute("SELECT artifact_id, title, path FROM artifacts ORDER BY created_at").fetchall()
    conn.close()
    for artifact_id, title, path in rows:
        print(f"{artifact_id} | {title} | {path}")


def cmd_status(args: argparse.Namespace) -> None:
    conn = connect()
    artifact_count = conn.execute("SELECT COUNT(*) FROM artifacts").fetchone()[0]
    edge_count = conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
    cas_count = conn.execute("SELECT COUNT(*) FROM cas_objects").fetchone()[0]
    conn.close()
    print(f"vault {vault_root()}")
    print(f"artifacts {artifact_count}")
    print(f"edges {edge_count}")
    print(f"cas_objects {cas_count}")
