"""Core types for SegAudit."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Mapping

ALLOWED_DOMAINS = frozenset({"adas", "medical", "industrial", "none"})


class SampleValidationError(ValueError):
    """Raised when a sample contract validation fails."""


def _require_mapping(value: Any, *, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise SampleValidationError(f"'{field_name}' must be a mapping.")
    return dict(value)


def _require_non_empty_string(value: Any, *, field_name: str) -> str:
    if not isinstance(value, str):
        raise SampleValidationError(f"'{field_name}' must be a non-empty string.")
    normalized = value.strip()
    if not normalized:
        raise SampleValidationError(f"'{field_name}' must be a non-empty string.")
    return normalized


@dataclass(slots=True)
class Sample:
    """Canonical internal sample representation."""

    pred: Any
    gt: Any | None = None
    logits: Any | None = None
    meta: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        """Validate the sample against the canonical contract."""
        meta = _require_mapping(self.meta, field_name="meta")
        sample_id = _require_non_empty_string(meta.get("sample_id"), field_name="meta.sample_id")
        domain = _require_non_empty_string(meta.get("domain"), field_name="meta.domain")
        sensor = _require_non_empty_string(meta.get("sensor"), field_name="meta.sensor")
        if domain not in ALLOWED_DOMAINS:
            allowed = ", ".join(sorted(ALLOWED_DOMAINS))
            raise SampleValidationError(
                f"'meta.domain' must be one of {{{allowed}}}, got '{domain}'."
            )
        if self.pred is None:
            raise SampleValidationError("'pred' is required and cannot be None.")
        meta["sample_id"] = sample_id
        meta["domain"] = domain
        meta["sensor"] = sensor
        self.meta = deepcopy(meta)
        self.pred = deepcopy(self.pred)
        if self.gt is not None:
            self.gt = deepcopy(self.gt)
        if self.logits is not None:
            self.logits = deepcopy(self.logits)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dictionary."""
        payload: dict[str, Any] = {"pred": deepcopy(self.pred), "meta": deepcopy(self.meta)}
        if self.gt is not None:
            payload["gt"] = deepcopy(self.gt)
        if self.logits is not None:
            payload["logits"] = deepcopy(self.logits)
        return payload

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> Sample:
        """Build and validate a Sample from a dictionary payload."""
        data = _require_mapping(payload, field_name="payload")
        if "pred" not in data:
            raise SampleValidationError("Sample payload is missing required field 'pred'.")
        if "meta" not in data:
            raise SampleValidationError("Sample payload is missing required field 'meta'.")
        return cls(
            pred=data["pred"],
            gt=data.get("gt"),
            logits=data.get("logits"),
            meta=data["meta"],
        )


def validate_sample(sample: Sample) -> None:
    """Validate a Sample instance."""
    sample.validate()
