# Handoff — S4B fixed CH0 grid retired (single scope)

Date: 2026-08-26
Scope: instrument the S4B fixed-grid decode approach on hardware, settle
the 310us anchor question with measured burst widths, close the scope.

## Verified this session

- Raised ceiling to 180 bytes: stage-1 sentinel pass proved selfloc
  `lea bp,[bp+174]` + BASIC PEEKs at O+180..187. Hardware-verified.
- CH0 latch/read works under NMI mask during a live IR frame:
  S4B1_ST2 (103B) and S4B1_ST3B (180B) both passed, keyboard intact.
- CH0 counts DOWN; start-burst envelope high measured at 526 / 578 /
  600 counts (220.4 / 242.2 / 251.4 us) across three runs.
- S4B1_ST3B instrumented probe: st=3, rise=0xC330, trail=0xC0D8,
  burst=0x258 (251.4us), half=0. The fixed 740-count anchor from the
  trailing edge samples the bit0 boundary and flip-flops vs S4A's
  half=1 at the same nominal offset.
- pjasm operand rules discovered and recorded (facts append above).
- 81 /7 iw decode confirmed working end to end through the gate.

## Open questions

- Edge-sync decoder design: after the start bit, how to reliably detect
  bit0's own rising edge (AGC-stretched, ~250us high) and sample each
  subsequent bit relative to its own edge rather than a fixed grid.
- Whether the locked S4 decode spec needs a revision: the "310us
  post-burst wait" is receiver-nominal and AGC-vulnerable. The spec
  still says fixed CH0 grid; this is now empirically contradicted.

## Loose ends

- pjasm's internal `budget_left` is reported against a 128-byte baseline
  and is misleading: our raised ceiling is 180, so a negative
  budget_left is fine as long as assembled size <= 180.
- S4B1_ST3B is exactly 180 bytes: zero headroom. Any further
  instrumentation needs either a tighter loop or a second raised
  ceiling.
- S4B1 stages 1 and 2 are subsumed by S4B1_ST3B (which reports
  rise/trail/burst/half); they are not independently anchored.

## Suggested next scope

Edge-sync decoder: detect the start-burst trailing edge, then latch CH0
on bit0's rising edge, sample 5x majority relative to that edge, and
per-bit re-sync on each data-bit rising edge. Gate each stage; IRPING
then S4B1_ST3B first.

## Ground truth

- docs/anchors/S4B1_ST2.BAS / S4B1_ST2.ASM
- docs/anchors/S4B1_ST3B.BAS / S4B1_ST3B.ASM
- docs/anchors/S4A.BAS / S4A.ASM
- docs/anchors/CH0CAL.ASM
- docs/anchors/BASLOAD.BAS
- IRPING (frozen DATA, platform skill Rule 5)
# Handoff — S4B fixed CH0 grid retired (single scope)

Date: 2026-08-26
Scope: instrument the S4B fixed-grid decode approach on hardware, settle
the 310us anchor question with measured burst widths, close the scope.

## Verified this session

- Raised ceiling to 180 bytes: stage-1 sentinel pass proved selfloc
  `lea bp,[bp+174]` + BASIC PEEKs at O+180..187. Hardware-verified.
- CH0 latch/read works under NMI mask during a live IR frame:
  S4B1_ST2 (103B) and S4B1_ST3B (180B) both passed, keyboard intact.
- CH0 counts DOWN; start-burst envelope high measured at 526 / 578 /
  600 counts (220.4 / 242.2 / 251.4 us) across three runs.
- S4B1_ST3B instrumented probe: st=3, rise=0xC330, trail=0xC0D8,
  burst=0x258 (251.4us), half=0. The fixed 740-count anchor from the
  trailing edge samples the bit0 boundary and flip-flops vs S4A's
  half=1 at the same nominal offset.
- pjasm operand rules discovered and recorded (facts append above).
- 81 /7 iw decode confirmed working end to end through the gate.

## Open questions

- Edge-sync decoder design: after the start bit, how to reliably detect
  bit0's own rising edge (AGC-stretched, ~250us high) and sample each
  subsequent bit relative to its own edge rather than a fixed grid.
- Whether the locked S4 decode spec needs a revision: the "310us
  post-burst wait" is receiver-nominal and AGC-vulnerable. The spec
  still says fixed CH0 grid; this is now empirically contradicted.

## Loose ends

- pjasm's internal `budget_left` is reported against a 128-byte baseline
  and is misleading: our raised ceiling is 180, so a negative
  budget_left is fine as long as assembled size <= 180.
- S4B1_ST3B is exactly 180 bytes: zero headroom. Any further
  instrumentation needs either a tighter loop or a second raised
  ceiling.
- S4B1 stages 1 and 2 are subsumed by S4B1_ST3B (which reports
  rise/trail/burst/half); they are not independently anchored.

## Suggested next scope

Edge-sync decoder: detect the start-burst trailing edge, then latch CH0
on bit0's rising edge, sample 5x majority relative to that edge, and
per-bit re-sync on each data-bit rising edge. Gate each stage; IRPING
then S4B1_ST3B first.

## Ground truth

- docs/anchors/S4B1_ST2.BAS / S4B1_ST2.ASM
- docs/anchors/S4B1_ST3B.BAS / S4B1_ST3B.ASM
- docs/anchors/S4A.BAS / S4A.ASM
- docs/anchors/CH0CAL.ASM
- docs/anchors/BASLOAD.BAS
- IRPING (frozen DATA, platform skill Rule 5)
