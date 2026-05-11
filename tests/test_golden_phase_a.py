import json
import os
from pathlib import Path

from neon.cli import main


def _run_demo(tmp_path: Path, capsys):
    old = Path.cwd()
    os.chdir(tmp_path)
    try:
        main(["demo", "--creator", "Carl Sowers"])
        capsys.readouterr()
        return tmp_path / ".neon-vault"
    finally:
        os.chdir(old)


def test_phase_a_golden_demo_artifact_shapes(tmp_path, capsys):
    vault = _run_demo(tmp_path, capsys)
    artifacts = vault / "artifacts"

    expected = {
        "demo-creator-root.neon": {
            "title": "Demo Creator Root",
            "artifact_type": "creator_identity",
            "parent_count": 0,
        },
        "demo-workflow.neon": {
            "title": "Demo Workflow",
            "artifact_type": "workflow",
            "parent_count": 1,
        },
        "demo-ai-assisted-workflow.neon": {
            "title": "Demo AI Assisted Workflow",
            "artifact_type": "workflow",
            "parent_count": 1,
        },
    }

    for filename, checks in expected.items():
        data = json.loads((artifacts / filename).read_text(encoding="utf-8"))
        assert data["kind"] == "artifact"
        assert data["neon_version"] == "0.1.0-alpha"
        assert data["artifact_id"].startswith(".N/")
        assert data["title"] == checks["title"]
        assert data["artifact_type"] == checks["artifact_type"]
        assert len(data["lineage"]["parents"]) == checks["parent_count"]
        assert data["proof"]["hash_algorithm"] == "sha256"


def test_phase_a_golden_proof_packet_shape(tmp_path, capsys):
    vault = _run_demo(tmp_path, capsys)
    proof = vault / "exports" / "demo-ai-assisted-workflow-proof"

    assert (proof / "artifact.neon").exists()
    assert (proof / "manifest.json").exists()
    assert (proof / "lineage.json").exists()
    assert (proof / "hashes.txt").exists()
    assert (proof / "SUMMARY.md").exists()
    assert (proof / "verification.json").exists()

    manifest = json.loads((proof / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["kind"] == "proof_packet"
    assert manifest["artifact_file"] == "artifact.neon"
    assert manifest["artifact_sha256"] in (proof / "hashes.txt").read_text(encoding="utf-8")
    assert manifest["parents"]


def test_phase_a_golden_command_outputs_are_stable_enough(tmp_path, capsys):
    vault = _run_demo(tmp_path, capsys)
    artifacts = vault / "artifacts"
    root = artifacts / "demo-creator-root.neon"
    derived = artifacts / "demo-ai-assisted-workflow.neon"
    proof = vault / "exports" / "demo-ai-assisted-workflow-proof"

    old = Path.cwd()
    os.chdir(tmp_path)
    try:
        main(["verify", str(proof)])
        verify_output = capsys.readouterr().out.strip()
        assert verify_output == "verified"

        main(["lineage", str(derived), "--root", str(artifacts)])
        lineage_output = capsys.readouterr().out
        assert "Demo Creator Root" in lineage_output
        assert "Demo Workflow" in lineage_output
        assert "Demo AI Assisted Workflow" in lineage_output

        main(["descendants", str(root), "--root", str(artifacts)])
        descendants_output = capsys.readouterr().out
        assert "Demo Workflow" in descendants_output
        assert "Demo AI Assisted Workflow" in descendants_output

        main(["metrics", str(derived), "--root", str(artifacts)])
        metrics_output = capsys.readouterr().out
        assert "vector=(2, 2, 0)" in metrics_output
        assert "pressure=(1, 0)" in metrics_output
        assert "derivation_ratio=0.00" in metrics_output
        assert "influence_ratio=0.00" in metrics_output
    finally:
        os.chdir(old)
