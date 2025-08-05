import math
from datetime import datetime, timedelta

from agentic_index_cli import scoring as ai
from lib.quality_metrics import _clamp


def test_clamp_bounds():
    assert _clamp(-1) == 0.0
    assert _clamp(2) == 1.0
    assert _clamp(0.5) == 0.5


def test_compute_recency_factor_boundaries(monkeypatch):
    from datetime import timezone

    fixed_now = datetime(2025, 1, 1, tzinfo=timezone.utc)

    class DummyDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            return fixed_now

    monkeypatch.setattr(ai, "datetime", DummyDatetime)

    recent = (fixed_now - timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
    mid = (fixed_now - timedelta(days=200)).strftime("%Y-%m-%dT%H:%M:%SZ")
    old = (fixed_now - timedelta(days=400)).strftime("%Y-%m-%dT%H:%M:%SZ")

    assert ai.compute_recency_factor(recent) == 1.0
    expected_mid = max(0.0, 1 - (200 - 30) / 335)
    assert math.isclose(ai.compute_recency_factor(mid), expected_mid)
    assert ai.compute_recency_factor(old) == 0.0


def test_compute_issue_health_zero_denominator():
    assert ai.compute_issue_health(0, 0) == 1.0
    almost = ai.compute_issue_health(1, 0)
    assert almost < 0.001


def test_license_freedom_variants():
    assert ai.license_freedom("MIT") == 1.0
    assert ai.license_freedom("GPL-3.0") == 0.5
    assert ai.license_freedom("Unknown") == 0.5
    assert ai.license_freedom(None) == 0.0


def test_ecosystem_integration_keywords():
    readme = "This tool integrates with LangChain"
    assert ai.ecosystem_integration(["misc"], readme) == 1.0
    assert ai.ecosystem_integration([], "nothing here") == 0.0


def test_compute_score_composition(monkeypatch):
    repo = {
        "stargazers_count": 10,
        "open_issues_count": 1,
        "closed_issues": 9,
        "pushed_at": "2025-01-01T00:00:00Z",
        "license": {"spdx_id": "MIT"},
        "topics": [],
    }

    monkeypatch.setattr(ai, "compute_recency_factor", lambda x: 0.5)
    monkeypatch.setattr(ai, "compute_issue_health", lambda a, b: 0.8)
    monkeypatch.setattr(ai, "readme_doc_completeness", lambda r: 0.6)
    monkeypatch.setattr(ai, "license_freedom", lambda l: 1.0)
    monkeypatch.setattr(ai, "ecosystem_integration", lambda t, r: 0.0)

    score = ai.compute_score(repo, "readme")
    expected = (
        0.30 * math.log2(10 + 1)
        + 0.25 * 0.5
        + 0.20 * 0.8
        + 0.15 * 0.6
        + 0.07 * 1.0
        + 0.03 * 0.0
    )
    expected = round(expected * 100 / 8, 2)
    assert math.isclose(score, expected)
