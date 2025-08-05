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
    xml = _write_xml(tmp_path, 0.73)
    assert main(str(xml)) == 1


def _copy_script(tmp_path: Path) -> Path:
    src = Path("scripts/coverage_gate.py")
    dest = tmp_path / "coverage_gate.py"
    dest.write_text(src.read_text())
    return dest


def test_high_coverage_instruction(tmp_path, capsys):
    xml = _write_xml(tmp_path, 0.87)
    script = _copy_script(tmp_path)
    assert main(str(xml), script_path=str(script)) == 0
    out = capsys.readouterr().out
    assert "run with --bump" in out
    assert "Bumped THRESHOLD" not in out
    assert "THRESHOLD = 74" in script.read_text()


def test_high_coverage_bump(tmp_path, capsys):
    xml = _write_xml(tmp_path, 0.87)
    script = _copy_script(tmp_path)
    assert main(str(xml), bump=True, script_path=str(script)) == 0
    out = capsys.readouterr().out
    assert "Bumped THRESHOLD to 85%" in out
    assert "THRESHOLD = 85" in script.read_text()
