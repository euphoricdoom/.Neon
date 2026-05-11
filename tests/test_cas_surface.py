from neon.cas import cas_path, cas_uri, parse_cas_uri


def test_cas_surface_exports():
    assert callable(cas_path)
    assert callable(cas_uri)
    assert callable(parse_cas_uri)
