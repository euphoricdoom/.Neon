def test_public_import_surface_stays_stable():
    from neon import cli

    expected = [
        "main",
        "build_parser",
        "make_artifact",
        "validate_artifact",
        "canonical_bytes",
        "read_json",
        "sha256_bytes",
    ]

    for name in expected:
        assert hasattr(cli, name), name
