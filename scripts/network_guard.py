from __future__ import annotations
import re
import sys
from pathlib import Path

ALLOW_PATH = Path('.network-allowlist')

def load_allowlist() -> set[str]:
    if not ALLOW_PATH.exists():
        return set()
    return {l.strip() for l in ALLOW_PATH.read_text().splitlines() if l.strip()}

DOMAIN_RE = re.compile(r"domain=['\"]?([\w.-]+)")


def parse_domains(text: str) -> set[str]:
    domains = set()
    for line in text.splitlines():
        m = DOMAIN_RE.search(line)
        if m:
            domains.add(m.group(1))
    return domains


def main(log_file: str) -> int:
    text = Path(log_file).read_text(encoding='utf-8', errors='ignore')
    seen = parse_domains(text)
    allowed = load_allowlist()
    bad = [d for d in seen if d not in allowed]
    if bad:
        print('Unexpected network domains:', ', '.join(sorted(bad)))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
