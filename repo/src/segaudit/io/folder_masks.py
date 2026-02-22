"""Folder masks adapter (GA target)."""

from collections.abc import Iterator

from segaudit.core.types import Sample


def iter_samples() -> Iterator[Sample]:
    raise NotImplementedError("folder_masks adapter is not implemented yet.")
