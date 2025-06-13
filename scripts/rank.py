import datetime
import urllib.request
from pathlib import Path


def generate_badges(top_repo: str, date: str):
    badges_dir = Path('badges')
    badges_dir.mkdir(exist_ok=True)

    sync_url = f"https://img.shields.io/static/v1?label=sync&message={date}&color=blue"
    top_url = f"https://img.shields.io/static/v1?label=top&message={urllib.request.quote(top_repo)}&color=brightgreen"

    def fetch(url, path):
        try:
            with urllib.request.urlopen(url) as resp:
                path.write_bytes(resp.read())
        except Exception:
            # Fallback minimal SVG if network fetch fails
            path.write_text('<svg xmlns="http://www.w3.org/2000/svg"></svg>')

    fetch(sync_url, badges_dir / 'last_sync.svg')
    fetch(top_url, badges_dir / 'top_repo.svg')


def main():
    # Placeholder ranking logic. In real usage, this would compute repo rankings.
    top_repo = 'example/repo'
    today = datetime.date.today().isoformat()

    # Write a simple top50.md with the top repo
    Path('top50.md').write_text(f"# Top 50\n1. {top_repo}\n")

    generate_badges(top_repo, today)


if __name__ == '__main__':
    main()
