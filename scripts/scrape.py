import argparse
import json
import os
from pathlib import Path
from typing import List, Dict, Any
import requests

RATE_LIMIT_REMAINING = None

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

def _extract(item: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "name": item.get("name"),
        "full_name": item.get("full_name"),
        "html_url": item.get("html_url"),
        "description": item.get("description"),
        "stargazers_count": item.get("stargazers_count"),
        "forks_count": item.get("forks_count"),
        "open_issues_count": item.get("open_issues_count"),
        "archived": item.get("archived"),
        "license": {"spdx_id": (item.get("license") or {}).get("spdx_id")},
        "language": item.get("language"),
        "pushed_at": item.get("pushed_at"),
        "owner": {"login": (item.get("owner") or {}).get("login")},
    }


def scrape(min_stars: int = 0, token: str | None = None) -> List[Dict[str, Any]]:
    global RATE_LIMIT_REMAINING
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    all_repos: Dict[str, Dict[str, Any]] = {}
    for query in QUERIES:
        params = {
            "q": f"{query} stars:>={min_stars}",
            "sort": "stars",
            "order": "desc",
            "per_page": 100,
        }
        response = requests.get(
            "https://api.github.com/search/repositories",
            headers=headers,
            params=params,
        )
        response.raise_for_status()
        remaining = int(response.headers.get("X-RateLimit-Remaining", "0"))
        if RATE_LIMIT_REMAINING is None or remaining < RATE_LIMIT_REMAINING:
            RATE_LIMIT_REMAINING = remaining
        for item in response.json().get("items", []):
            data = _extract(item)
            all_repos[data["full_name"]] = data
    return list(all_repos.values())


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch GitHub repos for AgentOps")
    parser.add_argument("--min-stars", type=int, default=0, dest="min_stars")
    args = parser.parse_args()
    token = os.getenv("GITHUB_TOKEN")
    repos = scrape(min_stars=args.min_stars, token=token)
    path = Path("data/repos.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(repos, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(repos)} repos to {path}")
    if RATE_LIMIT_REMAINING is not None:
        print(f"Rate limit remaining: {RATE_LIMIT_REMAINING}")


if __name__ == "__main__":
    main()
