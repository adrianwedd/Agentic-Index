# Metric Plugin Interface

The scoring system uses a small plugin registry so new metrics can be dropped in without modifying core code.  Providers implement the `MetricProvider` protocol from `lib.metrics_registry` and register themselves either programmatically or via the `agentic_index.metrics` entry point.

```python
from lib.metrics_registry import MetricProvider

class SecurityMetric:
    name = "security"
    weight = 0.05

    def score(self, repo: dict) -> float:
        return repo.get("security_score", 0.0)
```

Install the plugin package with an entry point:

```python
# setup.cfg or setup.py
entry_points = {
    "agentic_index.metrics": [
        "security = mypkg.metrics:SecurityMetric",
    ]
}
```

When `agentic_index_cli.internal.rank.compute_score` runs, it loads all registered providers and combines their weighted scores.
