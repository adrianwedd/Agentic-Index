#!/usr/bin/env python3
"""FunkyAF demonstration showcasing tests and pipeline.

This script provides an over-the-top walkthrough of the repository's
tooling.  It runs formatting checks, executes the test suite, validates
fixtures, and spins up a miniature pipeline using fixture data.  Along
the way it displays docstrings, progress bars, and a small metrics table
rendered with :mod:`rich` for a deluxe terminal experience.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress
from rich.table import Table

console = Console()


def run(cmd: list[str]) -> None:
    """Execute *cmd* and stream output via :class:`rich.console.Console`."""

    console.rule(f"[bold cyan]$ {' '.join(cmd)}")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.stdout:
        console.print(proc.stdout)
    if proc.stderr:
        console.print(proc.stderr, style="red")
    if proc.returncode != 0:
        console.print(f"command failed with {proc.returncode}", style="red")
        sys.exit(proc.returncode)


def show_doc(obj: object) -> None:
    """Render a function's docstring in a pretty panel."""

    doc = getattr(obj, "__doc__", "(no docstring)") or "(no docstring)"
    console.print(Panel(Markdown(doc), title=f"{obj.__module__}.{obj.__name__}"))


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    os.chdir(root)

    console.rule("[bold magenta]🎉 Welcome to the Agentic Index FunkyAF Demo!")
    console.print(f"Working directory: {root}\n")

    with Progress() as progress:
        fmt_task = progress.add_task("Formatting", total=2)
        progress.update(fmt_task, description="black")
        run(["black", "--check", "."])
        progress.advance(fmt_task)
        progress.update(fmt_task, description="isort")
        run(["isort", "--check-only", "."])
        progress.advance(fmt_task)

    with Progress() as progress:
        test_task = progress.add_task("pytest", total=1)
        run([sys.executable, "-m", "pytest", "-q"])
        progress.advance(test_task)

    with Progress() as progress:
        val_task = progress.add_task("validate fixtures", total=2)
        run([sys.executable, "scripts/validate_fixtures.py"])
        progress.advance(val_task)
        run([sys.executable, "scripts/validate_top100.py"])
        progress.advance(val_task)

    console.rule("🚀 Mini pipeline demo")

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

    show_doc(enricher.enrich)
    show_doc(rank.main)
    show_doc(inj.main)

    inj.REPOS_PATH = data_dir / "repos.json"
    inj.DATA_PATH = data_dir / "top100.md"
    inj.SNAPSHOT = data_dir / "last_snapshot.json"
    inj.BY_CAT_INDEX = data_dir / "by_category" / "index.json"
    inj.README_PATH = demo_dir / "README.md"
    inj.readme_utils.README_PATH = inj.README_PATH
    inj.ROOT = demo_dir

    with Progress() as progress:
        e_task = progress.add_task("enrich", total=1)
        enricher.enrich(inj.REPOS_PATH)
        progress.advance(e_task)

        r_task = progress.add_task("rank", total=1)
        rank.main(str(inj.REPOS_PATH))
        progress.advance(r_task)

        i_task = progress.add_task("inject", total=1)
        inj.main(force=True, top_n=5, limit=5)
        progress.advance(i_task)

    console.rule("README preview")
    console.print(inj.README_PATH.read_text())

    data = json.loads((data_dir / "repos.json").read_text())
    table = Table(title="Fixture Metrics")
    table.add_column("Repos", justify="right")
    table.add_column("Average Stars", justify="right")
    count = len(data["repos"])
    avg_stars = sum(r["stargazers_count"] for r in data["repos"]) / count
    table.add_row(str(count), f"{avg_stars:,.1f}")
    console.print(table)
    console.print(f"Demo artifacts stored in [bold]{demo_dir}[/]")

    console.rule("smoke test")
    run(["bash", "scripts/e2e_test.sh"])


if __name__ == "__main__":
    main()
