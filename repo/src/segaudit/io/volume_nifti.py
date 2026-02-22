"""NIfTI volume adapter (experimental)."""

from collections.abc import Iterator

from segaudit.core.types import Sample


def iter_samples() -> Iterator[Sample]:
    raise NotImplementedError("volume_nifti adapter is not implemented yet.")
