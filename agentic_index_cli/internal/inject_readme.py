"""Inject top100 table into ``README.md`` or check that it is up to date."""

from __future__ import annotations

import datetime
import difflib
import json
import os
import pathlib
import sys
import traceback

ROOT = pathlib.Path(__file__).resolve().parents[2]
README_PATH = ROOT / "README.md"
DATA_PATH = ROOT / "data" / "top100.md"
REPOS_PATH = ROOT / "data" / "repos.json"
RANKED_PATH = ROOT / "data" / "ranked.json"
SNAPSHOT = ROOT / "data" / "last_snapshot.json"
BY_CAT_INDEX = ROOT / "data" / "by_category" / "index.json"

CATEGORY_START = "<!-- CATEGORY:START -->"
CATEGORY_END = "<!-- CATEGORY:END -->"

CATEGORY_ICONS = {
    "General-purpose": "🌐",
    "Multi-Agent Coordination": "🤖",
    "RAG-centric": "📚",
    "Domain-Specific": "🎯",
    "DevTools": "🛠️",
    "Experimental": "🧪",
}

DEFAULT_SORT_FIELD = "score"

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


def _load_rows(
    sort_by: str = DEFAULT_SORT_FIELD,
    *,
    limit: int = 100,
    category: str | None = None,
    return_repos: bool = False,
) -> list[str] | tuple[list[str], list[dict]]:
    """Return table rows computed from repo data using v3 fields.

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

    required = [
        "name",
        "full_name",
        "AgenticIndexScore",
        "stars",
        "stars_delta",
        "score_delta",
        "recency_factor",
        "issue_health",
        "doc_completeness",
        "license_freedom",
        "ecosystem_integration",
        "stars_log2",
        "category",
    ]
    parsed = []
    filtered = []
    for idx, repo in enumerate(repos):
        if category and repo.get("category") != category:
            continue
        for key in required:
            if key not in repo:
                ident = repo.get("full_name", repo.get("name"))
                raise KeyError(
                    f"Missing required field '{key}' in repo at index {idx} (full_name={ident})"
                )
        name = repo.get("name", "")
        repo_score = float(repo.get("AgenticIndexScore", 0))
        stars = int(repo.get("stars", 0))
        stars_delta_raw = repo.get("stars_delta", 0)
        score_delta_raw = repo.get("score_delta", 0)
        rec_raw = repo.get("recency_factor")
        rec_val = float(rec_raw) if rec_raw is not None else 0.0
        rec_fmt = "-" if rec_raw is None else f"{rec_val:.2f}"
        health_raw = repo.get("issue_health")
        health_val = float(health_raw) if health_raw is not None else 0.0
        health_fmt = "-" if health_raw is None else f"{health_val:.2f}"
        docs_raw = repo.get("doc_completeness")
        docs_val = float(docs_raw) if docs_raw is not None else 0.0
        docs_fmt = "-" if docs_raw is None else f"{docs_val:.2f}"
        lic_raw = repo.get("license_freedom")
        lic_val = float(lic_raw) if lic_raw is not None else 0.0
        lic_fmt = "-" if lic_raw is None else f"{lic_val:.2f}"
        eco_raw = repo.get("ecosystem_integration")
        eco_val = float(eco_raw) if eco_raw is not None else 0.0
        eco_fmt = "-" if eco_raw is None else f"{eco_val:.2f}"
        log_raw = repo.get("stars_log2")
        log_val = float(log_raw) if log_raw is not None else 0.0
        log_fmt = "-" if log_raw is None else f"{log_val:.2f}"
        cat = repo.get("category", "-")
        parsed.append(
            {
                "name": name,
                "score": repo_score,
                "score_sort": repo_score,
                "stars": stars,
                "stars_sort": stars,
                "stars_delta": _fmt_delta(stars_delta_raw, is_int=True),
                "stars_delta_sort": (
                    int(str(stars_delta_raw).lstrip("+"))
                    if str(stars_delta_raw).lstrip("+-").isdigit()
                    else 0
                ),
                "score_delta": _fmt_delta(score_delta_raw),
                "score_delta_sort": (
                    float(str(score_delta_raw).lstrip("+"))
                    if str(score_delta_raw)
                    .replace("+", "")
                    .replace("-", "")
                    .replace(".", "")
                    .isdigit()
                    else 0.0
                ),
                "recency": rec_fmt,
                "recency_sort": rec_val,
                "issue_health": health_fmt,
                "issue_health_sort": health_val,
                "doc_completeness": docs_fmt,
                "doc_completeness_sort": docs_val,
                "license_freedom": lic_fmt,
                "license_freedom_sort": lic_val,
                "ecosystem": eco_fmt,
                "ecosystem_sort": eco_val,
                "stars_log2": log_fmt,
                "stars_log2_sort": log_val,
                "category": cat,
            }
        )
        filtered.append(repo)
    parsed.sort(key=lambda r: (-r.get(f"{sort_by}_sort", 0), r["name"].lower()))
    filtered.sort(
        key=lambda r: (
            -float(r.get(sort_by if sort_by != "score" else "AgenticIndexScore", 0)),
            r.get("name", "").lower(),
        )
    )

    rows = []
    for i, repo in enumerate(parsed[:limit], start=1):
        rows.append(
            "| {i} | {name} | {score:.2f} | {stars} | {sdelta} | {scdelta} | {rec} | {health} | {docs} | {licfr} | {eco} | {log2} | {cat} |".format(
                i=i,
                name=_clamp_name(repo["name"]),
                score=repo["score"],
                stars=repo["stars"],
                sdelta=repo["stars_delta"],
                scdelta=repo["score_delta"],
                rec=repo["recency"],
                health=repo["issue_health"],
                docs=repo["doc_completeness"],
                licfr=repo["license_freedom"],
                eco=repo["ecosystem"],
                log2=repo["stars_log2"],
                cat=repo["category"],
            )
        )
    if return_repos:
        return rows, filtered[:limit]
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


def _build_category_list(index_path: pathlib.Path | None = None) -> str:
    """Return markdown bullet list for category navigation."""
    if index_path is None:
        index_path = BY_CAT_INDEX
    if not index_path.exists():
        return ""
    try:
        index = json.loads(index_path.read_text())
    except Exception:
        return ""
    lines: list[str] = []
    for cat in sorted(index):
        info = index[cat]
        if isinstance(info, str):
            fname = info
            topics: list[str] = []
        else:
            fname = info.get("file") or info.get("path") or f"{cat}.json"
            topics = info.get("topics", [])
        md_name = f"README_{pathlib.Path(fname).stem}.md"
        emoji = CATEGORY_ICONS.get(cat, "•")
        topic_line = ""
        if topics:
            topic_line = "  \n_Topics: `" + "`, `".join(topics[:3]) + "`_"
        lines.append(f"- {emoji} [{cat}]({md_name}){topic_line}")
    return "\n".join(lines)


def _inject_category_section(text: str) -> str:
    """Inject category navigation section if markers are present."""
    try:
        start = text.index(CATEGORY_START)
        end = text.index(CATEGORY_END, start)
    except ValueError:
        return text
    body = _build_category_list()
    before = text[: start + len(CATEGORY_START)].rstrip()
    after = "\n" + text[end + len(CATEGORY_END) :].lstrip()
    return f"{before}\n{body}\n{CATEGORY_END}{after}"


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
        raise ValueError(
            f"Marker '{missing}' for TOP{top_n} not found in README"
        ) from exc

    before = readme_text[: start_idx + len(start_marker)].rstrip()
    after = "\n" + readme_text[end_idx + len(end_marker) :].lstrip()

    # standard header for schema v3 metrics
    header_lines = [
        "| Rank | Repo | Score | Stars | Δ Stars | Δ Score | Recency | Issue Health | Doc Complete | License Freedom | Ecosystem | log₂(Stars) | Category |",
        "|-----:|------|------:|------:|--------:|--------:|-------:|-------------:|-------------:|---------------:|---------:|------------:|----------|",
    ]

    cfg_limit = top_n if limit is None else limit

    rows = _load_rows(sort_by, limit=cfg_limit)
    table = "\n".join(header_lines + rows)

    new_text = f"{before}\n{table}\n{end_marker}{after}"
    new_text = _inject_category_section(new_text)
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
    limit: int | None = None,
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
        Field to sort by.
    top_n:
        Marker suffix used to locate the table.
    limit:
        Maximum number of rows to render. Defaults to ``top_n``.
    """
    try:
        row_limit = top_n if limit is None else limit
        new_text = build_readme(sort_by=sort_by, limit=row_limit, top_n=top_n)
    except Exception:
        traceback.print_exc()
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


