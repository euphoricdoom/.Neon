from pathlib import Path
import json

from neon.artifact import read_json, validate_artifact
from neon.topology import ancestry_chain, artifact_metrics, descendant_chain


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


def test_golden_metrics_match_expected():
    target = ROOT / "ai-assisted-workflow.neon"

    metrics = artifact_metrics(target, ROOT)

    actual = {
        "artifact_id": metrics.artifact_id,
        "parent_count": metrics.parent_count,
        "ancestor_count": metrics.ancestor_count,
        "lineage_depth": metrics.lineage_depth,
    }

    expected = json.loads((ROOT / "expected" / "metrics.json").read_text(encoding="utf-8"))

    assert actual == expected


def test_golden_graph_shape_matches_expected():
    target = ROOT / "ai-assisted-workflow.neon"

    chain = ancestry_chain(target, ROOT)

    rendered = ["graph TD"]

    for index in range(1, len(chain)):
        parent = chain[index - 1]["artifact_id"].replace(".N/", "N_")
        child = chain[index]["artifact_id"].replace(".N/", "N_")
        rendered.append(f"  {parent} --> {child}")

    actual = "\n".join(rendered).strip()
    expected = (ROOT / "expected" / "graph.mmd").read_text(encoding="utf-8").strip()

    assert actual == expected
