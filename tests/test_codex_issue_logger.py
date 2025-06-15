import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import agentic_index_cli.issue_logger as il
import scripts.codex_task_runner as ctr

SAMPLE = """
```codex-task
id: TEST-1
title: Sample
create_issue: true
repo: o/r
body: body text
labels: [auto, codex]
```
"""


def test_runner_creates_issue(monkeypatch, tmp_path):
    md = tmp_path / "tasks.md"
    md.write_text(SAMPLE)

    called = {}

    def fake_create(title, body, repo, labels=None, *, token=None):
        called["args"] = (title, body, repo, labels)
        return "url"

    monkeypatch.setattr(il, "create_issue", fake_create)
    ctr.main(["--file", str(md)])

    assert called["args"] == (
        "Sample",
        "body text\n\nTask ID: TEST-1",
        "o/r",
        ["auto", "codex"],
    )
