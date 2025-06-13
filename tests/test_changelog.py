import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts import rank


def test_changelog_update(tmp_path):
    prev_top = (
        "| # | Repo | ★ | Last Commit | Score | Category | One-liner |\n"
        "|---|------|----|------------|-------|----------|-----------|\n"
        "| 1 | old/repo | 100 | 2024-01-01 | 90 | Cat | desc |\n"
    )
    top_path = tmp_path / "top50.md"
    top_path.write_text(prev_top)
    changelog = tmp_path / "CHANGELOG.md"
    repos = [
        {
            "full_name": "new/repo",
            "stars": 200,
            "last_commit": "2024-01-02",
            "AgentOpsScore": 99,
            "category": "Cat",
            "one_liner": "desc",
        }
    ]
    data_file = tmp_path / "repos.json"
    data_file.write_text(json.dumps(repos))

    rank.rank(data_file, top_path, changelog)

    log = changelog.read_text()
    assert "Added new/repo" in log
    assert "Removed old/repo" in log
