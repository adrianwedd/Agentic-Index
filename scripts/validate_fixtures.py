#!/usr/bin/env python3
"""Validate README fixtures are up to date."""

from __future__ import annotations

import difflib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

FIXTURE = ROOT / "tests" / "fixtures" / "README_fixture.md"


def _generate_readme() -> str:
    """Return README text produced by the injector."""
    from agentic_index_cli.internal import inject_readme as inj

    return inj.build_readme(top_n=50, limit=50).strip()


def main() -> int:
    # Run the CLI in dry-run mode so failure is reported if README.md is stale.
    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "inject_readme.py"),
        "--dry-run",
        "--top-n",
        "50",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode not in (0, 1):
        sys.stderr.write(res.stderr)
        return res.returncode

    generated = _generate_readme()
    expected = FIXTURE.read_text().strip()

    if generated != expected:
        diff = difflib.unified_diff(
            expected.splitlines(True),
            generated.splitlines(True),
            fromfile=str(FIXTURE),
            tofile="generated",
        )
        print("Fixture drift detected:")
        for line in diff:
            print(line, end="")
        return 1
    return res.returncode


if __name__ == "__main__":
    sys.exit(main())
