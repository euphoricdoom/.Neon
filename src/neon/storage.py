"""Vault and SQLite storage helpers for .NeoN."""

from __future__ import annotations

import sqlite3
from pathlib import Path

VAULT_DIR = ".neon-vault"


def vault_root() -> Path:
    return Path.cwd() / VAULT_DIR


def db_path() -> Path:
    return vault_root() / "ledger.sqlite"


def objects_root() -> Path:
    return vault_root() / "objects" / "sha256"


def require_vault_dirs() -> None:
    for part in [
        "artifacts",
        "exports",
        "indexes",
        "proofs",
        "objects/sha256",
    ]:
        (vault_root() / part).mkdir(parents=True, exist_ok=True)


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


def connect() -> sqlite3.Connection:
    if not db_path().exists():
        raise SystemExit("No .neon-vault found. Run: neon init")
    conn = sqlite3.connect(db_path())
    init_db(conn)
    return conn
