# Issue Logger CLI Test Report

This document describes manual testing of the `issue_logger.py` CLI tool.

## Environment
- dependencies installed via `scripts/agent-setup.sh`
- no valid `GITHUB_TOKEN` available

## Observed Behavior
- Creating or commenting without any token fails with `Missing GITHUB_TOKEN`.
- Providing an invalid token results in a `401 Bad credentials` error from the API.

```
$ python -m agentic_index_cli.issue_logger --new-issue --repo openai/engflow --title "Test" --body "Msg" --debug
POST https://api.github.com/repos/openai/engflow/issues
{"title": "Test", "body": "Msg"}
agentic_index_cli.exceptions.APIError: Missing GITHUB_TOKEN. Set GITHUB_TOKEN or GITHUB_TOKEN_ISSUES to enable issue logging.
```

```
$ export GITHUB_TOKEN=bad
$ python -m agentic_index_cli.issue_logger --comment --repo openai/engflow --issue-number 1 --body "hi" --debug
POST https://api.github.com/repos/openai/engflow/issues/1/comments
{"body": "hi"}
agentic_index_cli.exceptions.APIError: 401 {"message":"Bad credentials","documentation_url":"https://docs.github.com/rest","status":"401"}
```

## Suggestions
- Clarify in the help output that environment variable `GITHUB_TOKEN` is required.
- Consider supporting repository selection via environment variable to avoid long command lines.
- Provide a dry-run mode that prints the intended API calls without needing a token.
