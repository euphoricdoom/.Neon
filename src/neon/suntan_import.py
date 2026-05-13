"""Sun_Tan import helpers for .NeoN.

This module validates and stages Sun_Tan origin-claim exports without
requiring .NeoN to depend on Sun_Tan internals.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from neon.artifact import read_json, utc_now, write_json
from neon.storage import vault_root


REQUIRED_SUNTAN_CLAIM_FIELDS = {
    "claim_version",
    "claim_type",
    "source_system",
    "artifact_hash",
    "bridge_payload_hash",
    "bridge_signature",
    "policy",
    "lineage",
}


def validate_suntan_origin_claim(data: dict[str, Any]) -> list[str]:
    """Return validation errors for a Sun_Tan origin claim export."""
    errors: list[str] = []
    missing = REQUIRED_SUNTAN_CLAIM_FIELDS.difference(data.keys())

    if missing:
        errors.append("missing fields: " + ", ".join(sorted(missing)))

    if data.get("claim_type") != "TRUSTED_ORIGIN":
        errors.append("claim_type must be TRUSTED_ORIGIN")

    artifact_hash = data.get("artifact_hash", "")
    if not isinstance(artifact_hash, str) or not artifact_hash.startswith("sha256:"):
        errors.append("artifact_hash must start with sha256:")

    payload_hash = data.get("bridge_payload_hash", "")
    if not isinstance(payload_hash, str) or not payload_hash.startswith("sha256:"):
        errors.append("bridge_payload_hash must start with sha256:")

    if not isinstance(data.get("bridge_signature"), str) or not data.get("bridge_signature"):
        errors.append("bridge_signature is required")

    if not isinstance(data.get("lineage", []), list):
        errors.append("lineage must be a list")

    return errors


def import_suntan_origin_claim(path: str | Path, out_dir: str | Path | None = None) -> Path:
    """Validate and stage a Sun_Tan origin claim into the .NeoN vault."""
    source = Path(path)
    data = read_json(source)
    errors = validate_suntan_origin_claim(data)

    if errors:
        raise ValueError("Invalid Sun_Tan origin claim: " + "; ".join(errors))

    target_dir = Path(out_dir) if out_dir is not None else vault_root() / "imports" / "suntan"
    target_dir.mkdir(parents=True, exist_ok=True)

    imported_path = target_dir / source.name
    shutil.copy2(source, imported_path)

    receipt = {
        "import_type": "suntan_origin_claim",
        "imported_at": utc_now(),
        "source_path": str(source),
        "imported_path": str(imported_path),
        "source_system": data.get("source_system"),
        "artifact_hash": data.get("artifact_hash"),
        "bridge_payload_hash": data.get("bridge_payload_hash"),
        "policy": data.get("policy"),
        "lineage": data.get("lineage", []),
    }
    write_json(target_dir / f"{source.stem}.receipt.json", receipt)

    return imported_path
