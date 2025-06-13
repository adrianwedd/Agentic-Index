import sys
from pathlib import Path

# ensure project root is on the path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from agentic_index_cli import helpers


def test_add():
    assert helpers.add(2, 3) == 5
