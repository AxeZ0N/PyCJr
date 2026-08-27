# Handoff — DEC1 edge-sync decoder stage 1 (single scope)

Date: 2026-08-27
Scope: land the edge-sync decoder's first rung — a two-edge span
capture — on hardware, retire the fixed-grid anchor, and record the
measured bit0->bit1 cell.

## Verified this session

- DEC1_ST1 assembled via pjasm (106 bytes) and passed the full
  emission gate: selfloc 8DAE7A00 matches pjasm, decode clean (zero
  db fallbacks), branch 11/11.
- Hardware pass 2/2. Run 1: flag=2 r0=CDD0:CA54 -> span 892 counts
  (373.8 us). Run 2: flag=2 r0=BB46:B7C8 -> span 894 counts
  (374.6 us). Keyboard intact both runs. loaded-106 gate observed.
- Span repeatability ~2 counts matches the recorded short-term H/L
  repeatability floor (<=2 ct).
- Measured span 892/894 counts matches the ENVSHAPE26 bit0 cell
  (882 counts): the first detected edge is bit0, not the start bit.
  Start burst swallowed by the arming window as previously recorded.

## Open questions

- Edge identity remains inference. A three-latch variant (start, bit0,
  bit1) or an explicit pre-wait before the first arm would pin it.
- Whether the ~374 us measured cell is stable across scancodes other
  than 'h' (h has bit0=1, bit1=1; a 1->0 or 0->0 transition has not
  been sampled yet).

## Loose ends

- BASLOAD anchor sv/sg are DEFINT; raw CH0 latches > 32767 overflow
  line 170. DEC1 used the in-memory sv!/sg!/256! variant. This is an
  instance of cartridge_basic_float16, not a new fact; the anchor
  listing for DEC1_ST1.BAS carries the float fix.
- DEC1_ST1.BAS is the runnable listing with the float fix, not the
  BASLOAD anchor verbatim.

## Suggested next scope

DEC1_ST2: use the measured ~890-count cell as the per-bit edge anchor
and implement the edge-sync sampler — wait each data bit's own rising
edge, sample the half-cell center relative to that edge, 5x majority,
opposite-halves validity, odd parity. Stage gate: IRPING then
S4B1_ST3B then DEC1_ST1 first.

## Ground truth

- docs/anchors/DEC1_ST1.BAS
- docs/anchors/DEC1_ST1.ASM
- Regression anchors by name: IRPING, CH0CAL, S4B1_ST3B, BASLOAD.
# Handoff — DEC1 edge-sync decoder stage 1 (single scope)

Date: 2026-08-27
Scope: land the edge-sync decoder's first rung — a two-edge span
capture — on hardware, retire the fixed-grid anchor, and record the
measured bit0->bit1 cell.

## Verified this session

- DEC1_ST1 assembled via pjasm (106 bytes) and passed the full
  emission gate: selfloc 8DAE7A00 matches pjasm, decode clean (zero
  db fallbacks), branch 11/11.
- Hardware pass 2/2. Run 1: flag=2 r0=CDD0:CA54 -> span 892 counts
  (373.8 us). Run 2: flag=2 r0=BB46:B7C8 -> span 894 counts
  (374.6 us). Keyboard intact both runs. loaded-106 gate observed.
- Span repeatability ~2 counts matches the recorded short-term H/L
  repeatability floor (<=2 ct).
- Measured span 892/894 counts matches the ENVSHAPE26 bit0 cell
  (882 counts): the first detected edge is bit0, not the start bit.
  Start burst swallowed by the arming window as previously recorded.

## Open questions

- Edge identity remains inference. A three-latch variant (start, bit0,
  bit1) or an explicit pre-wait before the first arm would pin it.
- Whether the ~374 us measured cell is stable across scancodes other
  than 'h' (h has bit0=1, bit1=1; a 1->0 or 0->0 transition has not
  been sampled yet).

## Loose ends

- BASLOAD anchor sv/sg are DEFINT; raw CH0 latches > 32767 overflow
  line 170. DEC1 used the in-memory sv!/sg!/256! variant. This is an
  instance of cartridge_basic_float16, not a new fact; the anchor
  listing for DEC1_ST1.BAS carries the float fix.
- DEC1_ST1.BAS is the runnable listing with the float fix, not the
  BASLOAD anchor verbatim.

## Suggested next scope

DEC1_ST2: use the measured ~890-count cell as the per-bit edge anchor
and implement the edge-sync sampler — wait each data bit's own rising
edge, sample the half-cell center relative to that edge, 5x majority,
opposite-halves validity, odd parity. Stage gate: IRPING then
S4B1_ST3B then DEC1_ST1 first.

## Ground truth

- docs/anchors/DEC1_ST1.BAS
- docs/anchors/DEC1_ST1.ASM
- Regression anchors by name: IRPING, CH0CAL, S4B1_ST3B, BASLOAD.
