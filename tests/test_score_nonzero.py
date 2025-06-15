import json
import os
import subprocess
from pathlib import Path

def test_score_nonzero(tmp_path):
    repo = {
        "name": "sample",
        "stargazers_count": 10,
        "open_issues_count": 1,
        "closed_issues": 2,
        "pushed_at": "2025-06-01T00:00:00Z",
        "license": {"spdx_id": "MIT"},
    }
    path = tmp_path / "repos.json"
    path.write_text(json.dumps({"schema_version": 1, "repos": [repo]}))
    env = os.environ.copy()
    env["PYTHONPATH"] = "."
    subprocess.run([
        "python",
        "scripts/rank.py",
        str(path),
    ], check=True, env=env)
    scored = json.loads(path.read_text())["repos"][0]
    assert scored["AgenticIndexScore"] > 0
