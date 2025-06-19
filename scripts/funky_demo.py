#!/usr/bin/env python3
"""FunkyAF demonstration of tests and pipeline."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

COL = "\033[95m"
END = "\033[0m"


def run(cmd: list[str]) -> None:
    print(f"\n{COL}💥 Running: {' '.join(cmd)}{END}")
    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.stdout:
        print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)
    if proc.returncode != 0:
        print(f"Command failed with {proc.returncode}")
        sys.exit(proc.returncode)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    os.chdir(root)
    print(f"{COL}🎉 Welcome to the Agentic Index FunkyAF Demo!{END}")
    print(f"Working directory: {root}")

    print(f"{COL}\n🤖 Step 1: Formatting checks{END}")
    run(["black", "--check", "."])
    run(["isort", "--check-only", "."])

    print(f"{COL}\n🔬 Step 2: Running tests{END}")
    run([sys.executable, "-m", "pytest", "-q"])

    print(f"{COL}\n📚 Step 3: Fixture validation{END}")
    run([sys.executable, "scripts/validate_fixtures.py"])
    run([sys.executable, "scripts/validate_top100.py"])

    print(f"{COL}\n🚀 Step 4: Mini pipeline demo{END}")
    demo_dir = Path(tempfile.mkdtemp(prefix="demo_artifacts_"))
    data_dir = demo_dir / "data"
    data_dir.mkdir()
    fixture = root / "tests" / "fixtures" / "data" / "repos.json"
    shutil.copy(fixture, data_dir / "repos.json")
    (data_dir / "last_snapshot.json").write_text("[]")
    (data_dir / "top100.md").write_text("")
    (data_dir / "by_category").mkdir()
    (data_dir / "by_category" / "index.json").write_text("{}")

    import agentic_index_cli.enricher as enricher
    import agentic_index_cli.internal.inject_readme as inj
    import agentic_index_cli.internal.rank_main as rank

    inj.REPOS_PATH = data_dir / "repos.json"
    inj.DATA_PATH = data_dir / "top100.md"
    inj.SNAPSHOT = data_dir / "last_snapshot.json"
    inj.BY_CAT_INDEX = data_dir / "by_category" / "index.json"
    inj.README_PATH = demo_dir / "README.md"
    inj.readme_utils.README_PATH = inj.README_PATH
    inj.ROOT = demo_dir

    print(f"{COL}✨ Enriching...{END}")
    enricher.enrich(inj.REPOS_PATH)
    print(f"{COL}✨ Ranking...{END}")
    rank.main(str(inj.REPOS_PATH))
    print(f"{COL}✨ Injecting README...{END}")
    inj.main(force=True, top_n=5, limit=5)

    print(f"{COL}\nOutput README:{END}")
    print(inj.README_PATH.read_text())
    print(f"{COL}Demo artifacts stored in {demo_dir}{END}")


if __name__ == "__main__":
    main()
