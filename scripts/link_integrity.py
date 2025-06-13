#!/usr/bin/env python3
"""Check README and docs for broken internal links and badges."""
from __future__ import annotations
import re
import sys
from pathlib import Path
from typing import Iterable

import requests


HEAD_RE = re.compile(r'^(#+)\s*(.+)$')
ANCHOR_RE = re.compile(r'\[[^\]]+\]\(#([^\)]+)\)')
IMG_RE = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')
HTML_IMG_RE = re.compile(r'<img\s+[^>]*src="([^"]+)"')


def slug(text: str) -> str:
    s = re.sub(r'[\s]+', '-', re.sub(r'[^\x00-\x7F]+', '', text))
    s = re.sub(r'[^a-zA-Z0-9\- ]', '', s)
    s = s.replace(' ', '-')
    return s.lower()


def extract_headings(lines: Iterable[str]) -> set[str]:
    anchors = set()
    for line in lines:
        m = HEAD_RE.match(line)
        if m:
            anchors.add(slug(m.group(2)))
    return anchors


def check_file(path: Path, headings: set[str], failures: list[str]) -> None:
    text = path.read_text(encoding='utf-8')
    for lineno, line in enumerate(text.splitlines(), 1):
        for anchor in ANCHOR_RE.findall(line):
            if anchor not in headings:
                failures.append(f'{path}:{lineno}: missing anchor {anchor}')
        for img in IMG_RE.findall(line) + HTML_IMG_RE.findall(line):
            if img.startswith('badges/'):
                if not Path(img).exists():
                    failures.append(f'{path}:{lineno}: missing badge {img}')
            if img.startswith('https://img.shields.io'):
                if not http_ok(img):
                    failures.append(f'{path}:{lineno}: badge url bad {img}')


def http_ok(url: str) -> bool:
    for _ in range(2):
        try:
            resp = requests.get(url, timeout=3)
            if resp.status_code == 200:
                return True
        except Exception:
            pass
    return False


def main(paths: Iterable[str] | None = None) -> int:
    if paths is None:
        paths = ["README.md"] + [str(p) for p in Path('docs').glob('*.md')]
    failures: list[str] = []
    for p in paths:
        path = Path(p)
        if not path.exists():
            continue
        text = path.read_text(encoding='utf-8').splitlines()
        headings = extract_headings(text)
        check_file(path, headings, failures)
    if failures:
        print('\n'.join(failures))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
