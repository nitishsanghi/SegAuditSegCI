# SoftwareX Submission Checklist (SegAudit)

Status legend:
- `TODO`: not started
- `IN_PROGRESS`: partially implemented
- `DONE`: completed and evidenced in repo
- `BLOCKED`: external dependency (editorial/legal/etc.)

PR usage rule:
- Include one or more `SX-###` IDs in each PR description.
- A requirement can be marked `DONE` only when evidence is in-repo and verifiable.

## A) Repository and Engineering Gates

| ID | Requirement | Status | Evidence Path | Notes |
|---|---|---|---|---|
| SX-010 | Public open-access GitHub repo URL recorded in template metadata | TODO | N/A | Needs final public URL + template metadata field |
| SX-011 | `README.md` and `LICENSE.txt` present | DONE | `README.md`, `LICENSE.txt` | Keep README high quality per SX-014 |
| SX-012 | Source code under `repo/src` | DONE | `repo/src/` | Preserve this layout |
| SX-013 | Open-source recognized license | DONE | `LICENSE.txt` | MIT currently selected |
| SX-014 | README explains purpose, install, usage clearly | IN_PROGRESS | `README.md` | Expand as features ship |
| SX-016 | Data policy Option C satisfied (deposit+cite+link or valid exception) | TODO | N/A | Finalize dataset strategy and references |
| SX-017 | Data availability statement prepared | TODO | N/A | Add manuscript-ready statement |
| SX-018 | Software citation metadata complete | IN_PROGRESS | `CITATION.cff` | Add archive PID/versioned release citation |
| SX-019 | DOI/PID usage for key references and software release | TODO | N/A | Requires release archival (e.g., Zenodo) |

## B) Manuscript Content Gates

| ID | Requirement | Status | Evidence Path | Notes |
|---|---|---|---|---|
| SX-001 | Two-part submission model honored (paper + open-source distribution) | IN_PROGRESS | repo structure | Paper artifact pending |
| SX-002 | Official SoftwareX template used | TODO | N/A | Choose Word or LaTeX OSP template |
| SX-003 | Correct article type selected (`Original Software Publication`) | TODO | N/A | Submission-time action |
| SX-004 | <= 3000 words under SoftwareX counting rules | TODO | N/A | Validate near final draft |
| SX-005 | <= 6 figures | TODO | N/A | Lock figure plan early |
| SX-006 | Abstract <= 250 words | TODO | N/A | Validate near final draft |
| SX-007 | 1-7 keywords | TODO | N/A | Add in final manuscript |
| SX-008 | Complete title page + corresponding author info | TODO | N/A | Submission-time content |
| SX-009 | CRediT statement included | TODO | N/A | Add before submission |
| SX-027 | Word path only: figures embedded in `.docx` | TODO | N/A | Required only if Word template path chosen |
| SX-028 | LaTeX path only: PDF + source ZIP uploaded | TODO | N/A | Required only if LaTeX path chosen |

## C) Ethics, Policy, and Declarations Gates

| ID | Requirement | Status | Evidence Path | Notes |
|---|---|---|---|---|
| SX-020 | Submission declaration constraints satisfied | TODO | N/A | Verify prior-publication status at submit |
| SX-021 | Competing interests declaration prepared | TODO | N/A | Required via declarations workflow |
| SX-022 | Funding declaration prepared (or no-funding statement) | TODO | N/A | Add explicit text |
| SX-023 | AI-use declaration included if applicable | TODO | N/A | Required if non-trivial AI tool use in manuscript prep |
| SX-024 | No AI listed as author/co-author | DONE | authorship policy | Keep enforced |
| SX-026 | Submission checklist complete (files, refs, permissions, etc.) | IN_PROGRESS | `.github/pull_request_template.md`, `.github/workflows/softwarex-checklist-guard.yml`, `.github/workflows/ci.yml`, `docs/DESIGN_DOC_POLICY.md`, `docs/design/INDEX.md`, `docs/design/TEMPLATE.md` | PR-level enforcement added with stable required check names and canonical design-doc gating; final submission checklist still pending |
| SX-029 | Proof corrections returned within 2 days after acceptance | TODO | N/A | Operational readiness |

## D) Tracking and Audit Trail

Recommended cadence:
1. Update this checklist at the end of every PR.
2. Move an item to `DONE` only with concrete repo evidence or clear submission artifact.
3. Keep unresolved items visible; do not silently defer.

Suggested commit discipline:
1. Include changed `SX-###` IDs in commit messages or PR descriptions.
2. Add a short "SoftwareX impact" section in each PR.
