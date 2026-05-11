"""Content-addressed storage primitives for .NeoN."""

from __future__ import annotations

import hashlib
from pathlib import Path


CAS_PREFIX = ".neon://sha256/"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def cas_uri(digest: str) -> str:
    return f"{CAS_PREFIX}{digest}"


def parse_cas_uri(uri: str) -> str:
    if not uri.startswith(CAS_PREFIX):
        raise SystemExit("Expected .neon://sha256/<digest>")
    return uri.removeprefix(CAS_PREFIX)


def cas_path(objects_root: Path, digest: str) -> Path:
    return objects_root / digest[:2] / digest
