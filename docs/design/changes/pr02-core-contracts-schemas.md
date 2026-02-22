# PR2 Core Contracts and Schemas

## Metadata
- Owner: SegAudit maintainers
- Date: 2026-02-22
- Roadmap PR: PR2
- Related SX IDs: SX-012, SX-014, SX-026

## Problem
Current scaffold has placeholder functions and no enforceable contract models. We need stable internal and output schemas before building adapters, metrics, and CLI outputs.

## Scope
1. Define `Sample` contract for evaluation and drift pathways.
2. Implement versioned schema models for:
- `report.json`
- `gate_summary.json`
- `drift.json`
- `baseline_stats.json`
3. Add schema validation and round-trip tests.

## Non-goals
1. No real metric computation.
2. No real I/O adapter implementation beyond contracts.
3. No CLI behavior changes beyond schema plumbing if needed.

## Contracts
1. `Sample` contains prediction payload, optional GT, optional logits, and metadata.
2. Required `Sample.meta` fields:
- `sample_id`: non-empty string
- `sensor`: non-empty string
- `domain`: non-empty string in `{adas, medical, industrial, none}`
3. Every output schema includes `schema_version`.
4. Validation must produce deterministic errors for missing/invalid fields.

## Data/Schema Impact
1. `repo/src/segaudit/core/types.py`: canonical `Sample`.
2. `repo/src/segaudit/report/schema.py`: versioned models and validators.
3. Test fixtures for minimal valid documents per schema.

## Determinism Rules
1. Stable field names and explicit defaults.
2. Stable serialization order in tests where practical.
3. No implicit random values in schema outputs.

## Test Plan
1. Unit tests for each schema validator (valid + invalid cases).
2. Round-trip serialization tests.
3. Regression tests for required fields and `schema_version`.

## Risks and Rollback
1. Risk: Overly rigid schema may block later modules.
- Mitigation: keep optional fields where evolution is expected.
2. Rollback: revert schema model additions as one commit if downstream breakage appears.
