from __future__ import annotations

import argparse

from neon.commands.core import (
    cmd_derive,
    cmd_descendants,
    cmd_export,
    cmd_init,
    cmd_lineage,
    cmd_metrics,
    cmd_register,
    cmd_store,
    cmd_verify,
)
from neon.symbols import SYMBOLS, symbolic_state


def cmd_symbolic_status(args: argparse.Namespace) -> None:
    print(symbolic_state(SYMBOLS["hot_context"], "v0.2", SYMBOLS["project"]))
    print("✓ λ.hashing")
    print("✓ λ.cas")
    print("✓ λ.proof-packets")
    print("✓ λ.lineage")
    print("✓ λ.symbolic-helpers")
    print("◐ λ.modular-decomposition")
    print("◐ λ.golden-freeze")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="neon")
    sub = parser.add_subparsers(required=True)

    p = sub.add_parser("init")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("register")
    p.add_argument("--title", required=True)
    p.add_argument("--creator", required=True)
    p.add_argument("--type", default="workflow")
    p.add_argument("--statement", default="")
    p.set_defaults(func=cmd_register)

    p = sub.add_parser("derive")
    p.add_argument("--parent", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--creator", required=True)
    p.add_argument("--type", default="workflow")
    p.add_argument("--statement", default="")
    p.set_defaults(func=cmd_derive)

    p = sub.add_parser("store")
    p.add_argument("artifact")
    p.set_defaults(func=cmd_store)

    p = sub.add_parser("export")
    p.add_argument("artifact")
    p.set_defaults(func=cmd_export)

    p = sub.add_parser("verify")
    p.add_argument("target")
    p.set_defaults(func=cmd_verify)

    p = sub.add_parser("lineage")
    p.add_argument("artifact")
    p.add_argument("--root", default=".")
    p.add_argument("--format", choices=["text", "json"], default="text")
    p.set_defaults(func=cmd_lineage)

    p = sub.add_parser("descendants")
    p.add_argument("artifact")
    p.add_argument("--root", default=".")
    p.add_argument("--format", choices=["text", "json"], default="text")
    p.set_defaults(func=cmd_descendants)

    p = sub.add_parser("metrics")
    p.add_argument("artifact")
    p.add_argument("--root", default=".")
    p.add_argument("--format", choices=["text", "json"], default="text")
    p.set_defaults(func=cmd_metrics)

    p = sub.add_parser("symbolic-status")
    p.set_defaults(func=cmd_symbolic_status)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
