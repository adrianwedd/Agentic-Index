"""Inject top100 table into ``README.md`` or check that it is up to date."""

from __future__ import annotations

import datetime
import difflib
import json
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
README_PATH = ROOT / "README.md"
DATA_PATH = ROOT / "data" / "top100.md"
REPOS_PATH = ROOT / "data" / "repos.json"
RANKED_PATH = ROOT / "data" / "ranked.json"
SNAPSHOT = ROOT / "data" / "last_snapshot.json"

OVERALL_COL = "Overall"
DEFAULT_SORT_FIELD = "overall"

DEFAULT_TOP_N = 100


def _markers(n: int) -> tuple[str, str]:
    """Return start and end markers for ``n``."""
    return f"<!-- TOP{n}:START -->", f"<!-- TOP{n}:END -->"


def _clamp_name(name: str, limit: int = 28) -> str:
    """Return ``name`` truncated and escaped for markdown."""
    safe = name.replace("|", "\\|").replace("`", "\\`")
    if len(safe) <= limit:
        return safe
    return safe[: limit - 3] + "..."


def _load_rows(sort_by: str = DEFAULT_SORT_FIELD, *, limit: int = 100) -> list[str]:
    """Return table rows computed from repo data using v2 fields.

    If ``data/ranked.json`` is present it is used in preference to
    ``repos.json``. Missing metric values render as ``-`` to make it clear
    they were unavailable.
    """
    try:
        if RANKED_PATH.exists():
            data = json.loads(RANKED_PATH.read_text())
            repos = data.get("repos", data)
        else:
            repos = json.loads(REPOS_PATH.read_text()).get("repos", [])
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Missing file: {exc.filename}") from exc
    except Exception as exc:
        raise ValueError(f"Failed to read {REPOS_PATH}: {exc}") from exc

    required = ["name", "AgenticIndexScore", "stars_7d", "score_delta"]
    parsed = []
    for idx, repo in enumerate(repos):
        for key in required:
            if key not in repo:
                ident = repo.get("full_name", repo.get("name"))
                raise KeyError(
                    f"Missing required field '{key}' in repo at index {idx} (full_name={ident})"
                )
        name = repo.get("name", "")
        repo_score = float(repo.get("AgenticIndexScore", 0))
        stars7 = int(repo.get("stars_7d", 0))
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
                "overall": repo_score,
                "stars_7d": stars7,
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
    for i, repo in enumerate(parsed[:limit], start=1):
        rows.append(
            "| {i} | {score:.2f} | {name} | {s30} | {maint} | {rel} | {docs} | {eco} | {lic} |".format(
                i=i,
                score=repo["overall"],
                name=_clamp_name(repo["name"]),
                s30=repo["stars_7d"],
                maint=repo["maintenance"],
                rel=repo["release"],
                docs=repo["docs"],
                eco=repo["ecosystem"],
                lic=repo["license"],
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


def build_readme(
    *,
    sort_by: str = DEFAULT_SORT_FIELD,
    limit: int | None = None,
    top_n: int = DEFAULT_TOP_N,
) -> str:
    """Return README text with the ranking table injected."""
    start_marker, end_marker = _markers(top_n)
    readme_text = README_PATH.read_text(encoding="utf-8")
    end_newline = readme_text.endswith("\n")
    try:
        start_idx = readme_text.index(start_marker)
        end_idx = readme_text.index(end_marker, start_idx)
    except ValueError as exc:
        missing = start_marker if start_marker not in readme_text else end_marker
        raise ValueError(f"Marker {missing} not found in README") from exc

    before = readme_text[: start_idx + len(start_marker)].rstrip()
    after = "\n" + readme_text[end_idx + len(end_marker) :].lstrip()

    # always inject standard header for v2 schema
    header_lines = [
        f'| Rank | <abbr title="{OVERALL_COL}">📊</abbr> {OVERALL_COL} | Repo | <abbr title="Stars gained in last 7 days">⭐ Δ7d</abbr> | <abbr title="Maintenance score">🔧 Maint</abbr> | <abbr title="Last release date">📅 Release</abbr> | <abbr title="Documentation score">📚 Docs</abbr> | <abbr title="Ecosystem fit">🧠 Fit</abbr> | <abbr title="License">⚖️ License</abbr> |',
        "|-----:|------:|------|-------:|-------:|-----------|-------:|-------:|---------|",
    ]

    cfg_limit = top_n if limit is None else limit

    rows = _load_rows(sort_by, limit=cfg_limit)
    table = "\n".join(header_lines + rows)

    new_text = f"{before}\n{table}\n{end_marker}{after}"
    if os.getenv("PYTEST_CURRENT_TEST") is None:
        ts = datetime.datetime.utcnow().isoformat(timespec="seconds")
        new_text = new_text.replace("{timestamp}", ts)
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


def main(
    *,
    force: bool = False,
    check: bool = False,
    write: bool = True,
    sort_by: str = DEFAULT_SORT_FIELD,
    top_n: int = DEFAULT_TOP_N,
) -> int:
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
        Field to sort by. One of ``overall``, ``stars_7d``, ``maintenance``, or ``last_release``.
    top_n:
        Number of table rows and marker suffix.
    """
    try:
        new_text = build_readme(sort_by=sort_by, limit=top_n, top_n=top_n)
    except Exception as exc:
        print(f"{exc.__class__.__name__}: {exc}", file=sys.stderr)
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
