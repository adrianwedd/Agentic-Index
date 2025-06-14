"""Fail CI if forbidden patterns appear in tracked files.

Patterns to block/allow are configured in ``.regression.yml`` and an optional
allowlist file. ``.regression.yml`` contains:

``forbidden`` - list of substrings to search for
``allowed_regex`` - regex patterns that override a match

``regression_allowlist.yml`` provides regexes for lines that should be ignored
entirely.
"""
from __future__ import annotations
import re
import subprocess
import sys
from pathlib import Path
import argparse
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


DEFAULT_GLOBS = [
    'agentic_index_cli/**/*.py',
    'scripts/**/*.py',
    'tests/**/*.py',
    'docs/**/*.md',
    'README.md',
]

ALLOWLIST_PATH = Path('regression_allowlist.yml')


def load_allowlist(path: Path = ALLOWLIST_PATH) -> list[str]:
    if not path.exists():
        return []
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}
    return data.get('allow', [])


def gather_files(globs: list[str] | None = None) -> list[Path]:
    globs = globs or DEFAULT_GLOBS
    files: list[Path] = []
    for g in globs:
        out = subprocess.check_output(['git', 'ls-files', g], text=True)
        files.extend(Path(p) for p in out.splitlines() if p)
    # deduplicate while preserving order
    seen = set()
    unique = []
    for f in files:
        if f not in seen:
            seen.add(f)
            unique.append(f)
    return [p for p in unique if p != CONFIG_PATH]


def check_files(paths: list[Path], config: dict) -> list[str]:
    allowed = [re.compile(p) for p in config.get('allowed_regex', [])]
    allowlist = [re.compile(p) for p in config.get('allowlist', [])]
    forbidden = config.get('forbidden', [])
    failures = []
    for p in paths:
        if p.resolve() == CONFIG_PATH.resolve():
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if any(r.search(line) for r in allowlist):
                continue
            for pat in forbidden:
                if pat in line:
                    if any(r.search(line) for r in allowed):
                        break
                    failures.append(f'{p}:{lineno}: {pat}')
                    break
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--allowlist', type=Path, default=ALLOWLIST_PATH,
                        help='YAML file containing allowed regex patterns')
    parser.add_argument('--add-allow', action='append', default=[],
                        dest='add_allow', help='Additional allowed regex')
    parser.add_argument('paths', nargs='*', help='Files to check')
    args = parser.parse_args(argv)

    cfg = load_config()
    cfg['allowlist'] = load_allowlist(args.allowlist)
    cfg['allowed_regex'].extend(args.add_allow)

    files = [Path(p) for p in args.paths] if args.paths else gather_files()
    fails = check_files(files, cfg)
    if fails:
        print('Forbidden patterns found:')
        for f in fails:
            print(f)
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
