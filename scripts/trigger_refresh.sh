#!/usr/bin/env bash
set -euo pipefail

# Trigger the GitHub Action workflow that refreshes repo data.
# Requires a GitHub token with workflow scope.

MIN_STARS=${MIN_STARS:-50}
AUTO_MERGE=${AUTO_MERGE:-false}

echo "Dispatching update workflow..."

gh workflow run update.yml -f min-stars="$MIN_STARS" -f auto-merge="$AUTO_MERGE"
