"""Inject top50 table into README.md."""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
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
    before = readme_text[: start_idx + len(START)]
    after = readme_text[end_idx:]
    table = DATA_PATH.read_text(encoding="utf-8").rstrip("\n") + "\n"
    new_text = before + "\n" + table + END + after[len(END):]
    if end_newline and not new_text.endswith("\n"):
        new_text += "\n"
    elif not end_newline:
        new_text = new_text.rstrip("\n")
    if new_text != readme_text:
        README_PATH.write_text(new_text, encoding="utf-8")
    return 0
