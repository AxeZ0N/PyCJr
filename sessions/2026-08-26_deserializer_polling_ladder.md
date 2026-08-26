# Handoff — Deserializer polling ladder (single scope)

Date: 2026-08-26
Scope: land the polling ladder S1V2 + S2V1, retire raw-ring dump,
anchor the reconstructed base26 encoder, formalize memory generation.

## Verified this session

- S1V2 (71B) hardware pass: loaded 71, flag=0, rising=17, falling=17,
  keyboard intact. bp-preserve verified.
- S2V1 (106B) hardware pass: loaded 106, st=1, edge count 22h (34),
  keyboard intact. CH0 latch/read per edge safe inside masked-NMI poll.
- B26VEC (pure BASIC) hardware pass: 11/11 frozen base26 vectors match.
- S3 raw-ring dump retired as a recording method; transcription failed,
  hardware and encoder exonerated.
- CH0CAL 38 D8 flagged as ungated-but-sound open item.
- memory_batch_spec locked as a repo fact (facts.md).

## Open questions

- S4 decode algorithm unspecced: no rule yet maps an edge-gap sequence
  to a scancode given measured AGC bounds.
- Per-symbol merge thresholds not set (assert ~170us, merge ~80us are
  candidate inputs only).
- Whether to extend debug_asm to cover 38 /r, re-anchor CH0CAL with
  39 /r, or leave both flagged.
- FAQ.md section 21 is truncated mid-sentence in the repo; needs a
  manual edit.

## Loose ends

- Original ENVSHAPE26 encoder source still unrecovered; reconstructed
  encoder is anchored now, original remains lost.
- S1 v1 (110B, bp-clobber) retired and never anchored; do not resurrect.
- The skill's Memory batch rules section now drifts behind the new
  repo fact memory_batch_spec until the user syncs it (FAQ section 13).
- Fixed-width base26 padding proposal (4 sym, leading A) stays a
  proposal; not locked.
- S3V1.BAS itself is not anchored; retired by decision.

## Suggested next scope

New session: spec S4 gap-classify + software-decode. No code until the
decode algorithm is written and agreed. Inputs: measured AGC bounds,
frame/IBG floor knowledge, B26VEC encoder for any on-machine dump that
is ever needed again.

## Ground truth

- docs/anchors/S1V2.BAS
- docs/anchors/S1V2.ASM
- docs/anchors/S2V1.BAS
- docs/anchors/S2V1.ASM
- docs/anchors/B26VEC.BAS (BASIC-only anchor; no .ASM pair — recorded
  exception, encoder carries no machine code)
- docs/anchors/BASLOAD.BAS
- docs/anchors/CH0CAL.ASM
- docs/anchors/ENVSHAPE.BAS
- docs/anchors/AGCPROBE.BAS
- IRPING (frozen DATA, platform skill Rule 5)
