"""Dataset adapter registry."""


def get_adapter(name: str) -> None:
    raise NotImplementedError(f"Adapter '{name}' is not implemented yet.")
