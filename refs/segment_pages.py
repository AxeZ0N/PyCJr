#!/usr/bin/env python3
# Document Layer Classifier (v3)
#
# Step 1: self-training character trigram language model.
# Step 2: continuous page axes (toc_frac, listing_frac, figureish).
#
# General-purpose OCR document layer classifier.
# No external dependencies; standard library only.
#
# v3 removes the brittle hard page-type enum. Each page gets three
# independent continuous scores instead:
#
#   toc_frac      fraction of dot-leader table-of-contents lines
#   listing_frac  fraction of assembly-listing address lines
#   figureish     mean per-line diagram-art score in [0,1]
#
# A downstream search tool thresholds these axes itself. No content is
# ever dropped; this module only marks pages.
#
# CLI:
#   train     INPUT [--output model.json] [--seed-alpha A] [--seed-punct P]
#   score     MODEL [--line L ... | --file F]
#   classify  INPUT MODEL [--output PATH]

import argparse
import json
import math
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ----------------------------------------------------------------------
# Shared constants
# ----------------------------------------------------------------------

DIAGRAM_PUNCT = set("+-|/\\.:;=<>[](){}*_^#@~")
REPEAT_RE = re.compile(r'([-+=|_.:*#~<>])\1{2,}')
DOT_RUN_RE = re.compile(r'\.(\s*\.){2,}')

# Footer/page token used by TOC-line detection and page segmentation.
PAGE_TOKEN_RE = re.compile(
    r'(?P<prefix>[A-Za-z0-9]+)\s*-\s*(?P<num>[0-9OIlTt\s]+)'
)

# Listing address normalization: OCR substitutes these for hex digits.
HEX_FIX = {
    "O": "0", "o": "0",
    "I": "1", "l": "1", "|": "1", "!": "1",
    "S": "5", "s": "5",
}
LISTING_ADDR_RE = re.compile(r'[0-9A-F]{4}')

# Prose gate band. The LM supplies only this gate, never a verdict.
PROSE_HI = -8.0     # at or above -> not diagram-like
PROSE_LO = -9.5     # at or below -> strongly diagram-like


# ----------------------------------------------------------------------
# Language model (Step 1, unchanged from the fixed v0.2 implementation)
# ----------------------------------------------------------------------

