import json
import logging
import time
import uuid
from pathlib import Path
from typing import List, Optional

import structlog

from agentic_index_cli.network import search_and_harvest

STATE_PATH = Path("state/sync_data.json")
logger = structlog.get_logger(__name__).bind(file=__file__)
_cache: List[dict] | None = None


def sync(org: Optional[str] = None, topics: Optional[List[str]] = None) -> List[dict]:
    """Fetch repo metadata and return the filtered list."""
    request_id = str(uuid.uuid4())
    log = logger.bind(func="sync", request_id=request_id)
    start_time = time.perf_counter()
    try:
        repos = search_and_harvest(min_stars=0, max_pages=1)
    except Exception as exc:
        log.exception("harvest-error", error=str(exc))
        return []

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
    log.info(
        "sync-complete",
        repos=len(repos),
        duration=time.perf_counter() - start_time,
    )
    return repos
