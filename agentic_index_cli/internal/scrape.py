"""Scrape GitHub repositories for inclusion in the index."""

import argparse
import asyncio
import json
import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, List

from pydantic import BaseModel, ValidationError

from agentic_index_cli.internal import http_utils

from ..exceptions import APIError, InvalidRepoError, RateLimitError
from ..validate import save_repos

RATE_LIMIT_REMAINING = None
logger = logging.getLogger(__name__)

QUERIES = [
    "agent framework",
    "autonomous agent",
    "LLM agent",
    "AI agent",
]

FIELDS = [
    "name",
    "full_name",
    "html_url",
    "description",
    "stargazers_count",
    "forks_count",
    "open_issues_count",
    "archived",
    "license",
    "language",
    "pushed_at",
    "owner",
]


class LicenseModel(BaseModel):
    """Subset of repo license information."""

    spdx_id: str | None = None


class OwnerModel(BaseModel):
    """Repository owner information."""

    login: str | None = None


class RepoModel(BaseModel):
    """Model for GitHub repository objects."""

    name: str
    full_name: str
    html_url: str
    description: str | None = None
    stargazers_count: int
    forks_count: int
    open_issues_count: int
    archived: bool
    license: LicenseModel | None = None
    language: str | None = None
    pushed_at: str
    owner: OwnerModel


def _get(url: str, *, headers: dict, params: dict | None = None) -> http_utils.Response:
    return http_utils.sync_get(url, params=params, headers=headers)


def _extract(item: Dict[str, Any]) -> Dict[str, Any]:
    try:
        repo = RepoModel(**item)
    except ValidationError as e:
        raise InvalidRepoError(str(e)) from e
    data = repo.model_dump()
    data["license"] = {"spdx_id": (repo.license.spdx_id if repo.license else None)}
    data["owner"] = {"login": repo.owner.login}
    return {field: data.get(field) for field in FIELDS}


def scrape(min_stars: int = 0, token: str | None = None) -> List[Dict[str, Any]]:
    """Return repository metadata from GitHub."""

    async def _scrape_async() -> List[Dict[str, Any]]:
        global RATE_LIMIT_REMAINING
        headers = {"Accept": "application/vnd.github+json"}
        if token:
            headers["Authorization"] = f"token {token}"
        all_repos: Dict[str, Dict[str, Any]] = {}
        tasks = []
        for query in QUERIES:
            params = {
                "q": f"{query} stars:>={min_stars}",
                "sort": "stars",
                "order": "desc",
                "per_page": 100,
            }
            tasks.append(
                asyncio.to_thread(
                    _get,
                    "https://api.github.com/search/repositories",
                    headers=headers,
                    params=params,
                )
            )
        try:
            responses = await asyncio.gather(*tasks)
        except Exception as exc:
            logger.warning("request failed: %s", exc)
            raise
        for response in responses:
            remaining = int(response.headers.get("X-RateLimit-Remaining", "0"))
            if RATE_LIMIT_REMAINING is None or remaining < RATE_LIMIT_REMAINING:
                RATE_LIMIT_REMAINING = remaining
            try:
                items = response.json().get("items", [])
            except ValueError as e:
                logger.warning("bad JSON skipped: %s", e)
                continue
            for item in items:
                try:
                    data = _extract(item)
                except InvalidRepoError as e:
                    logger.warning("invalid repo skipped: %s", e)
                    continue
                all_repos[data["full_name"]] = data
        return list(all_repos.values())

    return asyncio.run(_scrape_async())


def main() -> None:
    """CLI wrapper for :func:`scrape`."""
    parser = argparse.ArgumentParser(description="Fetch GitHub repos for Agentic Index")
    parser.add_argument("--min-stars", type=int, default=0, dest="min_stars")
    args = parser.parse_args()
    token = os.getenv("GITHUB_TOKEN")
    repos = scrape(min_stars=args.min_stars, token=token)
    path = Path("data/repos.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    save_repos(path, repos)
    logger.info("Wrote %s repos to %s", len(repos), path)
    if RATE_LIMIT_REMAINING is not None:
        logger.info("Rate limit remaining: %s", RATE_LIMIT_REMAINING)
