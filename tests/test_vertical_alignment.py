import subprocess
import sys


def test_vertical_alignment_passes():
    result = subprocess.run(
        [sys.executable, "scripts/check_vertical_alignment.py"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "VERTICAL ALIGNMENT OK" in result.stdout
