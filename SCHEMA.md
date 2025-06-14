# Repository Data Schema (v2)

Agentic-Index stores scraped repository data in `data/repos.json` using `schema_version: 2`.
Each entry includes raw GitHub fields plus derived metrics used for ranking.

## Key Fields

| Field | Description |
|-------|------------|
| `full_name` | owner/repo identifier |
| `stargazers_count` | GitHub stars |
| `forks_count` | GitHub forks |
| `open_issues_count` | number of open issues |
| `pushed_at` | last commit timestamp |
| `license` | license object or `null` |
| `owner.login` | repository owner |
| `AgenticIndexScore` | overall ranking score |
| `stars_7d` | star change over 7 days |
| `maintenance` | issue/PR hygiene score |
| `release_age` | days since latest release |
| `docs_quality` | README/examples heuristic |
| `ecosystem_fit` | keyword tag affinity |
| `license_score` | OSI compatibility score |

The complete JSON schema can be found in [`schemas/repo.schema.json`](schemas/repo.schema.json).

## Metric Pipeline

```
+---------+      +--------+      +----------+      +----------+
| Scraper | ---> | Cache  | ---> | Injector | ---> | Pull Req |
+---------+      +--------+      +----------+      +----------+
```

The scraper collects GitHub metadata. Scoring modules in `score/` compute the derived fields. `inject_readme.py` then updates the README table. CI opens a pull request with refreshed data.

See [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on adding new metrics and running tests.
