#!/usr/bin/env bash
set -euo pipefail

# Wrapper script for devcontainer initialization
bash "$(dirname "$0")/agent-setup.sh"
