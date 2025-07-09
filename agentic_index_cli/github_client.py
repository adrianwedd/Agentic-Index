import os
from typing import Any, Dict, Optional

import aiohttp

from .internal import http_utils

GITHUB_API = "https://api.github.com"
DEFAULT_HEADERS = {"Accept": "application/vnd.github+json"}
TOKEN = os.getenv("GITHUB_TOKEN")
if TOKEN:
    DEFAULT_HEADERS["Authorization"] = f"Bearer {TOKEN}"

MAX_RETRIES = int(os.getenv("NETWORK_RETRIES", str(http_utils.DEFAULT_RETRIES)))
REQUEST_TIMEOUT = float(os.getenv("NETWORK_TIMEOUT", str(http_utils.DEFAULT_TIMEOUT)))
BACKOFF_FACTOR = float(os.getenv("NETWORK_BACKOFF", str(http_utils.DEFAULT_BACKOFF)))


async def async_get(
    url: str,
    *,
    session: aiohttp.ClientSession,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
) -> http_utils.Response:
    """Make an authenticated async GET request to GitHub."""
    hdrs = DEFAULT_HEADERS if headers is None else {**DEFAULT_HEADERS, **headers}
    return await http_utils.async_get(
        url,
        params=params,
        headers=hdrs,
        session=session,
        retries=MAX_RETRIES,
        timeout=REQUEST_TIMEOUT,
        backoff_factor=BACKOFF_FACTOR,
    )


def get(
    url: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
) -> http_utils.Response:
    """Synchronous wrapper around :func:`async_get`."""
    hdrs = DEFAULT_HEADERS if headers is None else {**DEFAULT_HEADERS, **headers}
    return http_utils.sync_get(
        url,
        params=params,
        headers=hdrs,
        retries=MAX_RETRIES,
        timeout=REQUEST_TIMEOUT,
        backoff_factor=BACKOFF_FACTOR,
    )
