from types import SimpleNamespace

import agentic_index_cli.internal.link_integrity as li


def test_link_integrity(tmp_path, monkeypatch):
    md = tmp_path / "sample.md"
    md.write_text(
        "# Title\n\n[ok](#title)\n[bad](#missing)\n![](badges/foo.svg)\n![](https://img.shields.io/badge/test-blue)"
    )
    (tmp_path / "badges").mkdir()
    (tmp_path / "badges" / "foo.svg").write_text("<svg></svg>")

    # mock requests.get for shields url
    def fake_get(url, timeout=3):
        return SimpleNamespace(status_code=200)

    monkeypatch.setattr(li.requests, "get", fake_get)

    rc = li.main([str(md)])
    assert rc == 1  # missing anchor triggers failure
