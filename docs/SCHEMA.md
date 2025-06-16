# Index Schema

This document defines the fields produced by the Agentic Index enrichment pipeline. The resulting JSON is used by ranking tools and the website.
For detailed metric descriptions and GitHub field mappings see [METRICS_SCHEMA.md](METRICS_SCHEMA.md).

## Field Reference

| Field Name | Type | Description | Source Module | Update Frequency |
|------------|------|-------------|---------------|------------------|
| `rank` | `int` | Position in score ranking | `agentic_index_cli/agentic_index.py` | Nightly |
| `repo` | `str` | GitHub `owner/name` | `scraper/github.py` | Static |
| `score` | `float` | Composite score (0–10) | `agentic_index_cli/agentic_index.py` | Nightly |
| `stars_7d` | `int` | Net new stars in last 7d | `scraper/github.py` | Nightly |
| `maintenance` | `float` | Issue/PR hygiene (0–10) | `lib/quality_metrics.py` | Weekly |
| `release_age` | `int` | Days since last release | `scraper/github.py` | Nightly |
| `docs_quality` | `float` | Heuristic docs quality | `lib/quality_metrics.py` | Monthly |
| `ecosystem_fit` | `float` | Relevance to prompt/tooling space | `lib/quality_metrics.py` | Monthly |
| `license_score` | `float` | Open-source license rating | `lib/quality_metrics.py` | Static |

## Schema Versions

### v1
- Initial format containing raw GitHub metadata plus the computed `score`.
- License field could be either an object or SPDX string.
- Downstream tools expected `repos.json` without the additional metrics.

### v2
- Added enrichment metrics: `stars_7d`, `maintenance`, `docs_quality`, `ecosystem_fit`, `release_age`, and `license_score`.
- License is now stored only as an SPDX string.
- `scripts/migrate_schema_v2.py` upgrades old files. Tests consuming `repos.json` must update fixtures to include the new fields.

Future versions will follow the same pattern. Any tooling consuming the index should check the `schema_version` field before parsing.
