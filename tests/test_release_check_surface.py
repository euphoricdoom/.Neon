from pathlib import Path


def test_release_check_script_exists_and_runs_pytest_and_alignment():
    path = Path("scripts/release_check.py")
    assert path.exists()

    text = path.read_text(encoding="utf-8")
    assert "pytest" in text
    assert "scripts/check_vertical_alignment.py" in text
    assert "RELEASE CHECK OK" in text
