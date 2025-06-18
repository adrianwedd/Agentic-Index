import importlib.util
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "scorer", Path("scripts/score_metrics.py")
)
scorer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scorer)


def test_release_age():
    ts = (datetime.now(timezone.utc) - timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
    assert scorer._release_age(ts) >= 5
    assert scorer._release_age(None) is None
    assert scorer._release_age("bad") is None


def test_main_outputs_metrics(tmp_path):
    repo = {
        "name": "repo",
        "full_name": "owner/repo",
        "html_url": "https://example.com",
        "stargazers_count": 1,
        "forks_count": 0,
        "open_issues_count": 0,
        "archived": False,
        "license": {"spdx_id": "MIT"},
        "language": "Python",
        "pushed_at": "2025-01-01T00:00:00Z",
        "owner": {"login": "owner"},
        "stars": 1,
        "stars_delta": 0,
        "score_delta": 0.0,
        "recency_factor": 1.0,
        "issue_health": 1.0,
        "doc_completeness": 0.0,
        "license_freedom": 1.0,
        "ecosystem_integration": 0.0,
        "stars_log2": 1.0,
        "category": "Test",
    }
    path = tmp_path / "repos.json"
    path.write_text(json.dumps({"repos": [repo]}))
    scorer.main(str(path))
    data = json.loads(path.read_text())
    out = data["repos"][0]
    for key in [
        "maintenance",
        "docs_score",
        "ecosystem",
        "license_score",
        "release_age",
    ]:
        assert key in out


def test_main_invalid(tmp_path):
    path = tmp_path / "repos.json"
    path.write_text("[]")
    with pytest.raises(Exception):
        scorer.main(str(path))
