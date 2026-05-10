from neon.cli import make_artifact, validate_artifact


def test_valid_artifact_passes():
    artifact = make_artifact(
        title="Invoice Workflow",
        creator="Carl Sowers",
        artifact_type="workflow",
        statement="Example",
    )

    assert validate_artifact(artifact) == []


def test_invalid_artifact_fails():
    artifact = {"kind": "broken"}

    assert validate_artifact(artifact)
