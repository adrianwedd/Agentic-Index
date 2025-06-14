import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

import gh_api
from agentic_index_cli.validate import load_repos
from agentic_index_cli.internal.rank import SCORE_KEY


def test_score_endpoint(tmp_path, monkeypatch):
    state = tmp_path / "state"
    state.mkdir()
    sync_path = state / "sync_data.json"
    data = {
        "schema_version": 1,
        "repos": [
            {
                "name": "r1",
                "stargazers_count": 10,
                "open_issues_count": 1,
                "closed_issues": 2,
                "pushed_at": "2025-06-01T00:00:00Z",
                "license": {"spdx_id": "MIT"},
            },
            {
                "name": "r2",
                "stargazers_count": 5,
                "open_issues_count": 0,
                "closed_issues": 0,
                "pushed_at": "2025-05-20T00:00:00Z",
                "license": {"spdx_id": "MIT"},
            },
        ],
    }
    sync_path.write_text(json.dumps(data))
    monkeypatch.setenv("STATE_DIR", str(state))
    client = TestClient(gh_api.app)
    resp = client.post("/score")
    assert resp.status_code == 200
    scores = resp.json()["top_scores"]
    assert scores and all(s > 0 for s in scores)
    scored = load_repos(state / "scored_data.json")
    expected = [r[SCORE_KEY] for r in sorted(scored, key=lambda r: r[SCORE_KEY], reverse=True)[:5]]
    assert scores == expected
