"""Tests for versioned schema models."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile

import pytest

from segaudit.report.schema import (
    BaselineStatsSchema,
    DriftSchema,
    GateSummarySchema,
    ReportSchema,
    SchemaValidationError,
    load_schema_file,
    validate_schema,
)


def _report_payload() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "run_info": {"command": "segaudit eval", "runtime_sec": 1.2},
        "dataset": {"format": "folder_masks", "num_images": 2},
        "metric_config": {"boundary_radius_px": 2, "connectivity": 8},
        "summary_metrics": {"miou": 0.82, "macro_dice": 0.88},
        "per_class_metrics": {"0": {"iou": 0.9}, "1": {"iou": 0.74}},
        "slices": [
            {
                "slice_id": "class=road",
                "filters": {"class": "road"},
                "support": {"pixels": 100},
                "metrics": {"miou": 0.8},
            }
        ],
        "regressions": [{"metric": "miou", "delta": -0.01}],
        "drift": {"severity": "low"},
        "artifacts": {"report_html": "out/report.html"},
    }


def _gate_summary_payload() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "result": "pass",
        "checks": [{"name": "overall_miou", "status": "pass"}],
        "exit_code": 0,
        "deltas": [{"name": "overall_miou", "delta": -0.01}],
        "metadata": {"run_id": "abc123"},
    }


def _drift_payload() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "baseline_ref": {"baseline_id": "baseline_2026_01_01"},
        "signals": [
            {
                "name": "class_area",
                "current_stat": {"road": 0.44},
                "baseline_stat": {"road": 0.41},
                "distance_score": 0.06,
                "severity": "low",
                "alert": False,
            }
        ],
        "severity": "low",
        "disclaimer": "Risk signal only; quality confirmation requires ground truth.",
        "interpretation": "risk_signal",
        "requires_gt_for_quality_confirmation": True,
    }


def _baseline_stats_payload() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "reference_window": {"num_samples": 256},
        "signals": {"class_area": {"road": {"mean": 0.42}}},
        "detector_config": {"method": "js"},
        "thresholds": {"low": 0.05, "medium": 0.1, "high": 0.2},
        "class_map_hash": "sha256:deadbeef",
    }


def test_report_schema_round_trip() -> None:
    payload = _report_payload()
    model = ReportSchema.from_dict(payload)
    as_json = model.to_json()
    reconstructed = ReportSchema.from_dict(json.loads(as_json))
    assert reconstructed.to_dict() == payload


def test_gate_summary_schema_round_trip() -> None:
    payload = _gate_summary_payload()
    model = GateSummarySchema.from_dict(payload)
    as_json = model.to_json()
    reconstructed = GateSummarySchema.from_dict(json.loads(as_json))
    assert reconstructed.to_dict() == payload


def test_drift_schema_round_trip() -> None:
    payload = _drift_payload()
    model = DriftSchema.from_dict(payload)
    as_json = model.to_json()
    reconstructed = DriftSchema.from_dict(json.loads(as_json))
    assert reconstructed.to_dict() == payload


def test_baseline_stats_schema_round_trip() -> None:
    payload = _baseline_stats_payload()
    model = BaselineStatsSchema.from_dict(payload)
    as_json = model.to_json()
    reconstructed = BaselineStatsSchema.from_dict(json.loads(as_json))
    assert reconstructed.to_dict() == payload


def test_report_schema_missing_required_field_raises_error() -> None:
    payload = _report_payload()
    payload.pop("summary_metrics")
    with pytest.raises(SchemaValidationError, match="summary_metrics"):
        ReportSchema.from_dict(payload)


def test_report_schema_rejects_unsupported_schema_version() -> None:
    payload = _report_payload()
    payload["schema_version"] = "2.0"
    with pytest.raises(SchemaValidationError, match="schema_version"):
        ReportSchema.from_dict(payload)


def test_gate_summary_invalid_result_raises_error() -> None:
    payload = _gate_summary_payload()
    payload["result"] = "unknown"
    with pytest.raises(SchemaValidationError, match="'result'"):
        GateSummarySchema.from_dict(payload)


def test_drift_disclaimer_fields_are_enforced() -> None:
    payload = _drift_payload()
    payload["interpretation"] = "quality_signal"
    with pytest.raises(SchemaValidationError, match="interpretation"):
        DriftSchema.from_dict(payload)


def test_baseline_stats_missing_hash_raises_error() -> None:
    payload = _baseline_stats_payload()
    payload.pop("class_map_hash")
    with pytest.raises(SchemaValidationError, match="class_map_hash"):
        BaselineStatsSchema.from_dict(payload)


def test_generic_validator_dispatches_by_schema_kind() -> None:
    validate_schema(_report_payload(), "report")
    validate_schema(_gate_summary_payload(), "gate_summary")
    validate_schema(_drift_payload(), "drift")
    validate_schema(_baseline_stats_payload(), "baseline_stats")


def test_generic_validator_rejects_unknown_schema_kind() -> None:
    with pytest.raises(SchemaValidationError, match="Unsupported schema kind"):
        validate_schema(_report_payload(), "unknown")


def test_load_schema_file_validates_payload_from_disk() -> None:
    payload = _report_payload()
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "report.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        loaded = load_schema_file(path, "report")
    assert loaded == payload
