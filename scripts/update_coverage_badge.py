#!/usr/bin/env python3
"""Update coverage badge in README from coverage.xml."""
from __future__ import annotations

import argparse
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from agentic_index_cli.helpers.markdown import render_badge

BADGE_RE = re.compile(
    r"!?\[coverage\]\(https://img\.shields\.io/badge/coverage-\d+%25-[a-zA-Z]+\)"
)


def fetch_badge(url: str, dest: Path) -> None:
    """Download an SVG badge or create a local placeholder when offline."""
    if os.getenv("CI_OFFLINE") == "1":
        if dest.exists():
            return
        dest.write_bytes(b'<svg xmlns="http://www.w3.org/2000/svg"></svg>')
        return
    try:
        import urllib.request

        resp = urllib.request.urlopen(url)
        try:
            content = resp.read().rstrip(b"\n")
            dest.write_bytes(content)
        finally:
            if hasattr(resp, "close"):
                resp.close()
    except Exception:
        if dest.exists():
            return
        dest.write_bytes(b'<svg xmlns="http://www.w3.org/2000/svg"></svg>')


def _coverage_percent(path: Path) -> int:
    tree = ET.parse(path)
    rate = float(tree.getroot().attrib.get("line-rate", 0)) * 100
    return int(rate)


def _badge_url(percent: int) -> str:
    if percent >= 90:
        color = "brightgreen"
    elif percent >= 80:
        color = "brightgreen"
    elif percent >= 70:
        color = "yellow"
    elif percent >= 60:
        color = "orange"
    else:
        color = "red"
    return f"https://img.shields.io/badge/coverage-{percent}%25-{color}"


def build_readme(readme_path: Path, percent: int) -> str:
    """Return README text with an updated coverage badge."""
    text = readme_path.read_text(encoding="utf-8")
    url = _badge_url(percent)
    # Normalize to image syntax in case the badge was a regular link
    new_text = BADGE_RE.sub(render_badge("coverage", url), text)
    return new_text


def main(
    readme: str = "README.md",
    xml: str = "coverage.xml",
    *,
    check: bool = False,
    write: bool = True,
) -> int:
    readme_path = Path(readme)
    xml_path = Path(xml)
    percent = _coverage_percent(xml_path)
    new_text = build_readme(readme_path, percent)
    if check:
        if new_text != readme_path.read_text(encoding="utf-8"):
            print("Coverage badge out of date", file=sys.stderr)
            return 1
        return 0
    if write and new_text != readme_path.read_text(encoding="utf-8"):
        readme_path.write_text(new_text, encoding="utf-8")
        fetch_badge(_badge_url(percent), Path("badges") / "coverage.svg")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update coverage badge in README")
    parser.add_argument("--check", action="store_true", help="Fail if badge stale")
    parser.add_argument("--write", action="store_true", help="Write README")
    parser.add_argument("xml", nargs="?", default="coverage.xml")
    parser.add_argument("readme", nargs="?", default="README.md")
    args = parser.parse_args()
    if not args.write:
        args.write = not args.check
    sys.exit(main(args.readme, args.xml, check=args.check, write=args.write))
