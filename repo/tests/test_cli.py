"""CLI scaffold tests."""

from __future__ import annotations

import segaudit.cli as cli


def test_help_returns_zero() -> None:
    assert cli.main([]) == 0


def test_scaffolded_commands_present() -> None:
    parser = cli.build_parser()
    subparsers_actions = [
        action
        for action in parser._actions
        if action.__class__.__name__ == "_SubParsersAction"
    ]
    assert len(subparsers_actions) == 1
    commands = set(subparsers_actions[0].choices.keys())
    assert commands == {"eval", "gate", "drift", "report"}


def test_unimplemented_command_returns_error_code() -> None:
    assert cli.main(["eval"]) == 2
