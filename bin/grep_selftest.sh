#!/usr/bin/env bash
# grep_selftest.sh — smoke test the read-only repo grep engine.
set -euo pipefail

python3 refs/pcjr_repo_grep.py roots
python3 refs/pcjr_repo_grep.py stats
python3 refs/pcjr_repo_grep.py grep "carrier_high_us|gap2" --context 2
echo "grep_selftest OK"
