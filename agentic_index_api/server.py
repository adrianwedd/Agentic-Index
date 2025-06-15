from fastapi import FastAPI, Response
from typing import List

app = FastAPI()


@app.get("/status")
def status() -> dict:
    """Return service status."""
    return {"status": "ok"}


@app.get("/healthz")
def healthz() -> Response:
    """Kubernetes style health check."""
    return Response(status_code=200)


@app.post("/score")
def score() -> dict:
    """Return placeholder scores list."""
    return {"top_scores": ["example/repo"]}
