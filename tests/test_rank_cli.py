import json
import os
import subprocess
from pathlib import Path



def test_rank_ordering_and_tiebreak(tmp_path, monkeypatch):
    base = {
        "recency_factor": 1,
        "issue_health": 1,
        "doc_completeness": 0,
        "license_freedom": 1,
        "ecosystem_integration": 0,
    }
    data = [
        dict(base, name="B", stars=100),
        dict(base, name="A", stars=100),
        dict(base, name="C", stars=200),
    ]
    repo_file = tmp_path / "repos.json"
    repo_file.write_text(json.dumps(data))

    env = os.environ.copy()
    env["PYTEST_CURRENT_TEST"] = "y"
    subprocess.run(["python", "scripts/rank.py", str(repo_file)], check=True, env=env)

    ranked = json.loads(repo_file.read_text())
    assert ranked[0]["name"] == "C"
    assert [r["name"] for r in ranked[1:]] == ["B", "A"]
