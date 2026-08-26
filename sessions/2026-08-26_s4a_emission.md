# Handoff — S4A emission (single scope)

## Verified this session

- S4A (112B) hardware pass on h: st=3, half=1 (predicted first data
  bit of 0x23, LSB-first), keyboard alive.
- Finite arm + rising/trailing edge sync verified.
- 5x majority (>=3 -> 1) verified; returns a clean bit.
- End-quiet wait verified: NMI restored only after 400 consecutive
  quiet PC6 polls; the entire h press is masked, BIOS never buffers
  the key, no softlock. Desired behavior for S4B.
- debug_asm rel8/branch semantics confirmed; gate order selfloc ->
  rel8 -> branch -> decode now followed per-stage.
- Mid-frame-return defect closed: v1 softlock root-caused, v2 fix
  hardware-validated.

## Open questions

- LOOP-timing calibration margin: CX=90 landed on half=1 for one h
  run. Robustness across AGC recovery / temperature unmeasured. CH0
  grid is the spec'd answer but exceeds the 128-byte ceiling and
  needs a debug_asm 81 /7 iw fix.
- Whether the end-quiet wait completing in the post-keypress silence
  (masking the break frame) introduces any S4B timing interaction.

## Loose ends

- CH0 word-imm CMP (81 /7 iw) decode bug in debug_asm: the immediate
  leaked as IN AL,0x02. Not needed for S4A; blocks the CH0 grid for
  S4B.
- 128-byte code ceiling formalized as a hard constraint.
- S4A v1 139B CH0 variant retired; v2 112B LOOP-timing is the anchor.

## Suggested next scope

S4B: full 9-bit loop + parity on LOOP-timing, expect scancode=23h
parity_ok=1 on h. Alternative: extend debug_asm (81 /7 iw, C7 06) and
re-attempt the CH0 grid. Gate each stage before hardware.

## Ground truth

- docs/anchors/S4A.BAS
- docs/anchors/S4A.ASM
- docs/anchors/BASLOAD.BAS
- docs/anchors/CH0CAL.ASM
- docs/anchors/ENVSHAPE.BAS
- docs/anchors/AGCPROBE.BAS
- docs/anchors/S1V2.BAS / S1V2.ASM
- docs/anchors/S2V1.BAS / S2V1.ASM
- docs/anchors/B26VEC.BAS
- IRPING (frozen DATA, platform skill Rule 5)
