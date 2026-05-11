from pathlib import Path

from neon.artifact import read_json, validate_artifact
from neon.topology import ancestry_chain, descendant_chain


ROOT = Path("examples/golden")


def test_golden_artifacts_validate_cleanly():
    for path in ROOT.glob("*.neon"):
        data = read_json(path)
        errors = validate_artifact(data)
        assert errors == [], f"{path}: {errors}"


def test_golden_lineage_chain_matches_expected():
    target = ROOT / "ai-assisted-workflow.neon"

    chain = ancestry_chain(target, ROOT)

    rendered = []

    for index, item in enumerate(chain):
        prefix = "->" if index else "  "
        rendered.append(f"{prefix} {item['artifact_id']} | {item['title']}")

    actual = "\n".join(rendered).strip()
    expected = (ROOT / "expected" / "lineage.txt").read_text(encoding="utf-8").strip()

    assert actual == expected


def test_golden_descendants_chain_matches_expected():
    target = ROOT / "creator-root.neon"

    chain = descendant_chain(target, ROOT)

    rendered = [f"-> {item['artifact_id']} | {item['title']}" for item in chain]

    actual = "\n".join(rendered).strip()
    expected = (ROOT / "expected" / "descendants.txt").read_text(encoding="utf-8").strip()

    assert actual == expected
