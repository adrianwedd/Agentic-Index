import asyncio
import json
import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import aiohttp

from ..exceptions import APIError

logger = logging.getLogger(__name__)

CONCURRENCY_LIMIT = 5
_semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)

DEFAULT_RETRIES = 5
DEFAULT_TIMEOUT = 10
DEFAULT_BACKOFF = 1.0


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
    retries: int = DEFAULT_RETRIES,
    timeout: float = DEFAULT_TIMEOUT,
    backoff_factor: float = DEFAULT_BACKOFF,
) -> Response:
    """GET with exponential backoff, timeout and rate limit handling."""
    backoff = backoff_factor
    for attempt in range(retries):
        try:
            async with _semaphore:
                async with session.get(
                    url, params=params, headers=headers, timeout=timeout
                ) as resp:
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
        except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
            if attempt == retries - 1:
                raise APIError(f"GET {url} failed: {exc}") from exc
            logger.warning("Request error: %s; retrying in %s seconds", exc, backoff)
            await asyncio.sleep(backoff)
            backoff *= 2
    raise APIError(f"GET {url} failed after retries")


def sync_get(
    url: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    retries: int = DEFAULT_RETRIES,
    timeout: float = DEFAULT_TIMEOUT,
    backoff_factor: float = DEFAULT_BACKOFF,
) -> Response:
    """Synchronous wrapper around :func:`async_get`."""

    async def runner() -> Response:
        async with aiohttp.ClientSession() as session:
            return await async_get(
                url,
                params=params,
                headers=headers,
                session=session,
                retries=retries,
                timeout=timeout,
                backoff_factor=backoff_factor,
            )

    return asyncio.run(runner())
