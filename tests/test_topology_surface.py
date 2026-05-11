from neon.topology import (
    ancestry_chain,
    artifact_metrics,
    descendant_chain,
)


def test_topology_surface_exports():
    assert callable(ancestry_chain)
    assert callable(artifact_metrics)
    assert callable(descendant_chain)
