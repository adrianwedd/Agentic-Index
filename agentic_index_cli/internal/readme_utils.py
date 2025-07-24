from __future__ import annotations

import datetime
import difflib
import json
import os
import pathlib
import time
import traceback
import uuid

import structlog

from agentic_index_cli.templates import (
    FULL_ROW_TMPL,
    SUMMARY_ROW_TMPL,
)
from agentic_index_cli.templates import clamp_name as _clamp_name
from agentic_index_cli.templates import format_link as _format_link
from agentic_index_cli.templates import short_desc as _short_desc

ROOT = pathlib.Path(__file__).resolve().parents[2]
README_PATH = ROOT / "README.md"
DATA_PATH = ROOT / "data" / "top100.md"
REPOS_PATH = ROOT / "data" / "repos.json"
RANKED_PATH = ROOT / "data" / "ranked.json"
SNAPSHOT = ROOT / "data" / "last_snapshot.json"
BY_CAT_INDEX = ROOT.joinpath("data/by_category/index.json")

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

logger = structlog.get_logger(__name__).bind(file=__file__)


def _markers(n: int) -> tuple[str, str]:
    """Return start and end markers for ``n``."""
    return f"<!-- TOP{n}:START -->", f"<!-- TOP{n}:END -->"


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


def _load_rows(
    sort_by: str = DEFAULT_SORT_FIELD,
    *,
    limit: int = 100,
    category: str | None = None,
    return_repos: bool = False,
    link: bool = False,
    summary: bool = False,
    repos_path: pathlib.Path = REPOS_PATH,
    ranked_path: pathlib.Path = RANKED_PATH,
) -> list[str] | tuple[list[str], list[dict]]:
    """Return table rows computed from repo data using v3 fields."""
    try:
        if ranked_path.exists():
            data = json.loads(ranked_path.read_text())
            repos = data.get("repos", data)
        else:
            if not repos_path.exists():
                raise FileNotFoundError(str(repos_path))
            repos = json.loads(repos_path.read_text()).get("repos", [])
    except Exception as exc:
        logger.exception(
            "load-rows-error",
            func="_load_rows",
            request_id=str(uuid.uuid4()),
            error=str(exc),
        )
        raise

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
                "html_url": repo.get("html_url"),
                "description": repo.get("description"),
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
        name = repo["name"]
        if link:
            name = _format_link(name, repo.get("html_url"))
        else:
            name = _clamp_name(name)
        if summary:
            desc = _short_desc(repo.get("description"))
            row = SUMMARY_ROW_TMPL.render(
                i=i,
                name=name,
                desc=desc,
                score=f"{repo['score']:.2f}",
                stars=repo["stars"],
                delta=repo["stars_delta"],
            )
        else:
            row = FULL_ROW_TMPL.render(
                i=i,
                name=name,
                score=f"{repo['score']:.2f}",
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
        rows.append(row)
    if return_repos:
        return rows, filtered[:limit]
    return rows


def available_categories(
    repos_path: pathlib.Path = REPOS_PATH,
    ranked_path: pathlib.Path = RANKED_PATH,
) -> list[str]:
    """Return sorted list of categories present in ``REPOS_PATH``."""
    try:
        if ranked_path.exists():
            data = json.loads(ranked_path.read_text())
            repos = data.get("repos", data)
        else:
            repos = json.loads(repos_path.read_text()).get("repos", [])
    except Exception as exc:
        logger.exception(
            "category-load-error",
            func="available_categories",
            request_id=str(uuid.uuid4()),
            error=str(exc),
        )
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


def _build_category_list(index_path: pathlib.Path | None = None) -> str:
    """Return markdown bullet list for category navigation."""
    if index_path is None:
        index_path = BY_CAT_INDEX
    if not index_path.exists():
        raise FileNotFoundError(str(index_path))
    try:
        index = json.loads(index_path.read_text())
    except Exception:
        traceback.print_exc()
        raise
    lines: list[str] = []
    for cat in sorted(index):
        info = index[cat]
        if isinstance(info, str):
            fname = info
            topics: list[str] = []
        else:
            fname = info.get("file") or info.get("path") or f"{cat}.json"
            topics = info.get("topics", [])
        if not topics:
            try:
                data = json.loads((index_path.parent / fname).read_text())
                repos = data.get("repos", data)
                topics = _infer_topics(repos)
            except Exception:
                topics = []
        md_name = f"README_{pathlib.Path(fname).stem}.md"
        emoji = CATEGORY_ICONS.get(cat, "•")
        topic_line = ""
        if topics:
            topic_line = "  \n_Topics: `" + "`, `".join(topics[:3]) + "`_"
        lines.append(f"- {emoji} [{cat}]({md_name}){topic_line}")
    return "\n".join(lines)


def _inject_category_section(text: str, index_path: pathlib.Path = BY_CAT_INDEX) -> str:
    """Inject category navigation section if markers are present."""
    try:
        start = text.index(CATEGORY_START)
        end = text.index(CATEGORY_END, start)
    except ValueError:
        return text
    body = _build_category_list(index_path)
    before = text[: start + len(CATEGORY_START)].rstrip()
    after = "\n" + text[end + len(CATEGORY_END) :].lstrip()
    return f"{before}\n{body}\n{CATEGORY_END}{after}"


def build_readme(
    *,
    sort_by: str = DEFAULT_SORT_FIELD,
    limit: int | None = None,
    top_n: int = DEFAULT_TOP_N,
    readme_path: pathlib.Path = README_PATH,
    repos_path: pathlib.Path = REPOS_PATH,
    ranked_path: pathlib.Path = RANKED_PATH,
    index_path: pathlib.Path = BY_CAT_INDEX,
) -> str:
    """Return README text with the ranking table injected."""
    request_id = str(uuid.uuid4())
    log = logger.bind(func="build_readme", request_id=request_id)
    start_time = time.perf_counter()
    start_marker, end_marker = _markers(top_n)
    if not readme_path.exists():
        raise FileNotFoundError(str(readme_path))
    try:
        readme_text = readme_path.read_text(encoding="utf-8")
    except Exception as exc:
        log.exception("readme-load-error", error=str(exc))
        raise
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

    header_lines = [
        "| Rank | Repo | Description | Score | Stars | Δ Stars |",
        "|-----:|------|-------------|------:|------:|--------:|",
    ]

    cfg_limit = top_n if limit is None else limit

    rows = _load_rows(
        sort_by,
        limit=cfg_limit,
        link=True,
        summary=True,
        repos_path=repos_path,
        ranked_path=ranked_path,
    )
    table = "\n".join(header_lines + rows)

    new_text = f"{before}\n{table}\n{end_marker}{after}"
    # inject navigation using provided index
    new_text = _inject_category_section(new_text, index_path)
    if os.getenv("PYTEST_CURRENT_TEST") is None:
        ts = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
        new_text = new_text.replace("{timestamp}", ts)
    new_text = new_text.rstrip("\n")
    if end_newline:
        new_text += "\n"
    log.info(
        "build-readme-complete",
        duration=time.perf_counter() - start_time,
        rows=len(rows),
    )
    return new_text


def diff(new_text: str, readme_path: pathlib.Path | None = None) -> str:
    """Return a unified diff comparing ``new_text`` with ``readme_path``."""
    if readme_path is None:
        readme_path = README_PATH
    if not readme_path.exists():
        raise FileNotFoundError(str(readme_path))
    try:
        old_text = readme_path.read_text(encoding="utf-8")
    except Exception as exc:
        logger.exception(
            "diff-read-error",
            func="diff",
            request_id=str(uuid.uuid4()),
            error=str(exc),
        )
        raise
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


def build_category_table(
    category: str,
    *,
    sort_by: str = DEFAULT_SORT_FIELD,
    limit: int | None = None,
    repos_path: pathlib.Path = REPOS_PATH,
    ranked_path: pathlib.Path = RANKED_PATH,
) -> str:
    """Return a markdown table for ``category`` with optional topic metadata."""
    header_lines = [
        "| Rank | Repo | Score | Stars | Δ Stars | Δ Score | Recency | Issue Health | Doc Complete | License Freedom | Ecosystem | log₂(Stars) | Category |",
        "|-----:|------|------:|------:|--------:|--------:|-------:|------------:|-------------:|---------------:|---------:|------------:|----------|",
    ]
    cfg_limit = DEFAULT_TOP_N if limit is None else limit
    rows, repos = _load_rows(
        sort_by,
        limit=cfg_limit,
        category=category,
        return_repos=True,
        link=True,
        repos_path=repos_path,
        ranked_path=ranked_path,
    )
    topics = _infer_topics(repos)
    heading = f"## 🧠 Top Agentic-AI Repositories: {category}  \n"
    if topics:
        heading += "_GitHub Topics: " + ", ".join(f"`{t}`" for t in topics) + "_  \n"
    return heading + "\n".join(header_lines + rows) + "\n"
