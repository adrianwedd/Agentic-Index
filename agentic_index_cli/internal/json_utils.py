from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Tuple

_cache: Dict[Path, Tuple[float, Any]] = {}


def load_json(
    path: Path,
    *,
    cache: bool = False,
    stream: bool = False,
) -> Any:
    """Load JSON from ``path`` with optional caching or streaming."""
    mtime = path.stat().st_mtime
    if cache:
        entry = _cache.get(path)
        if entry and entry[0] == mtime:
            return entry[1]
    data: Any
    if stream:
        try:
            import ijson  # type: ignore
        except Exception:
            stream = False
    if stream:
        with path.open("rb") as fh:
            data = ijson.load(fh)
    else:
        with path.open() as fh:
            data = json.load(fh)
    if cache:
        _cache[path] = (mtime, data)
    return data
