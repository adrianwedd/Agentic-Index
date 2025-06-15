from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/status")
def status() -> dict:
    """Return service status."""
    return {"status": "ok"}


@app.get("/healthz")
def healthz() -> Response:
    """Kubernetes style health check."""
    return Response(status_code=200)
