#!/usr/bin/env bash
# Minimal test for scripts/behind_check.sh
set -euo pipefail

root_dir="$(cd "$(dirname "$0")/.." && pwd)"

repo=$(mktemp -d)
cd "$repo"

git init -b main >/dev/null

touch file
git add file
git commit -m "init" >/dev/null

# create feature branch and commit
git checkout -b feature >/dev/null
echo test > file
git commit -am "feature" >/dev/null

# commit on main to make feature behind
git checkout main >/dev/null
echo main > new
git add new
git commit -m "main" >/dev/null

git remote add origin .

export GITHUB_HEAD_REF=feature

if "$root_dir/scripts/behind_check.sh"; then
  echo "Expected failure when branch is behind" >&2
  exit 1
else
  exit 0
fi
