import sys
from pathlib import Path
import pytest

# ensure project root is on the path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from agentic_index_cli.helpers.markdown import render_badge


def test_render_badge_valid():
    text = render_badge('build', 'badges/build.svg')
    assert text == '![build](badges/build.svg)'


def test_render_badge_invalid():
    with pytest.raises(ValueError):
        render_badge('', 'foo')
    with pytest.raises(ValueError):
        render_badge('build', '')

