# Methodology

This document outlines how Agentic Index discovers repositories and calculates their scores.

<a id="scoring-formula"></a>
## Scoring Formula

```
Score = 0.30*log2(stars + 1)
      + 0.25*recency_factor
      + 0.20*issue_health
      + 0.15*doc_completeness
      + 0.07*license_freedom
      + 0.03*ecosystem_integration
```

Each component captures a different signal: community adoption, recent activity, maintenance health, documentation quality, licensing freedom, and how well the project fits in the wider ecosystem. Weights are reviewed quarterly and may be adjusted as the landscape evolves.

Metric functions are discovered at runtime via a small plugin registry. See [plugin-metrics](plugin-metrics.md) for how to add custom metrics.

## Formula History

| Version | Formula | Notes |
|---------|---------|-------|
| v1      | `Score = 0.30*log2(stars+1) + 0.25*recency_factor + 0.20*issue_health + 0.15*doc_completeness + 0.07*license_freedom + 0.03*ecosystem_integration` | Initial release. |

## Data Sources & Scraping

Agentic Index pulls data straight from the GitHub REST API. Seeds come from keyword searches like `"agent framework"` or `"LLM agent"`, plus a handful of curated lists. The helper script [`scripts/scrape_repos.py`](../scripts/scrape_repos.py) fetches metadata for each candidate repository:

* repository fields (`stargazers_count`, `forks_count`, `open_issues_count`, `pushed_at`, `license`)
* topics and latest release information
* a rolling star history so weekly delta can be calculated

Each run stores a timestamped snapshot in `data/history/` and caches responses under `.cache/` to avoid hitting rate limits. Set a `GITHUB_TOKEN_REPO_STATS` token in `.env` to authenticate these calls.

## Metric Examples

The score is a weighted sum of normalized metrics. Here are small examples using the v1 weights.

* **Stars:** a project with 500 stars contributes `0.30 * log2(500 + 1) ≈ 2.69`.
* **Recency factor:** if the last commit was 90 days ago then `compute_recency_factor` gives `1 - (90 - 30)/335 ≈ 0.82`; multiplied by `0.25` this yields about `0.21`.
* **Issue health:** with 10 open and 40 closed issues the ratio is `1 - 10 / 50 = 0.8`; weighted this becomes `0.16`.
* **Doc completeness:** a long README with code blocks scores `1.0` so contributes `0.15`.
* **License freedom:** MIT or Apache licences give `1.0 → 0.07`; GPL licences count as `0.5 → 0.035`.
* **Ecosystem integration:** if keywords like `langchain` appear in topics or the README the repo gets `0.03`; otherwise `0.0`.

Summing these components yields the final score shown in the ranking tables.

## Categories & Ranking

After scoring, repositories are assigned a coarse category using keyword heuristics from `infer_category` in the ranking tool. Mentions of "rag" flag a project as **RAG-centric**; "multi-agent" or "crew" hint at **Multi-Agent Coordination**; words like "devtool" create the **DevTools** bucket; research-focused repos fall under **Experimental**. Anything else is classed as **General-purpose**.

Scores determine the overall ranking order. The index sorts all repositories by their computed score and then writes per-category lists, so high scoring projects surface at the top of both the global table and their category page.
