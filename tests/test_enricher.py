import json
import subprocess


def test_enrich_schema(tmp_path):
    sample = [{
        "name": "repo",
        "full_name": "owner/repo",
        "html_url": "https://example.com",
        "description": "",
        "stargazers_count": 10,
        "forks_count": 0,
        "open_issues_count": 0,
        "archived": False,
        "license": {"spdx_id": "MIT"},
        "language": "Python",
        "pushed_at": "2025-01-01T00:00:00Z",
        "owner": {"login": "owner"},
    }]
    path = tmp_path / "repos.json"
    path.write_text(json.dumps({"schema_version": 1, "repos": sample}))
    subprocess.run(["python", "-m", "agentic_index_cli.enricher", str(path)], check=True)
    data = json.loads(path.read_text())
    repo = data["repos"][0]
    for key in [
        "stars_log2",
        "recency_factor",
        "issue_health",
        "doc_completeness",
        "license_freedom",
        "ecosystem_integration",
        "stars",
    ]:
        assert key in repo
