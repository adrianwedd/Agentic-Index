# Developer Contributing Notes

This section supplements the main [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Regenerating Fixtures

Tests rely on a snapshot of the README stored in `tests/fixtures/README_fixture.md`.
Whenever `scripts/inject_readme.py` changes or you update the ranking data,
regenerate the fixture so it stays in sync:

```bash
make regen-fixtures
```

The command rebuilds `README.md` and copies the result into the fixture file.
Pre-commit and CI will fail if the snapshot drifts.

## Editable Install

After cloning the repository, install the CLI in editable mode so the
`agentic-index` command is available on your path:

```bash
pip install -e .
```
