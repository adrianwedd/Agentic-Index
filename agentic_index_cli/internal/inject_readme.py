"""Inject top100 table into ``README.md`` or check that it is up to date."""

from __future__ import annotations

import sys
import time
import uuid

import structlog

import agentic_index_cli.internal.readme_utils as _readme_utils

from .readme_utils import (
    BY_CAT_INDEX,
    CATEGORY_END,
    CATEGORY_ICONS,
    CATEGORY_START,
    DATA_PATH,
    DEFAULT_SORT_FIELD,
    DEFAULT_TOP_N,
    RANKED_PATH,
    README_PATH,
    REPOS_PATH,
    ROOT,
    SNAPSHOT,
    _build_category_list,
    _fmt_delta,
    _infer_topics,
    _inject_category_section,
    _markers,
    available_categories,
    build_category_table,
)
from .readme_utils import build_readme as _build_readme
from .readme_utils import (
    diff,
)


def _load_rows(*args, **kwargs):
    """Proxy to ``readme_utils._load_rows`` using module paths."""
    return _readme_utils._load_rows(
        *args,
        repos_path=REPOS_PATH,
        ranked_path=RANKED_PATH,
        **kwargs,
    )


def build_readme(*args, **kwargs):
    """Proxy ``readme_utils.build_readme`` using module paths."""
    return _build_readme(
        *args,
        readme_path=README_PATH,
        repos_path=REPOS_PATH,
        ranked_path=RANKED_PATH,
        index_path=BY_CAT_INDEX,
        **kwargs,
    )


logger = structlog.get_logger(__name__).bind(file=__file__)


def main(
    *,
    force: bool = False,
    check: bool = False,
    write: bool = True,
    dry_run: bool = False,
    sort_by: str = DEFAULT_SORT_FIELD,
    top_n: int = DEFAULT_TOP_N,
    limit: int | None = None,
) -> int:
    """Synchronise the README table."""
    request_id = str(uuid.uuid4())
    log = logger.bind(func="main", request_id=request_id)
    start_time = time.perf_counter()
    for path in (DATA_PATH, REPOS_PATH, SNAPSHOT, BY_CAT_INDEX):
        if not path.exists():
            raise FileNotFoundError(str(path))
    if not (RANKED_PATH.exists() or REPOS_PATH.exists()):
        raise FileNotFoundError(str(REPOS_PATH))
    try:
        row_limit = top_n if limit is None else limit
        new_text = build_readme(sort_by=sort_by, limit=row_limit, top_n=top_n)
    except Exception as exc:
        log.exception("build-failed", error=str(exc))
        return 1

    if check:
        if not SNAPSHOT.exists():
            print(f"Warning: missing snapshot {SNAPSHOT}", file=sys.stderr)
            return 0
        if diff(new_text, README_PATH):
            print("README.md is out of date", file=sys.stderr)
            return 1
        return 0

    if dry_run:
        print(diff(new_text, README_PATH))
        return 0

    if write and (force or diff(new_text, README_PATH)):
        try:
            README_PATH.write_text(new_text, encoding="utf-8")
        except Exception as exc:
            log.exception("write-error", error=str(exc))
            raise

    log.info("inject-complete", duration=time.perf_counter() - start_time)
    return 0


def write_category_readme(
    category: str,
    *,
    force: bool = False,
    check: bool = False,
    write: bool = True,
    sort_by: str = DEFAULT_SORT_FIELD,
    top_n: int = DEFAULT_TOP_N,
    limit: int | None = None,
) -> int:
    """Write or check ``README_<category>.md``."""
    request_id = str(uuid.uuid4())
    log = logger.bind(func="write_category_readme", request_id=request_id)
    start_time = time.perf_counter()
    cfg_limit = top_n if limit is None else limit
    text = build_category_table(
        category,
        sort_by=sort_by,
        limit=cfg_limit,
        repos_path=REPOS_PATH,
        ranked_path=RANKED_PATH,
    )
    fname = f"README_{category.replace(' ', '_')}.md"
    path = ROOT / fname
    if check and path.exists() and diff(text, path):
        print(f"{fname} is out of date", file=sys.stderr)
        return 1
    if write and (force or not path.exists() or diff(text, path)):
        try:
            path.write_text(text, encoding="utf-8")
        except Exception as exc:
            log.exception("write-category-error", error=str(exc))
            raise
    log.info("write-category-complete", duration=time.perf_counter() - start_time)
    return 0


def write_all_categories(**kwargs) -> int:
    """Write or check README files for all categories."""
    request_id = str(uuid.uuid4())
    log = logger.bind(func="write_all_categories", request_id=request_id)
    start_time = time.perf_counter()
    status = 0
    for cat in available_categories(REPOS_PATH, RANKED_PATH):
        ret = write_category_readme(cat, **kwargs)
        status = max(status, ret)
    log.info("write-all-complete", duration=time.perf_counter() - start_time)
    return status
