#!/usr/bin/env python3
"""
PCjr Technical Reference utility (triage-fixed v3).

Operates on the digital-born .txt strip whose pages are marked as:

    <page number='N'>

Commands:
  stats [--verbose]            Entry count, coverage, and detected headings.
  query TERM [...]             Print content entries matching TERM (front matter skipped).
  peek N [M]                   Print entry N (or range N..M) by file position.
  split [--out DIR]            Best-effort split into per-section markdown files.
  index                        Print section -> first entry index mapping.

Examples:
  python pcjr_ref_util.py pcjr_techref.txt stats --verbose
  python pcjr_ref_util.py pcjr_techref.txt query "8255 bit assignments" --context 3 --max-pages 2
  python pcjr_ref_util.py pcjr_techref.txt peek 341
  python pcjr_ref_util.py pcjr_techref.txt peek 341 350
  python pcjr_ref_util.py pcjr_techref.txt split --out references
"""
import argparse
import re
import sys
from pathlib import Path

PAGE_RE = re.compile(r"^\s*<page number='(\d+)'>\s*$", re.IGNORECASE)

# TOC entry: dot leaders (dots may be separated by spaces) followed by a
# manual page number like "2-30" at the end of the line.
TOC_LINE_RE = re.compile(r"(?:\.\s*){3,}\s*\d{1,3}\s*-\s*\d{1,3}\s*$")

# Section headings from the manual TOC. Multi-word patterns only; single
# common words caused false positives in body text.
SECTIONS = [
    ("intro", "Introduction", [r"section\s+1\s+introduction"]),
    ("processor_8259", "Processor and 8259A",
     [r"processor\s+and\s+support", r"8259a\s+interrupt\s+controller"]),
    ("ram_rom", "64KB RAM and ROM", [r"64k\s?b?\s?ram", r"rom\s+subsystem"]),
    ("io_channel", "I/O Channel",
     [r"input\s*/\s*output\s+channel", r"system\s+board\s+i\s*/\s*o\s+channel"]),
    ("io_8255", "8255 Bit Assignments", [r"8255\s+bit\s+assignments"]),
    ("cassette", "Cassette Interface", [r"cassette\s+interface"]),
    ("video", "Video Subsystem",
     [r"video\s+color\s+graphics", r"video\s+subsystem", r"video\s+gate\s+array"]),
    ("sound", "Sound Subsystem",
     [r"sound\s+subsystem", r"complex\s+sound\s+generator", r"audio\s+tone\s+generator"]),
    ("ir_link", "Infra-Red Link", [r"infra[- ]?red\s+link", r"infra[- ]?red\s+receiver"]),
    ("keyboard", "Cordless Keyboard", [r"cordless\s+keyboard"]),
    ("cartridge", "Program Cartridge",
     [r"program\s+cartridge", r"cartridge\s+storage", r"rom\s+module"]),
    ("games", "Games Interface", [r"games\s+interface"]),
    ("serial", "Serial Port", [r"serial\s+port", r"rs232"]),
    ("power", "Power Supply", [r"system\s+power\s+supply"]),
    ("section3", "System Options", [r"section\s+3\s+system\s+options"]),
    ("section4", "Compatibility", [r"section\s+4\s+compatibility"]),
    ("section5", "System BIOS Usage", [r"section\s+5\s+system\s+bios"]),
    ("appendix_a", "ROM BIOS Listing",
     [r"appendix\s+a\b", r"rom\s+bios\s+listing",
      r"equates\s+and\s+data\s+areas",
      r"power[- ]on\s+self[- ]?test",
      r"boot\s+strap\s+loader"]),
    ("appendix_b", "Logic Diagrams", [r"appendix\s+b\b", r"logic\s+diagrams"]),
    ("appendix_c", "Characters Keystrokes Color",
     [r"appendix\s+c\b", r"characters,\s*keystrokes"]),
    ("appendix_d", "Unit Specifications", [r"appendix\s+d\b", r"unit\s+specifications"]),
]

def load_pages(path):
    """Read the file and return a list of page dicts: {idx, marker, lines}.

    idx is the 1-based position in the file (unique). marker is the value
    inside <page number='N'>, which may repeat.
    """
    pages = []
    current = None
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            match = PAGE_RE.match(line)
            if match:
                if current is not None:
                    pages.append(current)
                current = {
                    "idx": len(pages) + 1,
                    "marker": int(match.group(1)),
                    "lines": [],
                }
            elif current is not None:
                current["lines"].append(line)
    if current is not None:
        pages.append(current)
    return pages

def page_text(page):
    return "".join(page["lines"])

