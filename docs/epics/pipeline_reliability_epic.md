# Pipeline Reliability & Observability Epic

This epic outlines improvements identified during a review of the repository and its GitHub Actions workflows. The goal is to make the refresh pipeline more resilient, easier to debug, and simpler for contributors to run locally.

## 1. Strengthen Data Pipeline
- **Asynchronous Requests** – Refactor `agentic_index_cli/agentic_index.py` and the scraping helpers in `scripts/` to use `aiohttp` with concurrency controls. This will reduce run time and handle network hiccups more gracefully.
- **Central Retry Logic** – Extract the exponential backoff code used in `agentic_index_cli/internal/scrape.py` and `scripts/scrape_repos.py` into a shared utility. Apply consistent rate-limit handling across the pipeline.
- **Checkpointing** – Update `scripts/trigger_refresh.sh` and related workflows so intermediate JSON files are cached. If a step fails, reruns should resume from the last successful stage.
- **Structured Logging** – Replace scattered `print` calls with Python's `logging` module and emit step timing metrics. Log files should be uploaded as workflow artifacts for later analysis.

## 2. Expand Validation & Testing
- **Schema Enforcement** – Validate `data/repos.json` against `schemas/repo.schema.json` after every enrichment step, not only at the end. Add negative tests in `tests` to cover failure cases.
- **Simulate API Errors** – Extend `tests/test_scrape_mock.py` to include timeout and rate‑limit scenarios. The pipeline should retry and eventually surface a clear error if GitHub remains unreachable.
- **Coverage for Scripts** – Many helpers under `scripts/` lack tests. Add unit tests so their behaviour is captured before refactoring.

## 3. Harden GitHub Actions
- **Least‑Privilege Permissions** – Add explicit `permissions:` blocks to workflows such as `ci.yml`, `rank.yml` and `update.yml` (currently they run with the default broad token). Grant `contents: read` or `write` only where necessary.
- **Fail Fast** – Ensure each step stops the job when commands fail. Remove any remaining `|| true` patterns and set `fail-fast: true` in matrix strategies.
- **Traceability** – Upload `data/history/*.json` and log files as artifacts so failed runs can be inspected.

## 4. Improve Documentation
- **Refresh Guide** – Expand [docs/REFRESH.md](../REFRESH.md) with a numbered walkthrough of the nightly workflow, environment variables required, and tips for reproducing it locally.
- **Local Dev Script** – Document a one‑command wrapper (e.g. `./scripts/dev_refresh.sh`) that chains scrape, enrich, rank, and README injection. Mention this in [ONBOARDING.md](../ONBOARDING.md).
- **Architecture Diagram** – Update `docs/architecture/agentic_index_cli.svg` to reflect the new async components and logging layer once implemented.

## Acceptance Criteria
- Refresh workflow completes reliably even when GitHub intermittently fails.
- Workflow runs upload logs and intermediate artifacts for debugging.
- Documentation explains how to run and troubleshoot the pipeline locally.
