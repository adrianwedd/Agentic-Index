from pathlib import Path


def test_methodology_length():
    path = Path('docs/METHODOLOGY.md')
    assert path.exists()
    words = path.read_text().split()
    assert len(words) >= 400
