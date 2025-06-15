from pathlib import Path

from scripts.coverage_gate import main


def _write_xml(tmp_path: Path, rate: float) -> Path:
    p = tmp_path / "coverage.xml"
    p.write_text(f'<coverage line-rate="{rate}"></coverage>')
    return p


def test_gate_pass(tmp_path):
    xml = _write_xml(tmp_path, 0.81)
    assert main(str(xml)) == 0


def test_gate_fail(tmp_path):
    xml = _write_xml(tmp_path, 0.79)
    assert main(str(xml)) == 1
