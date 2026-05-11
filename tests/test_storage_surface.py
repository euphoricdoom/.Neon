from neon.storage import connect, objects_root, require_vault_dirs, vault_root


def test_storage_surface_exports():
    assert callable(connect)
    assert callable(objects_root)
    assert callable(require_vault_dirs)
    assert callable(vault_root)
