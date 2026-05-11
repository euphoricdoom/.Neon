"""Artifact lifecycle helpers for .NeoN runtime commands."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from neon.artifact import VERSION, slug, utc_now, validate_artifact, write_json
from neon.cas import sha256_bytes
from neon.storage import connect, vault_root


def neon_id(title: str, created_at: str, parent_ids: list[str] | None = None) -> str:
    parents = ",".join(parent_ids or [])
    return ".N/" + sha256_bytes(f"{title}|{created_at}|{parents}".encode("utf-8"))[:16]


def make_artifact(
    title: str,
    creator: str,
    artifact_type: str,
    statement: str,
    parents: list[str] | None = None,
) -> dict[str, Any]:
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
    raw = write_json(out, data)
    digest = sha256_bytes(raw)
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
