import os
from pathlib import Path

import agentic_index_cli.internal.inject_readme as inj
import agentic_index_cli.internal.readme_utils as rutils
import agentic_index_cli.internal.regression_check as rc

from .helpers import diff_unexpected_lines
from .test_inject_dry_run import _setup

ROOT = Path(__file__).resolve().parents[1]

ALLOW = rc.load_allowlist(ROOT / "regression_allowlist.yml")


def test_current_readme_matches_allowlist(
    tmp_path, monkeypatch, readme_fixture_path, data_fixture_dir
):
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    monkeypatch.setattr(
        rutils.os,
        "getenv",
        lambda k, d=None: None if k == "PYTEST_CURRENT_TEST" else os.getenv(k, d),
    )
    readme, modified = _setup(
        tmp_path, monkeypatch, readme_fixture_path, data_fixture_dir
    )
    diff = inj.diff(modified, readme)
    assert diff_unexpected_lines(diff, ALLOW) == []


def test_allowlist_filters_allowed_line(
    tmp_path, monkeypatch, readme_fixture_path, data_fixture_dir
):
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    monkeypatch.setattr(
        rutils.os,
        "getenv",
        lambda k, d=None: None if k == "PYTEST_CURRENT_TEST" else os.getenv(k, d),
    )
    readme, modified = _setup(
        tmp_path, monkeypatch, readme_fixture_path, data_fixture_dir
    )
    readme.write_text(readme.read_text() + "\nagentops\n")
    diff = inj.diff(modified, readme)
    assert diff_unexpected_lines(diff, ALLOW) == []


def test_unexpected_line_detected(
    tmp_path, monkeypatch, readme_fixture_path, data_fixture_dir
):
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    monkeypatch.setattr(
        rutils.os,
        "getenv",
        lambda k, d=None: None if k == "PYTEST_CURRENT_TEST" else os.getenv(k, d),
    )
    readme, modified = _setup(
        tmp_path, monkeypatch, readme_fixture_path, data_fixture_dir
    )
    readme.write_text(readme.read_text() + "\nBADLINE\n")
    diff = inj.diff(modified, readme)
    bad = diff_unexpected_lines(diff, ALLOW)
    assert bad and any("BADLINE" in b for b in bad)
