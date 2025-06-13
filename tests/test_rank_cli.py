import json
import os
import subprocess
from pathlib import Path



def test_rank_ordering_and_tiebreak(tmp_path, monkeypatch):
    data = [
        {"name": "B", "stars": 100},
        {"name": "A", "stars": 100},
        {"name": "C", "stars": 200},
    ]
    repo_file = tmp_path / "repos.json"
    repo_file.write_text(json.dumps(data))

    env = os.environ.copy()
    env["PYTEST_CURRENT_TEST"] = "y"
    subprocess.run(["python", "scripts/rank.py", str(repo_file)], check=True, env=env)

    ranked = json.loads(repo_file.read_text())
    assert ranked[0]["name"] == "C"
    assert [r["name"] for r in ranked[1:]] == ["B", "A"]
