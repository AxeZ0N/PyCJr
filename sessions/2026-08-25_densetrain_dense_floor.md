# Session — DENSETRAIN dense floor discovery

Date: 2026-08-25
Scope: pin the dense-traffic AGC floor, retire the 250us cell, close the
analog layer for gap-keyed encoding.

## Verified this session

- DENSETRAIN battery run: W=62us, 12-burst trains, S=260 down to 160,
  batch=2. AGCPROBE.BAS capture, CH0CAL ASM.
- Dense separation floor: clean at 240us, first fusion at 230us,
  collapse at <=200us. Safe margin: gaps >= 240us. `empirical`.
- H compresses under load: 550ct (230us) -> 476/478 (200us) ->
  406/404 (170us). The 170us in-traffic minimum reproduced deliberately.
  `empirical`.
- 250us dense cell retired: separation, not pulse width, is the binding
  constraint. Dense cell ~430us+. Supersedes decode_floor_mechanism.
- M-ary gap alphabet retired: L saturates at 190ct for all gaps below
  ~260us; staircase steps force an uneconomical alphabet above it.
- Remaining lever: framing-only ~2x. Periodic recovery gap is the single
  open analog idea.

## Open questions

- Does a periodic AGC-reset gap (>=1500us) every N symbols restore tight
  inter-symbol gaps below 240us without fusion?
- What is the 8088 gap-classifier loop budget at ~120 ch/s? Unmeasured;
  the next likely bottleneck.

## Loose ends

- DENSETRAIN S=260 row H had one 620ct outlier; not reproduced or
  explained. Cosmetic.
- S=230 fusion count is stochastic (1 of 11 gaps); single trial, not a
  rate.

## Suggested next scope (mandatory)

- Periodic-recovery probe: train with 1500us reset every 4th symbol,
  inter-symbol gaps 180/200/220us. Gate on edge fusion after each reset.
  If fusion stays suppressed, proceed; if not, the analog phase closes.

## Ground truth

- docs/anchors/AGCPROBE.BAS
- docs/anchors/CH0CAL.ASM
- docs/anchors/ENVSHAPE.BAS
- IRPING (frozen DATA, platform skill Rule 5)
