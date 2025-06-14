#!/usr/bin/env python3
"""Scrape GitHub repository metadata for Agentic Index."""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
from pathlib import Path
from typing import Dict, Any, List

import requests

from agentic_index_cli.validate import save_repos

HEADERS = {"Accept": "application/vnd.github+json"}
TOKEN = os.getenv("GITHUB_TOKEN")
if TOKEN:
    HEADERS["Authorization"] = f"token {TOKEN}"

DEFAULT_REPOS = ["octocat/Hello-World"]
HIST_DIR = Path("data/hist")


def _get(url: str) -> requests.Response:
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp


def _compute_stars_30d(full_name: str, stars: int) -> int:
    HIST_DIR.mkdir(parents=True, exist_ok=True)
    today = _dt.date.today()
    back = today - _dt.timedelta(days=30)
    prev_file = HIST_DIR / f"{back.isoformat()}.json"
    prev_stars = 0
    if prev_file.exists():
        try:
            prev_data = json.loads(prev_file.read_text())
            prev_stars = int(prev_data.get(full_name, 0))
        except Exception:
            prev_stars = 0
    delta = stars - prev_stars

    today_file = HIST_DIR / f"{today.isoformat()}.json"
    cur = {}
    if today_file.exists():
        try:
            cur = json.loads(today_file.read_text())
        except Exception:
            cur = {}
    cur[full_name] = stars
    today_file.write_text(json.dumps(cur, indent=2) + "\n")
    return delta


def fetch_repo(full_name: str) -> Dict[str, Any]:
    repo_resp = _get(f"https://api.github.com/repos/{full_name}")
    repo = repo_resp.json()
    release_resp = requests.get(
        f"https://api.github.com/repos/{full_name}/releases/latest",
        headers=HEADERS,
    )
    last_release = None
    if release_resp.status_code == 200:
        try:
            last_release = release_resp.json().get("published_at")
        except Exception:
            last_release = None

    stars = repo.get("stargazers_count", 0)
    topics = repo.get("topics", [])

    data = {
        "name": repo.get("name"),
        "full_name": repo.get("full_name"),
        "html_url": repo.get("html_url"),
        "description": repo.get("description"),
        "stargazers_count": stars,
        "forks_count": repo.get("forks_count"),
        "open_issues_count": repo.get("open_issues_count"),
        "archived": repo.get("archived"),
        "license": repo.get("license", {}).get("spdx_id"),
        "language": repo.get("language"),
        "pushed_at": repo.get("pushed_at"),
        "owner": {"login": repo.get("owner", {}).get("login")},
        "stars_30d": _compute_stars_30d(full_name, stars),
        "maintenance": 1.0,
        "docs_score": 0.0,
        "ecosystem": 1.0 if topics else 0.0,
        "last_release": last_release,
    }
    return data


def scrape(repos: List[str]) -> List[Dict[str, Any]]:
    results = []
    for r in repos:
        try:
            results.append(fetch_repo(r))
        except Exception as e:
            print(f"Failed to fetch {r}: {e}")
    return results


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Scrape GitHub repos")
    parser.add_argument("--one-shot", action="store_true", help="fetch once")
    parser.add_argument("--repos", nargs="*", default=DEFAULT_REPOS)
    args = parser.parse_args(argv)

    repos = scrape(args.repos)
    Path("data").mkdir(exist_ok=True)
    save_repos(Path("data/repos.json"), repos)


if __name__ == "__main__":
    main()
