#!/usr/bin/env bash

# Trigger the update workflow for Agentic Index or a specific category
set -euo pipefail

LOG_FILE=${LOG_FILE:-refresh.log}
exec > >(tee -a "$LOG_FILE") 2>&1

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
  local out="data/${cat}/repos.json"
  if [[ -f "$out" ]]; then
    echo "[skip] $cat"
    return
  fi
  echo "[run] $cat"
  if ./scripts/refresh_category.py "$cat"; then
    touch "data/${cat}/.done"
  fi
}

start_time=$(date +%s)
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

echo "Finished in $(( $(date +%s) - start_time ))s" >&2

