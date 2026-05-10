import os
from pathlib import Path

from neon.cli import main


def test_store_and_fetch_roundtrip(tmp_path):
    old = Path.cwd()
    os.chdir(tmp_path)

    try:
        main(["init"])
        main([
            "register",
            "--title", "CAS Artifact",
            "--creator", "Carl Sowers",
        ])

        artifact = tmp_path / ".neon-vault" / "artifacts" / "cas-artifact.neon"

        from neon.cli import canonical_bytes, read_json, sha256_bytes

        digest = sha256_bytes(canonical_bytes(read_json(artifact)))
        uri = f".neon://sha256/{digest}"

        main(["store", str(artifact)])

        fetched = tmp_path / "fetched.neon"
        main(["fetch", uri, "--out", str(fetched)])

        assert fetched.exists()
        assert fetched.read_text(encoding="utf-8") == artifact.read_text(encoding="utf-8")

    finally:
        os.chdir(old)
