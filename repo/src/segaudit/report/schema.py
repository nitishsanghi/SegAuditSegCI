"""Versioned report and summary schemas."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
import json
from typing import Any, Mapping

SCHEMA_VERSION_V1 = "1.0"
SUPPORTED_SCHEMA_VERSIONS = frozenset({SCHEMA_VERSION_V1})
GATE_RESULTS = frozenset({"pass", "fail", "error"})
EXIT_CODES = frozenset({0, 1, 2})
SEVERITY_LEVELS = frozenset({"low", "medium", "high"})
SCHEMA_KINDS = frozenset({"report", "gate_summary", "drift", "baseline_stats"})


class SchemaValidationError(ValueError):
    """Raised when a schema payload is invalid."""


def _as_mapping(value: Any, *, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise SchemaValidationError(f"'{field_name}' must be a mapping.")
    return dict(value)


def _as_list(value: Any, *, field_name: str) -> list[Any]:
    if not isinstance(value, list):
        raise SchemaValidationError(f"'{field_name}' must be a list.")
    return list(value)


def _as_dict_list(value: Any, *, field_name: str) -> list[dict[str, Any]]:
    items = _as_list(value, field_name=field_name)
    parsed: list[dict[str, Any]] = []
    for index, item in enumerate(items):
        parsed.append(_as_mapping(item, field_name=f"{field_name}[{index}]"))
    return parsed


def _as_non_empty_string(value: Any, *, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SchemaValidationError(f"'{field_name}' must be a non-empty string.")
    return value


def _as_int(value: Any, *, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise SchemaValidationError(f"'{field_name}' must be an integer.")
    return value


def _validate_schema_version(value: Any) -> str:
    schema_version = _as_non_empty_string(value, field_name="schema_version")
    if schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        supported = ", ".join(sorted(SUPPORTED_SCHEMA_VERSIONS))
        raise SchemaValidationError(
            f"'schema_version' must be one of {{{supported}}}, got '{schema_version}'."
        )
    return schema_version


def _require_keys(
    payload: Mapping[str, Any], required: tuple[str, ...], *, schema_name: str
) -> None:
    missing = [key for key in required if key not in payload]
    if missing:
        joined = ", ".join(missing)
        raise SchemaValidationError(
            f"{schema_name} payload is missing required field(s): {joined}."
        )


def _to_stable_json(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


@dataclass(slots=True)
class ReportSchema:
    """Schema model for report.json."""

    schema_version: str
    run_info: dict[str, Any]
    dataset: dict[str, Any]
    metric_config: dict[str, Any]
    summary_metrics: dict[str, Any]
    per_class_metrics: dict[str, Any]
    slices: list[dict[str, Any]]
    regressions: list[dict[str, Any]] | None = None
    drift: dict[str, Any] | None = None
    artifacts: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> ReportSchema:
        data = _as_mapping(payload, field_name="report")
        _require_keys(
            data,
            (
                "schema_version",
                "run_info",
                "dataset",
                "metric_config",
                "summary_metrics",
                "per_class_metrics",
                "slices",
            ),
            schema_name="report",
        )
        return cls(
            schema_version=_validate_schema_version(data["schema_version"]),
            run_info=_as_mapping(data["run_info"], field_name="run_info"),
            dataset=_as_mapping(data["dataset"], field_name="dataset"),
            metric_config=_as_mapping(data["metric_config"], field_name="metric_config"),
            summary_metrics=_as_mapping(data["summary_metrics"], field_name="summary_metrics"),
            per_class_metrics=_as_mapping(
                data["per_class_metrics"], field_name="per_class_metrics"
            ),
            slices=_as_dict_list(data["slices"], field_name="slices"),
            regressions=(
                _as_dict_list(data["regressions"], field_name="regressions")
                if "regressions" in data and data["regressions"] is not None
                else None
            ),
            drift=(
                _as_mapping(data["drift"], field_name="drift")
                if "drift" in data and data["drift"] is not None
                else None
            ),
            artifacts=(
                _as_mapping(data["artifacts"], field_name="artifacts")
                if "artifacts" in data and data["artifacts"] is not None
                else None
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "schema_version": self.schema_version,
            "run_info": deepcopy(self.run_info),
            "dataset": deepcopy(self.dataset),
            "metric_config": deepcopy(self.metric_config),
            "summary_metrics": deepcopy(self.summary_metrics),
            "per_class_metrics": deepcopy(self.per_class_metrics),
            "slices": deepcopy(self.slices),
        }
        if self.regressions is not None:
            payload["regressions"] = deepcopy(self.regressions)
        if self.drift is not None:
            payload["drift"] = deepcopy(self.drift)
        if self.artifacts is not None:
            payload["artifacts"] = deepcopy(self.artifacts)
        return payload

    def to_json(self) -> str:
        return _to_stable_json(self.to_dict())


@dataclass(slots=True)
class GateSummarySchema:
    """Schema model for gate_summary.json."""

    schema_version: str
    result: str
    checks: list[dict[str, Any]]
    exit_code: int
    deltas: list[dict[str, Any]] | None = None
    metadata: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> GateSummarySchema:
        data = _as_mapping(payload, field_name="gate_summary")
        _require_keys(
            data,
            ("schema_version", "result", "checks", "exit_code"),
            schema_name="gate_summary",
        )
        result = _as_non_empty_string(data["result"], field_name="result")
        if result not in GATE_RESULTS:
            allowed = ", ".join(sorted(GATE_RESULTS))
            raise SchemaValidationError(f"'result' must be one of {{{allowed}}}.")
        exit_code = _as_int(data["exit_code"], field_name="exit_code")
        if exit_code not in EXIT_CODES:
            allowed_exit = ", ".join(str(value) for value in sorted(EXIT_CODES))
            raise SchemaValidationError(f"'exit_code' must be one of {{{allowed_exit}}}.")
        return cls(
            schema_version=_validate_schema_version(data["schema_version"]),
            result=result,
            checks=_as_dict_list(data["checks"], field_name="checks"),
            exit_code=exit_code,
            deltas=(
                _as_dict_list(data["deltas"], field_name="deltas")
                if "deltas" in data and data["deltas"] is not None
                else None
            ),
            metadata=(
                _as_mapping(data["metadata"], field_name="metadata")
                if "metadata" in data and data["metadata"] is not None
                else None
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "schema_version": self.schema_version,
            "result": self.result,
            "checks": deepcopy(self.checks),
            "exit_code": self.exit_code,
        }
        if self.deltas is not None:
            payload["deltas"] = deepcopy(self.deltas)
        if self.metadata is not None:
            payload["metadata"] = deepcopy(self.metadata)
        return payload

    def to_json(self) -> str:
        return _to_stable_json(self.to_dict())


@dataclass(slots=True)
class DriftSchema:
    """Schema model for drift.json."""

    schema_version: str
    baseline_ref: dict[str, Any]
    signals: list[dict[str, Any]]
    severity: str
    disclaimer: str
    interpretation: str
    requires_gt_for_quality_confirmation: bool

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> DriftSchema:
        data = _as_mapping(payload, field_name="drift")
        _require_keys(
            data,
            (
                "schema_version",
                "baseline_ref",
                "signals",
                "severity",
                "disclaimer",
                "interpretation",
                "requires_gt_for_quality_confirmation",
            ),
            schema_name="drift",
        )
        severity = _as_non_empty_string(data["severity"], field_name="severity")
        if severity not in SEVERITY_LEVELS:
            allowed = ", ".join(sorted(SEVERITY_LEVELS))
            raise SchemaValidationError(f"'severity' must be one of {{{allowed}}}.")
        interpretation = _as_non_empty_string(
            data["interpretation"], field_name="interpretation"
        )
        if interpretation != "risk_signal":
            raise SchemaValidationError("'interpretation' must be 'risk_signal'.")
        requires_gt = data["requires_gt_for_quality_confirmation"]
        if not isinstance(requires_gt, bool):
            raise SchemaValidationError(
                "'requires_gt_for_quality_confirmation' must be a boolean."
            )
        if requires_gt is not True:
            raise SchemaValidationError(
                "'requires_gt_for_quality_confirmation' must be true for drift outputs."
            )
        return cls(
            schema_version=_validate_schema_version(data["schema_version"]),
            baseline_ref=_as_mapping(data["baseline_ref"], field_name="baseline_ref"),
            signals=_as_dict_list(data["signals"], field_name="signals"),
            severity=severity,
            disclaimer=_as_non_empty_string(data["disclaimer"], field_name="disclaimer"),
            interpretation=interpretation,
            requires_gt_for_quality_confirmation=requires_gt,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "baseline_ref": deepcopy(self.baseline_ref),
            "signals": deepcopy(self.signals),
            "severity": self.severity,
            "disclaimer": self.disclaimer,
            "interpretation": self.interpretation,
            "requires_gt_for_quality_confirmation": self.requires_gt_for_quality_confirmation,
        }

    def to_json(self) -> str:
        return _to_stable_json(self.to_dict())


@dataclass(slots=True)
class BaselineStatsSchema:
    """Schema model for baseline_stats.json."""

    schema_version: str
    reference_window: dict[str, Any]
    signals: dict[str, Any]
    detector_config: dict[str, Any]
    thresholds: dict[str, Any]
    class_map_hash: str

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> BaselineStatsSchema:
        data = _as_mapping(payload, field_name="baseline_stats")
        _require_keys(
            data,
            (
                "schema_version",
                "reference_window",
                "signals",
                "detector_config",
                "thresholds",
                "class_map_hash",
            ),
            schema_name="baseline_stats",
        )
        return cls(
            schema_version=_validate_schema_version(data["schema_version"]),
            reference_window=_as_mapping(
                data["reference_window"], field_name="reference_window"
            ),
            signals=_as_mapping(data["signals"], field_name="signals"),
            detector_config=_as_mapping(
                data["detector_config"], field_name="detector_config"
            ),
            thresholds=_as_mapping(data["thresholds"], field_name="thresholds"),
            class_map_hash=_as_non_empty_string(
                data["class_map_hash"], field_name="class_map_hash"
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "reference_window": deepcopy(self.reference_window),
            "signals": deepcopy(self.signals),
            "detector_config": deepcopy(self.detector_config),
            "thresholds": deepcopy(self.thresholds),
            "class_map_hash": self.class_map_hash,
        }

    def to_json(self) -> str:
        return _to_stable_json(self.to_dict())


def validate_report(payload: Mapping[str, Any]) -> ReportSchema:
    """Validate and parse a report schema payload."""
    return ReportSchema.from_dict(payload)


def validate_gate_summary(payload: Mapping[str, Any]) -> GateSummarySchema:
    """Validate and parse a gate_summary schema payload."""
    return GateSummarySchema.from_dict(payload)


def validate_drift(payload: Mapping[str, Any]) -> DriftSchema:
    """Validate and parse a drift schema payload."""
    return DriftSchema.from_dict(payload)


def validate_baseline_stats(payload: Mapping[str, Any]) -> BaselineStatsSchema:
    """Validate and parse a baseline_stats schema payload."""
    return BaselineStatsSchema.from_dict(payload)


def validate_schema(payload: Mapping[str, Any], schema_kind: str) -> None:
    """Validate a payload for a supported schema kind."""
    if schema_kind not in SCHEMA_KINDS:
        allowed = ", ".join(sorted(SCHEMA_KINDS))
        raise SchemaValidationError(
            f"Unsupported schema kind '{schema_kind}'. Expected one of {{{allowed}}}."
        )
    if schema_kind == "report":
        validate_report(payload)
        return
    if schema_kind == "gate_summary":
        validate_gate_summary(payload)
        return
    if schema_kind == "drift":
        validate_drift(payload)
        return
    validate_baseline_stats(payload)


def load_schema_file(path: str | Path, schema_kind: str) -> dict[str, Any]:
    """Load and validate a schema file from disk."""
    schema_path = Path(path)
    with schema_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, Mapping):
        raise SchemaValidationError(
            f"Top-level JSON payload in '{schema_path}' must be a mapping."
        )
    payload_dict = dict(payload)
    validate_schema(payload_dict, schema_kind)
    return payload_dict
