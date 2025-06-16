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
- Source `scripts/setup-env.sh` to validate your Python version, install system
  packages, and configure a virtual environment:
  ```bash
  source scripts/setup-env.sh
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

## PR–Issue Synchronization
Pull requests automatically get a tracking issue via
`.github/workflows/pr-sync.yml`. The workflow triggers on PR creation,
ready-for-review, and merge events. It runs `agentic_index_cli/task_daemon.py
sync-pr` with the event payload. The daemon creates a tracking issue when one
is missing, posts worklog comments to both the PR and the issue, and closes the
issue when the PR merges. The job requires `GITHUB_TOKEN` with permissions to
read and write issues and pull requests. Look for a hidden `tracking-issue`
comment on the PR to find the linked issue number.


## Issue-First Workflow
The `queue-sync` job converts tasks in `.codex/queue.yml` into GitHub issues.
Each entry is updated with `issue_id: <number>` after creation.
Pull requests must reference the associated issue using `Closes #<issue_id>`.
The `pr-validate` workflow blocks merges if the PR body lacks this link.
During execution the agent posts worklogs to both the PR and the issue.
A final log is archived on the issue when it closes.

### Adding Tasks
Add your task IDs under `queue:` in `.codex/queue.yml`. On push, the
`queue-sync` workflow creates issues automatically.

### Required Token Scopes
Automation needs a token with `repo` and `issues` scopes so it can create and
comment on issues and pull requests.

## Codex Tasks
Automation tasks are defined in markdown files using fenced `codex-task`
blocks. Each task block follows this schema:

```codex-task
id: GH-DEMO-1
title: Demo task
priority: 1           # lower numbers processed first
timeout: 3600         # optional, seconds
retries: 2            # optional retry count
create_issue: true    # create a GitHub issue
repo: owner/repo      # required when `create_issue` is true
steps:
  - short bullet
acceptance_criteria:
  - expected result
labels: [auto, codex]
```

Run `python scripts/codex_task_runner.py --file codex_tasks.md` to validate and
process tasks. The runner checks for duplicate IDs, missing fields, and invalid
values before creating issues or printing summaries.
