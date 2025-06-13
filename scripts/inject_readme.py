#!/usr/bin/env python3
"""Inject top50 table into README.md."""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"
DATA_PATH = ROOT / "data" / "top50.md"

START = "<!-- TOP50:START -->"
END = "<!-- TOP50:END -->"


def main() -> int:
    readme_text = README_PATH.read_text(encoding="utf-8")
    end_newline = readme_text.endswith("\n")

    try:
        start_idx = readme_text.index(START)
        end_idx = readme_text.index(END, start_idx)
    except ValueError:
        print("Markers not found in README.md", file=sys.stderr)
        return 1

    before = readme_text[: start_idx + len(START)].rstrip()
    after = "\n" + readme_text[end_idx + len(END):].lstrip()

    lines = [l.strip() for l in DATA_PATH.read_text(encoding="utf-8").splitlines()]
    header = lines[:2]
    rows = lines[2:]
    def rank_key(line: str) -> int:
        parts = line.split("|")
        return int(parts[1].strip()) if len(parts) > 2 else 0

    rows = sorted(rows, key=rank_key)
    table = "\n".join(header + rows)

    new_text = f"{before}\n{table}\n{END}{after}"
    new_text = new_text.rstrip("\n")
    if end_newline:
        new_text += "\n"

    if new_text != readme_text:
        README_PATH.write_text(new_text, encoding="utf-8")

    return 0


if __name__ == "__main__":
    sys.exit(main())
