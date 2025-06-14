from fastapi.testclient import TestClient
import agentic_index_cli.api_server as api


def test_token_priority(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "t1")
    monkeypatch.setenv("GITHUB_TOKEN_ISSUES", "t2")
    assert api.get_issue_token() == "t2"


def test_issue_comment(monkeypatch):
    called = {}

    def fake_comment(repo, issue_number, body, *, token=None):
        called['args'] = (repo, issue_number, body, token)
        return {'html_url': 'u'}

    monkeypatch.setattr(api, 'post_comment', fake_comment)
    client = TestClient(api.app)
    resp = client.post(
        "/issue",
        json={
            "repo": "o/r",
            "type": "comment",
            "issue_number": 1,
            "body": "msg",
        },
    )
    assert resp.status_code == 200
    assert resp.json() == {"url": "u"}
    assert called['args'] == ('o/r', 1, 'msg', None)


def test_issue_missing_field(monkeypatch):
    client = TestClient(api.app)
    resp = client.post(
        "/issue",
        json={"repo": "o/r", "type": "comment", "body": "x"},
    )
    assert resp.status_code == 400
