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
    python3 refs/pcjr_repo_grep.py read sessions/2026-08-24_agc_profile_probe.md
    python3 refs/pcjr_repo_grep.py read facts.md --max-lines 500

MCP: register tool `grep_repo` with
     dispatch(mode, query, context, literal, path, max_lines).
"""
from __future__ import annotations

import argparse
import difflib
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
        for k, ln in enumerate(r["before"], start=r["line_no"] - len(r["before"])):
            out.append(f"{r['file']}:{k}:  {ln}")
        out.append(f"{r['file']}:{r['line_no']}:> {r['line']}")
        for k, ln in enumerate(r["after"], start=r["line_no"] + 1):
            out.append(f"{r['file']}:{k}:  {ln}")
        out.append("---")
    return "\n".join(out)


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _suggest(path: str) -> list[str]:
    try:
        candidates = [
            str(f.relative_to(repo_root()))
            for f in iter_text_files(roots())
        ]
        return difflib.get_close_matches(path, candidates, n=3, cutoff=0.4)
    except Exception:
        return []


def _guard_read_path(path) -> tuple[Path | None, str | None]:
    """Validate a root-relative path for the read mode.

    Returns (resolved_target, error_string). Exactly one is None.
    Rejects: absolute paths, `..`, foreign roots, symlink escapes,
    non-files, and non-text suffixes.
    """
    if not isinstance(path, str) or not path.strip():
        return None, "ERROR: read requires a non-empty root-relative 'path'"

    p = Path(path)
    if p.is_absolute():
        return None, f"ERROR: absolute path refused: {path!r}"
    if ".." in p.parts:
        return None, f"ERROR: path traversal refused: {path!r}"

    if not p.parts or p.parts[0] not in ROOT_NAMES:
        return None, (
            f"ERROR: path must start with one of {ROOT_NAMES}; got {path!r}"
        )

    root = repo_root().resolve()
    try:
        candidate = (root / p).resolve(strict=False)
    except OSError as exc:
        return None, f"ERROR: cannot resolve {path!r}: {exc}"

    if not _is_within(candidate, root):
        return None, (
            f"ERROR: path resolves outside repo root (symlink?): {path!r}"
        )

    if not candidate.is_file():
        suggestions = _suggest(path)
        msg = f"ERROR: not a file under repo root: {path!r}"
        if suggestions:
            msg += " | did you mean: " + ", ".join(suggestions)
        return None, msg

    if candidate.suffix.lower() not in TEXT_SUFFIXES:
        return None, (
            f"ERROR: unsupported suffix {candidate.suffix!r}; "
            f"allowed: {sorted(TEXT_SUFFIXES)}"
        )

    return candidate, None


def _read_file(path, max_lines: int = 2000) -> dict:
    target, err = _guard_read_path(path)
    if err:
        return {"error": err}

    try:
        raw = target.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return {"error": f"cannot read {path!r}: {exc}"}

    all_lines = raw.splitlines()
    total = len(all_lines)

    try:
        max_lines = int(max_lines)
    except (TypeError, ValueError):
        return {"error": "max_lines must be an integer"}

    if max_lines is None or max_lines < 0:
        shown = all_lines
    else:
        shown = all_lines[:max_lines]

    return {
        "path": str(target.relative_to(repo_root())),
        "lines": len(shown),
        "text": "\n".join(f"{i}\t{line}" for i, line in enumerate(shown, 1)),
        "truncated": len(shown) < total,
        "total_lines": total,
    }


def dispatch(
    mode: str,
    query=None,
    context: int = 2,
    literal: bool = False,
    path=None,
    max_lines: int = 2000,
) -> dict:
    """MCP-facing dispatcher for tool `grep_repo`."""
    paths = roots()
    if mode == "query":
        if not query:
            return {"error": "grep_repo query requires 'query'"}
        records, err = _match_records(query, int(context), bool(literal), paths)
        if err:
            return {"error": err}
        return {"matches": len(records), "text": format_records(records)}
    if mode == "read":
        if not path:
            return {"error": "grep_repo read requires 'path'"}
        return _read_file(path, max_lines)
    if mode == "stats":
        return stats(paths)
    if mode == "roots":
        return {
            "roots": [str(p.relative_to(repo_root())) for p in paths],
            "existing": [p.exists() for p in paths],
        }
    return {"error": f"unknown mode {mode!r}; use query|read|stats|roots"}


TOOL_SCHEMA = {
    "type": "object",
    "properties": {
        "mode": {"type": "string"},
        "query": {"anyOf": [{"type": "string"}, {"type": "null"}], "default": None},
        "context": {"type": "integer", "default": 2},
        "literal": {"type": "boolean", "default": False},
        "path": {"anyOf": [{"type": "string"}, {"type": "null"}], "default": None},
        "max_lines": {"type": "integer", "default": 2000},
    },
    "required": ["mode"],
}


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Read-only repo grep/read (facts.md, sessions/, docs/)."
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("grep", help="search")
    g.add_argument("query")
    g.add_argument("--context", type=int, default=2)
    g.add_argument("--literal", action="store_true")

    r = sub.add_parser("read", help="read a full file, safety-guarded")
    r.add_argument("path")
    r.add_argument("--max-lines", type=int, default=2000)

    sub.add_parser("roots")
    sub.add_parser("stats")

    a = ap.parse_args()

    if a.cmd == "grep":
        records, err = _match_records(a.query, a.context, a.literal, roots())
        if err:
            print(err)
            raise SystemExit(2)
        print(format_records(records))
    elif a.cmd == "read":
        result = dispatch("read", path=a.path, max_lines=a.max_lines)
        if "error" in result:
            print(result["error"])
            raise SystemExit(2)
        if result.get("truncated"):
            print(
                f"# truncated: showing {result['lines']}/{result['total_lines']} lines",
                file=__import__("sys").stderr,
            )
        print(result["text"])
    elif a.cmd == "roots":
        for p in roots():
            print(p.relative_to(repo_root()))
    elif a.cmd == "stats":
        print(json.dumps(stats(roots()), indent=2))


if __name__ == "__main__":
    main()
