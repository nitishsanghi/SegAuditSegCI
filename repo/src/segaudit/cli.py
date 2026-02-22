"""CLI entrypoint for SegAudit."""

from __future__ import annotations

import argparse
import sys
from typing import Sequence

from segaudit import __version__


def _not_implemented(args: argparse.Namespace) -> int:
    command = getattr(args, "command", "unknown")
    print(
        f"Command '{command}' is scaffolded but not implemented yet.",
        file=sys.stderr,
    )
    return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="segaudit",
        description="SegAudit command line interface.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")

    command_help = {
        "eval": "Run segmentation evaluation and produce report.json.",
        "gate": "Evaluate gates against a report and return CI-safe exit code.",
        "drift": "Compute prediction-only drift signals.",
        "report": "Render static report artifacts.",
    }
    for command, help_text in command_help.items():
        cmd = subparsers.add_parser(command, help=help_text, description=help_text)
        cmd.set_defaults(handler=_not_implemented)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return 0
    return int(handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
