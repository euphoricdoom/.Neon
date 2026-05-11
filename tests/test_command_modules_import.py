def test_command_module_imports_cleanly():
    import neon.commands.core as core

    required = [
        "cmd_register",
        "cmd_derive",
        "cmd_store",
        "cmd_fetch",
        "cmd_verify",
    ]

    for name in required:
        assert hasattr(core, name), name
