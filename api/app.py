from fastapi import FastAPI, Body
from typing import List, Optional, Dict, Any

from .sync import sync

app = FastAPI()


@app.post("/sync")
def sync_endpoint(body: Dict[str, Any] = Body(default={})):  # type: ignore[dict-item]
    org: Optional[str] = body.get("org")
    topics: Optional[List[str]] = body.get("topics")
    repos = sync(org=org, topics=topics)
    return {"synced": len(repos)}
