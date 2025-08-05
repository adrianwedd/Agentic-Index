import importlib.util
import os
from pathlib import Path

import responses
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "sync_queue_to_issues.py"
spec = importlib.util.spec_from_file_location("sync_mod", SCRIPT)
sync_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync_mod)


@responses.activate
def test_sync_creates_issue(tmp_path, monkeypatch):
    qfile = tmp_path / "queue.yml"
    qfile.write_text("queue:\n  - T1\n")
    os.environ["GITHUB_REPOSITORY"] = "o/r"
    os.environ["GITHUB_TOKEN"] = "t"
    # Mock the GET request to search for existing issues
    responses.add(
        responses.GET,
        'https://api.github.com/search/issues?q="T1" in:title repo:o/r',
        json={"items": []},  # Empty results to simulate no existing issues
        status=200,
    )
    # Mock the POST request to create a new issue
    responses.add(
        responses.POST,
        "https://api.github.com/repos/o/r/issues",
        json={"html_url": "https://github.com/o/r/issues/1"},
        status=201,
    )
    changed = sync_mod.sync_queue(qfile, "o/r")
    assert changed
    data = yaml.safe_load(qfile.read_text())
    assert data["queue"][0]["issue_id"] == 1
