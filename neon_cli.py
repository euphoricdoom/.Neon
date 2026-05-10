#!/usr/bin/env python3
""".NeoN reference CLI spine.

Commands:
  init       Create a local .neon-vault folder
  register   Create and register a .neon artifact
  validate   Validate a .neon artifact shape
  export     Export a portable proof packet
  status     Show vault status

This implementation is intentionally small, local-first, and dependency-free.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import shutil
import sqlite3
import sys
from pathlib import Path
from typing import Any

VAULT_DIR = ".neon-vault"
DB_NAME = "ledger.sqlite"
NEON_VERSION = "0.1.0"
REQUIRED_ARTIFACT_FIELDS = [
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


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def vault_path(root: Path) -> Path:
    return root / VAULT_DIR


def db_path(root: Path) -> Path:
    return vault_path(root) / DB_NAME


def connect(root: Path) -> sqlite3.Connection:
    path = db_path(root)
    if not path.exists():
        raise SystemExit("No .neon-vault found. Run: python neon_cli.py init")
    return sqlite3.connect(path)


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS artifacts (
            artifact_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            creator TEXT NOT NULL,
            artifact_type TEXT NOT NULL,
            path TEXT NOT NULL,
            sha256 TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            artifact_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            summary TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"Invalid .neon file: root must be an object: {path}")
    return data


def write_json(path: Path, data: dict[str, Any]) -> str:
    encoded = json.dumps(data, indent=2, sort_keys=True).encode("utf-8")
    path.write_bytes(encoded)
    return sha256_bytes(encoded)


def safe_slug(text: str) -> str:
    return "".join(c.lower() if c.isalnum() else "-" for c in text).strip("-") or "artifact"


def stable_id(title: str, creator: str, created_at: str) -> str:
    seed = f"{title}|{creator}|{created_at}".encode("utf-8")
    return ".N/" + sha256_bytes(seed)[:16]


def validate_artifact(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_ARTIFACT_FIELDS:
        if field not in data:
            errors.append(f"missing required field: {field}")
    if data.get("kind") != "artifact":
        errors.append("kind must be 'artifact'")
    if not str(data.get("artifact_id", "")).startswith(".N/"):
        errors.append("artifact_id must start with .N/")
    if not isinstance(data.get("creator"), dict):
        errors.append("creator must be an object")
    if not isinstance(data.get("origin"), dict):
        errors.append("origin must be an object")
    if not isinstance(data.get("lineage"), dict):
        errors.append("lineage must be an object")
    if not isinstance(data.get("proof"), dict):
        errors.append("proof must be an object")
    return errors


def find_artifact(root: Path, artifact_ref: str) -> tuple[str, Path, str]:
    """Resolve artifact by id, title, or path. Returns (artifact_id, path, stored_hash)."""
    candidate = Path(artifact_ref)
    if candidate.exists():
        data = read_json(candidate)
        artifact_id = str(data.get("artifact_id", ""))
        return artifact_id, candidate, sha256_file(candidate)

    conn = connect(root)
    init_db(conn)
    row = conn.execute(
        "SELECT artifact_id, path, sha256 FROM artifacts WHERE artifact_id = ? OR title = ?",
        (artifact_ref, artifact_ref),
    ).fetchone()
    conn.close()
    if not row:
        raise SystemExit(f"Artifact not found: {artifact_ref}")
    artifact_id, path_text, stored_hash = row
    return artifact_id, Path(path_text), stored_hash


def cmd_init(args: argparse.Namespace) -> None:
    root = Path.cwd()
    vp = vault_path(root)
    (vp / "artifacts").mkdir(parents=True, exist_ok=True)
    (vp / "proofs").mkdir(parents=True, exist_ok=True)
    (vp / "exports").mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path(root))
    init_db(conn)
    conn.close()
    print(f"Initialized .NeoN vault at {vp}")


def cmd_register(args: argparse.Namespace) -> None:
    root = Path.cwd()
    conn = connect(root)
    init_db(conn)
    created_at = now_iso()
    artifact_id = stable_id(args.title, args.creator, created_at)
    artifact = {
        "neon_version": NEON_VERSION,
        "kind": "artifact",
        "artifact_id": artifact_id,
        "title": args.title,
        "artifact_type": args.type,
        "creator": {"name": args.creator, "role": "originator"},
        "origin": {"created_at": created_at, "statement": args.statement or ""},
        "lineage": {
            "parents": [],
            "events": [{"event_type": "created", "summary": "Registered artifact.", "created_at": created_at}],
        },
        "proof": {"hash_algorithm": "sha256", "signature": None, "anchors": []},
    }
    out = vault_path(root) / "artifacts" / f"{safe_slug(args.title)}.neon"
    digest = write_json(out, artifact)
    conn.execute(
        "INSERT INTO artifacts VALUES (?, ?, ?, ?, ?, ?, ?)",
        (artifact_id, args.title, args.creator, args.type, str(out), digest, created_at),
    )
    conn.execute(
        "INSERT INTO events (artifact_id, event_type, summary, created_at) VALUES (?, ?, ?, ?)",
        (artifact_id, "created", "Registered artifact", created_at),
    )
    conn.commit()
    conn.close()
    print(f"Registered {artifact_id}")
    print(f"Wrote {out}")
    print(f"sha256 {digest}")


def cmd_validate(args: argparse.Namespace) -> None:
    path = Path(args.path)
    if path.suffix != ".neon":
        raise SystemExit("Expected a .neon file")
    data = read_json(path)
    errors = validate_artifact(data)
    digest = sha256_file(path)
    if errors:
        print(f"INVALID {path}")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(f"VALID {path}")
    print(f"artifact_id {data['artifact_id']}")
    print(f"sha256 {digest}")


def cmd_export(args: argparse.Namespace) -> None:
    root = Path.cwd()
    artifact_id, artifact_path, stored_hash = find_artifact(root, args.artifact)
    if not artifact_path.exists():
        raise SystemExit(f"Artifact file missing: {artifact_path}")
    data = read_json(artifact_path)
    errors = validate_artifact(data)
    if errors:
        raise SystemExit("Cannot export invalid artifact: " + "; ".join(errors))
    current_hash = sha256_file(artifact_path)
    created_at = now_iso()
    export_name = safe_slug(data.get("title", artifact_id)) + "-proof"
    proof_dir = vault_path(root) / "exports" / export_name
    proof_dir.mkdir(parents=True, exist_ok=True)
    copied_artifact = proof_dir / artifact_path.name
    shutil.copy2(artifact_path, copied_artifact)
    manifest = {
        "neon_version": NEON_VERSION,
        "kind": "proof_packet",
        "artifact_id": artifact_id,
        "artifact_file": copied_artifact.name,
        "exported_at": created_at,
        "hash_algorithm": "sha256",
        "artifact_sha256": current_hash,
        "stored_ledger_sha256": stored_hash,
        "verification_status": "hash_match" if current_hash == stored_hash else "hash_mismatch",
    }
    write_json(proof_dir / "manifest.json", manifest)
    summary = (
        f"# .NeoN Proof Packet\n\n"
        f"Artifact: {data.get('title')}\n\n"
        f"Artifact ID: {artifact_id}\n\n"
        f"Exported: {created_at}\n\n"
        f"SHA-256: {current_hash}\n\n"
        f"Status: {manifest['verification_status']}\n"
    )
    (proof_dir / "SUMMARY.md").write_text(summary, encoding="utf-8")
    print(f"Exported proof packet: {proof_dir}")
    print(f"status {manifest['verification_status']}")


def cmd_status(args: argparse.Namespace) -> None:
    root = Path.cwd()
    conn = connect(root)
    init_db(conn)
    count = conn.execute("SELECT COUNT(*) FROM artifacts").fetchone()[0]
    events = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    conn.close()
    print(f"Vault: {vault_path(root)}")
    print(f"Artifacts: {count}")
    print(f"Events: {events}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="neon", description=".NeoN reference CLI spine")
    sub = parser.add_subparsers(required=True)

    p_init = sub.add_parser("init")
    p_init.set_defaults(func=cmd_init)

    p_register = sub.add_parser("register")
    p_register.add_argument("--title", required=True)
    p_register.add_argument("--creator", required=True)
    p_register.add_argument("--type", default="workflow")
    p_register.add_argument("--statement", default="")
    p_register.set_defaults(func=cmd_register)

    p_validate = sub.add_parser("validate")
    p_validate.add_argument("path")
    p_validate.set_defaults(func=cmd_validate)

    p_export = sub.add_parser("export")
    p_export.add_argument("artifact", help="artifact id, title, or .neon path")
    p_export.set_defaults(func=cmd_export)

    p_status = sub.add_parser("status")
    p_status.set_defaults(func=cmd_status)

    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
