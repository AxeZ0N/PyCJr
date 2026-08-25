# Session — Periodic-recovery probe + analog phase close

Date: 2026-08-25
Scope: test the periodic AGC-reset hypothesis, retire it on economics,
close the analog layer, hand off to the deserializer.

## Verified this session

- RECOVERY4 hardware run, AGCPROBE.BAS capture, CH0CAL ASM:
  CTRL_180 ed=12 (6 fusions), R4_180 ed=22 (1), R4_200 ed=24,
  R4_220 ed=24. Reset suppresses fusion mechanistically; S=200 is
  rescued by reset. Reset L reads 3140/3142ct = 1500us calibration.
- Reset economics: cost/sym = (W+S)+(R−S)/k; win needs R < 180+60k.
  At R=1500, k>22 required; measured k≈3. Retired, no break-even.
- IBG fact-check: 1500us is the verified safe replacement for the
  4840us IBG, not the proven minimum; true minimum unmeasured.
- Receiver observables are binary: PC6 = carrier-present only
  (manual entry 92); DC-on/DC-off/40kHz ternary collapses to OOK.
- Modulation alternatives closed: NRZ, M-ary (retired), width
  (duty-flat), amplitude (no PC6 axis), FM (fixed 40kHz demod).
- Keypress loss budget: 4×4840us stock (make/break × frame/IBG);
  cell is 2.3%. Framing-only ~2× + CPU hostage remain.
- Analog phase closes.

## Open questions

- Custom decoder gap-classifier loop budget at ~120 ch/s (unmeasured).
- Stock BIOS make-only behavior: held-key state tracking. Manual
  lookup 5-21..5-42 required before claiming make-only on stock path.
- True AGC IBG minimum below 1500us (unmeasured; z2 157→80 deferred).

## Loose ends

- R4_180 fusion was post-reset (block 3); one data point, not a rate.
- R4_220 L7=133 below the 79us L-saturation floor, unexplained.
- DENSETRAIN S=260 H 620ct outlier carried forward, cosmetic.

## Suggested next scope (mandatory)

- Custom deserializer. Stage 1: INT 02h handler samples one make frame
  via CH0 latched edge timestamps (CH0CAL path, hardware-proven),
  returns scancode, keyboard intact. Regression: IRPING first. This
  attacks both framing overhead and the 4.8ms/frame CPU hostage.

## Ground truth

- docs/anchors/AGCPROBE.BAS
- docs/anchors/CH0CAL.ASM
- docs/anchors/ENVSHAPE.BAS
- IRPING (frozen DATA, platform skill Rule 5)
