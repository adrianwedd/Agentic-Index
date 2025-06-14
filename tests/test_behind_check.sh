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

git checkout feature >/dev/null

export GITHUB_HEAD_REF=feature
output_file=$(mktemp)
export GITHUB_OUTPUT="$output_file"
"$root_dir/scripts/behind_check.sh"

grep -q 'behind=true' "$output_file"
