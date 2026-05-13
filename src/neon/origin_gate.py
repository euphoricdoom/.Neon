from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone
from uuid import uuid4


class OriginState(StrEnum):
    TRUSTED_ORIGIN = "TRUSTED_ORIGIN"
    VERIFIED_OPEN = "VERIFIED_OPEN"
    LOCAL_UNCLAIMED = "LOCAL_UNCLAIMED"
    UNKNOWN_ORIGIN = "UNKNOWN_ORIGIN"
    CONFLICTED_ORIGIN = "CONFLICTED_ORIGIN"


class ExecutionDecision(StrEnum):
    ALLOW_FULL = "ALLOW_FULL"
    ALLOW_LIMITED = "ALLOW_LIMITED"
    ALLOW_SANDBOXED = "ALLOW_SANDBOXED"
    ALLOW_READ_ONLY = "ALLOW_READ_ONLY"
    BLOCK = "BLOCK"
    QUARANTINE = "QUARANTINE"


class OverrideMode(StrEnum):
    NONE = "NONE"
    CREATOR_LOCAL_OVERRIDE = "CREATOR_LOCAL_OVERRIDE"
    TEMPORARY_TIMEBOX_OVERRIDE = "TEMPORARY_TIMEBOX_OVERRIDE"


@dataclass(frozen=True)
class OverrideInfo:
    active: bool = False
    mode: str = OverrideMode.NONE.value
    reason: str | None = None
    expires_at: str | None = None
    packet_path: str | None = None


@dataclass(frozen=True)
class OriginGateResult:
    artifact_ref: str
    origin_state: str
    execution_decision: str
    trusted_origin: bool
    policy_version: str | None = None
    evidence_score: float = 0.0
    signals: dict[str, str] = field(default_factory=dict)
    override: OverrideInfo = field(default_factory=OverrideInfo)
    required_next_actions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _sidecar_path(artifact_path: Path) -> Path:
    return artifact_path.with_suffix(artifact_path.suffix + ".origin.json")


def _base_signals() -> dict[str, str]:
    return {
        "lineage": "missing",
        "loop_claim": "missing",
        "signature": "missing",
        "artifact_hash": "missing",
        "cognitive_pulse": "missing",
    }