def available_categories() -> list[str]:
    """Return sorted list of categories present in ``REPOS_PATH``."""
    try:
        if RANKED_PATH.exists():
            data = json.loads(RANKED_PATH.read_text())
            repos = data.get("repos", data)
        else:
            repos = json.loads(REPOS_PATH.read_text()).get("repos", [])
    except Exception:
        return []
    return sorted({r.get("category", "-") for r in repos if r.get("category")})


def _infer_topics(repos: list[dict], limit: int = 5) -> list[str]:
    """Infer a small list of topics from ``repos``."""
    topics: list[str] = []
    for repo in repos[:limit]:
        for topic in repo.get("topics", []) or []:
            if topic not in topics:
                topics.append(topic)
            if len(topics) >= limit:
                break
        if len(topics) >= limit:
            break
    return topics


def build_category_table(
    category: str,
    *,
    sort_by: str = DEFAULT_SORT_FIELD,
    limit: int | None = None,
) -> str:
    """Return a markdown table for ``category`` with optional topic metadata."""
    header_lines = [
        "| Rank | Repo | Score | Stars | Δ Stars | Δ Score | Recency | Issue Health | Doc Complete | License Freedom | Ecosystem | log₂(Stars) | Category |",
        "|-----:|------|------:|------:|--------:|--------:|-------:|-------------:|-------------:|---------------:|---------:|------------:|----------|",
    ]
    cfg_limit = DEFAULT_TOP_N if limit is None else limit
    rows, repos = _load_rows(
        sort_by, limit=cfg_limit, category=category, return_repos=True
    )
    topics = _infer_topics(repos)
    heading = f"## 🧠 Top Agentic-AI Repositories: {category}  \n"
    if topics:
        heading += "_GitHub Topics: " + ", ".join(f"`{t}`" for t in topics) + "_  \n"
    return heading + "\n".join(header_lines + rows) + "\n"


def write_category_readme(
    category: str,
    *,
    force: bool = False,
    check: bool = False,
    write: bool = True,
    sort_by: str = DEFAULT_SORT_FIELD,
    top_n: int = DEFAULT_TOP_N,
    limit: int | None = None,
) -> int:
    """Write or check ``README_<category>.md``."""
    cfg_limit = top_n if limit is None else limit
    text = build_category_table(category, sort_by=sort_by, limit=cfg_limit)
    fname = f"README_{category.replace(' ', '_')}.md"
    path = ROOT / fname
    if check and path.exists() and diff(text, path):
        print(f"{fname} is out of date", file=sys.stderr)
        return 1
    if write and (force or not path.exists() or diff(text, path)):
        path.write_text(text, encoding="utf-8")
    return 0


def write_all_categories(**kwargs) -> int:
    """Write or check README files for all categories."""
    status = 0
    for cat in available_categories():
        ret = write_category_readme(cat, **kwargs)
        status = max(status, ret)
    return status