@dataclass
class LanguageModel:
    """Character trigram model trained on the document's own prose."""

    trigram_counts: Dict[str, int] = field(default_factory=dict)
    total_trigrams: int = 0
    vocab_size: int = 0

    @classmethod
    def from_json(cls, path: str) -> "LanguageModel":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(
            trigram_counts=dict(data["trigram_counts"]),
            total_trigrams=int(data["total_trigrams"]),
            vocab_size=int(data["vocab_size"]),
        )

    def to_json(self, path: str) -> None:
        data = {
            "trigram_counts": self.trigram_counts,
            "total_trigrams": self.total_trigrams,
            "vocab_size": self.vocab_size,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def train(self, text: str) -> None:
        """Count character trigrams over prose, one stripped line at a time.

        Blank lines and surrounding indentation are skipped so the model
        learns word-internal structure, not formatting whitespace.
        """
        counts = Counter()
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            s = "  " + stripped.lower() + "  "
            for i in range(len(s) - 2):
                counts[s[i:i + 3]] += 1

        for trigram, count in counts.items():
            self.trigram_counts[trigram] = (
                self.trigram_counts.get(trigram, 0) + count
            )
        self.total_trigrams = sum(self.trigram_counts.values())
        self.vocab_size = len(self.trigram_counts)

    def score_line(self, line: str) -> Optional[float]:
        """Return mean log-likelihood per character, or None for blanks."""
        stripped = line.strip()
        if not stripped:
            return None

        if self.vocab_size == 0:
            raise ValueError("LanguageModel has not been trained")

        s = "  " + stripped.lower() + "  "
        n = len(s) - 2
        if n <= 0:
            return None

        denom = self.total_trigrams + self.vocab_size
        log_sum = 0.0
        for i in range(n):
            trigram = s[i:i + 3]
            count = self.trigram_counts.get(trigram, 0)
            prob = (count + 1) / denom
            log_sum += math.log(prob)

        return log_sum / n


def page_stats(chunk: str) -> Tuple[float, float, float, int]:
    """Seed-page selection statistics for train mode."""
    lines = [line for line in chunk.splitlines() if line.strip()]
    if not lines:
        return 0.0, 0.0, 0.0, 0

    all_chars = [ch for line in lines for ch in line if not ch.isspace()]
    if not all_chars:
        return 0.0, 0.0, 0.0, len(lines)

    alpha = sum(ch.isalpha() for ch in all_chars)
    punct = sum(ch in DIAGRAM_PUNCT for ch in all_chars)
    digit = sum(ch.isdigit() for ch in all_chars)
    total = len(all_chars)
    return alpha / total, punct / total, digit / total, len(lines)


def select_seed_pages(
    text: str,
    alpha_ratio: float = 0.80,
    punct_ratio: float = 0.15,
    min_lines: int = 10,
) -> List[str]:
    """Select unambiguous prose pages for language-model training."""
    seed_texts = []
    for chunk in text.split("\f"):
        alpha, punct, _digit, nlines = page_stats(chunk)
        if nlines < min_lines:
            continue
        if alpha >= alpha_ratio and punct <= punct_ratio:
            seed_texts.append(chunk)
    return seed_texts


# ----------------------------------------------------------------------
# v3 page axes
# ----------------------------------------------------------------------

@dataclass
class LineFeat:
    line: str
    indent: int
    alpha_ratio: float
    digit_ratio: float
    punct_ratio: float
    word_count: int
    single_char_tokens: int
    repeat_runs: bool


@dataclass
class PageScores:
    page_id: str
    num_lines: int
    toc_frac: float
    listing_frac: float
    figureish: float


def is_toc_entry(line: str) -> bool:
    """True for 'text ......... 1-23' style table-of-contents lines."""
    stripped = line.strip()
    if not stripped:
        return False

    if not DOT_RUN_RE.search(stripped):
        return False

    m = PAGE_TOKEN_RE.search(stripped)
    if not m:
        return False
    if stripped[m.end():].strip():
        return False

    before = stripped[:m.start()]
    return bool(re.search(r'[A-Za-z]{2,}', before))


def is_listing_line(line: str) -> bool:
    """OCR-tolerant detection of a 4-hex assembly-listing address.

    Looks only at the first whitespace-delimited token and normalizes
    the OCR substitutions O->0, I/l/|/!->1, S->5.
    """
    stripped = line.lstrip()
    if not stripped:
        return False

    tok = stripped.split()[0]
    if len(tok) < 4:
        return False

    head = tok[:4].upper()
    norm = "".join(HEX_FIX.get(ch, ch) for ch in head)
    return LISTING_ADDR_RE.fullmatch(norm) is not None


def line_features(line: str) -> Optional[LineFeat]:
    """Structural features only; the language model is not involved."""
    if not line.strip():
        return None

    indent = len(line) - len(line.lstrip())
    stripped = line.strip()
    non_space = [ch for ch in stripped if not ch.isspace()]
    total = len(non_space)
    if total == 0:
        return None

    alpha = sum(ch.isalpha() for ch in non_space)
    digit = sum(ch.isdigit() for ch in non_space)
    punct = sum(ch in DIAGRAM_PUNCT for ch in non_space)

    tokens = stripped.split()
    word_count = sum(1 for t in tokens if sum(c.isalpha() for c in t) >= 2)
    single_char_tokens = sum(1 for t in tokens if len(t) == 1)
    repeat_runs = bool(REPEAT_RE.search(stripped))

    return LineFeat(
        line=stripped,
        indent=indent,
        alpha_ratio=alpha / total,
        digit_ratio=digit / total,
        punct_ratio=punct / total,
        word_count=word_count,
        single_char_tokens=single_char_tokens,
        repeat_runs=repeat_runs,
    )


def prose_gate(lm_score: Optional[float]) -> float:
    """Convert a language-model score into a [0,1] gate factor.

    - lm_score <= -9.5 : strongly diagram-like, full gate
    - lm_score >= -8.0 : prose-like, gate closed
    - between           : linear ramp
    """
    if lm_score is None:
        return 0.0
    if lm_score <= PROSE_LO:
        return 1.0
    if lm_score >= PROSE_HI:
        return 0.0
    return (PROSE_HI - lm_score) / (PROSE_HI - PROSE_LO)


def struct_score(feat: LineFeat, prev_indent: Optional[int]) -> float:
    """Unbounded structural diagram score; may be negative."""
    score = 0.0

    if feat.repeat_runs:
        score += 0.30
    if feat.punct_ratio > 0.35:
        score += 0.25
    if feat.single_char_tokens >= 3:
        score += 0.20
    if feat.digit_ratio > 0.30 and feat.alpha_ratio < 0.40:
        score += 0.15
    if prev_indent is not None and abs(feat.indent - prev_indent) > 6:
        score += 0.10
    if feat.word_count >= 6 and feat.alpha_ratio > 0.60:
        score -= 0.40
    if len(feat.line) > 60 and feat.punct_ratio < 0.40:
        score -= 0.20

    return score


def art_score(
    line: str,
    feat: Optional[LineFeat],
    lm_score: Optional[float],
    prev_indent: Optional[int],
) -> float:
    """Combined per-line figureish value in [0,1].

    TOC entries are navigation text and never diagram art, regardless
    of their dot leaders. All other lines combine the structural score
    with the language-model prose gate.
    """
    if not line.strip():
        return 0.0
    if is_toc_entry(line):
        return 0.0
    if feat is None:
        return 0.0

    s = struct_score(feat, prev_indent)
    g = prose_gate(lm_score)
    return max(0.0, min(1.0, s * g))


def score_page(chunk: str, model: LanguageModel, idx: int) -> PageScores:
    """Compute the three continuous axes for one form-feed chunk."""
    lines = [line for line in chunk.splitlines() if line.strip()]
    n = len(lines)
    if n == 0:
        return PageScores(f"?{idx}", 0, 0.0, 0.0, 0.0)

    toc_count = 0
    listing_count = 0
    art_total = 0.0
    prev_indent: Optional[int] = None

    for line in lines:
        if is_toc_entry(line):
            toc_count += 1
        if is_listing_line(line):
            listing_count += 1

        feat = line_features(line)
        lm = model.score_line(line)
        art_total += art_score(line, feat, lm, prev_indent)

        if feat is not None:
            prev_indent = feat.indent

    return PageScores(
        page_id=f"?{idx}",
        num_lines=n,
        toc_frac=toc_count / n,
        listing_frac=listing_count / n,
        figureish=art_total / n,
    )


def score_pages(raw_text: str, model: LanguageModel) -> List[PageScores]:
    """Score every chunk; 0-based page ids, blank chunks included."""
    return [
        score_page(chunk, model, idx)
        for idx, chunk in enumerate(raw_text.split("\f"))
    ]


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(
        description="Document layer classifier (v3, continuous axes)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    train_p = sub.add_parser("train", help="train a trigram language model")
    train_p.add_argument("input", help="raw OCR text (form-feed separated)")
    train_p.add_argument("--output", default="language_model.json",
                         help="output model file")
    train_p.add_argument("--seed-alpha", type=float, default=0.80,
                         help="minimum alphabetic ratio for seed pages")
    train_p.add_argument("--seed-punct", type=float, default=0.15,
                         help="maximum diagram punctuation ratio for seed pages")
    train_p.add_argument("--min-lines", type=int, default=10,
                         help="minimum non-blank lines for a seed page")

    score_p = sub.add_parser("score", help="score lines using a trained model")
    score_p.add_argument("model", help="path to model JSON")
    score_p.add_argument("--line", action="append", default=[],
                         help="line to score (may be repeated)")
    score_p.add_argument("--file", help="read lines from a file")

    cls_p = sub.add_parser(
        "classify",
        help="emit continuous page axes (toc_frac, listing_frac, figureish)",
    )
    cls_p.add_argument("input", help="raw OCR text (form-feed separated)")
    cls_p.add_argument("model", help="path to trained model JSON")
    cls_p.add_argument("--output", default="-",
                       help="write report (default stdout)")

    args = parser.parse_args(argv)

    if args.command == "train":
        text = Path(args.input).read_text(encoding="utf-8", errors="replace")
        seed_pages = select_seed_pages(
            text,
            alpha_ratio=args.seed_alpha,
            punct_ratio=args.seed_punct,
            min_lines=args.min_lines,
        )
        if not seed_pages:
            raise ValueError("No seed pages found; adjust seed thresholds")

        model = LanguageModel()
        for page in seed_pages:
            model.train(page)
        model.to_json(args.output)

        print(f"Seed pages selected: {len(seed_pages)}")
        print(f"Trigram vocabulary:  {model.vocab_size}")
        print(f"Total trigrams:      {model.total_trigrams}")
        print(f"Model saved to:      {args.output}")

    elif args.command == "score":
        model = LanguageModel.from_json(args.model)
        lines = list(args.line)
        if args.file:
            with open(args.file, "r", encoding="utf-8", errors="replace") as f:
                lines.extend(line.rstrip("\n") for line in f)
        if not lines:
            lines = [line.rstrip("\n") for line in sys.stdin]

        for line in lines:
            score = model.score_line(line)
            if score is None:
                print(f"None\t{line!r}")
            else:
                print(f"{score:.4f}\t{line}")

    elif args.command == "classify":
        raw = Path(args.input).read_text(encoding="utf-8", errors="replace")
        model = LanguageModel.from_json(args.model)
        pages = score_pages(raw, model)

        out_lines = [
            "page_id\tnum_lines\ttoc_frac\tlisting_frac\tfigureish",
        ]
        for p in pages:
            out_lines.append(
                f"{p.page_id}\t{p.num_lines}\t"
                f"{p.toc_frac:.3f}\t{p.listing_frac:.3f}\t{p.figureish:.3f}"
            )
        report = "\n".join(out_lines) + "\n"

        if args.output == "-":
            sys.stdout.write(report)
        else:
            Path(args.output).write_text(report, encoding="utf-8")
            print(f"Wrote: {args.output}")


if __name__ == "__main__":
    main()
