#!/usr/bin/env python3
"""Read-only repo grep for the PyCJr living repo.

Posture: the machine analogue of paste-first `git grep`. No git binary,
no subprocess, fixed roots, loopback-bind safe.

Roots (relative to repo root, which is this file's parent's parent):
    facts.md, sessions/, docs/

CLI:
    python3 refs/pcjr_repo_grep.py grep "carrier_high_us|burst_us" --context 2
    python3 refs/pcjr_repo_grep.py roots
    python3 refs/pcjr_repo_grep.py stats

MCP: register tool `grep_repo` with dispatch(mode, query, context, literal).
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT_NAMES = ["facts.md", "sessions", "docs"]
TEXT_SUFFIXES = {".md", ".txt", ".csv"}

def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent

def roots() -> list[Path]:
    r = repo_root()
    return [r / name for name in ROOT_NAMES if (r / name).exists()]

def iter_text_files(paths: list[Path]):
    for p in paths:
        if p.is_file():
            if p.suffix.lower() in TEXT_SUFFIXES:
                yield p
        elif p.is_dir():
            for child in sorted(p.rglob("*")):
                if child.is_file() and child.suffix.lower() in TEXT_SUFFIXES:
                    yield child

def _match_records(query: str, context: int, literal: bool, paths: list[Path]):
    pat = re.escape(query) if literal else query
    try:
        rx = re.compile(pat, re.IGNORECASE)
    except re.error as e:
        return None, f"Bad regex: {e}"

    records = []
    for f in iter_text_files(paths):
        try:
            lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError as e:
            records.append({"file": str(f.relative_to(repo_root())), "error": str(e)})
            continue
        for i, line in enumerate(lines, 1):
            if rx.search(line):
                lo = max(0, i - 1 - context)
                hi = min(len(lines), i + context)
                records.append({
                    "file": str(f.relative_to(repo_root())),
                    "line_no": i,
                    "line": line,
                    "before": lines[lo:i - 1],
                    "after": lines[i:hi],
                })
    return records, None

def stats(paths: list[Path]) -> dict:
    n_files = 0
    n_lines = 0
    per_root = {}
    for p in paths:
        files = list(iter_text_files([p]))
        per_root[p.name] = {"files": len(files)}
        for f in files:
            n_files += 1
            try:
                n_lines += sum(1 for _ in f.open(encoding="utf-8", errors="replace"))
            except OSError:
                pass
    return {
        "roots": [p.name for p in paths],
        "files": n_files,
        "lines": n_lines,
        "detail": per_root,
    }

def format_records(records) -> str:
    if not records:
        return "No matches."
    out = []
    for r in records:
        if "error" in r:
            out.append(f"{r['file']}: ERROR {r['error']}")
            continue
        # before lines are the (context) lines immediately preceding the
        # match; their 1-based numbers start at match_line - len(before).
        for k, ln in enumerate(r["before"], start=r["line_no"] - len(r["before"])):
            out.append(f"{r['file']}:{k}:  {ln}")
        out.append(f"{r['file']}:{r['line_no']}:> {r['line']}")
        # after lines start at match_line + 1.
        for k, ln in enumerate(r["after"], start=r["line_no"] + 1):
            out.append(f"{r['file']}:{k}:  {ln}")
        out.append("---")
    return "\n".join(out)

def dispatch(mode: str, query=None, context: int = 2, literal: bool = False) -> dict:
    """MCP-facing dispatcher for tool `grep_repo`."""
    paths = roots()
    if mode == "query":
        if not query:
            return {"error": "grep_repo query requires 'query'"}
        records, err = _match_records(query, int(context), bool(literal), paths)
        if err:
            return {"error": err}
        return {"matches": len(records), "text": format_records(records)}
    if mode == "stats":
        return stats(paths)
    if mode == "roots":
        return {
            "roots": [str(p.relative_to(repo_root())) for p in paths],
            "existing": [p.exists() for p in paths],
        }
    return {"error": f"unknown mode {mode!r}; use query|stats|roots"}

TOOL_SCHEMA = {
    "type": "object",
    "properties": {
        "mode": {"type": "string"},
        "query": {"anyOf": [{"type": "string"}, {"type": "null"}], "default": None},
        "context": {"type": "integer", "default": 2},
        "literal": {"type": "boolean", "default": False},
    },
    "required": ["mode"],
}

def main() -> None:
    ap = argparse.ArgumentParser(description="Read-only repo grep (facts.md, sessions/, docs/).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("grep", help="search")
    g.add_argument("query")
    g.add_argument("--context", type=int, default=2)
    g.add_argument("--literal", action="store_true")
    sub.add_parser("roots")
    sub.add_parser("stats")
    a = ap.parse_args()

    if a.cmd == "grep":
        records, err = _match_records(a.query, a.context, a.literal, roots())
        if err:
            print(err)
            raise SystemExit(2)
        print(format_records(records))
    elif a.cmd == "roots":
        for p in roots():
            print(p.relative_to(repo_root()))
    elif a.cmd == "stats":
        print(json.dumps(stats(roots()), indent=2))

if __name__ == "__main__":
    main()
