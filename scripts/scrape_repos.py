#!/usr/bin/env python3
"""Scrape GitHub repository metadata for Agentic Index."""

from __future__ import annotations

import argparse
import datetime as _dt
import functools
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

sys.path.append(str(Path(__file__).resolve().parents[1]))

import requests

from agentic_index_cli.validate import save_repos

logger = logging.getLogger(__name__)

HEADERS = {"Accept": "application/vnd.github+json"}
TOKEN = os.getenv("GITHUB_TOKEN_REPO_STATS") or os.getenv("GITHUB_TOKEN")
if TOKEN:
    HEADERS["Authorization"] = f"token {TOKEN}"

CACHE_DIR = Path(".cache")
API_LIMIT = None
API_REMAINING = None
CACHE_HITS = 0
API_CALLS = 0

REQUEST_TIMEOUT = 10
MAX_RETRIES = 5

DEFAULT_REPOS = ["octocat/Hello-World"]
HIST_DIR = Path("data/hist")


def retry(func):
    """Retry ``func`` with exponential backoff."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        backoff = 1
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                return func(*args, **kwargs)
            except requests.RequestException as exc:
                if attempt == MAX_RETRIES:
                    logger.error("Request failed after %s attempts: %s", attempt, exc)
                    raise
                logger.warning(
                    "Request error: %s; retrying in %s seconds", exc, backoff
                )
                time.sleep(backoff)
                backoff *= 2

    return wrapper


@retry
def _get(url: str) -> requests.Response:
    """GET with retry, timeout and rate-limit handling."""
    global API_LIMIT, API_REMAINING, API_CALLS
    resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    API_CALLS += 1
    if "X-RateLimit-Limit" in resp.headers and API_LIMIT is None:
        API_LIMIT = int(resp.headers["X-RateLimit-Limit"])
    if "X-RateLimit-Remaining" in resp.headers:
        API_REMAINING = int(resp.headers["X-RateLimit-Remaining"])
    if resp.status_code == 403 and resp.headers.get("X-RateLimit-Remaining") == "0":
        reset = int(resp.headers.get("X-RateLimit-Reset", "0"))
        sleep_for = max(0, reset - int(time.time()))
        logger.warning("Rate limit exceeded, sleeping %s seconds", sleep_for)
        time.sleep(sleep_for)
        raise requests.HTTPError("rate limit", response=resp)
    if resp.status_code >= 500:
        raise requests.HTTPError(f"server error {resp.status_code}", response=resp)
    if resp.status_code >= 400 and resp.status_code != 404:
        resp.raise_for_status()
    return resp


DELTA_DAYS = 7


def _compute_stars_delta(full_name: str, stars: int) -> int:
    HIST_DIR.mkdir(parents=True, exist_ok=True)
    today = _dt.date.today()
    back = today - _dt.timedelta(days=DELTA_DAYS)
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
    cache_file = CACHE_DIR / f"repo_{full_name.replace('/', '_')}.json"
    if cache_file.exists() and time.time() - cache_file.stat().st_mtime < 86400:
        global CACHE_HITS
        CACHE_HITS += 1
        try:
            return json.loads(cache_file.read_text())
        except Exception:
            pass

    repo_resp = _get(f"https://api.github.com/repos/{full_name}")
    repo = repo_resp.json()
    release_resp = _get(f"https://api.github.com/repos/{full_name}/releases/latest")
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
        "license": (repo.get("license") or {}).get("spdx_id"),
        "language": repo.get("language"),
        "pushed_at": repo.get("pushed_at"),
        "owner": {"login": repo.get("owner", {}).get("login")},
        "stars_7d": _compute_stars_delta(full_name, stars),
        "maintenance": 1.0,
        "docs_score": 0.0,
        "ecosystem": 1.0 if topics else 0.0,
        "last_release": last_release,
    }
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(json.dumps(data, indent=2) + "\n")
    return data


def scrape(repos: List[str], min_stars: int = 0) -> List[Dict[str, Any]]:
    results = []
    for r in repos:
        try:
            repo = fetch_repo(r)
        except Exception as e:
            print(f"Failed to fetch {r}: {e}")
        else:
            if repo.get("stargazers_count", 0) >= min_stars:
                results.append(repo)
    return results


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Scrape GitHub repos")
    parser.add_argument("--one-shot", action="store_true", help="fetch once")
    parser.add_argument("--repos", nargs="*", default=DEFAULT_REPOS)
    parser.add_argument("--min-stars", type=int, default=0)
    parser.add_argument("--output", default="data/repos.json")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    repos = scrape(args.repos, args.min_stars)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    save_repos(out_path, repos)

    # write a timestamped snapshot alongside the primary output
    hist_dir = out_path.parent / "history"
    hist_dir.mkdir(parents=True, exist_ok=True)
    today = _dt.date.today().isoformat()
    snapshot_path = hist_dir / f"{today}.json"
    save_repos(snapshot_path, repos)
    (out_path.parent / "last_snapshot.txt").write_text(str(snapshot_path))
    logger.info("Saved snapshot to %s", snapshot_path)

    projected = len(args.repos) * 2
    used = None
    if API_LIMIT is not None and API_REMAINING is not None:
        used = API_LIMIT - API_REMAINING
    summary = (
        f"API {used}/{API_LIMIT if API_LIMIT is not None else '?'} used, "
        f"projected {projected}, cache hits {CACHE_HITS}"
    )
    logger.info(summary)
    step = os.getenv("GITHUB_STEP_SUMMARY")
    if step:
        with open(step, "a", encoding="utf-8") as fh:
            fh.write(summary + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover - CLI entry
        logger.error("Scrape failed: %s", exc)
        sys.exit(1)
