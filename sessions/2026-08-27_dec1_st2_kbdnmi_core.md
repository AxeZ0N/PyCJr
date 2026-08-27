# Handoff — DEC1_ST2 KBDNMI-core, blocked on pjasm r8 gap

Date: 2026-08-27
Scope: land the edge-sync decoder's KBDNMI-core stage on CH0; ST2A
PC0 gate, ST2B trailing-edge span, then diagnose and record the pjasm
blocking gap.

## Verified this session

- DEC1_ST2A hardware pass: PC0 readable via polling bridge; pc6=40 at
  capture; keyboard intact. (anchor)
- DEC1_ST2B negative: single-poll trailing edge trimodal
  (140/218/240 us). No-stimulus control clean.
- Corrected the CH0 down-counter analysis; span = t0 - t1, no wrap.
- Pulled KBDNMI listing (entry 338): trailing edge requires 4
  consecutive LOW confirmation; ST2B omitted it — root cause.
- Pulled pjasm v6.0 source: table lacks test r8,imm / xor r8,r8 /
  shr r8,1 / inc r8 / dec r8 / or r8,r8 / xchg ah,al / jnb. KBDNMI
  core not expressible.

## Open questions

- Exact r8 opcode set to add to pjasm and their encode forms; budget
  impact on the 128-byte limit.
- Whether KBDNMI's N=4 confirmation is sufficient for the Pi AGC
  ripple (~22 us); to be tested after pjasm extension.
- CH1 time-base remains never empirically recorded; not needed for
  this stage (CH0 path).

## Loose ends

- ST2B.BAS/.ASM exist as files but failed hardware; not anchors. Do
  not promote.
- The 140 us single outlier from the first stimulus run remains
  unexplained; 240 us is the working hypothesis for the start-burst
  envelope HIGH.

## Suggested next scope

Extend pjasm with the missing r8 shapes (selftest each), then emit
ST2C: KBDNMI-core on CH0, N=4 trailing confirmation, 5x majority
halves, opposite-halves, odd parity, target `23h` for `h`. Regression:
IRPING -> S4B1_ST3B -> DEC1_ST2A.

## Ground truth

- docs/anchors/DEC1_ST2A.BAS
- docs/anchors/DEC1_ST2A.ASM
- Regression anchors by name: IRPING, S4B1_ST3B, DEC1_ST1, CH0CAL.
# Handoff — DEC1_ST2 KBDNMI-core, blocked on pjasm r8 gap

Date: 2026-08-27
Scope: land the edge-sync decoder's KBDNMI-core stage on CH0; ST2A
PC0 gate, ST2B trailing-edge span, then diagnose and record the pjasm
blocking gap.

## Verified this session

- DEC1_ST2A hardware pass: PC0 readable via polling bridge; pc6=40 at
  capture; keyboard intact. (anchor)
- DEC1_ST2B negative: single-poll trailing edge trimodal
  (140/218/240 us). No-stimulus control clean.
- Corrected the CH0 down-counter analysis; span = t0 - t1, no wrap.
- Pulled KBDNMI listing (entry 338): trailing edge requires 4
  consecutive LOW confirmation; ST2B omitted it — root cause.
- Pulled pjasm v6.0 source: table lacks test r8,imm / xor r8,r8 /
  shr r8,1 / inc r8 / dec r8 / or r8,r8 / xchg ah,al / jnb. KBDNMI
  core not expressible.

## Open questions

- Exact r8 opcode set to add to pjasm and their encode forms; budget
  impact on the 128-byte limit.
- Whether KBDNMI's N=4 confirmation is sufficient for the Pi AGC
  ripple (~22 us); to be tested after pjasm extension.
- CH1 time-base remains never empirically recorded; not needed for
  this stage (CH0 path).

## Loose ends

- ST2B.BAS/.ASM exist as files but failed hardware; not anchors. Do
  not promote.
- The 140 us single outlier from the first stimulus run remains
  unexplained; 240 us is the working hypothesis for the start-burst
  envelope HIGH.

## Suggested next scope

Extend pjasm with the missing r8 shapes (selftest each), then emit
ST2C: KBDNMI-core on CH0, N=4 trailing confirmation, 5x majority
halves, opposite-halves, odd parity, target `23h` for `h`. Regression:
IRPING -> S4B1_ST3B -> DEC1_ST2A.

## Ground truth

- docs/anchors/DEC1_ST2A.BAS
- docs/anchors/DEC1_ST2A.ASM
- Regression anchors by name: IRPING, S4B1_ST3B, DEC1_ST1, CH0CAL.
