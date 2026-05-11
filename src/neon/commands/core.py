"""Core runtime command handlers for .NeoN."""

from __future__ import annotations

import argparse
import json
import shutil
import sqlite3
from pathlib import Path

from neon.artifact import canonical_bytes, read_json, validate_artifact
from neon.cas import cas_path, cas_uri, sha256_bytes, sha256_file
from neon.lifecycle import make_artifact, resolve_artifact_path, save_artifact
from neon.metrics import summarize_metrics
from neon.storage import connect, db_path, init_db, require_vault_dirs, vault_root
from neon.topology import ancestry_chain, artifact_metrics, descendant_chain
from neon.verification import proof_packet_manifest, verify_artifact_file, verify_proof_packet


def cmd_init(args: argparse.Namespace) -> None:
    require_vault_dirs()
    conn = sqlite3.connect(db_path())
    init_db(conn)
    conn.close()
    identity = vault_root() / "identity.json"
    if not identity.exists():
        identity.write_text(
            json.dumps({"kind": "identity", "name": None}, indent=2),
            encoding="utf-8",
        )
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

    data = make_artifact(
        args.title,
        args.creator,
        args.type,
        args.statement,
        [parent["artifact_id"]],
    )

    out, digest = save_artifact(data)

    conn = connect()
    conn.execute(
        "INSERT INTO edges VALUES (?, ?, ?, datetime('now'))",
        (parent["artifact_id"], data["artifact_id"], "derived_from"),
    )
    conn.commit()
    conn.close()

    print(data["artifact_id"])
    print(out)
    print(digest)



def cmd_store(args: argparse.Namespace) -> None:
    data = read_json(Path(args.artifact))
    raw = canonical_bytes(data)
    digest = sha256_bytes(raw)

    out = cas_path(digest)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)

    conn = connect()
    conn.execute(
        "INSERT OR REPLACE INTO cas_objects VALUES (?, ?, ?, datetime('now'))",
        (digest, cas_uri(digest), str(out)),
    )
    conn.commit()
    conn.close()

    print(cas_uri(digest))



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
        print(json.dumps(metrics.__dict__, indent=2))
        return

    print(summarize_metrics(metrics))



def cmd_export(args: argparse.Namespace) -> None:
    artifact = resolve_artifact_path(args.artifact)
    data = read_json(artifact)

    digest = sha256_file(artifact)

    out = vault_root() / "exports" / f"{artifact.stem}-proof"
    out.mkdir(parents=True, exist_ok=True)

    shutil.copy2(artifact, out / "artifact.neon")

    manifest = proof_packet_manifest(
        version="0.1.0-alpha",
        artifact_id=data["artifact_id"],
        artifact_sha256=digest,
        exported_at="runtime",
        parents=data["lineage"].get("parents", []),
    )

    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(out)
