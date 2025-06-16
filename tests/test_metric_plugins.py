from agentic_index_cli.internal.rank import compute_score
from lib.metrics_registry import get_metrics, register


class DummyMetric:
    name = "dummy"
    weight = 1.0

    def score(self, repo: dict) -> float:
        return repo.get("dummy", 0.0)


def test_register_plugin_metric(monkeypatch):
    # snapshot existing metrics
    import lib.metrics_registry as mr

    original = mr._REGISTRY.copy()
    mr._REGISTRY = original.copy()

    register(DummyMetric())
    repo = {"dummy": 2.0}
    assert compute_score(repo) >= 2.0

    # cleanup
    mr._REGISTRY = original
