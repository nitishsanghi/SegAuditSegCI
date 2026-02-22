"""Drift detector methods and severity mapping."""

from typing import Any, Mapping, NoReturn


def score_drift(
    data: Any,
    baseline: Any,
    config: Mapping[str, Any] | None = None,
) -> NoReturn:
    # TODO: Define a typed drift contract: required signal keys, detector params,
    # and expected severity output schema.
    raise NotImplementedError("drift detectors are not implemented yet.")
