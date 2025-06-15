import importlib.util
import json
import time
from pathlib import Path
from unittest import mock

# load script module
spec = importlib.util.spec_from_file_location(
    "scraper", Path("scripts/scrape_repos.py")
)
scraper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scraper)


def test_cache_hit(monkeypatch, tmp_path):
    cache_dir = tmp_path / ".cache"
    cache_dir.mkdir()
    data = {"full_name": "owner/repo"}
    cache_file = cache_dir / "repo_owner_repo.json"
    cache_file.write_text(json.dumps(data))
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(scraper, "CACHE_DIR", cache_dir)
    monkeypatch.setattr(
        scraper.requests,
        "get",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("no call")),
    )
    repo = scraper.fetch_repo("owner/repo")
    assert repo["full_name"] == "owner/repo"
    assert scraper.CACHE_HITS == 1


@mock.patch("time.sleep", lambda s: None)
def test_rate_limit_backoff(monkeypatch):
    resp1 = mock.Mock()
    resp1.status_code = 403
    resp1.headers = {
        "X-RateLimit-Remaining": "0",
        "X-RateLimit-Reset": str(int(time.time()) + 1),
    }
    resp1.raise_for_status = mock.Mock()
    resp2 = mock.Mock()
    resp2.status_code = 200
    resp2.headers = {"X-RateLimit-Limit": "60", "X-RateLimit-Remaining": "59"}
    resp2.json.return_value = {}
    resp2.raise_for_status = mock.Mock()
    calls = iter([resp1, resp2])
    monkeypatch.setattr(scraper.requests, "get", lambda *a, **k: next(calls))
    scraper._get("https://api.github.com/repos/owner/repo")
    assert scraper.API_LIMIT == 60
    assert scraper.API_REMAINING == 59
