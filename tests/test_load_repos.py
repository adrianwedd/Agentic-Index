import json
import time
from pathlib import Path

from agentic_index_cli.validate import load_repos


def test_load_repos_cache(tmp_path: Path) -> None:
    data = {"schema_version": 1, "repos": [{"name": "foo"}]}
    path = tmp_path / "repos.json"
    path.write_text(json.dumps(data))
    assert load_repos(path, use_cache=True) == [{"name": "foo"}]

    # Update file after a delay to ensure mtime changes
    time.sleep(1.1)
    data["repos"][0]["name"] = "bar"
    path.write_text(json.dumps(data))
    assert load_repos(path, use_cache=True) == [{"name": "bar"}]
