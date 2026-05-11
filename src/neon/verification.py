"""Verification helpers for .NeoN proof packets and artifacts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from neon.artifact import read_json, validate_artifact
from neon.cas import sha256_file


def verify_proof_packet(path: Path) -> bool:
    manifest = read_json(path / "manifest.json")
    artifact = path / manifest["artifact_file"]
    return sha256_file(artifact) == manifest["artifact_sha256"]


def verify_artifact_file(path: Path) -> tuple[bool, list[str]]:
    data = read_json(path)
    errors = validate_artifact(data)
    return (not errors, errors)


def proof_packet_manifest(
    *,
    version: str,
    artifact_id: str,
    artifact_sha256: str,
    exported_at: str,
    parents: list[str],
) -> dict[str, Any]:
    return {
        "neon_version": version,
        "kind": "proof_packet",
        "artifact_id": artifact_id,
        "artifact_file": "artifact.neon",
        "artifact_sha256": artifact_sha256,
        "exported_at": exported_at,
        "parents": parents,
    }
