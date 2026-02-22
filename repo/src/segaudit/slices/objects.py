"""Object-level slice utilities."""

from typing import Any, Mapping, NoReturn


def object_statistics(
    segmentation: Any,
    image: Any | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> NoReturn:
    # TODO: Accept canonical segmentation inputs and return deterministic
    # per-object stats (size, thinness, support) for slice generation.
    raise NotImplementedError("object slicing utilities are not implemented yet.")
