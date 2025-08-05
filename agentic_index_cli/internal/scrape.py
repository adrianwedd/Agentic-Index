"""Scrape GitHub repositories for inclusion in the index."""

import argparse
import asyncio
import datetime
import json
import logging
import math
import os
import time
from pathlib import Path
from typing import Any, Dict, List

from pydantic import BaseModel, ValidationError

from agentic_index_cli.github_client import get as github_get
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
    "stars",
    "recency_factor",
    "issue_health",
    "doc_completeness",
    "license_freedom",
    "ecosystem_integration",
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
    return github_get(url, params=params, headers=headers)


def compute_recency_factor(pushed_at: str) -> float:
    """Compute recency factor based on last push date."""
    try:
        pushed_date = datetime.datetime.strptime(pushed_at, "%Y-%m-%dT%H:%M:%SZ")
        days = (datetime.datetime.now(datetime.timezone.utc) - pushed_date).days
        if days <= 30:
            return 1.0
        if days >= 365:
            return 0.0
        return max(0.0, 1 - (days - 30) / 335)
    except (ValueError, TypeError):
        return 0.0


def compute_issue_health(open_issues: int) -> float:
    """Compute issue health factor."""
    if open_issues <= 10:
        return 1.0
    elif open_issues <= 50:
        return 0.7
    elif open_issues <= 100:
        return 0.5
    else:
        return 0.2


def get_license_freedom(license_info: dict) -> float:
    """Compute license freedom factor."""
    if not license_info:
        return 0.5
    spdx_id = license_info.get("spdx_id", "")
    if not spdx_id:
        return 0.5
    spdx_id = spdx_id.lower()
    permissive = {"mit", "apache-2.0", "bsd-2-clause", "bsd-3-clause", "isc"}
    if spdx_id in permissive:
        return 1.0
    elif spdx_id in {"gpl-3.0", "gpl-2.0", "agpl-3.0"}:
        return 0.5
    return 0.5


def get_doc_completeness(full_name: str) -> float:
    """Check for presence of common documentation files."""
    doc_files = [
        "README.md",
        "docs/index.md",
        "docs/README.md",
        "documentation/README.md",
    ]
    for doc_file in doc_files:
        doc_url = f"https://raw.githubusercontent.com/{full_name}/HEAD/{doc_file}"
        try:
            resp = _get(doc_url)
            if resp.status_code == 200:
                return 1.0
        except Exception:
            pass
    return 0.0


def get_ecosystem_integration(description: str, topics: List[str]) -> float:
    """Check for ecosystem integration keywords."""
    text = (description or "").lower() + " " + " ".join(topics).lower()
    keywords = ["langchain", "openai", "plugin", "framework", "tool", "api"]
    for keyword in keywords:
        if keyword in text:
            return 1.0
    return 0.0


def _extract(item: Dict[str, Any]) -> Dict[str, Any]:
    try:
        repo = RepoModel(**item)
    except ValidationError as e:
        raise InvalidRepoError(str(e)) from e
    data = repo.model_dump()
    data["license"] = {"spdx_id": (repo.license.spdx_id if repo.license else None)}
    data["owner"] = {"login": repo.owner.login}

    # Compute scoring fields
    stars = data.get("stargazers_count", 0)
    open_issues = data.get("open_issues_count", 0)
    pushed_at = data.get("pushed_at", "")
    description = data.get("description", "")
    license_info = data.get("license", {})
    topics = data.get("topics", [])  # Assuming topics are now part of the scraped data

    data["stars"] = stars  # Add stars for consistency with ranker
    data["recency_factor"] = compute_recency_factor(pushed_at)
    data["issue_health"] = compute_issue_health(open_issues)
    data["doc_completeness"] = get_doc_completeness(data["full_name"])
    data["license_freedom"] = get_license_freedom(license_info)
    data["ecosystem_integration"] = get_ecosystem_integration(description, topics)

    return {
        field: data.get(field)
        for field in FIELDS
        + [
            "stars",
            "recency_factor",
            "issue_health",
            "doc_completeness",
            "license_freedom",
            "ecosystem_integration",
        ]
    }


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
