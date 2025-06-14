from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel
import matplotlib.pyplot as plt
import json


class RepoScore(BaseModel):
    name: str
    score: float


class RenderRequest(BaseModel):
    repos: List[RepoScore]
    export_json: bool = False


app = FastAPI()


@app.post("/render")
def render(req: RenderRequest):
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # markdown table
    md_lines = ["| Repo | Score |", "|------|-------|"]
    for r in req.repos:
        md_lines.append(f"| {r.name} | {r.score} |")
    md = "\n".join(md_lines) + "\n"
    md_path = output_dir / "scores.md"
    md_path.write_text(md)

    # bar plot
    plot_path = output_dir / "scores.png"
    if req.repos:
        names = [r.name for r in req.repos]
        scores = [r.score for r in req.repos]
        plt.figure()
        plt.bar(names, scores)
        plt.ylabel("Score")
        plt.tight_layout()
        plt.savefig(plot_path)
        plt.close()
    else:
        plot_path.write_text("")

    json_file: Optional[Path] = None
    if req.export_json:
        json_file = output_dir / "scores.json"
        with json_file.open("w", encoding="utf-8") as fh:
            json.dump([r.dict() for r in req.repos], fh)

    return {
        "markdown_file": str(md_path),
        "plot_file": str(plot_path),
        "json_file": str(json_file) if json_file else None,
        "markdown": md,
    }

