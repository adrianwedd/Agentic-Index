from __future__ import annotations

"""Minimal FastAPI server for posting GitHub issues or comments."""

import os
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .issue_logger import APIError, create_issue, post_comment


def get_issue_token() -> str | None:
    """Return GitHub token preferring GITHUB_TOKEN_ISSUES."""
    return os.getenv("GITHUB_TOKEN_ISSUES") or os.getenv("GITHUB_TOKEN")


app = FastAPI()


class IssueRequest(BaseModel):
    """Payload for creating issues or comments."""

    repo: str
    type: Literal["issue", "comment"]
    body: str
    title: str | None = None
    issue_number: int | None = None


@app.post("/issue")
def issue_endpoint(payload: IssueRequest):
    """Handle issue creation or commenting requests."""
    token = get_issue_token()
    try:
        if payload.type == "issue":
            if not payload.title:
                raise HTTPException(status_code=400, detail="title required for new issue")
            url = create_issue(payload.title, payload.body, payload.repo, token=token)
        else:
            if payload.issue_number is None:
                raise HTTPException(status_code=400, detail="issue_number required for comment")
            issue_url = f"https://api.github.com/repos/{payload.repo}/issues/{payload.issue_number}"
            url = post_comment(issue_url, payload.body, token=token)
    except APIError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return {"url": url}
