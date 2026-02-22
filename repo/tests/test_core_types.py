"""Tests for core typed contracts."""

from __future__ import annotations

import pytest

from segaudit.core.types import Sample, SampleValidationError


def test_sample_from_dict_validates_required_meta_fields() -> None:
    sample = Sample.from_dict(
        {
            "pred": [[0, 1], [1, 0]],
            "gt": [[0, 1], [0, 0]],
            "meta": {
                "sample_id": "img_0001",
                "domain": "none",
                "sensor": "rgb",
            },
        }
    )

    assert sample.meta["sample_id"] == "img_0001"
    assert sample.meta["domain"] == "none"
    assert sample.meta["sensor"] == "rgb"


def test_sample_missing_meta_raises_validation_error() -> None:
    with pytest.raises(SampleValidationError, match="missing required field 'meta'"):
        Sample.from_dict({"pred": [[0, 1], [1, 0]]})


def test_sample_invalid_domain_raises_validation_error() -> None:
    with pytest.raises(SampleValidationError, match=r"meta\.domain"):
        Sample.from_dict(
            {
                "pred": [[0, 1], [1, 0]],
                "meta": {
                    "sample_id": "img_0002",
                    "domain": "satellite",
                    "sensor": "rgb",
                },
            }
        )


def test_sample_round_trip_dict() -> None:
    payload = {
        "pred": [[1, 1], [0, 0]],
        "gt": [[1, 0], [0, 0]],
        "logits": [[[0.1, 0.9], [0.7, 0.3]]],
        "meta": {
            "sample_id": "img_0042",
            "domain": "medical",
            "sensor": "ct",
            "spacing": [1.0, 1.0, 5.0],
        },
    }

    sample = Sample.from_dict(payload)
    assert sample.to_dict() == payload


def test_sample_meta_fields_are_normalized() -> None:
    sample = Sample.from_dict(
        {
            "pred": [[0, 1], [1, 0]],
            "meta": {
                "sample_id": "  img_1001  ",
                "domain": "  none  ",
                "sensor": "  rgb  ",
            },
        }
    )
    assert sample.meta["sample_id"] == "img_1001"
    assert sample.meta["domain"] == "none"
    assert sample.meta["sensor"] == "rgb"


def test_sample_construction_deepcopies_payload_objects() -> None:
    payload = {
        "pred": [[1, 0], [0, 1]],
        "gt": [[1, 1], [0, 0]],
        "logits": [[[0.2, 0.8], [0.7, 0.3]]],
        "meta": {
            "sample_id": "img_2001",
            "domain": "none",
            "sensor": "rgb",
            "tags": ["day", "clear"],
        },
    }
    sample = Sample.from_dict(payload)

    payload["pred"][0][0] = 9
    payload["gt"][0][0] = 9
    payload["logits"][0][0][0] = 9.9
    payload["meta"]["tags"][0] = "night"

    assert sample.pred == [[1, 0], [0, 1]]
    assert sample.gt == [[1, 1], [0, 0]]
    assert sample.logits == [[[0.2, 0.8], [0.7, 0.3]]]
    assert sample.meta["tags"] == ["day", "clear"]
