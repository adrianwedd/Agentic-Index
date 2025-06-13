import json
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt


def load_snapshots(history_dir: Path):
    files = sorted(history_dir.glob('*.json'))
    dates = []
    snapshots = []
    for f in files:
        try:
            date = datetime.strptime(f.stem, '%Y-%m-%d')
        except ValueError:
            # skip files that don't match date pattern
            continue
        with f.open() as fh:
            try:
                snap = json.load(fh)
            except json.JSONDecodeError:
                snap = []
        dates.append(date)
        snapshots.append(snap)
    return dates, snapshots


def build_timeseries(dates, snapshots):
    if not snapshots:
        return {}, []
    latest = snapshots[-1]
    # assume list of dicts with keys 'name' and 'AgentOpsScore'
    scores_latest = {item.get('name'): item.get('AgentOpsScore') for item in latest if isinstance(item, dict)}
    top5 = sorted(scores_latest.items(), key=lambda x: x[1] if x[1] is not None else -1, reverse=True)[:5]
    repos = [name for name, _ in top5]
    series = {name: [] for name in repos}
    for snap in snapshots:
        mapping = {item.get('name'): item.get('AgentOpsScore') for item in snap if isinstance(item, dict)}
        for name in repos:
            series[name].append(mapping.get(name))
    return series, repos


def plot(series, dates, output: Path):
    if not series:
        print('No data to plot')
        return
    plt.figure(figsize=(8, 4))
    for name, scores in series.items():
        plt.plot(dates, scores, label=name)
    plt.xlabel('Date')
    plt.ylabel('AgentOpsScore')
    plt.legend()
    plt.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output)


def main():
    history_dir = Path('data/history')
    dates, snapshots = load_snapshots(history_dir)
    series, repos = build_timeseries(dates, snapshots)
    plot(series, dates, Path('docs/trends/top5_scores.png'))


if __name__ == '__main__':
    main()
