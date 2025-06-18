"""GitHub network access and caching utilities."""

from __future__ import annotations

import asyncio
import base64
import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import aiohttp
import structlog

from .internal import http_utils
from .scoring import SCORE_KEY, categorize, compute_score

logger = structlog.get_logger(__name__).bind(file=__file__)

GITHUB_API = "https://api.github.com"
HEADERS = {"Accept": "application/vnd.github+json"}
TOKEN = os.getenv("GITHUB_TOKEN")
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"

CACHE_DIR = Path(".cache")
CACHE_TTL = 86400  # seconds

SEARCH_TERMS = ["agent framework", "LLM agent"]
TOPIC_FILTERS = ["agent"]


def _load_cache(path: Path) -> Any | None:
    if path.exists() and time.time() - path.stat().st_mtime < CACHE_TTL:
        try:
            with path.open() as fh:
                return json.load(fh)
        except Exception:
            return None
    return None


def _save_cache(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def _get(
    url: str, *, params: dict | None = None, headers: dict | None = None
) -> http_utils.Response:
    """GET with retry and adaptive rate limit handling."""
    kwargs = {"headers": headers or HEADERS}
    if params is not None:
        kwargs["params"] = params
    return http_utils.sync_get(url, **kwargs)


def github_search(query: str, page: int = 1) -> List[Dict]:
    """Return GitHub search results for ``query``."""
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": 100,
        "page": page,
    }
    try:
        resp = _get(f"{GITHUB_API}/search/repositories", params=params)
    except Exception as exc:  # pragma: no cover - network error path
        logger.error("GitHub search error: %s", exc)
        return []
    if resp.status_code != 200:
        logger.error("GitHub search error %s: %s", resp.status_code, resp.text)
        return []
    return resp.json().get("items", [])


def fetch_repo(full_name: str) -> Optional[Dict]:
    """Return repository metadata for ``full_name``."""
    cache_file = CACHE_DIR / f"repo_{full_name.replace('/', '_')}.json"
    cached = _load_cache(cache_file)
    if cached:
        return cached
    try:
        resp = _get(f"{GITHUB_API}/repos/{full_name}")
    except Exception as exc:  # pragma: no cover - network error path
        logger.error("Repo fetch error %s: %s", full_name, exc)
        return None
    if resp.status_code != 200:
        logger.error("Repo fetch error %s %s", full_name, resp.status_code)
        return None
    data = resp.json()
    _save_cache(cache_file, data)
    return data


def fetch_readme(full_name: str) -> str:
    """Return decoded README text for ``full_name``."""
    cache_file = CACHE_DIR / f"readme_{full_name.replace('/', '_')}.txt"
    if cache_file.exists() and time.time() - cache_file.stat().st_mtime < CACHE_TTL:
        return cache_file.read_text()
    try:
        resp = _get(f"{GITHUB_API}/repos/{full_name}/readme")
    except Exception as exc:  # pragma: no cover - network error path
        logger.error("Readme fetch error %s: %s", full_name, exc)
        return ""
    if resp.status_code != 200:
        return ""
    data = resp.json()
    if "content" in data:
        text = base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(text)
        return text
    return ""


async def async_fetch_repo(
    full_name: str, session: aiohttp.ClientSession
) -> Optional[Dict]:
    cache_file = CACHE_DIR / f"repo_{full_name.replace('/', '_')}.json"
    cached = _load_cache(cache_file)
    if cached:
        return cached
    try:
        resp = await http_utils.async_get(
            f"{GITHUB_API}/repos/{full_name}", session=session
        )
    except Exception as exc:  # pragma: no cover - network error path
        logger.error("Repo fetch error %s: %s", full_name, exc)
        return None
    if resp.status_code != 200:
        logger.error("Repo fetch error %s %s", full_name, resp.status_code)
        return None
    data = resp.json()
    _save_cache(cache_file, data)
    return data


async def async_fetch_readme(full_name: str, session: aiohttp.ClientSession) -> str:
    cache_file = CACHE_DIR / f"readme_{full_name.replace('/', '_')}.txt"
    if cache_file.exists() and time.time() - cache_file.stat().st_mtime < CACHE_TTL:
        return cache_file.read_text()
    try:
        resp = await http_utils.async_get(
            f"{GITHUB_API}/repos/{full_name}/readme", session=session
        )
    except Exception as exc:  # pragma: no cover - network error path
        logger.error("Readme fetch error %s: %s", full_name, exc)
        return ""
    if resp.status_code != 200:
        return ""
    data = resp.json()
    if "content" in data:
        text = base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(text)
        return text
    return ""


