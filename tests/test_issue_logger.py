import os
import responses
import pytest

import agentic_index_cli.issue_logger as il


def test_token_fallback(monkeypatch):
    monkeypatch.delenv('GITHUB_TOKEN', raising=False)
    monkeypatch.setenv('GITHUB_TOKEN_ISSUES', 'tok')
    assert il.get_token() == 'tok'


def test_cli_create_issue(monkeypatch):
    called = {}

    def fake_create(title, body, repo):
        called['args'] = (title, body, repo)
        return 'x'

    monkeypatch.setattr(il, 'create_issue', fake_create)
    il.main(['--new-issue', '--repo', 'o/r', '--title', 't', '--body', 'b'])
    assert called['args'] == ('t', 'b', 'o/r')


@responses.activate
def test_post_comment_error(monkeypatch):
    responses.add(
        responses.POST,
        'https://api.github.com/repos/o/r/issues/1/comments',
        json={'message': 'bad'},
        status=401,
    )
    with pytest.raises(il.APIError):
        il.post_comment('https://api.github.com/repos/o/r/issues/1', 'msg', token='bad')
