import importlib
import importlib.util
import json
import os
import subprocess
from pathlib import Path
from unittest import mock

import pytest

# load modules dynamically so tests work from repo root
scrape_spec = importlib.util.spec_from_file_location(
    "scraper", Path("scripts/scrape_repos.py")
)
scraper = importlib.util.module_from_spec(scrape_spec)
scrape_spec.loader.exec_module(scraper)

score_spec = importlib.util.spec_from_file_location(
    "scorer", Path("scripts/score_metrics.py")
)
scorer = importlib.util.module_from_spec(score_spec)
score_spec.loader.exec_module(scorer)

inject_spec = importlib.util.spec_from_file_location(
    "inject", Path("scripts/inject_readme.py")
)
inject = importlib.util.module_from_spec(inject_spec)
inject_spec.loader.exec_module(inject)


def _resp(data):
    resp = mock.Mock()
    resp.status_code = 200
    resp.json.return_value = data
    resp.headers = {}
    resp.raise_for_status = mock.Mock()
    return resp


@pytest.mark.parametrize("min_stars", [0])
def test_end_to_end(tmp_path, monkeypatch, min_stars):
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
        "topics": ["tool"],
    }
    release = {"published_at": "2025-05-01T00:00:00Z"}

    def fake_get(url, headers=None, timeout=None):
        if url.endswith("/repos/owner/repo"):
            return _resp(repo)
        if url.endswith("/repos/owner/repo/releases/latest"):
            return _resp(release)
        raise AssertionError(url)

    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("CI_OFFLINE", "1")
    monkeypatch.setattr(scraper.requests, "get", fake_get)
    monkeypatch.setattr(scraper, "DEFAULT_REPOS", ["owner/repo"])

    scraper.main(["--one-shot", f"--min-stars={min_stars}"])

    data_file = tmp_path / "data/repos.json"
    assert data_file.exists()
    assert (tmp_path / "data/history").exists()

    # enrich with derived metrics required for injection
    enrich_path = Path("agentic_index_cli/enricher.py")
    import importlib

    enricher = importlib.import_module("agentic_index_cli.enricher")
    enricher.enrich(data_file)

    scorer.main(str(data_file))

    env = os.environ.copy()
    env.pop("PYTEST_CURRENT_TEST", None)
    env["CI_OFFLINE"] = "1"
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
    subprocess.run(
        ["python", "-m", "agentic_index_cli.ranker", str(data_file)],
        check=True,
        env=env,
    )

    readme = tmp_path / "README.md"
    readme.write_text("start\n<!-- TOP50:START -->\n<!-- TOP50:END -->\nend\n")

    inj_mod = importlib.import_module("agentic_index_cli.internal.inject_readme")
    for name, val in {
        "README_PATH": readme,
        "DATA_PATH": tmp_path / "data" / "top100.md",
        "REPOS_PATH": data_file,
        "SNAPSHOT": tmp_path / "data" / "last_snapshot.json",
    }.items():
        setattr(inj_mod, name, val)

    inj_mod.main(force=True, top_n=50)

    text = readme.read_text()
    assert "| 1 |" in text
