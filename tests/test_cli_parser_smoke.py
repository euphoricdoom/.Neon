from neon.cli import build_parser


def parse(argv):
    return build_parser().parse_args(argv)


def test_parser_accepts_core_command_shapes():
    cases = [
        ["init"],
        ["demo"],
        ["register", "--title", "T", "--creator", "C"],
        ["derive", "--parent", ".N/root", "--title", "T", "--creator", "C"],
        ["validate", "artifact.neon"],
        ["hash", "artifact.neon"],
        ["store", "artifact.neon"],
        ["fetch", ".neon://sha256/abc"],
        ["export", "artifact.neon"],
        ["verify", "packet"],
        ["graph", "artifact.neon"],
        ["lineage", "artifact.neon"],
        ["descendants", "artifact.neon"],
        ["metrics", "artifact.neon"],
        ["log", "artifact.neon"],
        ["list"],
        ["status"],
        ["symbolic-status"],
    ]

    for case in cases:
        args = parse(case)
        assert callable(args.func), case
