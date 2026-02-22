"""LiDAR/range adapter (experimental)."""

from collections.abc import Iterator

from segaudit.core.types import Sample


def iter_samples() -> Iterator[Sample]:
    raise NotImplementedError("lidar_range adapter is not implemented yet.")
