"""Scoring utilities for repositories."""

from __future__ import annotations

import math
import time
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional

import structlog

from agentic_index_cli.constants import SCORE_KEY

logger = structlog.get_logger(__name__).bind(file=__file__)

PERMISSIVE_LICENSES = {
    "mit",
    "apache-2.0",
    "bsd-2-clause",
    "bsd-3-clause",
    "isc",
    "zlib",
    "mpl-2.0",
}
VIRAL_LICENSES = {"gpl-3.0", "gpl-2.0", "agpl-3.0", "agpl-2.0"}


def compute_recency_factor(pushed_at: str) -> float:
    """Return a freshness score based on ``pushed_at`` timestamp."""
    pushed_date = datetime.strptime(pushed_at, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc
    )
    days = (datetime.now(timezone.utc) - pushed_date).days
    if days <= 30:
        return 1.0
    if days >= 365:
        return 0.0
    return max(0.0, 1 - (days - 30) / 335)


def compute_issue_health(open_issues: int, closed_issues: int) -> float:
    """Return ratio of closed to total issues."""
    denom = open_issues + closed_issues + 1e-6
    return 1 - open_issues / denom


def readme_doc_completeness(readme: str) -> float:
    """Return 1.0 if README is long and contains code blocks."""
    words = len(readme.split())
    has_code = "```" in readme
    if words >= 300 and has_code:
        return 1.0
    return 0.0


def license_freedom(license_spdx: Optional[str]) -> float:
    """Score how permissive a license is."""
    if not license_spdx:
        return 0.0
    key = license_spdx.lower()
    if key in PERMISSIVE_LICENSES:
        return 1.0
    if key in VIRAL_LICENSES:
        return 0.5
    return 0.5


def ecosystem_integration(topics: List[str], readme: str) -> float:
    """Return 1.0 if popular ecosystem keywords are present."""
    text = " ".join(topics).lower() + " " + readme.lower()
    keywords = ["langchain", "plugin", "openai", "tool", "extension", "framework"]
    for k in keywords:
        if k in text:
            return 1.0
    return 0.0


def categorize(description: str, topics: List[str]) -> str:
    """Return a coarse category for a project."""
    text = (description or "").lower() + " " + " ".join(topics).lower()
    if "rag" in text or "retrieval" in text:
        return "RAG-centric"
    if "multi-agent" in text or "crew" in text or "team" in text:
        return "Multi-Agent"
    if "dev" in text or "tool" in text or "test" in text:
        return "DevTools"
    if any(domain in text for domain in ["video", "game", "finance", "security"]):
        return "Domain-Specific"
    if "experimental" in text or "research" in text:
        return "Experimental"
    return "General-purpose"


def compute_score(repo: Dict, readme: str) -> float:
    """Compute the Agentic Index score for ``repo``."""
    request_id = str(uuid.uuid4())
    log = logger.bind(func="compute_score", request_id=request_id)
    start = time.perf_counter()
    stars = repo.get("stargazers_count", 0)
    open_issues = repo.get("open_issues_count", 0)
    closed_issues = repo.get("closed_issues", 0)
    recency = compute_recency_factor(repo.get("pushed_at"))
    issue_health = compute_issue_health(open_issues, closed_issues)
    doc_comp = readme_doc_completeness(readme)
    lic = repo.get("license")
    if isinstance(lic, dict):
        lic = lic.get("spdx_id")
    license_free = license_freedom(lic)
    eco = ecosystem_integration(repo.get("topics", []), readme)
    score = (
        0.30 * math.log2(stars + 1)
        + 0.25 * recency
        + 0.20 * issue_health
        + 0.15 * doc_comp
        + 0.07 * license_free
        + 0.03 * eco
    )
    final = round(score * 100 / 8, 2)
    log.debug(
        "score-computed",
        repo=repo.get("full_name", repo.get("name")),
        score=final,
        duration=time.perf_counter() - start,
    )
    return final
