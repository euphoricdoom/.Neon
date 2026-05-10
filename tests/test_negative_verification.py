import json
import os
from pathlib import Path

import pytest

from neon.cli import main


def test_tampered_proof_packet_fails(tmp_path):
    old = Path.cwd()
    os.chdir(tmp_path)

    try:
        main(["init"])
        main([
            "register",
            "--title", "Tamper Test",
            "--creator", "Carl Sowers",
        ])

        artifact = tmp_path / ".neon-vault" / "artifacts" / "tamper-test.neon"

        main(["export", str(artifact)])

        proof = tmp_path / ".neon-vault" / "exports" / "tamper-test-proof"
        exported = proof / "artifact.neon"

        data = json.loads(exported.read_text(encoding="utf-8"))
        data["title"] = "MALICIOUS CHANGE"
        exported.write_text(json.dumps(data, indent=2), encoding="utf-8")

        with pytest.raises(SystemExit):
            main(["verify", str(proof)])

    finally:
        os.chdir(old)
