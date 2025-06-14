# Security Practices

This project relies on GitHub Actions for automated checks. The
`GITHUB_TOKEN` used by workflows should be limited to the permissions
required for scanning and publishing results.

## Token Scope

For custom tokens, grant only `contents: read` and `security-events: write`.
Avoid broader scopes unless absolutely necessary.

## Rotation

Rotate tokens at least every 90 days or immediately if exposure is
suspected. Update the repository secrets with the new token and remove
the old one.
