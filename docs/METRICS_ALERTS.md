# Metrics Alerting

This repository includes a daily monitor that checks GitHub statistics for all tracked projects. If star counts drop or releases go stale, notifications can be sent to Slack or via email.

## Configuration

The checker reads `data/repos.json` by default. Adjust behaviour through environment variables:

| Variable | Purpose | Default |
|----------|---------|---------|
| `METRICS_FILE` | Path to the repo data JSON file | `data/repos.json` |
| `STAR_DROP_THRESHOLD` | Stars must not fall below this many from the recorded value | `1` |
| `RELEASE_AGE_THRESHOLD` | Allowed increase in days since last release | `30` |
| `SLACK_WEBHOOK_URL` | If set, alerts are POSTed to this Slack webhook | – |
| `SMTP_SERVER` | SMTP server for email alerts | – |
| `SMTP_PORT` | Port for SMTP server | `25` |
| `SMTP_USER`/`SMTP_PASS` | Credentials for SMTP authentication | – |
| `ALERT_EMAIL` | Destination email address | – |
| `FROM_EMAIL` | Sender address for email alerts | value of `ALERT_EMAIL` |

## Customisation

Set the thresholds or webhook variables as secrets in GitHub Actions or in your local environment. When the scheduled workflow runs, any metrics that fall outside the configured ranges trigger a Slack message or an email summarising the issues.
