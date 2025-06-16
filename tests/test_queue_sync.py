import os
from pathlib import Path

import responses

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_queue_sync.py"
import importlib.util

spec = importlib.util.spec_from_file_location("queue_check", SCRIPT)
queue_check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(queue_check)


@responses.activate
def test_queue_sync_reports(tmp_path, capsys):
    qdir = tmp_path / ".codex"
    qdir.mkdir()
    qfile = qdir / "queue.yml"
    qfile.write_text("queue:\n  - T1\n  - T2\n")

    responses.add(
        responses.GET,
        "https://api.github.com/repos/o/r/issues",
        json=[
            {"body": "x\n\nTask: T1"},
            {"body": "y\n\nTask: T3"},
        ],
        status=200,
    )

    os.environ["GITHUB_TOKEN"] = "t"
    rc = queue_check.main(["--repo", "o/r", "--file", str(qfile)])
    captured = capsys.readouterr().out
    assert rc == 1
    assert "Add missing tasks: T3" in captured
    assert "Remove stale tasks: T2" in captured
