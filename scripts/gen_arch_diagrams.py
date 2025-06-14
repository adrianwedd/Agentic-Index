#!/usr/bin/env python
"""Generate architecture diagrams for Agentic Index using pydeps."""
import subprocess
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "architecture"
MODULES = ["agentic_index_cli"]

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

for mod in MODULES:
    out_file = OUTPUT_DIR / f"{mod}.svg"
    cmd = [
        "pydeps",
        mod,
        "-o",
        str(out_file),
        "--noshow",
        "--max-bacon=2",
        "--cluster",
    ]
    subprocess.run(cmd, check=True)
print(f"Generated diagrams under {OUTPUT_DIR}")
