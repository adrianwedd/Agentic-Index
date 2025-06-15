import csv
from pathlib import Path

import agentic_index_cli.agentic_index as ai


def test_run_index_creates_outputs(tmp_path, monkeypatch):
    data = [
        {
            "name": "repo",
            "stars": 10,
            "last_commit": "2025-06-01T00:00:00Z",
            ai.SCORE_KEY: 1.0,
            "category": "General",
            "description": "desc",
        }
    ]
    monkeypatch.setattr(ai, "search_and_harvest", lambda min_stars: data)
    ai.run_index(min_stars=0, iterations=1, output=tmp_path)

    assert (tmp_path / "top100.csv").exists()
    assert (tmp_path / "top100.md").exists()
    assert (tmp_path / "CHANGELOG.md").exists()

    with open(tmp_path / "top100.csv") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert rows and rows[0]["name"] == "repo"
