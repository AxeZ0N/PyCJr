#!/usr/bin/env python3
"""Non-destructive migration + audit for the PyCJr living-repo layout.

Ownership: user-run. Default is a dry run. It never mutates refs/ content
or pyproject.toml. It creates directories, seeds facts.md and
sessions/README.md only when missing, and deletes superseded artifacts
only with --delete-superseded --yes.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SEED_FACTS = """# PyCJr — Facts Journal (append-only)

Rules:
- Append only. One fact per heading line.
- Updates append a new line with `supersedes:`; never edit old lines.
- Grep target:
  git grep -n -i -E -C2 "carrier_high_us|burst_us|gap2" -- facts.md sessions docs

## 2026-08-22 · carrier_high_us = 13 · empirical · pi_source_verified
Burst 62us; carrier 13us high / 12us low. Supersedes Rule 8 "12 high / 13 low".

## 2026-08-22 · ch0_clock = 2.38636 MHz · empirical
14.31818/6 = CPU/2. Slope: 1500us->3428, 10000us->23704, 20000us->47636.

## 2026-08-22 · poll_quant = 72ct = 30.17us · empirical
F000h polling budget ~1.85s.

## 2026-08-22 · gap2_1126 = stretched envelope H · empirical
1126 ct ~471us. NOT silence. NOT a 440us bit cell.

## 2026-08-22 · open_3840 resolved · empirical
38-vs-40 variance = arming window (for fl=1 to 100) swallowed frame 1 start burst.

## 2026-08-22 · envshape_anchor · empirical
ENVSHAPE clean: st=1 ed=38 in0=0 it=61440 nh19 nl18, kb intact. Added to anchors.

## 2026-08-22 · stage5_clean_anchor · empirical
STAGE5: st=1 edges=40 init=0 max_delta=3456 at_edge=20, kb intact. 38/40 variance closed.

## 2026-08-22 · ch0cal_anchor · empirical
CH0CAL: st=1 ed=38 in0=0 it=61440, kb intact. gap1: 3428/23704/47636.
"""

SUPERSEDED = [
    "docs/anchors_and_gates.md",
    "docs/tooling_reference.md",
    "bds/30_project/pcjrduino_project.md",
    "pcjrduino",  # directory, if present
]

def preflight() -> list[str]:
    problems = []
    ref = ROOT / "refs" / "deepseek_reference.txt"
    if not ref.exists():
        problems.append("refs/deepseek_reference.txt missing — MCP search_ref will not work.")
    return problems

def reconcile_max_delta() -> list[str]:
    hits = []
    roots = [ROOT / "facts.md", ROOT / "docs", ROOT / "bds", ROOT / "sessions"]
    for root in roots:
        if not root.exists():
            continue
        files = root.rglob("*") if root.is_dir() else [root]
        for f in files:
            if f.is_file() and f.suffix in {".md", ".txt"}:
                try:
                    text = f.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
                for i, line in enumerate(text.splitlines(), 1):
                    if "max_delta=3528" in line or "max_delta = 3528" in line:
                        hits.append(f"{f.relative_to(ROOT)}:{i}")
    return hits

def version_scan() -> list[str]:
    stale = []
    for p in (ROOT / "bds").rglob("*.md"):
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if ("System Prompt (v4)" in text or "Verified Skill (v4)" in text
                or "Workflow (v4)" in text or "Engineer (v4" in text):
            stale.append(str(p.relative_to(ROOT)))
    return stale

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="create directories and seed files (default is dry run)")
    ap.add_argument("--delete-superseded", action="store_true",
                    help="delete listed superseded artifacts")
    ap.add_argument("--yes", action="store_true", help="confirm deletion")
    a = ap.parse_args()

    report: list[str] = []

    report.append("== preflight ==")
    report.extend("WARN " + p for p in preflight())

    for d in ["sessions", "docs"]:
        t = ROOT / d
        if not t.exists():
            report.append(f"MISSING dir {t.relative_to(ROOT)} — {'create' if a.apply else 'would create'}")
            if a.apply:
                t.mkdir(parents=True, exist_ok=True)

    facts = ROOT / "facts.md"
    if not facts.exists():
        report.append(f"MISSING facts.md — {'seed' if a.apply else 'would seed'}")
        if a.apply:
            facts.write_text(SEED_FACTS, encoding="utf-8")

    sread = ROOT / "sessions" / "README.md"
    if (ROOT / "sessions").exists() and not sread.exists():
        report.append(f"MISSING sessions/README.md — {'seed' if a.apply else 'would seed'}")
        if a.apply:
            sread.write_text(
                "# Sessions\nOne file per scope: YYYY-MM-DD_scope.md. Append-only narrative.\n",
                encoding="utf-8",
            )

    report.append("== superseded ==")
    for rel in SUPERSEDED:
        p = ROOT / rel
        if p.exists():
            if a.delete_superseded and a.yes:
                if p.is_dir():
                    shutil.rmtree(p)
                else:
                    p.unlink()
                report.append(f"DELETED {rel}")
            else:
                report.append(f"PRESENT {rel} — delete with --delete-superseded --yes (or plain rm)")
        else:
            report.append(f"absent  {rel}")

    report.append("== audits ==")
    md = reconcile_max_delta()
    report.append(f"max_delta=3528 hits: {len(md)}")
    report.extend("  " + h for h in md)
    vs = version_scan()
    report.append(f"stale v4 version strings in bds/: {len(vs)}")
    report.extend("  " + h for h in vs)

    print("\n".join(report))
    if not a.apply:
        print("\nDRY RUN. Re-run with --apply to create/seed. "
              "Deletes need --delete-superseded --yes.")

if __name__ == "__main__":
    main()