def is_front_matter(text):
    """Return True if the page looks like TOC / front matter, not body text."""
    upper = text.upper()
    markers = ("TAB INDEX", "CONTENTS", "TABLE OF CONTENTS")
    if any(marker in upper for marker in markers):
        return True

    non_empty = [ln for ln in text.splitlines() if ln.strip()]
    if not non_empty:
        return False

    toc_lines = sum(1 for ln in non_empty if TOC_LINE_RE.search(ln))
    if toc_lines >= 3 and (toc_lines / len(non_empty)) >= 0.3:
        return True

    return False

def section_index_for_page(text):
    """Return the SECTIONS index whose pattern matches a short heading line."""
    for i, (_, _, patterns) in enumerate(SECTIONS):
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped or len(stripped) > 60:
                continue
            for pattern in patterns:
                if re.search(pattern, stripped, re.IGNORECASE):
                    return i
    return None

def compile_pattern(pattern, label):
    """Compile a user-supplied regex; exit cleanly on invalid syntax."""
    try:
        return re.compile(pattern, re.IGNORECASE)
    except re.error as exc:
        print(f"Error: invalid {label} pattern '{pattern}': {exc}", file=sys.stderr)
        sys.exit(1)

def first_nonempty(pg):
    for ln in pg["lines"]:
        stripped = ln.strip()
        if stripped:
            return stripped
    return ""

def cmd_stats(pages, verbose):
    front = 0
    classified = 0
    unclassified = []
    headings = []

    for pg in pages:
        text = page_text(pg)
        if is_front_matter(text):
            front += 1
            continue
        idx = section_index_for_page(text)
        if idx is not None:
            classified += 1
            key, title, _ = SECTIONS[idx]
            headings.append((pg["idx"], pg["marker"], title, key))
        else:
            unclassified.append(pg)

    content = len(pages) - front
    print(f"Total entries: {len(pages)}")
    print(f"Content entries (front matter skipped): {content}")
    print(f"Classified (heading detected): {classified}")
    print(f"Unclassified (no heading match): {len(unclassified)}")

    if headings:
        print("\nDetected headings:")
        for idx, marker, title, key in headings:
            print(f"  entry {idx:>3} (marker {marker}): {title} ({key})")

    if verbose and unclassified:
        print("\nUnclassified content entries (first non-empty line shown):")
        for pg in unclassified:
            print(f"  entry {pg['idx']:>3} (marker {pg['marker']}): {first_nonempty(pg)[:70]}")

    if classified == 0:
        print("  (no headings detected; page markers may not match the expected format)")

def cmd_query(pages, term, context, max_pages, include_front):
    if max_pages < 1:
        print("Error: --max-pages must be >= 1", file=sys.stderr)
        sys.exit(1)

    pattern = compile_pattern(term, "search term")
    shown = 0
    skipped = 0

    for pg in pages:
        text = page_text(pg)
        if not include_front and is_front_matter(text):
            skipped += 1
            continue

        match = pattern.search(text)
        if not match:
            continue

        shown += 1
        if shown > max_pages:
            print(f"\n... more matches exist. Refine the term or raise --max-pages.")
            break

        print(f"\n--- entry {pg['idx']} (marker {pg['marker']}) ---")
        lines = text.splitlines()

        if context <= 0 or len(lines) <= 200:
            print(text, end="")
        else:
            hits = {i for i, line in enumerate(lines) if pattern.search(line)}
            keep = set()
            for h in hits:
                for j in range(max(0, h - context), min(len(lines), h + context + 1)):
                    keep.add(j)
            for j in sorted(keep):
                print(lines[j])

    if shown == 0:
        if skipped > 0:
            print(f"No content entries matched '{term}' (skipped {skipped} front-matter entries).")
            print("Use --include-front to search the table of contents.")
        else:
            print(f"No entries matched '{term}'.")

