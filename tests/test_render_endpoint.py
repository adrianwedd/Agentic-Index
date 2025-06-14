import sys
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

from agentic_index_cli.api import app


def test_render_endpoint(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    client = TestClient(app)
    data = {
        "repos": [
            {"name": "foo", "score": 10},
            {"name": "bar", "score": 20}
        ],
        "export_json": True,
    }
    resp = client.post("/render", json=data)
    assert resp.status_code == 200
    res = resp.json()
    assert "| Repo | Score |" in res["markdown"]
    assert Path(res["markdown_file"]).exists()
    assert Path(res["plot_file"]).exists()
    assert Path(res["json_file"]).exists()
