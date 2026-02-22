# SegAudit

SegAudit is a CI-grade quality platform for segmentation systems.

This repository currently contains PR1 scaffold:
- Python package and CLI entrypoint
- Source layout under `repo/src`
- Test skeleton
- GitHub Actions CI skeleton
- SoftwareX tracking docs (`docs/SOFTWAREX_REQUIREMENTS.md`, `docs/SOFTWAREX_CHECKLIST.md`)

## Quickstart

```bash
python -m pip install -e ".[dev]"
segaudit --help
pytest -q
```

## Planned Commands

- `segaudit eval`
- `segaudit gate`
- `segaudit drift`
- `segaudit report`

These commands are scaffolded in this PR and return a non-zero code until implemented.

## Repository Layout

```text
repo/src/segaudit/   # package source
repo/tests/          # tests
repo/examples/       # demo assets (planned)
repo/data/           # tiny data or generators (planned)
docs/                # SoftwareX requirements + submission checklist
```
