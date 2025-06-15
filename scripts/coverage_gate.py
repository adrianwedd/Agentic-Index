"""Fail CI if coverage falls below a set threshold."""

import sys
import xml.etree.ElementTree as ET

THRESHOLD = 80  # updated threshold for core logic tests


def main(path: str = "coverage.xml") -> int:
    """Return exit code ``1`` if coverage is below ``THRESHOLD``."""
    tree = ET.parse(path)
    rate = float(tree.getroot().attrib.get("line-rate", 0)) * 100
    percent = int(rate)
    print(f"Coverage {percent}% (threshold {THRESHOLD}%)")
    if percent < THRESHOLD:
        print("Coverage below threshold. Add tests or adjust THRESHOLD.")
        return 1
    if percent > THRESHOLD + 5 and THRESHOLD < 90:
        print("TODO: coverage increased; consider raising THRESHOLD")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "coverage.xml"))
