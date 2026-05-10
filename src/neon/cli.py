from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VAULT_DIR = ".neon-vault"
VERSION = "0.1.0-alpha"
REQUIRED_FIELDS = [
    "neon_version",
    "kind",
    "artifact_id",
    "title",
    "artifact_type",
    "creator",
    "origin",
    "lineage",
    "proof",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def vault_root() -> Path:
    return Path.cwd() / VAULT_DIR


def db_path() -> Path:
    return vault_root() / "ledger.sqlite"


def objects_root() -> Path:
    return vault_root() / "objects" / "sha256"


def canonical_bytes(data: dict[str, Any]) -> bytes:
    return json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def slug(text: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in text).strip("-") or "artifact"


def neon_id(title: str, created_at: str, parent_ids: list[str] | None = None) -> str:
    parents = ",".join(parent_ids or [])
    return ".N/" + sha256_bytes(f"{title}|{created_at}|{parents}".encode("utf-8"))[:16]


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"Invalid .neon object: root must be an object: {path}")
    return data


def write_json(path: Path, data: dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = canonical_bytes(data)
    path.write_bytes(raw)
    return sha256_bytes(raw)


def connect() -> sqlite3.Connection:
    if not db_path().exists():
        raise SystemExit("No .neon-vault found. Run: neon init")
    conn = sqlite3.connect(db_path())
    init_db(conn)
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS artifacts (
            artifact_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            path TEXT NOT NULL,
            hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS edges (
            source_id TEXT NOT NULL,
            target_id TEXT NOT NULL,
            edge_type TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS cas_objects (
            digest TEXT PRIMARY KEY,
            uri TEXT NOT NULL,
            path TEXT NOT NULL,
            stored_at TEXT NOT NULL
        )
        """
    )
    conn.commit()


def require_vault_dirs() -> None:
    for part in [
        "artifacts",
        "exports",
        "indexes",
        "proofs",
        "objects/sha256",
    ]:
        (vault_root() / part).mkdir(parents=True, exist_ok=True)


def validate_artifact(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"missing field: {field}")
    if data.get("kind") != "artifact":
        errors.append("kind must be artifact")
    if not str(data.get("artifact_id", "")).startswith(".N/"):
        errors.append("artifact_id must start with .N/")
    if not isinstance(data.get("creator"), dict):
        errors.append("creator must be an object")
    if not isinstance(data.get("origin"), dict):
        errors.append("origin must be an object")
    lineage = data.get("lineage")
    if not isinstance(lineage, dict):
        errors.append("lineage must be an object")
    else:
        if not isinstance(lineage.get("parents", []), list):
            errors.append("lineage.parents must be a list")
        if not isinstance(lineage.get("events", []), list):
            errors.append("lineage.events must be a list")
    proof = data.get("proof")
    if not isinstance(proof, dict):
        errors.append("proof must be an object")
    elif proof.get("hash_algorithm") != "sha256":
        errors.append("proof.hash_algorithm must be sha256")
    return errors


def make_artifact(title: str, creator: str, artifact_type: str, statement: str, parents: list[str] | None = None) -> dict[str, Any]:
    created_at = utc_now()
    parents = parents or []
    event_type = "derived_from" if parents else "originated"
    return {
        "neon_version": VERSION,
        "kind": "artifact",
        "artifact_id": neon_id(title, created_at, parents),
        "title": title,
        "artifact_type": artifact_type,
        "creator": {"name": creator},
        "origin": {"created_at": created_at, "statement": statement},
        "lineage": {
            "parents": parents,
            "events": [{"event_type": event_type, "created_at": created_at}],
        },
        "proof": {"hash_algorithm": "sha256", "anchors": []},
    }


def save_artifact(data: dict[str, Any]) -> tuple[Path, str]:
    errors = validate_artifact(data)
    if errors:
        raise SystemExit("Cannot save invalid artifact: " + "; ".join(errors))
    out = vault_root() / "artifacts" / f"{slug(data['title'])}.neon"
    digest = write_json(out, data)
    conn = connect()
    conn.execute(
        "INSERT OR REPLACE INTO artifacts VALUES (?, ?, ?, ?, ?)",
        (data["artifact_id"], data["title"], str(out), digest, utc_now()),
    )
    conn.commit()
    conn.close()
    return out, digest


def resolve_artifact_path(ref: str) -> Path:
    candidate = Path(ref)
    if candidate.exists():
        return candidate
    conn = connect()
    row = conn.execute(
        "SELECT path FROM artifacts WHERE artifact_id = ? OR title = ?",
        (ref, ref),
    ).fetchone()
    conn.close()
    if not row:
        raise SystemExit(f"Artifact not found: {ref}")
    return Path(row[0])


def index_neon_files(root: Path) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for path in root.rglob("*.neon"):
        try:
            data = read_json(path)
        except SystemExit:
            continue
        artifact_id = data.get("artifact_id")
        if isinstance(artifact_id, str):
            index[artifact_id] = path
    return index


def ancestry_chain(start: Path, search_root: Path) -> list[dict[str, Any]]:
    index = index_neon_files(search_root)
    chain: list[dict[str, Any]] = []
    seen: set[str] = set()

    def visit(path: Path) -> None:
        data = read_json(path)
        artifact_id = data.get("artifact_id")
        if not isinstance(artifact_id, str):
            raise SystemExit(f"Artifact missing artifact_id: {path}")
        if artifact_id in seen:
            return
        seen.add(artifact_id)
        for parent_id in data.get("lineage", {}).get("parents", []):
            parent_path = index.get(parent_id)
            if parent_path is None:
                chain.append({"artifact_id": parent_id, "title": "<missing>", "path": None})
            else:
                visit(parent_path)
        chain.append({"artifact_id": artifact_id, "title": data.get("title", ""), "path": str(path)})

    visit(start)
    return chain


def cas_path(digest: str) -> Path:
    return objects_root() / digest[:2] / digest


def cas_uri(digest: str) -> str:
    return f".neon://sha256/{digest}"


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
    path = Path(args.artifact)
    data = read_json(path)
    errors = validate_artifact(data)
    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("VALID")
    print(data["artifact_id"])
    print(sha256_file(path))


def cmd_hash(args: argparse.Namespace) -> None:
    data = read_json(Path(args.artifact))
    print(sha256_bytes(canonical_bytes(data)))


def cmd_store(args: argparse.Namespace) -> None:
    data = read_json(Path(args.artifact))
    raw = canonical_bytes(data)
    digest = sha256_bytes(raw)
    out = cas_path(digest)
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
    uri = args.uri
    prefix = ".neon://sha256/"
    if not uri.startswith(prefix):
        raise SystemExit("Expected .neon://sha256/<digest>")
    digest = uri.removeprefix(prefix)
    path = cas_path(digest)
    if not path.exists():
        raise SystemExit(f"Object not found: {uri}")
    if args.out:
        dest = Path(args.out)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
        print(dest)
    else:
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
    manifest = {
        "neon_version": VERSION,
        "kind": "proof_packet",
        "artifact_id": data["artifact_id"],
        "artifact_file": "artifact.neon",
        "artifact_sha256": digest,
        "exported_at": utc_now(),
        "parents": data["lineage"].get("parents", []),
    }
    write_json(out / "manifest.json", manifest)
    write_json(out / "lineage.json", data["lineage"])
    (out / "hashes.txt").write_text(f"{digest}  artifact.neon\n", encoding="utf-8")
    (out / "SUMMARY.md").write_text(
        f"# .NeoN Proof Packet\n\nArtifact: {data['title']}\n\nID: {data['artifact_id']}\n\nSHA-256: {digest}\n",
        encoding="utf-8",
    )
    verification = {"status": "created", "artifact_sha256": digest, "checked_at": utc_now()}
    write_json(out / "verification.json", verification)
    print(out)


def cmd_verify(args: argparse.Namespace) -> None:
    target = Path(args.target)
    if target.is_dir():
        manifest = read_json(target / "manifest.json")
        artifact = target / manifest["artifact_file"]
        ok = sha256_file(artifact) == manifest["artifact_sha256"]
        print("verified" if ok else "failed")
        raise SystemExit(0 if ok else 1)
    data = read_json(target)
    errors = validate_artifact(data)
    print("verified" if not errors else "failed")
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
    search_root = Path(args.root)
    chain = ancestry_chain(start, search_root)
    if args.format == "json":
        print(json.dumps(chain, indent=2))
        return
    for index, item in enumerate(chain):
        prefix = "->" if index else "  "
        print(f"{prefix} {item['artifact_id']} | {item['title']}")


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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="neon")
    sub = parser.add_subparsers(required=True)

    p = sub.add_parser("init")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("register")
    p.add_argument("--title", required=True)
    p.add_argument("--creator", required=True)
    p.add_argument("--type", default="workflow")
    p.add_argument("--statement", default="")
    p.set_defaults(func=cmd_register)

    p = sub.add_parser("derive")
    p.add_argument("--parent", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--creator", required=True)
    p.add_argument("--type", default="workflow")
    p.add_argument("--statement", default="")
    p.set_defaults(func=cmd_derive)

    for name, func, arg in [
        ("validate", cmd_validate, "artifact"),
        ("hash", cmd_hash, "artifact"),
        ("store", cmd_store, "artifact"),
        ("export", cmd_export, "artifact"),
        ("verify", cmd_verify, "target"),
        ("log", cmd_log, "artifact"),
    ]:
        p = sub.add_parser(name)
        p.add_argument(arg)
        p.set_defaults(func=func)

    p = sub.add_parser("fetch")
    p.add_argument("uri")
    p.add_argument("--out")
    p.set_defaults(func=cmd_fetch)

    p = sub.add_parser("graph")
    p.add_argument("artifact")
    p.add_argument("--format", choices=["mermaid", "json"], default="mermaid")
    p.set_defaults(func=cmd_graph)

    p = sub.add_parser("lineage")
    p.add_argument("artifact")
    p.add_argument("--root", default=".")
    p.add_argument("--format", choices=["text", "json"], default="text")
    p.set_defaults(func=cmd_lineage)

    p = sub.add_parser("list")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("status")
    p.set_defaults(func=cmd_status)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
