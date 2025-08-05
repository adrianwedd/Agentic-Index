"""Fail CI if coverage falls below a set threshold."""

import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

THRESHOLD = 74  # updated threshold to match current coverage level


def _update_threshold(new_value: int, file_path: str) -> None:
    """Replace ``THRESHOLD`` assignment in ``file_path`` with ``new_value``."""
    path = Path(file_path)
    text = path.read_text()
    pattern = r"^(THRESHOLD\s*=\s*)\d+"
    new_text, count = re.subn(pattern, rf"\g<1>{new_value}", text, flags=re.M)
    if count != 1:
        raise ValueError("THRESHOLD constant not found")
    path.write_text(new_text)


def main(
    path: str = "coverage.xml", *, bump: bool = False, script_path: str | None = None
) -> int:
    """Return exit code ``1`` if coverage is below ``THRESHOLD``."""
    tree = ET.parse(path)
    rate = float(tree.getroot().attrib.get("line-rate", 0)) * 100
    percent = int(rate)
    print(f"Coverage {percent}% (threshold {THRESHOLD}%)")
    if percent < THRESHOLD:
        print("Coverage below threshold. Add tests or adjust THRESHOLD.")
        return 1
    if percent > THRESHOLD + 5 and THRESHOLD < 90:
        new_threshold = min(90, (percent // 5) * 5)
        if bump or os.getenv("BUMP_THRESHOLD"):
            target = script_path or __file__
            _update_threshold(new_threshold, target)
            print(f"Bumped THRESHOLD to {new_threshold}%")
        else:
            print(
                f"Coverage increased; run with --bump to raise THRESHOLD to {new_threshold}%"
            )
    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default="coverage.xml")
    parser.add_argument("--bump", action="store_true")
    args = parser.parse_args()
    sys.exit(main(args.path, bump=args.bump))
