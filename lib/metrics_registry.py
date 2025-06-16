from __future__ import annotations

from dataclasses import dataclass
from importlib import metadata
from typing import Callable, Dict, Iterable, Protocol


class MetricProvider(Protocol):
    """Interface for scoring metric providers."""

    name: str
    weight: float

    def score(self, repo: dict) -> float: ...


@dataclass
class FunctionMetric:
    """Simple callable-based metric provider."""

    name: str
    weight: float
    func: Callable[[dict], float]

    def score(self, repo: dict) -> float:  # type: ignore[override]
        return self.func(repo)


_REGISTRY: Dict[str, MetricProvider] = {}
_LOADED = False


def register(metric: MetricProvider) -> None:
    """Register ``metric`` under its ``name``."""

    _REGISTRY[metric.name] = metric


def get_metrics() -> Iterable[MetricProvider]:
    """Return all registered metrics, loading plugins if needed."""

    _load_plugins()
    return list(_REGISTRY.values())


def _load_plugins() -> None:
    global _LOADED
    if _LOADED:
        return
    try:
        entry_points = metadata.entry_points().select(group="agentic_index.metrics")
    except Exception:
        entry_points = []
    for ep in entry_points:
        try:
            provider = ep.load()
            if isinstance(provider, MetricProvider) or hasattr(provider, "score"):
                register(provider)
        except Exception:
            continue
    _LOADED = True
