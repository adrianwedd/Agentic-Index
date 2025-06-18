import json
from pathlib import Path

import agentic_index_cli.internal.rank_main as rank_mod
from scripts import refresh_category


def test_refresh_generates_by_category(tmp_path, monkeypatch):
    def fake_sync(topics=None, org=None):
        return [
            {
                "name": "r",
                "full_name": "o/r",
                "stargazers_count": 1,
                "forks_count": 0,
                "open_issues_count": 0,
                "pushed_at": "2025-01-01T00:00:00Z",
                "owner": {"login": "o"},
                "license": {"spdx_id": "MIT"},
                "topics": ["t"],
            }
        ]

    monkeypatch.setattr(refresh_category, "sync", fake_sync)
    monkeypatch.setattr(rank_mod, "infer_category", lambda repo: "Experimental")

    out_dir = tmp_path / "data"
    refresh_category.refresh("Experimental", out_dir)

    by_cat = out_dir / "by_category"
    assert (by_cat / "Experimental.json").exists()
    index = json.loads((by_cat / "index.json").read_text())
    assert index == {"Experimental": "Experimental.json"}
