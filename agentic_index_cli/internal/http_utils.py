import asyncio
import json
import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import aiohttp

logger = logging.getLogger(__name__)

CONCURRENCY_LIMIT = 5
_semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)


@dataclass
class Response:
    status_code: int
    headers: Dict[str, Any]
    text: str

    def json(self) -> Any:
        return json.loads(self.text)


async def async_get(
    url: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    session: aiohttp.ClientSession,
    retries: int = 5,
) -> Response:
    """GET with exponential backoff and rate limit handling."""
    backoff = 1
    for attempt in range(retries):
        try:
            async with _semaphore:
                async with session.get(url, params=params, headers=headers) as resp:
                    text = await resp.text()
                    if (
                        resp.status == 403
                        and resp.headers.get("X-RateLimit-Remaining") == "0"
                    ):
                        reset = int(resp.headers.get("X-RateLimit-Reset", "0"))
                        sleep_for = max(0, reset - int(time.time()))
                        logger.warning("Rate limit hit, sleeping %s seconds", sleep_for)
                        await asyncio.sleep(sleep_for)
                        continue
                    if resp.status >= 500:
                        logger.warning("Server error %s", resp.status)
                        await asyncio.sleep(backoff)
                        backoff *= 2
                        continue
                    return Response(resp.status, dict(resp.headers), text)
        except aiohttp.ClientError as exc:
            if attempt == retries - 1:
                raise
            logger.warning("Request error: %s; retrying in %s seconds", exc, backoff)
            await asyncio.sleep(backoff)
            backoff *= 2
    raise aiohttp.ClientError(f"failed GET {url} after retries")


def sync_get(
    url: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    retries: int = 5,
) -> Response:
    """Synchronous wrapper around :func:`async_get`."""

    async def runner() -> Response:
        async with aiohttp.ClientSession() as session:
            return await async_get(
                url, params=params, headers=headers, session=session, retries=retries
            )

    return asyncio.run(runner())
