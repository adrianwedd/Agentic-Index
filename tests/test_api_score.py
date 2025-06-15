from fastapi.testclient import TestClient
from agentic_index_api.server import app


def test_score_endpoint():
    client = TestClient(app)
    resp = client.post("/score", json={})
    assert resp.status_code == 200
    data = resp.json()
    assert "top_scores" in data
    assert isinstance(data["top_scores"], list)
