import json
import os
from pathlib import Path

import agentic_index_cli.internal.rank as rank_mod


def test_by_category_generation(tmp_path, monkeypatch):
    repos = [
        {
            "name": "a",
            "full_name": "o/a",
            "stargazers_count": 10,
            "forks_count": 0,
            "open_issues_count": 0,
            "pushed_at": "2025-01-01T00:00:00Z",
            "owner": {"login": "o"},
            "AgenticIndexScore": 1.0,
            "category": "Cat1",
            "topics": ["x"],
        },
        {
            "name": "b",
            "full_name": "o/b",
            "stargazers_count": 5,
            "forks_count": 0,
            "open_issues_count": 0,
            "pushed_at": "2025-01-02T00:00:00Z",
            "owner": {"login": "o"},
            "AgenticIndexScore": 2.0,
            "category": "Cat2",
            "topics": ["y"],
        },
    ]
    data = {"schema_version": 3, "repos": repos}
    data_path = tmp_path / "repos.json"
    data_path.write_text(json.dumps(data))

    monkeypatch.setattr(rank_mod, "infer_category", lambda repo: repo["category"])
    os.environ["PYTEST_CURRENT_TEST"] = "1"
    rank_mod.main(str(data_path))

    out_dir = tmp_path / "by_category"
    index = json.loads((out_dir / "index.json").read_text())
    assert set(index.keys()) == {"Cat1", "Cat2"}

    c1 = json.loads((out_dir / index["Cat1"]).read_text())
    assert c1["repos"][0]["topics"] == ["x"]
    assert c1["repos"][0]["category"] == "Cat1"
