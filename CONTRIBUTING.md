# Contributing

Thanks for your interest in improving Agentic Index!

Please read our [Code of Conduct](./CODE_OF_CONDUCT.md) before participating.

To propose additions or changes:

1. Fork the repo and create your branch.
1. Make your changes with clear commits.
1. Open a pull request describing what you changed.
1. Tag your PR with `feature`, `enhancement`, `bug`, `fix`, `ci`, or `docs` so it appears in the release notes.

We welcome fixes to data, new repo suggestions, and other improvements.

Before opening a pull request, ensure the README table is up to date:

```bash
pre-commit run inject-readme --all-files
```

To run the scraping and ranking tools locally, install the CLI:

```bash
pip install agentic-index-cli
```

### Architecture

```
+---------+      +--------+      +----------+      +----------+
| Scraper | ---> | Cache  | ---> | Injector | ---> | Pull Req |
+---------+      +--------+      +----------+      +----------+
```

## Development environment

Set up Python 3.11 and install dependencies:

```bash
pip install -r requirements.txt
pip install -e .
pip install pre-commit
pre-commit install
```

Run the full test suite before pushing changes:

```bash
pytest -q
```
To view an HTML coverage report, run:
```bash
coverage html -d cov_html && open cov_html/index.html
```

### Test and workflow quickstart

```bash
pip install -r requirements.txt
pytest -q
python scripts/inject_readme.py
```

## Adding a New Metric

Touch files under `score/*.py`, update `scripts/inject_readme.py` and document your column in `README.md`. Include tests covering the metric and regenerate snapshots with the injector.
New metrics should maintain overall test coverage (see badges) and update any affected snapshots.




## Working on Launch Readiness Review Issues

A comprehensive project review was conducted in June 2025 to identify areas for improvement before launch. Findings from this review have been translated into actionable GitHub issues.

Contributors looking to help address these key items should refer to the main tracking issue:

*   **EPIC Issue:** `EPIC: Launch-readiness fixes (June 2025 review)` (Search for this issue in the repository's GitHub Issues tab).

This EPIC issue links to all individual tasks spawned from the review. Alternatively, you can view the full review document and linked issues in [REVIEW-2025-06.md](docs/REVIEW-2025-06.md).
