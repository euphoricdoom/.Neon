from __future__ import annotations

import json
from pathlib import Path

from neon.origin_gate import (
    ExecutionDecision,
    OriginState,
    resolve_execution_decision,
    write_override_packet,
)


def test_local_unclaimed_detection(tmp_path: Path):
    artifact = tmp_path / "example.py"
    artifact.write_text("print('hello')\n", encoding="utf-8")

    result = resolve_execution_decision(artifact)

    assert result.origin_state == OriginState.LOCAL_UNCLAIMED.value
    assert result.execution_decision == ExecutionDecision.ALLOW_LIMITED.value
    assert result.trusted_origin is False



def test_creator_override_allows_full_execution_without_truth_promotion(tmp_path: Path):
    artifact = tmp_path / "example.py"
    artifact.write_text("print('hello')\n", encoding="utf-8")

    result = resolve_execution_decision(
        artifact,
        override_mode="creator-local",
        override_reason="vibe coding",
    )

    assert result.origin_state == OriginState.LOCAL_UNCLAIMED.value
    assert result.execution_decision == ExecutionDecision.ALLOW_FULL.value
    assert result.trusted_origin is False
    assert result.override.active is True



def test_override_packet_written(tmp_path: Path):
    artifact = tmp_path / "example.py"
    artifact.write_text("print('hello')\n", encoding="utf-8")

    result = resolve_execution_decision(
        artifact,
        override_mode="creator-local",
        override_reason="testing override packets",
    )

    packet = write_override_packet(result, root=tmp_path)

    assert packet.exists()

    data = json.loads(packet.read_text(encoding="utf-8"))

    assert data["packet_type"] == "origin_gate_override"
    assert data["origin_state"] == OriginState.LOCAL_UNCLAIMED.value
    assert data["execution_decision"] == ExecutionDecision.ALLOW_FULL.value
    assert data["trusted_origin"] is False



def test_tampered_hash_becomes_conflicted_origin(tmp_path: Path):
    artifact = tmp_path / "example.py"
    artifact.write_text("print('v1')\n", encoding="utf-8")

    sidecar = artifact.with_suffix(".py.origin.json")
    sidecar.write_text(
        json.dumps(
            {
                "origin_state": "TRUSTED_ORIGIN",
                "artifact_hash": "sha256:deadbeef",
                "policy_version": "v1",
            }
        ),
        encoding="utf-8",
    )

    result = resolve_execution_decision(artifact)

    assert result.origin_state == OriginState.CONFLICTED_ORIGIN.value
    assert result.trusted_origin is False



def test_override_cannot_promote_truth_state(tmp_path: Path):
    artifact = tmp_path / "example.py"
    artifact.write_text("print('v1')\n", encoding="utf-8")

    sidecar = artifact.with_suffix(".py.origin.json")
    sidecar.write_text(
        json.dumps(
            {
                "origin_state": "TRUSTED_ORIGIN",
                "artifact_hash": "sha256:deadbeef",
                "policy_version": "v1",
            }
        ),
        encoding="utf-8",
    )

    result = resolve_execution_decision(
        artifact,
        override_mode="creator-local",
        override_reason="cannot rewrite truth",
    )

    assert result.origin_state == OriginState.CONFLICTED_ORIGIN.value
    assert result.execution_decision == ExecutionDecision.ALLOW_READ_ONLY.value
    assert result.trusted_origin is False
