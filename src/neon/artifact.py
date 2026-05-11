"""Artifact primitives for .NeoN.

This module owns the readable `.neon` artifact shape and validation rules.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

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


def canonical_bytes(data: dict[str, Any]) -> bytes:
    return json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False).encode("utf-8")


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"Invalid .neon object: root must be an object: {path}")
    return data


def write_json(path: Path, data: dict[str, Any]) -> bytes:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = canonical_bytes(data)
    path.write_bytes(raw)
    return raw


def slug(text: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in text).strip("-") or "artifact"


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
