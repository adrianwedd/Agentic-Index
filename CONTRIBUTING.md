# Contributing

Thanks for your interest in improving Agentic Index!

Please read our [Code of Conduct](./CODE_OF_CONDUCT.md) before participating.

To propose additions or changes:

1. Fork the repo and create your branch.
1. Make your changes with clear commits.
1. Open a pull request describing what you changed.

We welcome fixes to data, new repo suggestions, and other improvements.

Before opening a pull request, ensure the README table is up to date:

```bash
pre-commit run inject-readme --all-files
```

To run the scraping and ranking tools locally, install the CLI:

```bash
pip install agentic-index-cli
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

## Working on Launch Readiness Review Issues

A comprehensive project review was conducted in June 2025 to identify areas for improvement before launch. Findings from this review have been translated into actionable GitHub issues.

Contributors looking to help address these key items should refer to the main tracking issue:

*   **EPIC Issue:** `EPIC: Launch-readiness fixes (June 2025 review)` (Search for this issue in the repository's GitHub Issues tab).

This EPIC issue links to all individual tasks spawned from the review. Alternatively, you can view the full review document and linked issues in [REVIEW-2025-06.md](docs/REVIEW-2025-06.md).
