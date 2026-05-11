from pathlib import Path

import pytest

from neon.artifact import canonical_bytes, read_json, slug, validate_artifact, write_json
from neon.cas import CAS_PREFIX, cas_path, cas_uri, parse_cas_uri, sha256_bytes
from neon.proof import build_proof_packet
from neon.symbols import SYMBOLS, symbolic_state


def test_artifact_canonical_bytes_are_stable():
    left = {"b": 2, "a": 1}
    right = {"a": 1, "b": 2}

    assert canonical_bytes(left) == canonical_bytes(right)


def test_artifact_read_write_roundtrip(tmp_path):
    path = tmp_path / "artifact.neon"
    data = {"a": 1, "b": 2}

    raw = write_json(path, data)

    assert path.exists()
    assert raw == canonical_bytes(data)
    assert read_json(path) == data


def test_slug_is_predictable():
    assert slug("AI Assisted Invoice Workflow") == "ai-assisted-invoice-workflow"


def test_validate_artifact_rejects_missing_fields():
    errors = validate_artifact({"kind": "artifact"})

    assert errors
    assert "missing field: neon_version" in errors


def test_cas_uri_roundtrip():
    digest = sha256_bytes(b"hello")
    uri = cas_uri(digest)

    assert uri.startswith(CAS_PREFIX)
    assert parse_cas_uri(uri) == digest


def test_invalid_cas_uri_rejected():
    with pytest.raises(SystemExit):
        parse_cas_uri("http://example.com/nope")


def test_cas_path_uses_digest_prefix(tmp_path):
    digest = "abcdef"

    assert cas_path(tmp_path, digest) == tmp_path / "ab" / digest


def test_build_proof_packet_shape():
    packet = build_proof_packet(
        version="0.1.0-alpha",
        artifact_id=".N/example",
        artifact_sha256="abc",
        exported_at="2026-05-10T00:00:00+00:00",
        parents=[".N/root"],
    )

    assert packet["kind"] == "proof_packet"
    assert packet["artifact_file"] == "artifact.neon"
    assert packet["parents"] == [".N/root"]


def test_symbolic_state_composes_status_operator_subject():
    assert symbolic_state(SYMBOLS["hot_context"], "v0.2", SYMBOLS["project"]) == "⚡ π.v0.2"


def test_symbolic_state_rejects_invalid_status():
    with pytest.raises(ValueError):
        symbolic_state("?", "v0.2")
