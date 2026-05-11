from neon import cli


def test_cli_exports_legacy_helpers_for_compatibility():
    assert callable(cli.make_artifact)
    assert callable(cli.validate_artifact)
    assert callable(cli.canonical_bytes)
    assert callable(cli.read_json)
    assert callable(cli.sha256_bytes)
