"""Inject top50 table into ``README.md`` or check that it is up to date."""

from __future__ import annotations

import pathlib
import sys
import json


ROOT = pathlib.Path(__file__).resolve().parents[2]
README_PATH = ROOT / "README.md"
DATA_PATH = ROOT / "data" / "top50.md"
REPOS_PATH = ROOT / "data" / "repos.json"
SNAPSHOT = ROOT / "data" / "last_snapshot.json"

START = "<!-- TOP50:START -->"
END = "<!-- TOP50:END -->"


def _load_rows() -> list[str]:
    """Return table rows computed from ``repos.json`` with stable deltas."""
    repos = json.loads(REPOS_PATH.read_text()).get("repos", [])

    if not SNAPSHOT.exists():
        SNAPSHOT.write_text(json.dumps(repos, indent=2))
    baseline = json.loads(SNAPSHOT.read_text())

    baseline_map = {r.get("full_name", r.get("name")): r for r in baseline}

    parsed = []
    for repo in repos:
        name = repo.get("name")
        score = float(repo.get("AgenticIndexScore", 0))
        stars = repo.get("stars", repo.get("stargazers_count", 0))
        old = baseline_map.get(repo.get("full_name"))
        if old:
            prev_stars = old.get("stars", old.get("stargazers_count", 0))
            prev_score = float(old.get("AgenticIndexScore", 0))
        else:
            prev_stars = stars
            prev_score = score
        stars_delta = stars - prev_stars
        score_delta = round(score - prev_score, 2)
        cat = repo.get("category", "")
        parsed.append((name, score, stars_delta, score_delta, cat))

    parsed.sort(key=lambda r: (-r[1], r[0].lower()))

    rows = []
    for i, (name, score, sd, qd, cat) in enumerate(parsed[:50], start=1):
        sd_str = "" if sd == 0 else _fmt_delta(str(sd), is_int=True)
        qd_str = "" if qd == 0 else _fmt_delta(str(qd))
        rows.append(f"| {i} | {name} | {score:.2f} | {sd_str} | {qd_str} | {cat} |")
    return rows


def _fmt_delta(val: str | int | float, *, is_int: bool = False) -> str:
    """Normalise delta strings to always include a ``+`` sign when non-negative."""
    if isinstance(val, (int, float)):
        if val == 0:
            return ""
        val = str(val)
    if val.startswith("+") or val.startswith("-") or val.startswith("+new"):
        return val
    try:
        if is_int:
            num = int(val)
            if num == 0:
                return ""
            return f"{num:+d}"
        num = float(val)
        if num == 0:
            return ""
        return f"{num:+.1f}".rstrip("0").rstrip(".")
    except ValueError:
        return val


def main(*, force: bool = False, check: bool = False, write: bool = True) -> int:
    """Synchronise the README table.

    Parameters
    ----------
    force:
        Write the README even if no changes detected.
    check:
        If ``True``, do not write. Exit ``1`` if README would change.
    write:
        Whether to update ``README.md``. Defaults to ``True``.
    """

    readme_text = README_PATH.read_text(encoding="utf-8")
    end_newline = readme_text.endswith("\n")
    try:
        start_idx = readme_text.index(START)
        end_idx = readme_text.index(END, start_idx)
    except ValueError:
        print("Markers not found in README.md", file=sys.stderr)
        return 1

    before = readme_text[: start_idx + len(START)].rstrip()
    after = "\n" + readme_text[end_idx + len(END) :].lstrip()

    block_lines = [
        l for l in readme_text[start_idx + len(START) : end_idx].splitlines() if l.strip()
    ]
    if len(block_lines) >= 2:
        header_lines = block_lines[:2]
    else:
        header_lines = [
            "| Rank | Repo | Score | ▲ StarsΔ | ▲ ScoreΔ | Category |",
            "|-----:|------|------:|-------:|--------:|----------|",
        ]

    rows = _load_rows()
    table = "\n".join(header_lines + rows)

    new_text = f"{before}\n{table}\n{END}{after}"
    new_text = new_text.rstrip("\n")
    if end_newline:
        new_text += "\n"

    if check:
        if new_text != readme_text:
            print("README.md is out of date", file=sys.stderr)
            return 1
        return 0

    if write and (force or new_text != readme_text):
        README_PATH.write_text(new_text, encoding="utf-8")

    return 0
