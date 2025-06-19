# Release 0.1.1 Hardening Epic

This epic captures the remaining work needed to stabilize the Agentic Index pipeline and tooling for the upcoming 0.1.1 release.

## 1. Finalize Pipeline Automation
- **End‑to‑End Smoke Test** – `scripts/e2e_test.sh` chains scraping, enrichment, ranking and README injection using fixture data. The script should fail on any step error.
- **CI Integration** – Add a GitHub Actions job that runs the smoke test on pull requests.
- **Rollback Steps** – Document how to revert pipeline state if a step corrupts the dataset.

## 2. Strengthen API Server
- **Parameter Validation** – Use Pydantic models for all request bodies to enforce schema and provide helpful errors.
- **Error Logging** – Include request IDs in logs and surface stack traces in debug mode.
- **Rate Limit Metrics** – Track GitHub API quota usage and expose it via `/status`.

## 3. Documentation and Release Prep
- **Changelog Update** – Summarize user‑visible changes since 0.1.0.
- **Upgrade Guide** – Note any breaking interface changes and recommended migration steps.
- **Release Checklist** – Provide a script or checklist for tagging and publishing the release.

## Acceptance Criteria
- The smoke test passes locally and in CI.
- API endpoints reject malformed input with clear error messages.
- Release notes fully describe new features and fixes.

## 4. Additional Hardening
- **Non-Interactive Setup** – Allow `scripts/setup-env.sh` to read tokens from a `.env` file so CI can run without prompts.
- **Pipeline Rollback Guide** – Provide instructions for reverting data if a refresh introduces bad results.
- **Fixture-Based E2E Test** – Use small fixture data in `scripts/e2e_test.sh` so the pipeline can be validated quickly.
- **Validation Log** – See `../e2e_pipeline_validation.md` for the latest end-to-end refresh attempt and results.
