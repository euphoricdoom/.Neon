from neon.cli import build_parser


def test_cli_exposes_core_command_surface():
    parser = build_parser()
    subparsers = None

    for action in parser._actions:
        if hasattr(action, "choices") and action.choices:
            subparsers = action
            break

    assert subparsers is not None

    commands = set(subparsers.choices.keys())
    expected = {
        "init",
        "demo",
        "register",
        "derive",
        "validate",
        "hash",
        "store",
        "fetch",
        "export",
        "verify",
        "graph",
        "lineage",
        "descendants",
        "metrics",
        "log",
        "list",
        "status",
        "symbolic-status",
    }

    assert expected <= commands
