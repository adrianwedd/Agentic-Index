from __future__ import annotations

import os
from pathlib import Path
from fastapi import FastAPI

from agentic_index_cli.validate import load_repos, save_repos
from agentic_index_cli.internal.rank import (
    compute_score,
    infer_category,
    SCORE_KEY,
)


def get_state_dir() -> Path:
    return Path(os.getenv("STATE_DIR", "state"))


def load_sync_data() -> list[dict]:
    path = get_state_dir() / "sync_data.json"
    return load_repos(path) if path.exists() else []


def save_scored_data(repos: list[dict]) -> None:
    path = get_state_dir() / "scored_data.json"
    save_repos(path, repos)


app = FastAPI()


@app.post("/score")
def score_endpoint():
    repos = load_sync_data()
    for repo in repos:
        repo[SCORE_KEY] = compute_score(repo)
        repo["category"] = infer_category(repo)
    repos.sort(key=lambda r: r[SCORE_KEY], reverse=True)
    save_scored_data(repos)
    top_scores = [r[SCORE_KEY] for r in repos[:5]]
    return {"top_scores": top_scores}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
