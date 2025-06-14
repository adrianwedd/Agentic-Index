"""Inject top50 table into ``README.md`` or check that it is up to date."""

from __future__ import annotations

import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
README_PATH = ROOT / "README.md"
DATA_PATH = ROOT / "data" / "top50.md"

START = "<!-- TOP50:START -->"
END = "<!-- TOP50:END -->"


def _load_rows() -> list[str]:
    """Return normalised rows from ``top50.md`` sorted deterministically."""
    lines = [
        l.strip() for l in DATA_PATH.read_text(encoding="utf-8").splitlines() if l.strip()
    ]
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
        stars_delta = _fmt_delta(cells[3], is_int=True)
        score_delta = _fmt_delta(cells[4])
        cat = cells[5]
        parsed.append((repo, score, stars_delta, score_delta, cat))

    parsed.sort(key=lambda r: (-r[1], r[0].lower()))

    return [
        f"| {i} | {repo} | {score:.2f} | {sd} | {qd} | {cat} |"
        for i, (repo, score, sd, qd, cat) in enumerate(parsed, start=1)
    ]


def _fmt_delta(val: str, *, is_int: bool = False) -> str:
    """Normalise delta strings to always include a ``+`` sign when non-negative."""
    if val.startswith("+") or val.startswith("-") or val.startswith("+new"):
        return val
    try:
        if is_int:
            num = int(val)
            return f"{num:+d}"
        num = float(val)
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
