import json
import os
import subprocess
from pathlib import Path

from agentic_index_cli.config import load_config


def test_load_default():
    cfg = load_config()
    assert cfg['ranking']['top_n'] == 100


def test_cli_override(tmp_path):
    repo = {
        "name": "A",
        "stars": 10,
        "recency_factor": 1,
        "issue_health": 1,
        "doc_completeness": 0,
        "license_freedom": 1,
        "ecosystem_integration": 0,
    }
    data = {"schema_version": 1, "repos": [repo, dict(repo, name="B", stars=5)]}
    repo_file = tmp_path / "repos.json"
    repo_file.write_text(json.dumps(data))

    cfg_file = tmp_path / "cfg.yaml"
    cfg_file.write_text("""\
ranking:
  top_n: 1
  delta_days: 7
  min_stars: 0
output:
  markdown_table_limit: 1
""")

    script = Path(__file__).resolve().parents[1] / "scripts" / "rank.py"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
    env.pop("PYTEST_CURRENT_TEST", None)
    subprocess.run([
        "python", str(script), str(repo_file), "--config", str(cfg_file)
    ], check=True, cwd=tmp_path, env=env)

    top_md = tmp_path / "data" / "top100.md"
    lines = [l for l in top_md.read_text().splitlines() if l.startswith("|")]
    assert len(lines) == 3
