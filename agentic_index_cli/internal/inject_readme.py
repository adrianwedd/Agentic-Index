"""Inject top50 table into ``README.md`` or check that it is up to date."""

from __future__ import annotations

import pathlib
import sys
import json
import difflib


ROOT = pathlib.Path(__file__).resolve().parents[2]
README_PATH = ROOT / "README.md"
DATA_PATH = ROOT / "data" / "top50.md"
REPOS_PATH = ROOT / "data" / "repos.json"
SNAPSHOT = ROOT / "data" / "last_snapshot.json"

START = "<!-- TOP50:START -->"
END = "<!-- TOP50:END -->"


def _clamp_name(name: str, limit: int = 28) -> str:
    """Return ``name`` truncated and escaped for markdown."""
    safe = name.replace("|", "\\|").replace("`", "\\`")
    if len(safe) <= limit:
        return safe
    return safe[: limit - 3] + "..."


def _load_rows() -> list[str]:
    """Return table rows computed from ``repos.json`` using v2 fields."""
    repos = json.loads(REPOS_PATH.read_text()).get("repos", [])

    parsed = []
    for repo in repos:
        name = repo.get("name", "")
        score = float(repo.get("AgenticIndexScore", 0))
        stars30 = int(repo.get("stars_30d", 0))
        maint = float(repo.get("maintenance", 0))
        release = repo.get("last_release") or "-"
        if release and release != "-":
            release = release.split("T")[0]
        docs = float(repo.get("docs_score", 0))
        ecosys = float(repo.get("ecosystem", 0))
        lic = repo.get("license")
        if isinstance(lic, dict):
            lic = lic.get("spdx_id")
        lic = lic or "-"
        parsed.append((name, score, stars30, maint, release, docs, ecosys, lic))

    parsed.sort(key=lambda r: (-r[1], r[0].lower()))

    rows = []
    for i, (name, score, s30, maint, rel, docs, eco, lic) in enumerate(parsed[:50], start=1):
        rows.append(
            f"| {i} | {score:.2f} | {_clamp_name(name)} | {s30} | {maint:.2f} | {rel} | {docs:.2f} | {eco:.2f} | {lic} |"
        )
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


def build_readme() -> str:
    """Return README text with the top50 table injected."""
    readme_text = README_PATH.read_text(encoding="utf-8")
    end_newline = readme_text.endswith("\n")
    start_idx = readme_text.index(START)
    end_idx = readme_text.index(END, start_idx)

    before = readme_text[: start_idx + len(START)].rstrip()
    after = "\n" + readme_text[end_idx + len(END) :].lstrip()

    # always inject standard header for v2 schema
    header_lines = [
        "| Rank | <abbr title=\"Score\">📊</abbr> Score | Repo | <abbr title=\"Stars gained in last 30 days\">⭐ Δ30d</abbr> | <abbr title=\"Maintenance score\">🔧 Maint</abbr> | <abbr title=\"Last release date\">📅 Release</abbr> | <abbr title=\"Documentation score\">📚 Docs</abbr> | <abbr title=\"Ecosystem fit\">🧠 Fit</abbr> | <abbr title=\"License\">⚖️ License</abbr> |",
        "|-----:|------:|------|-------:|-------:|-----------|-------:|-------:|---------|",
    ]

    rows = _load_rows()
    table = "\n".join(header_lines + rows)

    new_text = f"{before}\n{table}\n{END}{after}"
    new_text = new_text.rstrip("\n")
    if end_newline:
        new_text += "\n"
    return new_text


def diff(new_text: str, readme_path: pathlib.Path | None = None) -> str:
    """Return a unified diff comparing ``new_text`` with ``readme_path``."""
    if readme_path is None:
        readme_path = README_PATH
    old_text = readme_path.read_text(encoding="utf-8")
    if not new_text.endswith("\n"):
        new_text += "\n"
    if not old_text.endswith("\n"):
        old_text += "\n"
    return "".join(
        difflib.unified_diff(
            old_text.splitlines(keepends=True),
            new_text.splitlines(keepends=True),
            fromfile=str(readme_path),
            tofile="generated",
        )
    )


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

    try:
        new_text = build_readme()
    except ValueError:
        print("Markers not found in README.md", file=sys.stderr)
        return 1

    if check:
        if diff(new_text):
            print("README.md is out of date", file=sys.stderr)
            return 1
        return 0

    if write and (force or diff(new_text)):
        README_PATH.write_text(new_text, encoding="utf-8")

    return 0
