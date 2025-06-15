"""Verify README table matches ``data/top100.md``."""

import sys
from pathlib import Path

README = Path('README.md')
TOP = Path('data/top100.md')
START = '<!-- TOP50:START -->'
END = '<!-- TOP50:END -->'


def main() -> int:
    """Return exit code ``1`` if README table is out of sync."""
    readme = README.read_text(encoding='utf-8')
    try:
        s = readme.index(START) + len(START)
        e = readme.index(END, s)
    except ValueError:
        print('Markers not found', file=sys.stderr)
        return 1
    table = readme[s:e].strip()
    top = TOP.read_text(encoding='utf-8').strip()
    if table != top:
        print('README table out of sync', file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())

