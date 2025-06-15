import runpy
import sys
from pathlib import Path


def test_inject_script_check(monkeypatch, tmp_path):
    calls = {}

    def fake_main(force=False, check=False, write=True, sort_by="score"):
        calls["args"] = (force, check, write, sort_by)
        return 0

    monkeypatch.setattr("agentic_index_cli.internal.inject_readme.main", fake_main)
    script = Path(__file__).resolve().parents[1] / "scripts" / "inject_readme.py"
    sys.argv = [str(script), "--check"]
    runpy.run_path(script, run_name="__main__")
    assert calls["args"] == (False, True, False, "score")
