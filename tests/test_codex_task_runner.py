import sys
from pathlib import Path

# ensure project root on path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import scripts.codex_task_runner as ctr

SAMPLE_MD = """
# Tasks

```codex-task
id: TASK-2
priority: 2
title: Second task
timeout: 100
retries: 1
steps:
  - step two
acceptance_criteria:
  - done
```

```codex-task
id: TASK-1
priority: 1
title: First task
timeout: 50
retries: 0
```
"""


def test_parse_and_sort(tmp_path, capsys):
    md = tmp_path / "codex_tasks.md"
    md.write_text(SAMPLE_MD)

    tasks = ctr.sort_tasks(ctr.parse_tasks(md))
    assert [t["id"] for t in tasks] == ["TASK-1", "TASK-2"]
    assert tasks[0]["timeout"] == 50
    assert tasks[1]["retries"] == 1

    ctr.main(["--file", str(md), "--summary-only"])
    out = capsys.readouterr().out
    assert "TASK-1" in out
    assert "First task" in out
    assert "TASK-2" in out

    ctr.main(["--file", str(md), "--summary-only", "--start-from", "TASK-2"])
    out = capsys.readouterr().out
    assert "TASK-1" not in out
    assert "TASK-2" in out
