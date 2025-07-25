import json
from pathlib import Path

from agentic_index_api import sync_utils


def test_sync_filters_and_writes(tmp_path, monkeypatch):
    repos = [
        {"name": "a", "maintainer": "openai", "topics": "ai,agents"},
        {"name": "b", "maintainer": "openai", "topics": "ml"},
        {"name": "c", "maintainer": "other", "topics": "agents"},
    ]
    monkeypatch.setattr(sync_utils, "search_and_harvest", lambda min_stars=0, max_pages=1: repos)
    monkeypatch.setattr(sync_utils, "STATE_PATH", tmp_path / "sync.json")

    result = sync_utils.sync(org="openai", topics=["agents"])
    assert {r["name"] for r in result} == {"a"}
    assert (tmp_path / "sync.json").exists()
    saved = json.loads(Path(tmp_path / "sync.json").read_text())
    assert len(saved) == len(result)

