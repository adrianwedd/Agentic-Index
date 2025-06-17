import json
from pathlib import Path

import agentic_index_cli.internal.inject_readme as inj


def test_category_section_injected(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    by_cat = data_dir / "by_category"
    by_cat.mkdir(parents=True)

    index = {
        "DevTools": {"file": "DevTools.json", "topics": ["agents", "cli", "tools"]},
        "NLP": "NLP.json",
    }
    (by_cat / "index.json").write_text(json.dumps(index))

    (by_cat / "NLP.json").write_text(
        json.dumps(
            {"schema_version": 3, "repos": [{"topics": ["nlp"], "category": "NLP"}]}
        )
    )

    (data_dir / "repos.json").write_text('{"schema_version":3,"repos":[]}')
    (data_dir / "top100.md").write_text(
        "| Rank | Repo | Score | ▲ StarsΔ | ▲ ScoreΔ | Category |\n|-----:|------|------:|-------:|--------:|----------|\n"
    )
    (data_dir / "last_snapshot.json").write_text("[]")

    readme = tmp_path / "README.md"
    readme.write_text(
        "start\n<!-- TOP50:START -->\nfoo\n<!-- TOP50:END -->\n<!-- CATEGORY:START -->\nold\n<!-- CATEGORY:END -->\nend\n"
    )

    for name, val in {
        "README_PATH": readme,
        "DATA_PATH": data_dir / "top100.md",
        "REPOS_PATH": data_dir / "repos.json",
        "SNAPSHOT": data_dir / "last_snapshot.json",
        "BY_CAT_INDEX": by_cat / "index.json",
    }.items():
        setattr(inj, name, val)

    assert inj.main(top_n=50) == 0
    out = readme.read_text()
    start = out.index("<!-- CATEGORY:START -->") + len("<!-- CATEGORY:START -->")
    end = out.index("<!-- CATEGORY:END -->", start)
    snippet = out[start:end].strip()
    expected = "\n".join(
        [
            "- 🛠️ [DevTools](README_DevTools.md)  ",
            "_Topics: `agents`, `cli`, `tools`_",
            "- • [NLP](README_NLP.md)  ",
            "_Topics: `nlp`_",
        ]
    )
    assert snippet == expected
