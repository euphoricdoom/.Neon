from neon.lineage import LineageGraph


def build_graph():
    graph = LineageGraph()

    graph.add_artifact({
        "artifact_id": ".N/root",
        "lineage": {"parents": []},
    })

    graph.add_artifact({
        "artifact_id": ".N/child",
        "lineage": {"parents": [".N/root"]},
    })

    graph.add_artifact({
        "artifact_id": ".N/grandchild",
        "lineage": {"parents": [".N/child"]},
    })

    return graph


def test_walk_parents():
    graph = build_graph()

    parents = graph.walk_parents(".N/grandchild")

    assert ".N/child" in parents
    assert ".N/root" in parents


def test_walk_descendants():
    graph = build_graph()

    descendants = graph.walk_descendants(".N/root")

    assert ".N/child" in descendants
    assert ".N/grandchild" in descendants


def test_lineage_depth():
    graph = build_graph()

    assert graph.lineage_depth(".N/root") == 0
    assert graph.lineage_depth(".N/child") == 1
    assert graph.lineage_depth(".N/grandchild") == 2
