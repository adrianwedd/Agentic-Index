import sys
import xml.etree.ElementTree as ET

THRESHOLD = 49  # will auto-bump after next coverage uplift


def main(path: str = "coverage.xml") -> int:
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
