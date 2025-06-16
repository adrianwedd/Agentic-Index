#!/usr/bin/env bash

# Trigger the update workflow for Agentic Index or a specific category
set -euo pipefail

CATEGORIES=(
  "Frameworks"
  "Multi-Agent Coordination"
  "RAG-centric"
  "DevTools"
  "Domain-Specific"
  "Experimental"
)

run_category() {
  local cat="$1"
  ./scripts/refresh_category.py "$cat"
}

case "${1:-}" in
  --all)
    for c in "${CATEGORIES[@]}"; do
      run_category "$c"
    done
    ;;
  "")
    if ! command -v gh >/dev/null 2>&1; then
      echo "Error: GitHub CLI 'gh' not found. Install from https://cli.github.com/." >&2
      exit 1
    fi

    if ! gh auth status >/dev/null 2>&1; then
      echo "Error: GitHub CLI is not authenticated. Run 'gh auth login' or set GH_TOKEN." >&2
      exit 1
    fi

    gh workflow run update.yml \
      -f ref=main \
      -f min-stars="50" \
      -f auto-merge="true"
    ;;
  *)
    run_category "$1"
    ;;
esac

