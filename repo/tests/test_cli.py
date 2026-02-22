"""CLI scaffold tests."""

from __future__ import annotations

import segaudit.cli as cli


def test_help_returns_zero() -> None:
    assert cli.main([]) == 0


def test_scaffolded_commands_present() -> None:
    parser = cli.build_parser()
    for command in {"eval", "gate", "drift", "report"}:
        args = parser.parse_args([command])
        assert args.command == command
        assert args.handler is cli._not_implemented


def test_unimplemented_command_returns_error_code() -> None:
    assert cli.main(["eval"]) == 2
