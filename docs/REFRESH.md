# Refresh Pipeline

This page explains how the automatic refresh of `repos.json` and the ranking table works.

1. **Cron job** – The `update.yml` workflow runs every night via cron. It installs dependencies, runs the scraper and ranker and commits updates.
2. **Manual dispatch** – You can trigger the same workflow from the GitHub UI or via `gh workflow run`. Optional inputs allow setting `min-stars` and enabling `auto-merge`.
3. **Auto-merge** – If `auto-merge` is true, the workflow uses an action to merge the refresh PR once checks succeed.
4. **Webhook** – After merging, a webhook notifies any downstream services that new data is available.

The workflow creates a refresh pull request only when any of
`data/top50.md`, `data/repos.json`, or `README.md` change during the run.
If nothing changes, the job ends without opening a PR.

See [`trigger_refresh.sh`](https://github.com/adrianwedd/Agentic-Index/blob/main/scripts/trigger_refresh.sh) for the command-line helper.
