# Rolling Back a Failed Pipeline

If a refresh step corrupts `data/repos.json` or other generated files, follow these steps to restore a known-good state.

## Reverting GitHub Data

1. Identify the last healthy commit in the repository history.
2. Revert the faulty commit or reset the branch:
   ```bash
   git checkout main
   git revert <bad-commit-sha>
   # or
   git reset --hard <good-commit-sha>
   git push --force-with-lease
   ```
   You can also use GitHub's "Revert" button on the merge commit if the change was merged via pull request.
3. Verify that `data/repos.json` and related artifacts match the previous version.

## Cleaning Local Caches

Stale files may live under `.cache/` and `data/`. Remove them before re-running the pipeline:

```bash
rm -rf .cache
rm -f data/*.json data/*.md
```

Re-run the pipeline from the first step to regenerate fresh data.
