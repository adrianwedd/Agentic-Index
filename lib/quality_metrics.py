"""Quality metrics helpers for Agentic Index.

These functions convert raw repository data from the GitHub API into
normalized scores used by the ranking scripts. Scores are expressed on
A 0.0–1.0 scale.
"""

from __future__ import annotations

import math
from typing import Iterable

from agentic_index_cli.scoring import (
    compute_issue_health,
    compute_recency_factor,
    license_freedom,
)

from .metrics_registry import FunctionMetric, register


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    """Clamp ``value`` between ``low`` and ``high``."""
    return max(low, min(high, value))


def maintenance_score(days_since_commit: float, open_issue_ratio: float) -> float:
    """Return a maintenance health score.

    Parameters
    ----------
    days_since_commit:
        Days since the last commit.
    open_issue_ratio:
        Fraction of currently open issues relative to total issues.
        Values outside ``0-1`` are clamped.

    Returns
    -------
    float
        Normalized score between ``0.0`` (poor) and ``1.0`` (excellent).
    """
    recency = 1.0 - _clamp(days_since_commit, 0.0, 365.0) / 365.0
    issues = 1.0 - _clamp(open_issue_ratio)
    score = 0.5 * recency + 0.5 * issues
    return round(_clamp(score), 2)


def docs_score(has_docs_dir: bool, readme_len: int) -> float:
    """Return a documentation quality score.

    ``readme_len`` is interpreted as the number of words in the README.
    ``has_docs_dir`` indicates whether a dedicated ``docs/`` directory exists.
    """
    readme_component = _clamp(readme_len / 1000.0)
    docs_bonus = 0.25 if has_docs_dir else 0.0
    total = readme_component + docs_bonus
    return round(_clamp(total), 2)


def ecosystem_tag(
    topics: Iterable[str] | None,
    language: str | None,
    dependencies: Iterable[str] | None,
) -> str:
    """Infer an ecosystem tag from repo metadata."""
    topics = {t.lower() for t in topics or []}
    deps = {d.lower() for d in dependencies or []}
    lang = (language or "").lower()

    if "langchain" in topics or "langchain" in deps:
        return "langchain"
    if "python" in lang:
        return "python"
    if "rust" in lang:
        return "rust"
    return "other"


# ---------------------------------------------------------------------------
# Metric providers used by the ranking script
# ---------------------------------------------------------------------------


def _stars_metric(repo: dict) -> float:
    return math.log2(repo.get("stars", repo.get("stargazers_count", 0)) + 1)


def _recency_metric(repo: dict) -> float:
    recency = repo.get("recency_factor")
    if recency is None:
        pushed = repo.get("pushed_at", "1970-01-01T00:00:00Z")
        recency = compute_recency_factor(pushed)
    return recency


def _issues_metric(repo: dict) -> float:
    issue_health = repo.get("issue_health")
    if issue_health is None:
        issue_health = compute_issue_health(
            repo.get("open_issues_count", 0), repo.get("closed_issues", 0)
        )
    return issue_health


def _docs_metric(repo: dict) -> float:
    return repo.get("doc_completeness", 0.0)


def _license_metric(repo: dict) -> float:
    license_free = repo.get("license_freedom")
    if license_free is None:
        lic = repo.get("license")
        if isinstance(lic, dict):
            lic = lic.get("spdx_id")
        license_free = license_freedom(lic)
    return license_free


def _ecosystem_metric(repo: dict) -> float:
    return repo.get("ecosystem_integration", 0.0)


# register built-in metrics
register(FunctionMetric("stars", 0.30, _stars_metric))
register(FunctionMetric("recency", 0.25, _recency_metric))
register(FunctionMetric("issue_health", 0.20, _issues_metric))
register(FunctionMetric("docs", 0.15, _docs_metric))
register(FunctionMetric("license", 0.07, _license_metric))
register(FunctionMetric("ecosystem", 0.03, _ecosystem_metric))
