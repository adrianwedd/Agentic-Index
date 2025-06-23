#!/usr/bin/env bash
set -euo pipefail

# Simple end-to-end smoke test using fixture data
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

ARTIFACTS=$(mktemp -d e2e_demo_XXXX)
DATA_DIR="$ARTIFACTS/data"
mkdir -p "$DATA_DIR/by_category"

# Seed with fixture repos and README
cp tests/fixtures/data/repos.json "$DATA_DIR/repos.json"
printf '[]' > "$DATA_DIR/last_snapshot.json"
cp tests/snapshots/README.md "$ARTIFACTS/README.md"
touch "$DATA_DIR/top100.md"
printf '{}' > "$DATA_DIR/by_category/index.json"

export PYTHONPATH="$ROOT"

python -m agentic_index_cli.enricher "$DATA_DIR/repos.json"
python -m agentic_index_cli.internal.rank_main "$DATA_DIR/repos.json"
python - "$DATA_DIR" "$ARTIFACTS/README.md" <<'EOF'
import sys
from pathlib import Path
import agentic_index_cli.internal.readme_utils as ru
from agentic_index_cli.internal.inject_readme import build_readme

data_dir = Path(sys.argv[1])
readme_path = Path(sys.argv[2])

ru.DATA_PATH = data_dir / "top100.md"
ru.REPOS_PATH = data_dir / "repos.json"
ru.RANKED_PATH = data_dir / "ranked.json"
ru.SNAPSHOT = data_dir / "last_snapshot.json"
ru.BY_CAT_INDEX = data_dir / "by_category/index.json"

text = build_readme(
    limit=5,
    top_n=50,
    readme_path=readme_path,
    repos_path=ru.REPOS_PATH,
    ranked_path=ru.RANKED_PATH,
    index_path=ru.BY_CAT_INDEX,
)
readme_path.write_text(text, encoding="utf-8")
EOF

echo "E2E test complete. Artifacts in $ARTIFACTS"
