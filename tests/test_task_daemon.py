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
