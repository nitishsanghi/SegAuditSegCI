"""Core types for SegAudit."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Sample:
    """Canonical internal sample representation."""

    pred: Any
    gt: Any | None = None
    logits: Any | None = None
    meta: dict[str, Any] = field(default_factory=dict)
