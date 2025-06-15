import json
import logging
from pathlib import Path
from typing import List, Optional

from agentic_index_cli.agentic_index import search_and_harvest

STATE_PATH = Path("state/sync_data.json")
logger = logging.getLogger(__name__)
_cache: List[dict] | None = None


def sync(org: Optional[str] = None, topics: Optional[List[str]] = None) -> List[dict]:
    """Fetch repo metadata and return the filtered list."""
    repos = search_and_harvest(min_stars=0, max_pages=1)

    if org:
        repos = [r for r in repos if r.get("maintainer") == org]
    if topics:
        lowered = [t.lower() for t in topics]
        repos = [
            r
            for r in repos
            if any(t in r.get("topics", "").lower().split(",") for t in lowered)
        ]

    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(repos, indent=2))

    global _cache
    _cache = repos
    logger.info("synced %s repos", len(repos))
    return repos
