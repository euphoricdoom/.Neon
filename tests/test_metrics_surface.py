from neon.metrics import summarize_metrics


def test_metrics_surface_exports():
    assert callable(summarize_metrics)
