#!/usr/bin/env bash
set -euo pipefail

# Simple end-to-end smoke test using fixture data
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

ARTIFACTS=$(mktemp -d e2e_demo_XXXX)
DATA_DIR="$ARTIFACTS/data"
mkdir -p "$DATA_DIR/by_category"

# Seed with fixture repos
cp tests/fixtures/data/repos.json "$DATA_DIR/repos.json"
printf '[]' > "$DATA_DIR/last_snapshot.json"
touch "$DATA_DIR/top100.md"
printf '{}' > "$DATA_DIR/by_category/index.json"

export PYTHONPATH="$ROOT"

python -m agentic_index_cli.enricher "$DATA_DIR/repos.json"
python -m agentic_index_cli.internal.rank_main "$DATA_DIR/repos.json"
python -m agentic_index_cli.internal.inject_readme \
  --force --top-n 5 --limit 5 \
  --repos "$DATA_DIR/repos.json" \
  --data "$DATA_DIR/top100.md" \
  --snapshot "$DATA_DIR/last_snapshot.json" \
  --index "$DATA_DIR/by_category/index.json" \
  --readme "$ARTIFACTS/README.md"

echo "E2E test complete. Artifacts in $ARTIFACTS"
