"""COCO RLE adapter (experimental)."""

from collections.abc import Iterator

from segaudit.core.types import Sample


def iter_samples() -> Iterator[Sample]:
    raise NotImplementedError("coco_rle adapter is not implemented yet.")
