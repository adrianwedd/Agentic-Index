#!/usr/bin/env python3
"""Fail CI if forbidden patterns appear in tracked files.

Patterns to block/allow are configured in `.regression.yml`:
  forbidden: list of substrings
  allowed_regex: list of regex patterns that override a match
"""
from __future__ import annotations
import re
import subprocess
import sys
from pathlib import Path
import yaml

CONFIG_PATH = Path('.regression.yml')


def load_config(path: Path = CONFIG_PATH) -> dict:
    if not path.exists():
        return {"forbidden": [], "allowed_regex": []}
    with open(path, 'r', encoding='utf-8') as f:
        cfg = yaml.safe_load(f) or {}
    cfg.setdefault('forbidden', [])
    cfg.setdefault('allowed_regex', [])
    return cfg


def gather_files() -> list[Path]:
    out = subprocess.check_output(['git', 'ls-files'], text=True)
    return [Path(p) for p in out.splitlines() if p]


def check_files(paths: list[Path], config: dict) -> list[str]:
    allowed = [re.compile(p) for p in config.get('allowed_regex', [])]
    forbidden = config.get('forbidden', [])
    failures = []
    for p in paths:
        try:
            text = p.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for pat in forbidden:
                if pat in line:
                    if any(r.search(line) for r in allowed):
                        break
                    failures.append(f'{p}:{lineno}: {pat}')
                    break
    return failures


def main(paths: list[str] | None = None) -> int:
    cfg = load_config()
    files = [Path(p) for p in paths] if paths else gather_files()
    fails = check_files(files, cfg)
    if fails:
        print('Forbidden patterns found:')
        for f in fails:
            print(f)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
