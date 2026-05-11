from neon.lifecycle import (
    make_artifact,
    neon_id,
    resolve_artifact_path,
    save_artifact,
)


def test_lifecycle_surface_exports():
    assert callable(make_artifact)
    assert callable(neon_id)
    assert callable(resolve_artifact_path)
    assert callable(save_artifact)
