from __future__ import annotations

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
    repo: str
    type: Literal["issue", "comment"]
    body: str
    title: str | None = None
    issue_number: int | None = None


@app.post("/issue")
def issue_endpoint(payload: IssueRequest):
    token = get_issue_token()
    try:
        if payload.type == "issue":
            if not payload.title:
                raise HTTPException(status_code=400, detail="title required for new issue")
            data = create_issue(payload.repo, payload.title, payload.body, token=token)
        else:
            if payload.issue_number is None:
                raise HTTPException(status_code=400, detail="issue_number required for comment")
            data = post_comment(payload.repo, payload.issue_number, payload.body, token=token)
    except APIError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return {"url": data.get("html_url", "")}
