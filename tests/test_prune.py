import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

import agentic_index_cli.prune as prune


def setup_temp_repo(tmp_path):
    repos = [
        {
            "full_name": "old/repo",
            "pushed_at": (datetime.now(timezone.utc) - timedelta(days=400)).isoformat(),
        },
        {
            "full_name": "fresh/repo",
            "pushed_at": (datetime.now(timezone.utc) - timedelta(days=10)).isoformat(),
        },
    ]
    repo_file = tmp_path / "repos.json"
    with open(repo_file, "w") as f:
        json.dump({"schema_version": 1, "repos": repos}, f)
    changelog = tmp_path / "CHANGELOG.md"
    return repo_file, changelog


def test_prune_removes_inactive(tmp_path):
    repo_file, changelog = setup_temp_repo(tmp_path)
    removed = prune.prune(365, repos_path=repo_file, changelog_path=changelog)

    assert removed == ["old/repo"]

    with open(repo_file) as f:
        data = json.load(f)
    assert len(data["repos"]) == 1
    assert data["repos"][0]["full_name"] == "fresh/repo"

    log = changelog.read_text().strip()
    assert "Removed old/repo" in log
