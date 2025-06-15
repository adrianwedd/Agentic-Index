from __future__ import annotations

from fastapi import FastAPI, Response
from typing import List

"""Minimal API server with optional auth."""

import os
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel
import json

from fastapi import FastAPI, Response, HTTPException, Request
from fastapi.concurrency import run_in_threadpool

from agentic_index_cli.internal.scrape import scrape
from agentic_index_cli.validate import save_repos
from agentic_index_cli.internal.rank import compute_score, SCORE_KEY
from agentic_index_cli import issue_logger

API_KEY = os.getenv("API_KEY")
_whitelist = os.getenv("IP_WHITELIST", "")
IP_WHITELIST = {ip.strip() for ip in _whitelist.split(",") if ip.strip()}

PROTECTED_PATHS = {"/sync", "/score", "/render", "/issue"}

SYNC_DATA_PATH = Path("state/sync_data.json")


def _load_sync_data() -> List[dict[str, Any]]:
    """Return list of repos from :data:`SYNC_DATA_PATH`."""
    try:
        with SYNC_DATA_PATH.open() as fh:
            data = json.load(fh)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=400, detail="sync data missing") from exc
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail="invalid sync data") from exc
    if not isinstance(data, list) or not all(isinstance(r, dict) for r in data):
        raise HTTPException(status_code=400, detail="invalid sync data")
    return data

app = FastAPI()


@app.middleware("http")
async def _auth(request: Request, call_next):
    if request.url.path in PROTECTED_PATHS:
        client_ip = request.client.host if request.client else None
        if client_ip not in IP_WHITELIST:
            key = request.headers.get("X-API-KEY")
            if not API_KEY or key != API_KEY:
                return Response(status_code=401)
    return await call_next(request)


@app.get("/status")
def status() -> dict:
    """Return service status."""
    return {"status": "ok"}


@app.get("/healthz")
def healthz() -> Response:
    """Kubernetes style health check."""
    return Response(status_code=200)



@app.post("/sync")
async def sync(min_stars: int = 0) -> dict[str, Any]:
    """Fetch repository data and write to ``data/repos.json``."""
    token = os.getenv("GITHUB_TOKEN")

    def _run() -> dict[str, Any]:
        repos = scrape(min_stars=min_stars, token=token)
        save_repos(Path("data/repos.json"), repos)
        return {"repos": len(repos)}

    return await run_in_threadpool(_run)


@app.post("/score")
def score() -> dict[str, Any]:
    """Return top 5 repositories sorted by score."""

    repos = _load_sync_data()
    scored = []
    for repo in repos:
        score = compute_score(repo)
        name = repo.get("full_name") or repo.get("name")
        if name:
            scored.append({"name": name, "score": score})

    scored.sort(key=lambda r: r["score"], reverse=True)
    return {"top_scores": scored[:5]}


@app.post("/render")
async def render() -> dict[str, str]:
    """Regenerate markdown outputs like README."""

    from agentic_index_cli.generate_outputs import main as _main

    await run_in_threadpool(_main)
    return {"status": "ok"}


class IssueBody(BaseModel):
    repo: str
    title: Optional[str] = None
    body: str = ""
    issue_number: Optional[int] = None


@app.post("/issue")
async def issue(payload: IssueBody) -> Any:
    """Create a GitHub issue or comment."""

    token = issue_logger.get_token()

    def _run() -> Any:
        if payload.issue_number is not None:
            return issue_logger.post_comment(
                payload.repo, payload.issue_number, payload.body, token=token
            )
        if not payload.title:
            raise HTTPException(status_code=400, detail="title required")
        return issue_logger.create_issue(
            payload.repo, payload.title, payload.body, token=token
        )

    return await run_in_threadpool(_run)
