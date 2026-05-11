from neon.metrics import ContinuityMetrics, summarize_metrics



def test_derivation_ratio_zero_safe():
    metrics = ContinuityMetrics(
        artifact_id=".N/example",
        parent_count=0,
        child_count=2,
        ancestor_count=0,
        descendant_count=4,
        lineage_depth=1,
    )

    assert metrics.derivation_ratio == 4.0



def test_influence_ratio_zero_safe():
    metrics = ContinuityMetrics(
        artifact_id=".N/example",
        parent_count=0,
        child_count=3,
        ancestor_count=1,
        descendant_count=1,
        lineage_depth=1,
    )

    assert metrics.influence_ratio == 3.0



def test_continuity_vector_shape():
    metrics = ContinuityMetrics(
        artifact_id=".N/example",
        parent_count=1,
        child_count=2,
        ancestor_count=3,
        descendant_count=4,
        lineage_depth=5,
    )

    assert metrics.continuity_vector == (5, 3, 4)



def test_pressure_vector_shape():
    metrics = ContinuityMetrics(
        artifact_id=".N/example",
        parent_count=7,
        child_count=8,
        ancestor_count=9,
        descendant_count=10,
        lineage_depth=11,
    )

    assert metrics.pressure_vector == (7, 8)



def test_summary_contains_key_fields():
    metrics = ContinuityMetrics(
        artifact_id=".N/example",
        parent_count=1,
        child_count=2,
        ancestor_count=3,
        descendant_count=4,
        lineage_depth=5,
    )

    summary = summarize_metrics(metrics)

    assert ".N/example" in summary
    assert "vector=" in summary
    assert "pressure=" in summary
