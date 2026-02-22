# SoftwareX Requirements (Repository Source of Truth)

This document captures the SoftwareX author-guide requirements that directly affect SegAudit engineering, release, and submission workflow.

## Source
- Guide file: `Guide for authors - SoftwareX - ISSN 2352-7110 | ScienceDirect.com by Elsevier.pdf`
- Journal page used: `https://www.sciencedirect.com/journal/softwarex/publish/guide-for-authors`
- Extracted locally on 2026-02-22 via `PyPDF2` for page-level parsing.
- Page references below are from the extracted PDF pages.

## Usage Rules
- Treat `MUST` items as release-gating for SoftwareX submission.
- Treat `SHOULD` items as strongly recommended unless the editor advises otherwise.
- If the guide changes, update this file and `docs/SOFTWAREX_CHECKLIST.md` in the same PR.

## Locked Requirements

### Submission Model
- `SX-001` (`MUST`): Submit as two parts: (a) a short descriptive paper and (b) an open-source software distribution with support material. (p.3)
- `SX-002` (`MUST`): Use the journal-specific SoftwareX template (Word or LaTeX). (p.3, p.19, p.25)
- `SX-003` (`MUST`): Select `Original Software Publication` for first publication; select `Software Update` only for updates to previously published SoftwareX software. (p.26)

### Manuscript Limits and Structure
- `SX-004` (`MUST`): Paper limit is 3000 words max, excluding title/authors/affiliations/references/metadata tables and including abstract/running text/captions/footnotes. (p.26)
- `SX-005` (`MUST`): Maximum six figures. (p.26)
- `SX-006` (`MUST`): Abstract must be concise and not exceed 250 words. (p.13)
- `SX-007` (`MUST`): Provide 1 to 7 keywords. (p.13)
- `SX-008` (`MUST`): Include required title-page fields, including corresponding author contact details. (p.12-13)
- `SX-009` (`MUST`): Provide CRediT author contributions statement. (p.20-21)

### Repository and Code Distribution
- `SX-010` (`MUST`): Software must be publicly available in an open-access GitHub repository and the repository URL must be recorded in template metadata. (p.26)
- `SX-011` (`MUST`): Repository must include `README.md` and `LICENSE.txt`. (p.26)
- `SX-012` (`MUST`): Source code must be under `repo/src`. (p.26)
- `SX-013` (`MUST`): Software/code must be open source under a recognized legal license (OSI-recognized or approved by editorial office). (p.26)
- `SX-014` (`SHOULD`): README should clearly explain purpose, installation, and usage for reuse and validation. (p.26)
- `SX-015` (`INFO`): SoftwareX archives accepted code in its GitHub repository after acceptance. (p.4)

### Data, Reproducibility, and Citation
- `SX-016` (`MUST`): Data policy Option C applies: deposit research data in a relevant repository, cite/link it in the article, or explain why sharing is not possible. (p.17)
- `SX-017` (`MUST`): Provide a data availability statement at submission. (p.18)
- `SX-018` (`MUST`): Cite software properly in references (software citation elements including creator/title/venue/date/identifier/version). (p.23-24)
- `SX-019` (`SHOULD`): Use DOI links where possible for persistent referencing. (p.22)

### Ethics and Declarations
- `SX-020` (`MUST`): Submission declaration requirements apply (not published elsewhere, not under consideration elsewhere, approved by all authors). (p.5)
- `SX-021` (`MUST`): Declare competing interests via the declarations process. (p.6-7)
- `SX-022` (`MUST`): Declare funding sources (or explicit no-funding statement). (p.7)
- `SX-023` (`MUST`): If generative AI tools were used in manuscript preparation beyond basic spelling/grammar/reference checks, include the required AI disclosure section before references. (p.7-8)
- `SX-024` (`MUST`): AI tools cannot be listed as authors/co-authors. (p.8)

### Review and Production Workflow
- `SX-025` (`INFO`): Peer review is single-anonymized and typically uses at least two reviewers. (p.4)
- `SX-026` (`MUST`): Submission checklist compliance is required (all files uploaded, references matched, permissions obtained, etc.). (p.25)
- `SX-027` (`MUST`): If Word template is used, figures must be embedded in the `.docx`. (p.3, p.19, p.25)
- `SX-028` (`MUST`): If LaTeX template is used, upload manuscript PDF plus full source ZIP in Editorial Manager. (p.26)
- `SX-029` (`MUST`): Proof corrections are expected within two days. (p.27)

## Local Interpretation for SegAudit
- Treat `SX-010` to `SX-014` and `SX-016` to `SX-019` as engineering-release inputs.
- Treat `SX-001` to `SX-009` and `SX-020` to `SX-029` as manuscript/submission gates.
- Every implementation PR should reference relevant `SX-###` IDs in its description.
