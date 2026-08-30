#!/usr/bin/env python3
"""Usage tests for the PyCJr grep tools (pytest).

Assumes wiring is functional — instantiation succeeding is sufficient.
Exercises the retrieval workflows an agent actually performs and asserts
stable content truth. Anomalies needing human review are surfaced via
warnings, not failures.

Run:
    python3 -m pytest test_usage.py -v
Treat warnings as errors with:
    python3 -m pytest test_usage.py -v -W error::UserWarning
"""

import sys
import warnings
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent
REF_DIR = REPO / "refs"
sys.path.insert(0, str(REF_DIR))

import pcjr_repo_grep as GREP
import pcjr_manual as MANUAL
import pcjr_bios as BIOS

@pytest.fixture(scope="module")
def manual():
    return MANUAL.ManualStore(
        REF_DIR / "pcjr_technical_reference.txt",
        REF_DIR / "pages.jsonl",
    )

@pytest.fixture(scope="module")
def bios():
    p = REF_DIR / "ibm_pcjr-bios.lst"
    if not p.exists():
        pytest.skip("BIOS listing absent (gitignored)")
    return BIOS.BiosStore(p)

# --- repo workflows ---------------------------------------------------------

def test_files_discovers_ch0cal_anchor():
    r = GREP.dispatch("files", query="CH0CAL")
    assert r["total"] > 0, "CH0CAL anchor not discoverable by filename"

def test_facts_heading_lookup_and_read():
    headings = GREP.dispatch("facts_headings")["headings"]
    hw = [h for h in headings if "hardware_map" in h["heading"]]
    assert hw, "hardware_map heading missing from facts.md"
    idx = headings.index(hw[0])
    start = hw[0]["line"]
    end = headings[idx + 1]["line"] - 1 if idx + 1 < len(headings) else start + 60
    body = GREP.dispatch("read", path="facts.md", start_line=start, end_line=end)
    assert body["lines"] > 0, "read of hardware_map span is empty"

def test_facts_grep_known_fact():
    r = GREP.dispatch("facts", query="carrier_high_us", max_matches=3)
    assert r["total_hits"] > 0, "known fact not greppable in the fact layer"

def test_facts_heading_format_drift():
    headings = GREP.dispatch("facts_headings")["headings"]
    overlong = [h for h in headings if h["heading"].count("\u00b7") >= 3]
    if overlong:
        warnings.warn(
            f"{len(overlong)} heading(s) have 4+ dot-separated fields; "
            "facts_headings takes the last field as status — verify against spec",
            UserWarning,
        )

# --- manual workflows -------------------------------------------------------

def test_manual_grep_register(manual):
    g = manual.grep("8255", max_matches=8)
    assert g["total_hits"] > 0, "8255 not greppable in the prose strip"
    for m in g["matches"]:
        assert m["page_id"] in g["pages"], f"metadata missing for {m['page_id']}"

def test_manual_query_topic(manual):
    q = manual.query("keyboard", max_pages=3)
    assert q["total_pages_matched"] > 0, "keyboard query matches nothing"

def test_jsonl_metadata_full_coverage(manual):
    st = manual.stats()
    assert st["total_pages"] > 0
    assert st["jsonl_covered"] == st["total_pages"], (
        f"metadata join covers {st['jsonl_covered']}/{st['total_pages']}"
    )

def test_peek_index_semantics(manual):
    pid = manual.peek(1)["entries"][0]["page_id"]
    if not pid.startswith(("?", "i", "ii", "iii", "1-", "2-")):
        warnings.warn(
            f"peek 1 is {pid}; index is strip-file order, not physical page order "
            "— document in the skill",
            UserWarning,
        )

# --- hex normalization ------------------------------------------------------

def test_hex_normalization_never_drops_matches(manual):
    norm = manual.grep("A0h", max_matches=3)["total_hits"]
    lit = manual.grep("A0h", raw=True, max_matches=3)["total_hits"]
    assert norm >= lit, f"normalization dropped matches: norm={norm} lit={lit}"

def test_a0h_corpus_presence(manual):
    a0h = manual.grep("A0h", max_matches=3)["total_hits"]
    a0 = manual.grep("A0", raw=True, max_matches=3)["total_hits"]
    if a0h == 0:
        warnings.warn(
            f"A0h absent from prose (A0 literal hits: {a0}); "
            "the register may live only in the BIOS dump — do not rely on prose grep",
            UserWarning,
        )

# --- BIOS -------------------------------------------------------------------

def test_bios_grep_address(bios):
    assert bios.grep("F000", max_matches=3)["total_hits"] > 0

def test_bios_line_shape(bios):
    first = bios.peek(1, 3)["entries"]
    assert first, "BIOS listing is empty"
    if not any(ch.isdigit() for ch in first[0]["text"]):
        warnings.warn(
            "first BIOS line has no digits; address-per-line assumption may not hold",
            UserWarning,
        )

# --- BIOS whitespace tolerance (2026-08-30) ---------------------------------

def test_bios_grep_whitespace_collapse(tmp_path):
    """Single-space needle must match column-padded listing text.

    Regression for the false negative where ``PROC NEAR`` returned 0
    hits against ``PROC    NEAR`` (four spaces). Collapse applies to
    matching only; the recorded text keeps the original line.
    """
    p = tmp_path / "mini.lst"
    p.write_text("036C                            BITS_ON_OFF PROC    NEAR\n",
                 encoding="utf-8")
    store = BIOS.BiosStore(p)
    r = store.grep("PROC NEAR", context=0, max_matches=5)
    assert r["total_hits"] == 1
    assert r["matches"][0]["text"] == \
        "036C                            BITS_ON_OFF PROC    NEAR"

def test_bios_grep_preserves_column_spacing(tmp_path):
    """Returned text must keep original column padding, not collapsed form."""
    p = tmp_path / "mini.lst"
    original = "036C                            BITS_ON_OFF PROC    NEAR"
    p.write_text(original + "\n", encoding="utf-8")
    store = BIOS.BiosStore(p)
    r = store.grep("BITS_ON_OFF", context=0, max_matches=5)
    assert r["matches"][0]["text"] == original
    assert "    " in r["matches"][0]["text"], \
        "column padding was collapsed in the returned text"

def test_bios_grep_proc_near_corpus(bios):
    """Corpus smoke: PROC NEAR must not false-negative on the real .lst.

    This is the query that returned a clean zero before the collapse
    change; it now resolves to 100+ PROC directives.
    """
    assert bios.grep("PROC NEAR", max_matches=3)["total_hits"] > 0
