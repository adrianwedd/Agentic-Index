# Unified Pipeline & Developer Experience Epic

This epic captures high-level improvements identified during a review of the repository. Each section lists concrete change requests. Completing them should result in a cleaner architecture, better documentation, and stronger tests.

## 1. Consolidate the Data Pipeline
- **Unify Scraping & Ranking** – Merge duplicated logic from `scripts/` and `agentic_index_cli/internal/` into a single canonical implementation under `agentic_index_cli`.
- **Clarify Workflow Usage** – Update `.github/workflows/update.yml` to use the canonical pipeline end-to-end.
- **Remove Redundant Files** – Delete outdated scripts once functionality lives in the library.

## 2. Expand Test Coverage
- **Cover Pipeline Utilities** – Add unit tests for scraping, enrichment, and ranking helpers.
- **Include `scripts/` in Coverage** – Configure `pytest` to measure both `agentic_index_cli` and `scripts` directories.
- **Raise the Threshold** – Increment `scripts/coverage_gate.py` from 49% toward 70% as tests improve.

## 3. Harden GitHub Actions
- **Explicit Permissions** – Add least‑privilege `permissions:` blocks to `ci.yml`, `rank.yml`, and `update.yml`.
- **Expose Failures** – Remove `|| true` from workflow steps so errors are not hidden.

## 4. Improve Documentation
- **Revise CLI Docs** – Rewrite `docs/cli.md` and the README quick‑start examples to reflect the consolidated command set.
- **Expand CONTRIBUTING** – Include setup instructions (`pip install -e .`, pre‑commit, running tests) for new contributors.
- **Explain FAST_START** – Clarify how `FAST_START.md` is generated and when to run the related command.

## 5. Optimize Scraping Performance
- **Adjust API Parameters** – Increase `per_page` in GitHub search calls and replace fixed delays with adaptive rate‑limit handling.
- **Cache Intermediate Data** – Store raw and enriched data files to avoid re-scraping unchanged repositories.

## 6. Formalize Licensing
- **Add LICENSE File** – Provide a root `LICENSE` describing the dual MIT/CC‑BY‑SA licensing.
- **Include Metadata** – Update `pyproject.toml` with license information and ensure badges point to the correct file.

## Acceptance Criteria
- A single, well-documented pipeline processes data from scraping through ranking and output generation.
- CI passes with the new tests and stricter coverage gate.
- Documentation clearly explains commands, contributor workflow, and licensing.

