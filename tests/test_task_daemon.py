import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from agentic_index_cli import task_daemon as td

SAMPLE_MD = """
### GH-TASK-1 First task
Body text

### GH-TASK-2 Second task
More text
"""


def test_parse_tasks(tmp_path):
    p = tmp_path / "tasks.md"
    p.write_text(SAMPLE_MD)
    tasks = td.parse_tasks(p)
    assert [t["id"] for t in tasks] == ["GH-TASK-1", "GH-TASK-2"]
    assert tasks[0]["title"] == "First task"


def test_process_creates_issue(monkeypatch, tmp_path):
    p = tmp_path / "tasks.md"
    p.write_text(SAMPLE_MD)
    calls = []

    def fake_create(title, body, repo, labels=None):
        calls.append((title, body, repo, labels))
        return "url"

    monkeypatch.setattr(td.issue_logger, "create_issue", fake_create)
    monkeypatch.setattr(td, "STATE_PATH", tmp_path / "state.json")
    td.process_tasks(p, "o/r")
    assert len(calls) == 2
    assert calls[0][0] == "First task"
    assert "GH-TASK-1" in calls[0][1]


import json


def test_process_skips_existing(monkeypatch, tmp_path):
    p = tmp_path / "tasks.md"
    p.write_text(SAMPLE_MD)
    monkeypatch.setattr(td, "STATE_PATH", tmp_path / "state.json")
    tasks = td.parse_tasks(p)
    td.save_state({tasks[0]["id"]: {"hash": td.task_hash(tasks[0]), "url": "u"}})
    calls = []

    def fake_create(title, body, repo, labels=None):
        calls.append(title)
        return "url"

    monkeypatch.setattr(td.issue_logger, "create_issue", fake_create)
    td.process_tasks(p, "o/r")
    # only second task should trigger create_issue
    assert calls == ["Second task"]


def test_process_worklogs(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    wl_dir = tmp_path / "worklog"
    wl_dir.mkdir()
    data = {"task_id": "GH-TASK-1"}
    (wl_dir / "log.json").write_text(json.dumps(data))
    monkeypatch.setattr(td, "STATE_PATH", tmp_path / "state.json")
    td.save_state(
        {"GH-TASK-1": {"hash": "h", "url": "https://api.github.com/repos/o/r/issues/1"}}
    )
    called = {}

    def fake_post(url, d, **kw):
        called["url"] = url
        called["data"] = d

    monkeypatch.setattr(td.issue_logger, "post_worklog_comment", fake_post)
    td.process_worklogs()
    assert called["url"].endswith("/1")
    assert not (wl_dir / "log.json").exists()
    assert (wl_dir / "log.posted").exists()


def test_process_worklogs_start(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    wl_dir = tmp_path / "worklog"
    wl_dir.mkdir()
    data = {"task_id": "GH-TASK-1", "event": "start", "cr": "cr", "steps": ["s"]}
    (wl_dir / "log.json").write_text(json.dumps(data))
    monkeypatch.setattr(td, "STATE_PATH", tmp_path / "state.json")
    td.save_state(
        {"GH-TASK-1": {"hash": "h", "url": "https://api.github.com/repos/o/r/issues/1"}}
    )
    called = {}

    def fake_post(url, cr, steps=None):
        called["url"] = url
        called["cr"] = cr

    monkeypatch.setattr(td.internal_issue_logger, "post_agent_log", fake_post)
    td.process_worklogs()
    assert called["url"].endswith("/1")
    assert called["cr"] == "cr"
