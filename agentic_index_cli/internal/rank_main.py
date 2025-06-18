from __future__ import annotations

import datetime
import json
import os
from pathlib import Path

from jinja2 import Template

import lib.quality_metrics  # ensure built-in metrics are registered
from agentic_index_cli.config import load_config
from agentic_index_cli.scoring import (
    compute_issue_health,
    compute_recency_factor,
    license_freedom,
)
from agentic_index_cli.validate import load_repos, save_repos

from .badges import generate_badges
from .inject_readme import _format_link, _short_desc
from .scoring import SCORE_KEY, compute_score
from .scoring import infer_category as _infer_category
from .snapshot import persist_history, write_by_category

infer_category = _infer_category

SUMMARY_ROW_TMPL = Template(
    "| {{ i }} | {{ name }} | {{ desc }} | {{ score }} | {{ stars }} | {{ delta }} |"
)


def main(json_path: str = "data/repos.json", *, config: dict | None = None) -> None:
    """Rank repositories and write results back to disk."""
    cfg = config or load_config()
    top_n = cfg.get("ranking", {}).get("top_n", 100)
    delta_days = cfg.get("ranking", {}).get("delta_days", 7)
    data_file = Path(json_path)
    is_test = os.getenv("PYTEST_CURRENT_TEST") is not None
    repos = load_repos(data_file)

    data_dir = data_file.parent
    history_dir = data_dir / "history"
    history_dir.mkdir(exist_ok=True)
    last_snapshot_file = data_dir / "last_snapshot.txt"
    prev_map: dict[str, dict] = {}
    if last_snapshot_file.exists():
        prev_path = Path(last_snapshot_file.read_text().strip())
        if not prev_path.is_absolute():
            prev_path = history_dir / prev_path.name
        if prev_path.exists():
            try:
                prev_repos = load_repos(prev_path)
                prev_map = {r.get("full_name", r.get("name")): r for r in prev_repos}
            except Exception:
                prev_map = {}

    for repo in repos:
        if "AgentOpsScore" in repo:
            repo[SCORE_KEY] = repo.pop("AgentOpsScore")

    for repo in repos:
        repo.setdefault("stars", repo.get("stargazers_count", 0))
        if "recency_factor" not in repo and repo.get("pushed_at"):
            repo["recency_factor"] = compute_recency_factor(repo["pushed_at"])
        if "issue_health" not in repo:
            repo["issue_health"] = compute_issue_health(
                repo.get("open_issues_count", 0), repo.get("closed_issues", 0)
            )
        repo.setdefault("doc_completeness", 0.0)
        if "license_freedom" not in repo:
            lic = repo.get("license")
            if isinstance(lic, dict):
                lic = lic.get("spdx_id")
            repo["license_freedom"] = license_freedom(lic)
        repo.setdefault("ecosystem_integration", 0.0)

    skip_repo_write = (
        is_test and data_file.resolve() == Path("data/repos.json").resolve()
    )
    skip_top_write = is_test

    for repo in repos:
        repo[SCORE_KEY] = compute_score(repo)
        repo["category"] = infer_category(repo)
        prev = prev_map.get(repo.get("full_name", repo.get("name")))
        if prev:
            repo["stars_delta"] = repo.get("stars", 0) - prev.get(
                "stars", prev.get("stargazers_count", 0)
            )
            repo["forks_delta"] = repo.get("forks_count", 0) - prev.get(
                "forks_count", 0
            )
            repo["issues_closed_delta"] = repo.get("closed_issues", 0) - prev.get(
                "closed_issues", 0
            )
            repo["score_delta"] = round(
                repo[SCORE_KEY] - float(prev.get(SCORE_KEY, 0)), 2
            )
        else:
            repo["stars_delta"] = "+new"
            repo["forks_delta"] = "+new"
            repo["issues_closed_delta"] = "+new"
            repo["score_delta"] = "+new"

    zero_scores = sum(1 for r in repos if r[SCORE_KEY] == 0)
    allowed_zero = max(1, int(len(repos) * 0.02))
    assert zero_scores <= allowed_zero, "too many repos scored 0.0"

    repos.sort(key=lambda r: r[SCORE_KEY], reverse=True)
    if not skip_repo_write:
        save_repos(data_file, repos)
        persist_history(data_file, repos, delta_days=delta_days)
        write_by_category(data_dir, repos)

    header = [
        "| Rank | Repo | Description | Score | Stars | Δ Stars |",
        "|-----:|------|-------------|------:|------:|--------:|",
    ]

    def fmt(val: str | int | float) -> str:
        if isinstance(val, str):
            return val
        sign = "+" if val >= 0 else ""
        return f"{sign}{val}"

    rows = [
        SUMMARY_ROW_TMPL.render(
            i=i,
            name=_format_link(repo["name"], repo.get("html_url")),
            desc=_short_desc(repo.get("description")),
            score=f"{repo[SCORE_KEY]:.2f}",
            stars=repo.get("stars", repo.get("stargazers_count", 0)),
            delta=fmt(repo["stars_delta"]),
        )
        for i, repo in enumerate(repos[:top_n], start=1)
    ]
    if not skip_top_write:
        Path("data").mkdir(exist_ok=True)
        Path("data/top100.md").write_text("\n".join(header + rows) + "\n")

    today_iso = datetime.date.today().isoformat()
    top_repo_name = repos[0]["name"] if repos else "unknown"
    generate_badges(top_repo_name, today_iso, len(repos))