def cmd_split(pages, out_dir):
    out = Path(out_dir)
    try:
        out.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"Error: cannot create directory '{out_dir}': {exc}", file=sys.stderr)
        sys.exit(1)

    buckets = {}
    current = None

    for pg in pages:
        text = page_text(pg)
        if is_front_matter(text):
            continue
        idx = section_index_for_page(text)
        if idx is not None:
            current = SECTIONS[idx][0]
        if current:
            buckets.setdefault(current, []).append(pg)

    written = 0
    classified_idxs = set()

    for key, title, _ in SECTIONS:
        pgs = buckets.get(key, [])
        if not pgs:
            continue
        classified_idxs.update(pg["idx"] for pg in pgs)
        fname = out / f"{key}.md"
        try:
            with open(fname, "w", encoding="utf-8") as f:
                f.write(f"# {title}\n\n")
                f.write(f"<!-- section: {key} -->\n\n")
                for pg in pgs:
                    f.write(f"<!-- entry {pg['idx']} (marker {pg['marker']}) -->\n\n")
                    f.write(page_text(pg))
                    f.write("\n\n")
        except OSError as exc:
            print(f"Error: cannot write '{fname}': {exc}", file=sys.stderr)
            sys.exit(1)
        written += 1
        print(f"Wrote {fname} ({len(pgs)} entries)")

    unclassified = []
    for pg in pages:
        if is_front_matter(page_text(pg)):
            continue
        if pg["idx"] not in classified_idxs:
            unclassified.append(pg)

    if unclassified:
        fname = out / "_uncategorized.md"
        try:
            with open(fname, "w", encoding="utf-8") as f:
                f.write("# Unclassified Entries\n\n")
                f.write("<!-- These entries matched no section heading. Diagnose with `stats --verbose`. -->\n\n")
                for pg in unclassified:
                    f.write(f"<!-- entry {pg['idx']} (marker {pg['marker']}) -->\n\n")
                    f.write(page_text(pg))
                    f.write("\n\n")
        except OSError as exc:
            print(f"Error: cannot write '{fname}': {exc}", file=sys.stderr)
            sys.exit(1)
        written += 1
        print(f"Wrote {fname} ({len(unclassified)} entries) — review these gaps")

    content_total = len([pg for pg in pages if not is_front_matter(page_text(pg))])
    print(f"\nCoverage: {len(classified_idxs)}/{content_total} content entries classified; "
          f"{len(unclassified)} unclassified.")

    if written == 0:
        print("No sections detected; nothing was written. Run 'stats' to inspect headings.")

def cmd_index(pages):
    current = None
    first = {}
    for pg in pages:
        text = page_text(pg)
        if is_front_matter(text):
            continue
        idx = section_index_for_page(text)
        if idx is not None:
            current = SECTIONS[idx][0]
            first.setdefault(current, pg["idx"])

    if not first:
        print("No sections detected. Run 'stats' to inspect headings.")
        return

    print("Section -> first entry index")
    for key, title, _ in SECTIONS:
        if key in first:
            print(f"  {key:>16}: entry {first[key]} ({title})")

def cmd_peek(pages, start, end):
    end = end or start
    if start < 1:
        print("Error: entry index must be >= 1", file=sys.stderr)
        sys.exit(1)
    if end < start:
        print("Error: end entry must be >= start entry", file=sys.stderr)
        sys.exit(1)

    found = {pg["idx"]: pg for pg in pages}
    for n in range(start, end + 1):
        pg = found.get(n)
        if pg is None:
            print(f"\n--- entry {n}: NOT FOUND ---")
            continue
        print(f"\n--- entry {n} (marker {pg['marker']}) ---")
        print(page_text(pg), end="")

def main():
    ap = argparse.ArgumentParser(description="PCjr Technical Reference utility")
    ap.add_argument("file", help="path to the .txt strip")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("stats")
    sp.add_argument("--verbose", action="store_true", help="list unclassified entries")

    sp = sub.add_parser("query")
    sp.add_argument("term")
    sp.add_argument("--context", type=int, default=2, help="lines around each match (0 = whole page)")
    sp.add_argument("--max-pages", type=int, default=3)
    sp.add_argument("--include-front", action="store_true", help="also search TOC/front matter")

    sub.add_parser("index")

    sp = sub.add_parser("split")
    sp.add_argument("--out", default="references")

    sp = sub.add_parser("peek")
    sp.add_argument("start", type=int, help="first entry index to print")
    sp.add_argument("end", nargs="?", type=int, help="last entry index to print (default: same as start)")

    args = ap.parse_args()

    try:
        pages = load_pages(args.file)
    except (OSError, FileNotFoundError) as exc:
        print(f"Error: cannot read '{args.file}': {exc}", file=sys.stderr)
        sys.exit(1)

    if not pages:
        print(
            "No pages found. Does the file contain <page number='N'> markers on their own lines?",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.cmd == "stats":
        cmd_stats(pages, args.verbose)
    elif args.cmd == "query":
        cmd_query(pages, args.term, args.context, args.max_pages, args.include_front)
    elif args.cmd == "index":
        cmd_index(pages)
    elif args.cmd == "split":
        cmd_split(pages, args.out)
    elif args.cmd == "peek":
        cmd_peek(pages, args.start, args.end)

if __name__ == "__main__":
    main()
