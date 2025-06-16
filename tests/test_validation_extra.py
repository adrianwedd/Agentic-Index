import json
import subprocess


def test_validation_extra(tmp_path):
    repo = {
        "full_name": "owner/repo",
        "stargazers_count": 5,
        "forks_count": 1,
        "open_issues_count": 0,
        "pushed_at": "2025-01-01T00:00:00Z",
        "license": {"spdx_id": "MIT"},
        "owner": {"login": "owner"},
        "stars_7d": 1,
        "maintenance": 0.5,
        "docs_quality": 0.5,
        "ecosystem_fit": 0.3,
        "release_age": 10,
        "license_score": 9.5,
    }
    path = tmp_path / "repos.json"
    path.write_text(json.dumps({"schema_version": 2, "repos": [repo]}))
    result = subprocess.run(
        ["python", "-m", "agentic_index_cli.validate", str(path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