async def async_harvest_repo(
    full_name: str, session: aiohttp.ClientSession
) -> Optional[Dict]:
    cache_file = CACHE_DIR / f"meta_{full_name.replace('/', '_')}.json"
    cached = _load_cache(cache_file)
    if cached:
        return cached
    repo = await async_fetch_repo(full_name, session)
    if not repo:
        return None
    readme = await async_fetch_readme(full_name, session)
    score = compute_score(repo, readme)
    category = categorize(repo.get("description", ""), repo.get("topics", []))
    first_paragraph = readme.split("\n\n")[0][:200]
    data = {
        "name": full_name,
        "description": repo.get("description", ""),
        "stars": repo.get("stargazers_count", 0),
        "forks": repo.get("forks_count", 0),
        "open_issues": repo.get("open_issues_count", 0),
        "closed_issues": repo.get("closed_issues", 0),
        "last_commit": repo.get("pushed_at", ""),
        "language": repo.get("language", ""),
        "license": (
            repo.get("license")
            if not isinstance(repo.get("license"), dict)
            else repo.get("license").get("spdx_id")
        ),
        "maintainer": repo.get("owner", {}).get("login"),
        "topics": ",".join(repo.get("topics", [])),
        "readme_excerpt": first_paragraph,
        SCORE_KEY: score,
        "category": category,
    }
    _save_cache(cache_file, data)
    return data


def harvest_repo(full_name: str) -> Optional[Dict]:
    cache_file = CACHE_DIR / f"meta_{full_name.replace('/', '_')}.json"
    cached = _load_cache(cache_file)
    if cached:
        return cached
    repo = fetch_repo(full_name)
    if not repo:
        return None
    readme = fetch_readme(full_name)
    score = compute_score(repo, readme)
    category = categorize(repo.get("description", ""), repo.get("topics", []))
    first_paragraph = readme.split("\n\n")[0][:200]
    data = {
        "name": full_name,
        "description": repo.get("description", ""),
        "stars": repo.get("stargazers_count", 0),
        "forks": repo.get("forks_count", 0),
        "open_issues": repo.get("open_issues_count", 0),
        "closed_issues": repo.get("closed_issues", 0),
        "last_commit": repo.get("pushed_at", ""),
        "language": repo.get("language", ""),
        "license": (
            repo.get("license")
            if not isinstance(repo.get("license"), dict)
            else repo.get("license").get("spdx_id")
        ),
        "maintainer": repo.get("owner", {}).get("login"),
        "topics": ",".join(repo.get("topics", [])),
        "readme_excerpt": first_paragraph,
        SCORE_KEY: score,
        "category": category,
    }
    _save_cache(cache_file, data)
    return data


async def async_search_and_harvest(
    min_stars: int = 0, max_pages: int = 1
) -> List[Dict]:
    seen = set()
    results: List[Dict] = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for term in SEARCH_TERMS:
            for page in range(1, max_pages + 1):
                query = f"{term} stars:>={min_stars}"
                resp = await http_utils.async_get(
                    f"{GITHUB_API}/search/repositories",
                    params={
                        "q": query,
                        "sort": "stars",
                        "order": "desc",
                        "per_page": 100,
                        "page": page,
                    },
                    session=session,
                )
                for repo in resp.json().get("items", []):
                    full_name = repo["full_name"]
                    if full_name in seen:
                        continue
                    seen.add(full_name)
                    tasks.append(
                        asyncio.create_task(async_harvest_repo(full_name, session))
                    )

        for topic in TOPIC_FILTERS:
            for page in range(1, max_pages + 1):
                query = f"topic:{topic} stars:>={min_stars}"
                resp = await http_utils.async_get(
                    f"{GITHUB_API}/search/repositories",
                    params={
                        "q": query,
                        "sort": "stars",
                        "order": "desc",
                        "per_page": 100,
                        "page": page,
                    },
                    session=session,
                )
                for repo in resp.json().get("items", []):
                    full_name = repo["full_name"]
                    if full_name in seen:
                        continue
                    seen.add(full_name)
                    tasks.append(
                        asyncio.create_task(async_harvest_repo(full_name, session))
                    )

        for fut in asyncio.as_completed(tasks):
            try:
                meta = await fut
            except Exception as exc:  # pragma: no cover - worker error path
                logger.error("harvest failed: %s", exc)
                continue
            if meta:
                results.append(meta)
    return results


def search_and_harvest(min_stars: int = 0, max_pages: int = 1) -> List[Dict]:
    start = time.perf_counter()
    results = asyncio.run(async_search_and_harvest(min_stars, max_pages))
    logger.info("search_and_harvest completed in %.2fs", time.perf_counter() - start)
    return results
