import json
import os
from pathlib import Path

import agentic_index_cli.internal.rank_main as rank_mod


def test_rank_writes_ranked_json(tmp_path):
    repos = [
        {
            "name": "a",
            "full_name": "o/a",
            "stargazers_count": 10,
            "forks_count": 0,
            "open_issues_count": 0,
            "pushed_at": "2025-01-01T00:00:00Z",
            "owner": {"login": "o"},
            "license": {"spdx_id": "MIT"},
        }
    ]
    repo_file = tmp_path / "repos.json"
    repo_file.write_text(json.dumps({"schema_version": 1, "repos": repos}))
    os.environ["PYTEST_CURRENT_TEST"] = "1"
    rank_mod.main(str(repo_file))
    ranked_file = tmp_path / "ranked.json"
    assert ranked_file.exists()
    data = json.loads(ranked_file.read_text())
    assert isinstance(data.get("repos"), list)
    assert data["repos"][0]["name"] == "a"
