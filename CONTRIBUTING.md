# Contributing

Thanks for your interest in improving Agentic Index!

Please read our [Code of Conduct](./CODE_OF_CONDUCT.md) before participating.

To propose additions or changes:

1. Fork the repo and create your branch.
1. Make your changes with clear commits.
1. Open a pull request describing what you changed.
1. Tag your PR with `feature`, `enhancement`, `bug`, `fix`, `ci`, or `docs` so it appears in the release notes.

We welcome fixes to data, new repo suggestions, and other improvements.

## Quick Setup

After cloning the repository, run the environment setup script and install the package in editable mode:

```bash
source scripts/setup-env.sh
pip install -e .
pre-commit install
```

Run the test suite to ensure everything works:

```bash
PYTHONPATH="$PWD" pytest -q
```

Refer to [SCHEMA.md](./docs/SCHEMA.md) for details on metric fields used in `repos.json`.

Before opening a pull request, ensure the README table is up to date:

```bash
pre-commit run inject-readme --all-files
```


To run the scraping and ranking tools locally, install the CLI:

```bash
pip install agentic-index-cli
```

### Schema Migrations

Older `repos.json` files may use a previous schema version. Upgrade them in
place with the migration scripts:

```bash
python scripts/migrate_schema_v2.py path/to/repos.json
python scripts/migrate_schema_v3.py path/to/repos.json
```

## PR Checklist

Before requesting review, verify:

- [ ] Architectural changes are clearly explained.
- [ ] Security implications are considered.
- [ ] Tests cover new or updated code.
- [ ] Documentation is updated as needed.

### Pair Review for Sensitive Changes

Security-sensitive work and large refactors must be reviewed by a second
maintainer. Mention another maintainer when opening these PRs.

### Architecture

```
+---------+      +--------+      +----------+      +----------+
| Scraper | ---> | Cache  | ---> | Injector | ---> | Pull Req |
+---------+      +--------+      +----------+      +----------+
```
Additional dependency diagrams live in `docs/architecture`. Generate them with
`python scripts/gen_arch_diagrams.py` to explore how modules interact.

## Development environment

Set up Python 3.11 and install dependencies:

```bash
pip install -r requirements.txt
pip install -e .
pip install black isort  # formatting tools
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

### Nightly Metrics Refresh

Our scheduled workflow keeps metrics current by running these steps:

1. `scripts/scrape_repos.py` collects GitHub metadata.
2. `scripts/score_metrics.py` computes `stars_7d`, maintenance, docs, and ecosystem values.
3. `agentic_index_cli.ranker` sorts repos and updates `data/top100.md`.
4. `scripts/inject_readme.py` writes the table into `README.md`.
5. Changes are committed automatically via a pull request.

## Adding a New Metric

Touch files under `score/*.py`, update `scripts/inject_readme.py` and document your column in `README.md`. Include tests covering the metric and regenerate snapshots with the injector.
New metrics should maintain overall test coverage (see badges) and update any affected snapshots.

Type hints are gradually being added across the codebase. Run `mypy` before
submitting changes and keep overall type coverage above **70%** for CLI modules.

## Codex Queue

Automation tasks can be orchestrated through a simple queue file located at `.codex/queue.yml`.
To simulate execution locally run:

```bash
python scripts/codex_task_runner.py
```

Define modular tasks in the YAML file to integrate with Codex tooling.


## Deployment Workflow

The website hosted via GitHub Pages is deployed automatically from the
`deploy_site.yml` workflow. If you modify the deployment logic, ensure the
following:

1. Build assets into `web/dist` using `npm run build`.
2. The workflow copies all contents (including hidden files) with `rsync` before
   publishing to the `gh-pages` branch.
3. `git remote rm origin` is guarded so the step succeeds even when the remote
   is absent.
4. Pull request previews are posted with the `create-or-update-comment` action
   using `issue-number`.

After editing the workflow, run `pre-commit` and `pytest -q` to confirm the repo
passes formatting and tests before opening a pull request.

## Security Scanning

Dependency and container scans run automatically in CI:

* **pip-audit** – checks Python dependencies for CVEs.
* **Trivy** – scans the repository filesystem.
* **Snyk** – tests dependencies weekly and on pull requests.
* **FOSSA** – verifies license compliance.

To run the Python audit locally:

```bash
pip install pip-audit
pip-audit -r requirements.txt
```

Trivy can scan the repo locally with:

```bash
trivy fs .
```


### License Summary

Generate a report of third-party licenses to help verify compliance.
Install dependencies as described in
[docs/CI_SETUP.md](./docs/CI_SETUP.md) and run:

```bash
pip-licenses --format=json --output-file=reports/licenses.json
```

The resulting JSON file lists each package and license used by the project.





## Working on Launch Readiness Review Issues

A comprehensive project review was conducted in June 2025 to identify areas for improvement before launch. Findings from this review have been translated into actionable GitHub issues.

Contributors looking to help address these key items should refer to the main tracking issue:

*   **EPIC Issue:** `EPIC: Launch-readiness fixes (June 2025 review)` (Search for this issue in the repository's GitHub Issues tab).

This EPIC issue links to all individual tasks spawned from the review. Alternatively, you can view the full review document and linked issues in [REVIEW-2025-06.md](docs/REVIEW-2025-06.md).

## Blameless Retrospectives

When a bug reaches production, hold a short blameless retrospective to
identify contributing factors and improve the process. The focus is on
learning, not on assigning fault.
