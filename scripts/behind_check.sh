#!/usr/bin/env bash
set -euo pipefail

echo "🔍 Checking if the branch is behind 'main'..."

git fetch origin main
behind_count=$(git rev-list --count HEAD..origin/main)

if [ "$behind_count" -gt 0 ]; then
    echo "⚠️  Branch is behind 'main' by $behind_count commits."
    if [[ "${GITHUB_OUTPUT:-}" ]]; then
        echo "behind=true" >> "$GITHUB_OUTPUT"
        echo "behind_count=$behind_count" >> "$GITHUB_OUTPUT"
    fi
    echo "ℹ️  Continuing without failure."
else
    echo "✅ Branch is up to date with 'main'."
    if [[ "${GITHUB_OUTPUT:-}" ]]; then
        echo "behind=false" >> "$GITHUB_OUTPUT"
        echo "behind_count=0" >> "$GITHUB_OUTPUT"
    fi
fi
