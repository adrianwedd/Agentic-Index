import agentic_index_cli.internal.scrape as scrape


def test_extract():
    item = {
        "name": "repo",
        "full_name": "owner/repo",
        "html_url": "url",
        "description": "d",
        "stargazers_count": 1,
        "forks_count": 2,
        "open_issues_count": 3,
        "archived": False,
        "license": {"spdx_id": "MIT"},
        "language": "Python",
        "pushed_at": "2025-01-01T00:00:00Z",
        "owner": {"login": "owner"},
    }
    data = scrape._extract(item)
    assert data["full_name"] == "owner/repo"
    assert data["license"]["spdx_id"] == "MIT"
