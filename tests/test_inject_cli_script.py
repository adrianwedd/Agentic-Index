import runpy
import sys
from pathlib import Path


def test_inject_script_check(monkeypatch, tmp_path):
    calls = {}

    def fake_main(
        force=False,
        check=False,
        write=True,
        dry_run=False,
        sort_by="score",
        top_n=100,
        limit=None,
        repos_path=None,
        ranked_path=None,
        readme_path=None,
        index_path=None,
    ):
        calls["args"] = (
            force,
            check,
            write,
            sort_by,
            top_n,
            limit,
            repos_path,
            ranked_path,
        )
        return 0

    monkeypatch.setattr("agentic_index_cli.internal.inject_readme.main", fake_main)
    script = Path(__file__).resolve().parents[1] / "scripts" / "inject_readme.py"
    sys.argv = [str(script), "--check"]
    runpy.run_path(script, run_name="__main__")
    assert calls["args"] == (
        False,
        True,
        False,
        "score",
        100,
        None,
        None,
        None,
    )


def test_inject_script_category(monkeypatch):
    calls = {}

    def fake_cat(category, **kwargs):
        calls["cat"] = category
        calls.update(kwargs)
        return 0

    monkeypatch.setattr(
        "agentic_index_cli.internal.inject_readme.write_category_readme", fake_cat
    )
    script = Path(__file__).resolve().parents[1] / "scripts" / "inject_readme.py"
    sys.argv = [str(script), "--category", "Foo"]
    runpy.run_path(script, run_name="__main__")
    assert calls["cat"] == "Foo"


def test_inject_script_all_categories(monkeypatch):
    called = {}

    def fake_all(**kwargs):
        called.update(kwargs)
        return 0

    monkeypatch.setattr(
        "agentic_index_cli.internal.inject_readme.write_all_categories", fake_all
    )
    script = Path(__file__).resolve().parents[1] / "scripts" / "inject_readme.py"
    sys.argv = [str(script), "--all-categories"]
    runpy.run_path(script, run_name="__main__")
    assert called != {}


def test_inject_script_dry_run(monkeypatch):
    called = {}

    def fake_main(**kwargs):
        called.update(kwargs)
        return 0

    monkeypatch.setattr(
        "agentic_index_cli.internal.inject_readme.main",
        fake_main,
    )
    script = Path(__file__).resolve().parents[1] / "scripts" / "inject_readme.py"
    sys.argv = [str(script), "--dry-run"]
    runpy.run_path(script, run_name="__main__")
    assert called["check"] is True
    assert called["write"] is False
