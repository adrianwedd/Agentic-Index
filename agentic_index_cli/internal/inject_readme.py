"""Inject top50 table into ``README.md`` or check that it is up to date."""

from __future__ import annotations

import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
README_PATH = ROOT / "README.md"
DATA_PATH = ROOT / "data" / "top50.md"

START = "<!-- TOP50:START -->"
END = "<!-- TOP50:END -->"


def _load_table() -> str:
    lines = [l.strip() for l in DATA_PATH.read_text(encoding="utf-8").splitlines() if l.strip()]
    header = lines[:2]
    body = lines[2:]

    parsed = []
    for row in body:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cells) < 6:
            continue
        repo = cells[1]
        try:
            score = float(cells[2])
        except ValueError:
            score = 0.0
        stars_delta = cells[3]
        score_delta = cells[4]
        cat = cells[5]
        parsed.append((repo, score, stars_delta, score_delta, cat))

    parsed.sort(key=lambda r: (-r[1], r[0].lower()))

    rows = [
        f"| {i} | {repo} | {score:.2f} | {sd} | {qd} | {cat} |"
        for i, (repo, score, sd, qd, cat) in enumerate(parsed, start=1)
    ]
    return "\n".join(header + rows)


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

    table = _load_table()

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
