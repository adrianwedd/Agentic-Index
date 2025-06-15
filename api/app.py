from fastapi import FastAPI, Body
from typing import List, Optional, Dict, Any
from pathlib import Path
import json
import matplotlib.pyplot as plt
from pydantic import BaseModel

from .sync import sync


class RepoScore(BaseModel):
    name: str
    score: float


class RenderRequest(BaseModel):
    repos: List[RepoScore]
    export_json: bool = False

app = FastAPI()


@app.post("/sync")
def sync_endpoint(body: Dict[str, Any] = Body(default={})):  # type: ignore[dict-item]
    org: Optional[str] = body.get("org")
    topics: Optional[List[str]] = body.get("topics")
    repos = sync(org=org, topics=topics)
    return {"synced": len(repos)}


@app.post("/render")
def render_endpoint(req: RenderRequest):
    """Render markdown and plot from repo scores."""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    md_lines = ["| Repo | Score |", "|------|-------|"]
    for r in req.repos:
        md_lines.append(f"| {r.name} | {r.score} |")
    markdown = "\n".join(md_lines) + "\n"
    md_path = output_dir / "scores.md"
    md_path.write_text(markdown)

    plot_path = output_dir / "scores.png"
    if req.repos:
        plt.figure()
        plt.bar([r.name for r in req.repos], [r.score for r in req.repos])
        plt.ylabel("Score")
        plt.tight_layout()
        plt.savefig(plot_path)
        plt.close()
    else:
        plot_path.write_text("")

    json_file: Optional[Path] = None
    if req.export_json:
        json_file = output_dir / "scores.json"
        json_file.write_text(json.dumps([r.dict() for r in req.repos]))

    return {
        "markdown_file": str(md_path),
        "plot_file": str(plot_path),
        "json_file": str(json_file) if json_file else None,
        "markdown": markdown,
    }
