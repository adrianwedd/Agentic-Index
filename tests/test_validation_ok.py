import json
import subprocess


def test_validation_ok(tmp_path):
    repo = {
        "full_name": "owner/repo",
        "stargazers_count": 10,
        "forks_count": 1,
        "open_issues_count": 0,
        "pushed_at": "2025-01-01T00:00:00Z",
        "license": {"spdx_id": "MIT"},
        "owner": {"login": "owner"},
    }
    path = tmp_path / "repos.json"
    path.write_text(json.dumps({"schema_version": 1, "repos": [repo]}))
    result = subprocess.run(
        ["python", "-m", "agentic_index_cli.validate", str(path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0

