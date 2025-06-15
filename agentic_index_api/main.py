from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException

DATA_FILE = Path("repos.json")
HISTORY_DIR = Path("data/history")

app = FastAPI(title="Agentic Index API")


def _load_repos() -> list[dict[str, Any]]:
    if DATA_FILE.exists():
        with DATA_FILE.open() as f:
            data = json.load(f)
        return data.get("repos", [])
    return []


REPOS = _load_repos()
SCORE_KEY = None
for repo in REPOS:
    if "AgenticIndexScore" in repo:
        SCORE_KEY = "AgenticIndexScore"
        break
    if "AgentOpsScore" in repo:
        SCORE_KEY = "AgentOpsScore"
        break
if SCORE_KEY is None:
    SCORE_KEY = "score"

RANKED = sorted(REPOS, key=lambda r: r.get(SCORE_KEY, 0), reverse=True)
NAME_MAP = {}
for r in REPOS:
    NAME_MAP[r.get("name")] = r
    if "full_name" in r:
        NAME_MAP[r["full_name"]] = r


@app.get("/repo/{name}")
def get_repo(name: str) -> dict[str, Any]:
    repo = NAME_MAP.get(name)
    if not repo:
        raise HTTPException(status_code=404, detail="Repo not found")
    rank = next((i + 1 for i, r in enumerate(RANKED) if r is repo), None)
    stars = repo.get("stargazers_count") or repo.get("stars")
    return {
        "name": repo.get("full_name", repo.get("name")),
        "rank": rank,
        "stars": stars,
        "score": repo.get(SCORE_KEY),
        "metadata": repo,
    }


@app.get("/history/{name}")
def get_history(name: str) -> dict[str, Any]:
    points = []
    for path in sorted(HISTORY_DIR.glob("*.json")):
        date = path.stem
        with path.open() as f:
            data = json.load(f)
        for entry in data:
            if not isinstance(entry, dict):
                continue
            if entry.get("name") == name or entry.get("full_name") == name:
                for key in ("AgentOpsScore", "AgenticIndexScore", "score"):
                    if key in entry:
                        points.append({"date": date, "score": entry[key]})
                        break
                break
    if not points:
        raise HTTPException(status_code=404, detail="No history found")
    return {"name": name, "history": points}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
