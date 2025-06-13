import json
import os
import tempfile
import timeit
from pathlib import Path

import responses

from agentic_index_cli.internal import scrape, rank


def _make_items(start: int, count: int) -> list[dict]:
    items = []
    for i in range(start, start + count):
        items.append(
            {
                "name": f"repo{i}",
                "full_name": f"owner/repo{i}",
                "html_url": f"https://example.com/repo{i}",
                "description": "benchmark repo",
                "stargazers_count": i,
                "forks_count": 0,
                "open_issues_count": 0,
                "archived": False,
                "license": {"spdx_id": "MIT"},
                "language": "Python",
                "pushed_at": "2025-01-01T00:00:00Z",
                "owner": {"login": "owner"},
            }
        )
    return items


def run() -> bool:
    with tempfile.TemporaryDirectory() as td:
        repo_path = Path(td) / "repos.json"
        with responses.RequestsMock() as rsps:
            per_query = 500 // len(scrape.QUERIES)
            idx = 0
            for _ in scrape.QUERIES:
                items = _make_items(idx, per_query)
                idx += per_query
                rsps.add(
                    responses.GET,
                    "https://api.github.com/search/repositories",
                    json={"items": items},
                    headers={"X-RateLimit-Remaining": "99"},
                    match_querystring=False,
                    status=200,
                )
            repos = scrape.scrape(min_stars=0, token=None)
        repo_path.write_text(json.dumps(repos))
        env = os.environ.copy()
        env["PYTEST_CURRENT_TEST"] = "benchmark"
        rank.main(str(repo_path))
    return repo_path.exists()


def main() -> None:
    duration = timeit.timeit(run, number=1)
    print(f"Pipeline completed in {duration:.2f}s")


if __name__ == "__main__":
    main()
