#!/usr/bin/env bash
# Run the pcjr_byte workbench selftest (ALL_PASS gates vs IRPING golden).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

exec python3 "$REPO_ROOT/refs/pcjr_byte.py" selftest
