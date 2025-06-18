import json
import re
import shutil
import sys
from pathlib import Path

import pytest

# ensure project root is on the path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import agentic_index_cli.internal.inject_readme as inj

from .helpers import _parse_table, assert_readme_equivalent

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"
README_SNAP = FIXTURE_DIR / "README_fixture.md"

EXPECTED_HEADERS = [
    "Rank",
    "Repo",
    "Description",
    "Score",
    "Stars",
    "Δ Stars",
]


def _setup(tmp_path, monkeypatch, readme_fixture_path, data_fixture_dir):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    shutil.copy(data_fixture_dir / "top100.md", data_dir / "top100.md")
    data = json.loads((data_fixture_dir / "repos.json").read_text())
    (data_dir / "repos.json").write_text(json.dumps(data))
    try:
        shutil.copy(
            data_fixture_dir / "last_snapshot.json", data_dir / "last_snapshot.json"
        )
    except FileNotFoundError:
        (data_dir / "last_snapshot.json").write_text("{}")

    readme = tmp_path / "README.md"
    readme.write_text(readme_fixture_path.read_text())

    monkeypatch.setattr(inj, "README_PATH", readme)
    monkeypatch.setattr(inj, "DATA_PATH", data_dir / "top100.md")
    monkeypatch.setattr(inj, "REPOS_PATH", data_dir / "repos.json")
    monkeypatch.setattr(inj, "SNAPSHOT", data_dir / "last_snapshot.json")
    by_cat = data_dir / "by_category"
    by_cat.mkdir()
    (by_cat / "index.json").write_text("{}")
    monkeypatch.setattr(inj, "BY_CAT_INDEX", by_cat / "index.json")

    modified = inj.build_readme(top_n=50, limit=50).strip()
    return readme, modified


@pytest.mark.xfail(
    not README_SNAP.exists(), reason="README fixture missing", strict=True
)
def test_inject_readme_check(
    tmp_path, monkeypatch, readme_fixture_path, data_fixture_dir
):
    readme, modified = _setup(
        tmp_path, monkeypatch, readme_fixture_path, data_fixture_dir
    )
    headers, rows = _parse_table(modified)
    assert headers == EXPECTED_HEADERS
    assert all(len(r) == len(EXPECTED_HEADERS) for r in rows)
    assert_readme_equivalent(readme.read_text().strip(), modified, {"score": 0.005})
    assert inj.main(check=True, top_n=50) == 0


def _bump_score(text: str, delta: float) -> str:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("| 1 |"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            cells[3] = f"{float(cells[3]) + delta:.2f}"
            lines[i] = "| " + " | ".join(cells) + " |"
            break
    return "\n".join(lines)


def _change_cell(text: str, col: int, value: str) -> str:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("| 1 |"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            cells[col] = value
            lines[i] = "| " + " | ".join(cells) + " |"
            break
    return "\n".join(lines)


@pytest.mark.parametrize(
    "modifier,should_pass",
    [
        (lambda txt: _bump_score(txt, 0.015), True),
        (lambda txt: _bump_score(txt, 0.05), False),
        (lambda txt: _change_cell(txt, 5, "MIT"), False),
        (lambda txt: _change_cell(txt, 0, "2"), False),
    ],
)
@pytest.mark.xfail(
    not README_SNAP.exists(), reason="README fixture missing", strict=True
)
def test_readme_tolerances(
    tmp_path, monkeypatch, readme_fixture_path, data_fixture_dir, modifier, should_pass
):
    readme, modified = _setup(
        tmp_path, monkeypatch, readme_fixture_path, data_fixture_dir
    )
    modified = modifier(modified)
    headers, rows = _parse_table(modified)
    assert headers == EXPECTED_HEADERS
    assert all(len(r) == len(EXPECTED_HEADERS) for r in rows)
    if should_pass:
        assert_readme_equivalent(readme.read_text().strip(), modified, {"score": 0.005})
    else:
        with pytest.raises(AssertionError):
            assert_readme_equivalent(
                readme.read_text().strip(), modified, {"score": 0.005}
            )


@pytest.mark.xfail(
    not README_SNAP.exists(), reason="README fixture missing", strict=True
)
def test_env_tolerance(tmp_path, monkeypatch, readme_fixture_path, data_fixture_dir):
    readme, modified = _setup(
        tmp_path, monkeypatch, readme_fixture_path, data_fixture_dir
    )
    modified = _bump_score(modified, 0.004)
    monkeypatch.setenv("README_TOLERANCES", "Score=0.005")
    assert_readme_equivalent(readme.read_text().strip(), modified)
