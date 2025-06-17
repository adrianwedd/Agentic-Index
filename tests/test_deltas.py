import json
import os
import subprocess
from pathlib import Path

from agentic_index_cli.internal import rank as rank_mod


def test_delta_calculation(tmp_path, monkeypatch):
    prev = {
        "schema_version": 1,
        "repos": [
            {
                "name": "repo1",
                "full_name": "o/repo1",
                "stars": 5,
                "forks_count": 1,
                "closed_issues": 2,
                "recency_factor": 1,
                "issue_health": 1,
                "doc_completeness": 0,
                "license_freedom": 1,
                "ecosystem_integration": 0,
                rank_mod.SCORE_KEY: 1.0,
            }
        ],
    }
    current = {
        "schema_version": 1,
        "repos": [
            {
                "name": "repo1",
                "full_name": "o/repo1",
                "stars": 8,
                "forks_count": 2,
                "closed_issues": 4,
                "recency_factor": 1,
                "issue_health": 1,
                "doc_completeness": 0,
                "license_freedom": 1,
                "ecosystem_integration": 0,
            },
            {
                "name": "repo2",
                "full_name": "o/repo2",
                "stars": 3,
                "forks_count": 0,
                "closed_issues": 0,
                "recency_factor": 1,
                "issue_health": 1,
                "doc_completeness": 0,
                "license_freedom": 1,
                "ecosystem_integration": 0,
            },
        ],
    }

    data_dir = tmp_path
    repo_file = data_dir / "repos.json"
    repo_file.write_text(json.dumps(current))
    hist = data_dir / "history"
    hist.mkdir()
    prev_path = hist / "prev.json"
    prev_path.write_text(json.dumps(prev))
    (data_dir / "last_snapshot.txt").write_text(str(prev_path))

    env = os.environ.copy()
    env["PYTEST_CURRENT_TEST"] = "y"
    subprocess.run(
        ["python", "-m", "agentic_index_cli.ranker", str(repo_file)],
        check=True,
        env=env,
    )

    data = json.loads(repo_file.read_text())
    rep1 = next(r for r in data["repos"] if r["name"] == "repo1")
    rep2 = next(r for r in data["repos"] if r["name"] == "repo2")

    assert rep1["stars_delta"] == 3
    assert rep2["stars_delta"] == "+new"
