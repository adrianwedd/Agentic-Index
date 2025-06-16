import importlib.util
import json
import sys
from pathlib import Path
from unittest import mock

# ensure project root on path for script imports
sys.path.append(str(Path(__file__).resolve().parents[1]))

spec = importlib.util.spec_from_file_location(
    "scraper", Path("scripts/scrape_repos.py")
)
scraper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scraper)


def make_response(data, status=200):
    resp = mock.Mock()
    resp.status_code = status
    resp.json.return_value = data
    resp.headers = {}
    resp.raise_for_status = mock.Mock()
    return resp


def test_one_shot_fields(tmp_path, monkeypatch):
    repo = {
        "name": "repo",
        "full_name": "owner/repo",
        "html_url": "https://example.com",
        "description": "desc",
        "stargazers_count": 10,
        "forks_count": 1,
        "open_issues_count": 0,
        "archived": False,
        "license": {"spdx_id": "MIT"},
        "language": "Python",
        "pushed_at": "2025-06-01T00:00:00Z",
        "owner": {"login": "owner"},
    }
    topics = {"names": ["tool", "agent"]}
    release = {"published_at": "2025-05-01T00:00:00Z"}

    def fake_get(url, headers=None, timeout=None):
        if url.endswith("/repos/owner/repo"):
            return make_response(repo)
        if url.endswith("/repos/owner/repo/topics"):
            assert (
                headers
                and headers.get("Accept") == "application/vnd.github.mercy-preview+json"
            )
            return make_response(topics)
        if url.endswith("/repos/owner/repo/releases/latest"):
            return make_response(release)
        raise AssertionError(url)

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(scraper.requests, "get", fake_get)
    monkeypatch.setattr(scraper, "DEFAULT_REPOS", ["owner/repo"])
    scraper.main(["--one-shot"])

    data = json.loads((tmp_path / "data/repos.json").read_text())
    repo_data = data["repos"][0]
    for field in ["stars_7d", "maintenance", "docs_score", "ecosystem", "last_release"]:
        assert field in repo_data
    assert repo_data["topics"] == ["tool", "agent"]
