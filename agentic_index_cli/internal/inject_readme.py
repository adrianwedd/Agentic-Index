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
RANKED_PATH = ROOT / "data" / "ranked.json"
SNAPSHOT = ROOT / "data" / "last_snapshot.json"

OVERALL_COL = "Overall"

START = "<!-- TOP50:START -->"
END = "<!-- TOP50:END -->"


def _clamp_name(name: str, limit: int = 28) -> str:
    """Return ``name`` truncated and escaped for markdown."""
    safe = name.replace("|", "\\|").replace("`", "\\`")
    if len(safe) <= limit:
        return safe
    return safe[: limit - 3] + "..."


def _load_rows(sort_by: str = 'score') -> list[str]:
    """Return table rows computed from repo data using v2 fields.

    If ``data/ranked.json`` is present it is used in preference to
    ``repos.json``. Missing metric values render as ``-`` to make it clear
    they were unavailable.
    """
    if RANKED_PATH.exists():
        data = json.loads(RANKED_PATH.read_text())
        repos = data.get("repos", data)
    else:
        repos = json.loads(REPOS_PATH.read_text()).get("repos", [])

    parsed = []
    for repo in repos:
        name = repo.get("name", "")
        repo_score = float(repo.get("AgenticIndexScore", 0))
        stars30 = int(repo.get("stars_30d", 0))
        maint_raw = repo.get("maintenance")
        maint_val = float(maint_raw) if maint_raw is not None else 0.0
        maint_fmt = "-" if maint_raw is None else f"{maint_val:.2f}"
        release = repo.get("last_release") or "-"
        if release and release != "-":
            release = release.split("T")[0]
        release_key = 0.0
        if release and release != "-":
            try:
                release_key = float(release.replace("-", ""))
            except Exception:
                release_key = 0.0
        docs_raw = repo.get("docs_score")
        docs_val = float(docs_raw) if docs_raw is not None else 0.0
        docs_fmt = "-" if docs_raw is None else f"{docs_val:.2f}"
        ecosys_raw = repo.get("ecosystem")
        ecosys_val = float(ecosys_raw) if ecosys_raw is not None else 0.0
        ecosys_fmt = "-" if ecosys_raw is None else f"{ecosys_val:.2f}"
        lic = repo.get("license")
        if isinstance(lic, dict):
            lic = lic.get("spdx_id")
        lic = lic or "-"
        parsed.append(
            {
                "name": name,
                "score": repo_score,
                "stars_30d": stars30,
                "maintenance": maint_fmt,
                "maintenance_sort": maint_val,
                "release": release,
                "release_key": release_key,
                "docs": docs_fmt,
                "docs_sort": docs_val,
                "ecosystem": ecosys_fmt,
                "ecosystem_sort": ecosys_val,
                "license": lic,
            }
        )
    if sort_by == "last_release":
        parsed.sort(key=lambda r: (-r["release_key"], r["name"].lower()))
    elif sort_by == "maintenance":
        parsed.sort(key=lambda r: (-r["maintenance_sort"], r["name"].lower()))
    else:
        parsed.sort(key=lambda r: (-r[sort_by], r["name"].lower()))

    rows = []
    for i, repo in enumerate(parsed[:50], start=1):
        rows.append(
            "| {i} | {score:.2f} | {name} | {s30} | {maint} | {rel} | {docs} | {eco} | {lic} |".format(
                i=i,
                score=repo['score'],
                name=_clamp_name(repo['name']),
                s30=repo['stars_30d'],
                maint=repo['maintenance'],
                rel=repo['release'],
                docs=repo['docs'],
                eco=repo['ecosystem'],
                lic=repo['license'],
            )
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


def build_readme(*, sort_by: str = 'score') -> str:
    """Return README text with the top50 table injected."""
    readme_text = README_PATH.read_text(encoding="utf-8")
    end_newline = readme_text.endswith("\n")
    start_idx = readme_text.index(START)
    end_idx = readme_text.index(END, start_idx)

    before = readme_text[: start_idx + len(START)].rstrip()
    after = "\n" + readme_text[end_idx + len(END) :].lstrip()

    # always inject standard header for v2 schema
    header_lines = [
        f"| Rank | <abbr title=\"{OVERALL_COL}\">📊</abbr> {OVERALL_COL} | Repo | <abbr title=\"Stars gained in last 30 days\">⭐ Δ30d</abbr> | <abbr title=\"Maintenance score\">🔧 Maint</abbr> | <abbr title=\"Last release date\">📅 Release</abbr> | <abbr title=\"Documentation score\">📚 Docs</abbr> | <abbr title=\"Ecosystem fit\">🧠 Fit</abbr> | <abbr title=\"License\">⚖️ License</abbr> |",
        "|-----:|------:|------|-------:|-------:|-----------|-------:|-------:|---------|",
    ]

    rows = _load_rows(sort_by)
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


def main(*, force: bool = False, check: bool = False, write: bool = True, sort_by: str = 'score') -> int:
    """Synchronise the README table.

    Parameters
    ----------
    force:
        Write the README even if no changes detected.
    check:
        If ``True``, do not write. Exit ``1`` if README would change.
    write:
        Whether to update ``README.md``. Defaults to ``True``.
    sort_by:
        Field to sort by. One of ``score``, ``stars_30d``, ``maintenance``, or ``last_release``.
    """
    try:
        new_text = build_readme(sort_by=sort_by)
    except ValueError:
        print("Markers not found in README.md", file=sys.stderr)
        return 1

    if check:
        if not SNAPSHOT.exists():
            print(f"Warning: missing snapshot {SNAPSHOT}", file=sys.stderr)
            return 0
        if diff(new_text):
            print("README.md is out of date", file=sys.stderr)
            return 1
        return 0

    if write and (force or diff(new_text)):
        README_PATH.write_text(new_text, encoding="utf-8")

    return 0
