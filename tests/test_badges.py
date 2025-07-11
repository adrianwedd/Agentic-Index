import os
import subprocess


def test_badges_generation(tmp_path):
    # Run the ranking script which should create badges
    subprocess.run(["python", "-m", "agentic_index_cli.enricher"], check=True)
    subprocess.run(["python", "-m", "agentic_index_cli.ranker"], check=True)

    for name in ["last_sync.svg", "top_repo.svg", "repo_count.svg"]:
        path = os.path.join("badges", name)
        assert os.path.exists(path), f"Missing {name}"
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "<svg" in content
