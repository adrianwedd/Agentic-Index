import json
import runpy
import sys
from pathlib import Path

import agentic_index_cli.enricher as enricher
import agentic_index_cli.internal.inject_readme as inj
import agentic_index_cli.internal.rank_main as rank
from agentic_index_cli import scoring as ai


def test_cli_all_categories(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
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
            "category": "Dummy1",
            "description": "Dummy1",
            "topics": ["foo"],
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
            "category": "Dummy2",
            "description": "Dummy2",
            "topics": ["bar"],
        },
    ]
    data = {"schema_version": 3, "repos": repos}
    data_path = data_dir / "repos.json"
    data_path.write_text(json.dumps(data))
    (data_dir / "top100.md").write_text("")
    (data_dir / "last_snapshot.json").write_text("[]")

    for name, val in {
        "ROOT": tmp_path,
        "REPOS_PATH": data_path,
        "DATA_PATH": data_dir / "top100.md",
        "SNAPSHOT": data_dir / "last_snapshot.json",
        "BY_CAT_INDEX": data_dir / "by_category" / "index.json",
    }.items():
        setattr(inj, name, val)

    monkeypatch.setattr(rank, "infer_category", lambda repo: repo["category"])
    monkeypatch.setattr(ai, "categorize", lambda desc, topics: desc)
    monkeypatch.setattr(enricher, "categorize", lambda desc, topics: desc)
    enricher.enrich(data_path)
    rank.main(str(data_path))

    script = Path(__file__).resolve().parents[1] / "scripts" / "inject_readme.py"
    sys.argv = [str(script), "--all-categories"]
    runpy.run_path(script, run_name="__main__")

    for cat in ["Dummy1", "Dummy2"]:
        path = tmp_path / f"README_{cat}.md"
        assert path.exists()
        text = path.read_text()
        assert f"Top Agentic-AI Repositories: {cat}" in text
