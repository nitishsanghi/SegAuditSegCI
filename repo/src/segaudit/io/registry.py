"""Dataset adapter registry."""

from typing import NoReturn


def get_adapter(name: str) -> NoReturn:
    raise NotImplementedError(f"Adapter '{name}' is not implemented yet.")
