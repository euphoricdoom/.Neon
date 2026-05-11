from neon.cli import build_parser


def test_build_parser_returns_argparse_parser():
    parser = build_parser()
    assert parser.prog == "neon"
