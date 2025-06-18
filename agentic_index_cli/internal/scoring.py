from __future__ import annotations

from lib.metrics_registry import get_metrics

SCORE_KEY = "AgenticIndexScore"


def compute_score(repo: dict) -> float:
    """Return the Agentic Index score using registered metrics."""
    score = 0.0
    for metric in get_metrics():
        try:
            val = metric.score(repo)
        except Exception:
            val = 0.0
        score += metric.weight * val
    return round(score, 2)


def infer_category(repo: dict) -> str:
    """Derive a high-level category from repo metadata."""
    blob = (
        " ".join(repo.get("topics", []))
        + " "
        + repo.get("description", "")
        + " "
        + repo.get("name", "")
    )
    text = blob.lower()
    if "rag" in text:
        return "RAG-centric"
    if "multi-agent" in text or "multi agent" in text or "crew" in text:
        return "Multi-Agent Coordination"
    if "devtool" in text or "runtime" in text or "tool" in text:
        return "DevTools"
    if "experiment" in text or "research" in text:
        return "Experimental"
    return "General-purpose"
