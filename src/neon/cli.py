from __future__ import annotations

import argparse

from neon.commands.core import (
    cmd_demo,
    cmd_derive,
    cmd_descendants,
    cmd_export,
    cmd_fetch,
    cmd_graph,
    cmd_hash,
    cmd_init,
    cmd_lineage,
    cmd_list,
    cmd_log,
    cmd_metrics,
    cmd_register,
    cmd_status,
    cmd_store,
    cmd_validate,
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


def add_artifact_arg(subparsers: argparse._SubParsersAction, name: str, func) -> None:
    parser = subparsers.add_parser(name)
    parser.add_argument("artifact")
    parser.set_defaults(func=func)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="neon")
    sub = parser.add_subparsers(required=True)

    p = sub.add_parser("init")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("demo")
    p.add_argument("--creator", default="Carl Sowers")
    p.set_defaults(func=cmd_demo)

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

    add_artifact_arg(sub, "validate", cmd_validate)
    add_artifact_arg(sub, "hash", cmd_hash)
    add_artifact_arg(sub, "store", cmd_store)
    add_artifact_arg(sub, "export", cmd_export)
    add_artifact_arg(sub, "log", cmd_log)

    p = sub.add_parser("verify")
    p.add_argument("target")
    p.set_defaults(func=cmd_verify)

    p = sub.add_parser("fetch")
    p.add_argument("uri")
    p.add_argument("--out")
    p.set_defaults(func=cmd_fetch)

    p = sub.add_parser("graph")
    p.add_argument("artifact")
    p.add_argument("--format", choices=["mermaid", "json"], default="mermaid")
    p.set_defaults(func=cmd_graph)

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

    p = sub.add_parser("list")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("status")
    p.set_defaults(func=cmd_status)

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
