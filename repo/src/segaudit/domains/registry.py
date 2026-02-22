"""Domain pack registry."""

from typing import NoReturn


def get_domain_pack(name: str) -> NoReturn:
    raise NotImplementedError(f"Domain pack '{name}' is not implemented yet.")
