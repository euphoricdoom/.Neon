import os
from pathlib import Path

from neon.cli import main


def test_workledger_end_to_end(tmp_path):
    old = Path.cwd()
    os.chdir(tmp_path)
    try:
        main(["init"])
        main(["register", "--title", "Invoice Workflow", "--creator", "Carl Sowers"])

        parent = tmp_path / ".neon-vault" / "artifacts" / "invoice-workflow.neon"
        assert parent.exists()

        main([
            "derive",
            "--parent", str(parent),
            "--title", "AI Assisted Workflow",
            "--creator", "Carl Sowers",
        ])

        child = tmp_path / ".neon-vault" / "artifacts" / "ai-assisted-workflow.neon"
        assert child.exists()

        main(["validate", str(child)])
        main(["hash", str(child)])
        main(["store", str(child)])
        main(["export", str(child)])

        proof = tmp_path / ".neon-vault" / "exports" / "ai-assisted-workflow-proof"
        assert (proof / "artifact.neon").exists()
        assert (proof / "manifest.json").exists()
        assert (proof / "hashes.txt").exists()
        assert (proof / "SUMMARY.md").exists()
        assert (proof / "lineage.json").exists()
        assert (proof / "verification.json").exists()

        main(["verify", str(proof)])
        main(["graph", str(child)])
    finally:
        os.chdir(old)
