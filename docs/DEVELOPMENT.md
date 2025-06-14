# Development Guide

This page explains how to set up a working environment for Agentic Index contributors.

## Workflow

```mermaid
graph TD
    A[Fork repository] --> B(Clone locally)
    B --> C(Install dependencies)
    C --> D(`pre-commit install`)
    D --> E(Make changes)
    E --> F(`pre-commit run --files <files>`)
    F --> G(`pytest -q`)
    G --> H(Push and open PR)
```

## Common commands

```bash
# install runtime deps
pip install -r requirements.txt

# install the package in editable mode
pip install -e .

# set up hooks and run lint/tests automatically
pre-commit install

# run the full test suite
pytest -q
```

## Troubleshooting FAQ

**Q: Network errors when installing packages?**

Use the default PyPI mirror or the mirror in `docs/CI_SETUP.md` if your network blocks outbound HTTPS.

**Q: GitHub API rate limit when scraping?**

Export `GITHUB_TOKEN_REPO_STATS` with a personal token to increase limits or reduce the `--min-stars` argument when testing locally.

**Q: Paths not recognized on Windows?**

Run the tools in WSL or use forward slashes (e.g. `python scripts/inject_readme.py`).

### README injection must be idempotent

Running `python scripts/inject_readme.py` twice in a row should leave `README.md`
unchanged. CI checks this with `pytest -k test_inject_idempotent`. If the second
run rewrites the file, adjust the injector so only the table body between the
`<!-- TOP50:START -->` and `<!-- TOP50:END -->` markers is regenerated.

Whenever `data/top50.md` or `data/repos.json` change, regenerate the README and
commit the updated files so `tests/test_inject_dry_run.py` stays in sync. The
test tolerates minor score drift (±0.01) but still fails if the table structure
diverges.
