import json
import subprocess


def test_validation_dup(tmp_path):
    repo_a = {
        "full_name": "owner/repo",
        "stargazers_count": 10,
        "forks_count": 1,
        "open_issues_count": 0,
        "pushed_at": "2025-01-01T00:00:00Z",
        "license": {"spdx_id": "MIT"},
        "owner": {"login": "owner"},
        "AgenticIndexScore": 1,
    }
    repo_b = dict(repo_a)
    repo_b["AgenticIndexScore"] = 2
    data = [repo_a, repo_b]
    path = tmp_path / "repos.json"
    path.write_text(json.dumps(data))
    result = subprocess.run(
        ["python", "-m", "agentic_index_cli.quality.validate", str(path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "duplicate entries" in result.stderr

