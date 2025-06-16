# Metrics Schema (v3)

This document lists all fields produced by the Agentic Index enrichment pipeline (schema version 3). It includes GitHub API mappings, descriptions, data types, source modules and formatting details. Derived fields note the calculation logic.

## Field Reference

| Field Name | Type | Description | Source Module | Format / Notes |
|------------|------|-------------|---------------|----------------|
| `name` | string | Repository short name | `agentic_index_cli.agentic_index.harvest_repo` | GitHub `full_name` without owner |
| `full_name` | string | Repository `owner/name` identifier | GitHub API | from `full_name` field |
| `html_url` | string | Repository HTML URL | GitHub API | |
| `description` | string\|null | Repository description text | GitHub API | nullable |
| `stargazers_count` | integer | Raw star count from GitHub | GitHub API | |
| `forks_count` | integer | Number of forks | GitHub API | |
| `open_issues_count` | integer | Open issues on GitHub | GitHub API | |
| `archived` | boolean | Whether the repo is archived | GitHub API | |
| `license` | object\|null | License metadata | GitHub API | stored as `{"spdx_id": str}` or `null` |
| `language` | string\|null | Primary language | GitHub API | nullable |
| `pushed_at` | string | Timestamp of last push | GitHub API | ISO 8601 date-time |
| `owner.login` | string | Repository owner login | GitHub API | nested under `owner` |
| `stars` | integer | GitHub star count | `scraper.py` → `RepoModel` | alias of `stargazers_count` |
| `stars_delta` | integer\|"+new" | Star change since last run | `rank.py`, snapshot comparator | formatted with sign, e.g. `+12`, `-3`, `+new` when new repo |
| `score_delta` | number\|"+new" | Score change since last run | `rank.py` | formatted like `+0.5` |
| `recency_factor` | number | Normalized push recency (0–1) | `agentic_index_cli.agentic_index.compute_recency_factor` | higher = more recent |
| `issue_health` | number | Ratio of closed to total issues (0–1) | `agentic_index_cli.agentic_index.compute_issue_health` | 1 means all issues closed |
| `doc_completeness` | number | README completeness indicator | `agentic_index_cli.agentic_index.readme_doc_completeness` | 1 if README >300 words and has code blocks |
| `license_freedom` | number | License permissiveness score (0–1) | `agentic_index_cli.agentic_index.license_freedom` | MIT/Apache = 1.0, GPL = 0.5, none = 0.0 |
| `ecosystem_integration` | number | Presence of ecosystem keywords in README | `agentic_index_cli.agentic_index.ecosystem_integration` | 0–1 range |
| `stars_log2` | number | `log2(stars)` value | `rank.py` | computed for scoring |
| `category` | string | Repository category label | `rank.py` → `infer_category` | e.g. "Frameworks", "Tools" |

### GitHub Field Mapping

| GitHub API Field | Internal Name |
|-----------------|---------------|
| `full_name` | `full_name` |
| `stargazers_count` | `stars` |
| `forks_count` | `forks_count` |
| `open_issues_count` | `open_issues_count` |
| `pushed_at` | `pushed_at` (used to compute `recency_factor`) |
| `license.spdx_id` | `license.spdx_id` |
| `owner.login` | `owner.login` |

Derived fields such as `recency_factor`, `issue_health`, `doc_completeness`, `license_freedom`, `ecosystem_integration`, `stars_delta`, `score_delta`, and `stars_log2` are calculated during enrichment and ranking. See `agentic_index_cli/agentic_index.py` and `agentic_index_cli/internal/rank.py` for the algorithms.


