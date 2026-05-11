"""Proof packet helpers for .NeoN."""

from __future__ import annotations

from typing import Any


def build_proof_packet(
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
