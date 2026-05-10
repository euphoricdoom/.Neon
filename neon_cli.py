#!/usr/bin/env python3
"""Minimal .NeoN CLI seed.

Commands:
  init      Create a local .neon-vault folder
  register  Create and register a .neon artifact
  status    Show vault status
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import sqlite3
import sys
from pathlib import Path

VAULT_DIR = ".neon-vault"
DB_NAME = "ledger.sqlite"


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


def stable_id(title: str, creator: str, created_at: str) -> str:
    seed = f"{title}|{creator}|{created_at}".encode("utf-8")
    return ".N/" + hashlib.sha256(seed).hexdigest()[:16]


def write_json(path: Path, data: dict) -> str:
    encoded = json.dumps(data, indent=2, sort_keys=True).encode("utf-8")
    path.write_bytes(encoded)
    return hashlib.sha256(encoded).hexdigest()


def cmd_register(args: argparse.Namespace) -> None:
    root = Path.cwd()
    conn = connect(root)
    init_db(conn)
    created_at = now_iso()
    artifact_id = stable_id(args.title, args.creator, created_at)
    artifact = {
        "neon_version": "0.1.0",
        "kind": "artifact",
        "artifact_id": artifact_id,
        "title": args.title,
        "artifact_type": args.type,
        "creator": {"name": args.creator, "role": "originator"},
        "origin": {"created_at": created_at, "statement": args.statement or ""},
        "lineage": {"parents": [], "events": [{"event_type": "created", "summary": "Registered artifact."}]},
        "proof": {"hash_algorithm": "sha256", "signature": None, "anchors": []},
    }
    safe_name = "".join(c.lower() if c.isalnum() else "-" for c in args.title).strip("-") or "artifact"
    out = vault_path(root) / "artifacts" / f"{safe_name}.neon"
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
    parser = argparse.ArgumentParser(prog="neon", description="Minimal .NeoN CLI seed")
    sub = parser.add_subparsers(required=True)

    p_init = sub.add_parser("init")
    p_init.set_defaults(func=cmd_init)

    p_register = sub.add_parser("register")
    p_register.add_argument("--title", required=True)
    p_register.add_argument("--creator", required=True)
    p_register.add_argument("--type", default="workflow")
    p_register.add_argument("--statement", default="")
    p_register.set_defaults(func=cmd_register)

    p_status = sub.add_parser("status")
    p_status.set_defaults(func=cmd_status)

    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
