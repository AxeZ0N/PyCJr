# 2026-08-29 · Document layer pipeline

## Verified this session
- segmenter v5: 610 chunks, 501 emitted, Appendix A dropped by default.
- continuous axes contract green: toc_frac, listing_frac, figureish.
- listing axis separates BIOS pages cleanly: listing_frac 0.631-0.750, figureish ~0.
- region segmentation green on all four legs:
  - prose pages 3-133, 3-135 -> zero regions
  - embedded schematic 3-134 -> exactly one strong region (lines 19-27, low frac 0.889)
  - listing pages listing_frac >= 0.30 -> zero figure regions
- region seeding changed to LM-only (<= -9.0) after structural AND-gate failed.

## Open questions
- How to correct listing_frac false positives on 2-61/2-62 video pages.
- Whether label-dominant connector pages need a separate axis or acceptance.

## Loose ends
- --seg-out remains opt-in; default segmented output not yet wired.
- Earlier threshold-based attempts (sigma, percentile, hybrid) are superseded and not part of v3.
- Mixed-page discovery list surfaced figure/table pages, not a clean prose+figure anchor.

## Suggested next scope
- Tighten is_listing_line against video scan labels; re-run 2-61/2-62.
- Wire default pages.seg.txt output with --no-seg override.
- If needed, add a fragment-line axis for label-layout connector pages.

## Ground truth
- No machine-code anchors this session (document pipeline only).
