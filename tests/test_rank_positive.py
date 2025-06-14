import json
import os
import subprocess


def test_ranker_positive_score(tmp_path):
    repo = {
        "name": "repo",
        "stars": 50,
        "recency_factor": 1,
        "issue_health": 1,
        "doc_completeness": 0,
        "license_freedom": 1,
        "ecosystem_integration": 0,
    }
    path = tmp_path / "repos.json"
    path.write_text(json.dumps({"schema_version": 1, "repos": [repo]}))
    env = os.environ.copy()
    env["PYTEST_CURRENT_TEST"] = "y"
    subprocess.run(["python", "scripts/rank.py", str(path)], check=True, env=env)
    result = json.loads(path.read_text())["repos"][0]
    assert result["AgenticIndexScore"] > 0