def _read_sidecar(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def resolve_origin_state(artifact_path: str | Path):
    path = Path(artifact_path)
    signals = _base_signals()

    if not path.exists() or not path.is_file():
        return OriginState.UNKNOWN_ORIGIN, signals, 0.0, ["provide_existing_artifact"], None

    sidecar = _sidecar_path(path)
    current_hash = sha256_file(path)

    if not sidecar.exists():
        signals["artifact_hash"] = "matched"
        return OriginState.LOCAL_UNCLAIMED, signals, 0.25, ["create_loop_claim"], None

    data = _read_sidecar(sidecar)
    if data is None:
        return OriginState.CONFLICTED_ORIGIN, signals, 0.0, ["repair_origin_sidecar"], None

    expected_hash = str(data.get("artifact_hash", "")).removeprefix("sha256:")
    if not expected_hash:
        return OriginState.CONFLICTED_ORIGIN, signals, 0.0, ["add_artifact_hash_to_origin_sidecar"], data.get("policy_version")

    if expected_hash != current_hash:
        signals["artifact_hash"] = "mismatched"
        return OriginState.CONFLICTED_ORIGIN, signals, 0.0, ["inspect_hash_mismatch"], data.get("policy_version")

    signals["artifact_hash"] = "matched"
    signals["lineage"] = data.get("lineage", "missing")
    signals["loop_claim"] = data.get("loop_claim", "missing")
    signals["signature"] = data.get("signature", "missing")
    signals["cognitive_pulse"] = data.get("cognitive_pulse", "missing")
    policy_version = data.get("policy_version")

    if data.get("origin_state") == OriginState.TRUSTED_ORIGIN.value:
        trusted_requirements_met = (
            signals["lineage"] == "valid"
            and signals["loop_claim"] == "valid"
            and signals["signature"] == "valid"
            and signals["artifact_hash"] == "matched"
            and bool(policy_version)
        )
        if trusted_requirements_met:
            return OriginState.TRUSTED_ORIGIN, signals, 1.0, [], policy_version
        return OriginState.CONFLICTED_ORIGIN, signals, 0.0, ["repair_trusted_origin_evidence"], policy_version

    if data.get("origin_state") == OriginState.VERIFIED_OPEN.value:
        return OriginState.VERIFIED_OPEN, signals, 0.75, [], policy_version

    return OriginState.LOCAL_UNCLAIMED, signals, 0.35, ["create_loop_claim"], policy_version


def default_execution_decision(origin_state: OriginState, action: str = "run") -> ExecutionDecision:
    action = action.lower()
    if origin_state == OriginState.TRUSTED_ORIGIN:
        return ExecutionDecision.ALLOW_FULL
    if origin_state == OriginState.VERIFIED_OPEN:
        return ExecutionDecision.ALLOW_LIMITED
    if origin_state == OriginState.LOCAL_UNCLAIMED:
        return ExecutionDecision.ALLOW_LIMITED
    if origin_state == OriginState.UNKNOWN_ORIGIN:
        return ExecutionDecision.ALLOW_READ_ONLY if action in {"read", "inspect"} else ExecutionDecision.ALLOW_SANDBOXED
    if origin_state == OriginState.CONFLICTED_ORIGIN:
        return ExecutionDecision.ALLOW_READ_ONLY
    return ExecutionDecision.BLOCK


def resolve_execution_decision(
    artifact_path: str | Path,
    *,
    action: str = "run",
    override_mode: str | None = None,
    override_reason: str | None = None,
) -> OriginGateResult:
    origin_state, signals, evidence_score, next_actions, policy_version = resolve_origin_state(artifact_path)
    decision = default_execution_decision(origin_state, action)
    override = OverrideInfo()

    if override_mode == "creator-local" and origin_state == OriginState.LOCAL_UNCLAIMED:
        decision = ExecutionDecision.ALLOW_FULL
        override = OverrideInfo(active=True, mode=OverrideMode.CREATOR_LOCAL_OVERRIDE.value, reason=override_reason)
    elif override_mode == "creator-local" and origin_state == OriginState.UNKNOWN_ORIGIN:
        decision = ExecutionDecision.ALLOW_LIMITED
        override = OverrideInfo(active=True, mode=OverrideMode.CREATOR_LOCAL_OVERRIDE.value, reason=override_reason)
    elif override_mode == "creator-local" and origin_state == OriginState.CONFLICTED_ORIGIN:
        decision = ExecutionDecision.ALLOW_READ_ONLY
        override = OverrideInfo(active=True, mode=OverrideMode.CREATOR_LOCAL_OVERRIDE.value, reason=override_reason)

    return OriginGateResult(
        artifact_ref=str(artifact_path),
        origin_state=origin_state.value,
        execution_decision=decision.value,
        trusted_origin=origin_state == OriginState.TRUSTED_ORIGIN,
        policy_version=policy_version,
        evidence_score=evidence_score,
        signals=signals,
        override=override,
        required_next_actions=next_actions,
    )


def write_override_packet(result: OriginGateResult, *, root: str | Path = ".") -> Path:
    if not result.override.active:
        raise ValueError("override inactive")

    out_dir = Path(root) / ".neon" / "packets"
    out_dir.mkdir(parents=True, exist_ok=True)

    packet_id = f"origin_gate_override_{uuid4().hex[:8]}"
    out = out_dir / f"{packet_id}.json"

    packet = {
        "packet_type": "origin_gate_override",
        "packet_id": packet_id,
        "artifact_ref": result.artifact_ref,
        "origin_state": result.origin_state,
        "execution_decision": result.execution_decision,
        "trusted_origin": result.trusted_origin,
        "override_mode": result.override.mode,
        "reason": result.override.reason,
        "created_at": utc_now(),
        "expires_at": result.override.expires_at,
        "signature_required": True,
        "signals": result.signals,
    }

    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out
