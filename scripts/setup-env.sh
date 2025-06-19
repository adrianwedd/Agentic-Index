#!/usr/bin/env bash
set -euo pipefail

# Wrapper script for devcontainer initialization
bash "$(dirname "${BASH_SOURCE[0]}")/agent-setup.sh"

# Ensure the script is sourced so exports persist
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  echo "Please source this script: source scripts/setup-env.sh"
  exit 1
fi

PY_VER=$(python3 -c 'import sys; print("{}.{}.{}".format(*sys.version_info[:3]))')
if ! python3 - <<'PY'
import sys

raise SystemExit(0 if sys.version_info >= (3,11) else 1)
PY
then
  echo "Python 3.11 or newer required. Found $PY_VER"
  return 1
fi

MISSING=()
for pkg in libffi-dev libssl-dev; do
  if ! dpkg -s "$pkg" >/dev/null 2>&1; then
    MISSING+=("$pkg")
  fi
done
if (( ${#MISSING[@]} )); then
  echo "Installing system packages: ${MISSING[*]}"
  sudo apt-get update
  sudo apt-get install -y "${MISSING[@]}"
fi

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
pip install black isort flake8 mypy bandit pre-commit
pre-commit install --install-hooks

export PYTHONPATH="$PWD"

# Enable offline mode for tests by default
: "${CI_OFFLINE:=1}"
export CI_OFFLINE

if [[ -f .env ]]; then
  echo "Loading environment variables from .env"
  set -o allexport
  source .env
  set +o allexport
fi

REQUIRED_VARS=(GITHUB_TOKEN_REPO_STATS API_KEY)
MISSING=()
for var in "${REQUIRED_VARS[@]}"; do
  if [[ -z "${!var:-}" ]]; then
    MISSING+=("$var")
  fi
done
if (( ${#MISSING[@]} )); then
  echo "Warning: missing variables ${MISSING[*]}." >&2
fi

python - <<'PY'
import sys

try:
    import agentic_index_cli
except Exception as e:
    sys.exit(f"Sanity check failed: {e}")
PY

echo "Environment setup complete."
