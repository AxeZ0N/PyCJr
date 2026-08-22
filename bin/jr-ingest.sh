#!/usr/bin/env bash
# jr-ingest.sh — apply an assistant-emitted payload zip to the PyCJr
# living repo. Append + commit in one user-run step.
#
# Payload convention (zip contents):
#   COMMIT.txt                   one-line commit message (required)
#   facts.append.md              new fact headings; appended, deduped by heading
#   sessions/<file>.md           session narrative; appended, or created if new
#   docs/test_log.append.md      new run entries; appended
#
# Guarantees:
#   - Only paths in the allowlist are applied.
#   - No existing file is overwritten. facts/test_log append; session
#     files append-or-create.
#   - facts headings already present in facts.md are skipped with a warning.
#
# Usage:
#   jr-ingest.sh <payload.zip>
#   jr-ingest.sh --dry-run <payload.zip>
set -euo pipefail

usage() {
  echo "Usage: jr-ingest.sh [--dry-run] <payload.zip>" >&2
  exit 1
}

DRY=0
if [ "${1:-}" = "--dry-run" ]; then
  DRY=1
  shift
fi
[ "$#" -eq 1 ] || usage
PAYLOAD="$1"

command -v unzip >/dev/null 2>&1 || { echo "ERROR: unzip not found" >&2; exit 1; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

unzip -qo "$PAYLOAD" -d "$WORK"

# --- commit message ------------------------------------------------------
if [ ! -f "$WORK/COMMIT.txt" ]; then
  echo "ERROR: payload is missing COMMIT.txt" >&2
  exit 1
fi
MSG="$(tr -d '\r' < "$WORK/COMMIT.txt" | sed '/^[[:space:]]*$/d' | head -n 1)"
[ -n "$MSG" ] || { echo "ERROR: COMMIT.txt is empty" >&2; exit 1; }

APPLIED_FILES=()

reject_path() {
  case "$1" in
    /*) echo "ERROR: absolute path: $1" >&2; exit 1 ;;
    *..*) echo "ERROR: '..' in path: $1" >&2; exit 1 ;;
  esac
}

append_repo_file() {
  local rel="$1" target="$2"
  reject_path "$rel"
  if [ "$DRY" -eq 0 ]; then
    cat "$WORK/$rel" >> "$REPO_ROOT/$target"
    APPLIED_FILES+=("$target")
  fi
  echo "APPEND ${target}"
}

# --- facts ---------------------------------------------------------------
if [ -f "$WORK/facts.append.md" ]; then
  reject_path "facts.append.md"
  [ -f "$REPO_ROOT/facts.md" ] || { echo "ERROR: facts.md missing; run bin/migrate_repo.py first" >&2; exit 1; }

  existing="$(grep '^## ' "$REPO_ROOT/facts.md" 2>/dev/null | sed 's/^## //' | sed 's/[[:space:]]*$//' || true)"
  heading=""
  block=""
  added=0

  flush_fact_block() {
    if [ -z "$heading" ]; then
      return
    fi
    if grep -Fxq "$heading" <<< "$existing"; then
      echo "SKIP facts heading (already present): $heading"
    else
      if [ "$DRY" -eq 0 ]; then
        printf '%s' "$block" >> "$REPO_ROOT/facts.md"
        added=1
      fi
      echo "APPEND facts heading: $heading"
    fi
  }

  while IFS= read -r line || [ -n "$line" ]; do
    if [[ "$line" == "## "* ]]; then
      flush_fact_block
      heading="${line#'## '}"
      heading="$(sed 's/[[:space:]]*$//' <<< "$heading")"
      block=""
    fi
    block="${block}${line}"$'\n'
  done < "$WORK/facts.append.md"
  flush_fact_block

  if [ "$DRY" -eq 0 ] && [ "$added" -eq 1 ]; then
    APPLIED_FILES+=("facts.md")
  fi
fi

# --- test log ------------------------------------------------------------
if [ -f "$WORK/docs/test_log.append.md" ]; then
  append_repo_file "docs/test_log.append.md" "docs/test_log.md"
fi

# --- sessions ------------------------------------------------------------
for rel in "$WORK"/sessions/*.md; do
  [ -e "$rel" ] || continue
  f="${rel#"$WORK"/}"
  reject_path "$f"
  case "$f" in
    sessions/*.md) ;;
    *) echo "ERROR: not under sessions/: $f" >&2; exit 1 ;;
  esac
  if [ "$DRY" -eq 0 ]; then
    mkdir -p "$(dirname "$REPO_ROOT/$f")"
    cat "$rel" >> "$REPO_ROOT/$f"
    APPLIED_FILES+=("$f")
  fi
  echo "APPEND ${f}"
done

# --- commit --------------------------------------------------------------
if [ "$DRY" -eq 1 ]; then
  echo
  echo "DRY RUN — no changes written, no commit."
  exit 0
fi

if [ "${#APPLIED_FILES[@]}" -eq 0 ]; then
  echo "Nothing new to commit."
  exit 0
fi

cd "$REPO_ROOT"
git add -- "${APPLIED_FILES[@]}"
git commit -m "$MSG"
echo "committed: $MSG"
