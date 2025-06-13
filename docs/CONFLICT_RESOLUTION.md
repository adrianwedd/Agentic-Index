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
