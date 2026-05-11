"""Run the minimum .NeoN release/prototype verification suite."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> int:
    print("$", " ".join(cmd))
    result = subprocess.run(cmd, cwd=ROOT, text=True, check=False)
    return result.returncode


def main() -> int:
    checks = [
        [sys.executable, "-m", "pytest", "-q"],
        [sys.executable, "scripts/check_vertical_alignment.py"],
    ]

    for cmd in checks:
        code = run(cmd)
        if code != 0:
            print(f"FAILED: {' '.join(cmd)}")
            return code

    print("RELEASE CHECK OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
