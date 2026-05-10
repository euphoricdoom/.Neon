from neon.cli import canonical_bytes, sha256_bytes


def test_canonical_hash_stable():
    a = {"b": 2, "a": 1}
    b = {"a": 1, "b": 2}

    assert sha256_bytes(canonical_bytes(a)) == sha256_bytes(canonical_bytes(b))
