# Repository Data Schema (v3)

Agentic-Index stores scraped repository data in `data/repos.json` using `schema_version: 3`.
Each entry includes raw GitHub fields plus derived metrics used for ranking.

## Key Fields

| Field | Description |
|-------|------------|
| `full_name` | owner/repo identifier |
| `stargazers_count` | GitHub stars |
| `forks_count` | GitHub forks |
| `open_issues_count` | number of open issues |
| `pushed_at` | last commit timestamp |
| `owner.login` | repository owner |
| `category` | manual project category |
| `stars` | alias of stargazers_count |
| `stars_delta` | star change since last run |
| `score_delta` | ranking score change |
| `recency_factor` | commit freshness metric |
| `issue_health` | open vs closed issue ratio |
| `doc_completeness` | README/docs coverage |
| `license_freedom` | license compatibility score |
| `ecosystem_integration` | ecosystem fit score |
| `stars_log2` | log2 transformed stars |

The complete JSON schema can be found in [`schemas/repo.schema.json`](schemas/repo.schema.json).

## Metric Pipeline

```
+---------+      +--------+      +----------+      +----------+
| Scraper | ---> | Cache  | ---> | Injector | ---> | Pull Req |
+---------+      +--------+      +----------+      +----------+
```

The scraper collects GitHub metadata. Quality metrics in `lib/quality_metrics.py` compute the derived fields. The CLI in `agentic_index_cli/agentic_index.py` then updates the README table. CI opens a pull request with refreshed data.

See [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on adding new metrics and running tests.
