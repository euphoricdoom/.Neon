import subprocess
import shutil
from pathlib import Path
import os

def run_cmd(*args):
    print(f"Running: {' '.join(args)}")
    res = subprocess.run(["python3", "-m", "src.neon.cli", *args], capture_output=True, text=True, check=True)
    return res

def test_full_workflow():
    if Path(".neon-vault").exists():
        shutil.rmtree(".neon-vault")

    # Init
    res = run_cmd("init")
    assert "initialized" in res.stdout
    assert Path(".neon-vault").exists()
    assert Path(".neon-vault/objects/sha256").exists()

    # Register
    res = run_cmd("register", "--title", "Test Flow", "--creator", "Tester")
    out_lines = [l for l in res.stdout.strip().split('\n') if l]
    print(f"Register output: {out_lines}")
    assert len(out_lines) == 2
    aid1 = out_lines[0]
    file1 = out_lines[1]
    assert aid1.startswith(".N/")
    assert Path(file1).exists()

    # Validate
    res = run_cmd("validate", file1)
    assert "valid" in res.stdout

    # Derive
    res = run_cmd("derive", "--parent", file1, "--title", "Derived Flow", "--creator", "Tester2")
    out_lines = [l for l in res.stdout.strip().split('\n') if l]
    aid2 = out_lines[0]
    assert aid2.startswith(".N/")
    assert out_lines[1].startswith("derived from")

    # List
    res = run_cmd("list")
    assert "test-flow.neon" in res.stdout
    assert "derived-flow.neon" in res.stdout

    # Hash
    file2 = ".neon-vault/artifacts/derived-flow.neon"
    res = run_cmd("hash", file2)
    digest = res.stdout.strip()
    assert len(digest) == 64

    # Store
    res = run_cmd("store", file2)
    assert digest in res.stdout
    assert Path(f".neon-vault/objects/sha256/{digest}").exists()

    # Fetch
    res = run_cmd("fetch", f".neon://sha256/{digest}")
    assert "Derived Flow" in res.stdout

    # Export
    res = run_cmd("export", file2)
    export_dir = Path(res.stdout.strip())
    assert export_dir.exists()
    assert (export_dir / "manifest.json").exists()
    assert (export_dir / "hashes.txt").exists()
    assert (export_dir / "SUMMARY.md").exists()
    assert (export_dir / "lineage.json").exists()
    assert (export_dir / "verification.json").exists()

    # Verify
    res = run_cmd("verify", str(export_dir))
    assert "verified" in res.stdout

    # Graph
    res = run_cmd("graph", file2)
    assert "graph TD" in res.stdout
    assert "-->" in res.stdout

    # Status
    res = run_cmd("status")
    assert "Artifacts: 2" in res.stdout

    # Log
    res = run_cmd("log")
    assert "Test Flow" in res.stdout
    assert "Derived Flow" in res.stdout

if __name__ == "__main__":
    test_full_workflow()
    print("All tests passed.")
