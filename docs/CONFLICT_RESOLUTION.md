# Resolving Merge Conflicts

Pull requests occasionally fall behind `main`. Use this workflow to bring your branch up to date without polluting the history.

```bash
git fetch origin
git checkout <feature-branch>
git rebase origin/main            # fix conflicts as they appear
git push --force-with-lease
```

Only use GitHub's web editor for quick documentation fixes when the conflict is trivial. For anything more involved, resolve locally with the steps above.

When committing your fixes, follow this message pattern:

```
fix: resolve merge conflicts with main
```

Avoid `git merge main`; rebasing keeps the history linear and reduces noise for reviewers and CI.

## Bot PR permissions

For `update.yml` to refresh the data automatically, GitHub Actions must be allowed to open pull requests. Enable this under **Settings ▸ Actions ▸ General ▸ Workflow permissions** by checking “Allow GitHub Actions to create pull requests.” If you plan to let the bot auto-merge its PRs, also check “Allow GitHub Actions to approve pull requests.” Ensure branch protection rules still require status checks to pass.

## Automated Rebase

1. Add the `needs-rebase` label to your pull request.
2. Comment `/rebase` on the PR.
3. The bot opens a draft PR named `<original>-rebased` for review.

