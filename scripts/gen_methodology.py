"""Generate docs/METHODOLOGY.md from rank.py and README.md."""

from pathlib import Path
import importlib.util
import textwrap


def load_rank_docstring():
    path = Path(__file__).parent / "rank.py"
    spec = importlib.util.spec_from_file_location("rank", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return textwrap.dedent(mod.__doc__ or "")


def extract_formula(readme_text: str) -> str:
    for line in readme_text.splitlines():
        if "Score =" in line:
            return line.strip()
    return ""


def main():
    doc = load_rank_docstring()
    readme_text = Path("README.md").read_text()
    formula = extract_formula(readme_text)

    content = ["# Methodology", ""]
    content.append(doc.strip())
    content.append("")
    if formula:
        content.append("## Scoring Formula")
        content.append("")
        content.append(formula)
        content.append("")
    output = "\n".join(content)
    Path("docs").mkdir(exist_ok=True)
    Path("docs/METHODOLOGY.md").write_text(output)


if __name__ == "__main__":
    main()
