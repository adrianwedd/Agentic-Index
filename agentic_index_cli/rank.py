"""Public ranking helpers."""
from typing import Dict

from .agentic_index import compute_score as _compute_score

__all__ = ["compute_score"]


def compute_score(repo: Dict, readme: str) -> float:
    """Proxy to :func:`agentic_index_cli.agentic_index.compute_score`."""
    return _compute_score(repo, readme)
