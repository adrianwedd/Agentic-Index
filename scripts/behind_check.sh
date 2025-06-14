#!/usr/bin/env bash
# Check if current branch is behind main by more than 0 commits
set -euo pipefail

# Ensure repository is up-to-date
# Expect GITHUB_HEAD_REF environment variable to be set to current branch

git fetch origin "$GITHUB_HEAD_REF" "main"
behind=$(git rev-list --left-right --count origin/$GITHUB_HEAD_REF...origin/main | awk '{print $2}')
if [ "$behind" -gt 0 ]; then
  echo "Branch is behind main by $behind commits" >&2
  exit 1
fi
