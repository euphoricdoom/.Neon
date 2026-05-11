import os
from pathlib import Path

from neon.cli import main


def test_demo_loop_creates_inspectable_prototype(tmp_path, capsys):
    old = Path.cwd()
    os.chdir(tmp_path)
    try:
        main(["demo", "--creator", "Carl Sowers"])
        output = capsys.readouterr().out

        assert "Demo continuity loop complete" in output
        assert "Metrics:" in output
        assert "vector=" in output
        assert "pressure=" in output

        artifacts = tmp_path / ".neon-vault" / "artifacts"
        root = artifacts / "demo-creator-root.neon"
        derived = artifacts / "demo-ai-assisted-workflow.neon"
        proof = tmp_path / ".neon-vault" / "exports" / "demo-ai-assisted-workflow-proof"

        assert root.exists()
        assert derived.exists()
        assert proof.exists()

        main(["verify", str(proof)])
        verify_output = capsys.readouterr().out
        assert "verified" in verify_output

        main(["lineage", str(derived), "--root", str(artifacts)])
        lineage_output = capsys.readouterr().out
        assert ".N/" in lineage_output
        assert "Demo Creator Root" in lineage_output
        assert "Demo AI Assisted Workflow" in lineage_output

        main(["descendants", str(root), "--root", str(artifacts)])
        descendants_output = capsys.readouterr().out
        assert "Demo Workflow" in descendants_output
        assert "Demo AI Assisted Workflow" in descendants_output

        main(["metrics", str(derived), "--root", str(artifacts)])
        metrics_output = capsys.readouterr().out
        assert "vector=" in metrics_output
        assert "pressure=" in metrics_output
        assert "derivation_ratio=" in metrics_output
    finally:
        os.chdir(old)
