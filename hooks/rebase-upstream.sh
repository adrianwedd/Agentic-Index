#!/bin/sh
if git status -uno | grep -q 'behind'; then
  echo "Warning: branch is behind upstream. Run: git fetch origin && git rebase origin/main" >&2
fi
