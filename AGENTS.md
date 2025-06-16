# AGENTS.md

## Code Style
- Format Python code with **Black** using default settings.
- Ensure imports are sorted with **isort**.

## Testing
- Run the full suite with:
  ```bash
  PYTHONPATH="$PWD" pytest -q
  ```
- Validate formatting using:
  ```bash
  black --check . && isort --check-only .
  ```

## Setup
- Use `scripts/agent-setup.sh` to install all dependencies and pre-commit hooks:
  ```bash
  bash scripts/agent-setup.sh
  ```

## PR Guidelines
- Separate large formatting-only commits from functional changes.
- Include a short summary of changes and test results in the PR description.
- Ensure CI passes before requesting review.

## Codex Queue Sync
- Keep `.codex/queue.yml` aligned with open Codex issues using
  `scripts/check_queue_sync.py`.
- The `queue-check` workflow runs on PRs that modify the queue file.

## GitHub Comment Integration
- `agentic_index_cli/internal/issue_logger.py` posts agent logs to issues.
- Set `GITHUB_TOKEN` so automation jobs can comment on tasks.

