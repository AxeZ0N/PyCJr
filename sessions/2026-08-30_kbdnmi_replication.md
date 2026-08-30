# Handoff — KBDNMI byte-identical CALL entry (replication)

Date: 2026-08-30
Scope: Replicate stock KBDNMI decode from a Cartridge BASIC CALL by
reproducing the NMI phase-locked entry, not by altering decode logic.

## 1. Verified this session

- Manual 2-99: NMI fires on the start bit's leading edge; ISR then
  polls the trailing edge. Stock's phase reference is hardware-set,
  once per frame, on the raw data edge (PC0 latch).
- Overshoot is hardware-intrinsic: 658-660 CH1 ticks across no-CLI,
  CLI, re-arm, and one-shot builds. Not interrupts, not entry phase,
  not loop code (supersedes wait_overshoot_ch1_anomaly).
- Entry state measurably changes the envelope: FRAMEGAP re-arm merged
  the 310 us silence HIGH (ripple 3-4, bwidth 551 us); one-shot armed
  on a data edge (ripple 1-2, bwidth 462 us = one full bit).
- The original BITSAMP rej=1 was entry-phase compensation, not a
  decode shortcut. Reproduction confirmed byte-identical I6 is the
  gate that fails on a bad reference edge.
- Gap-gated low-first one-shot built and lint-passed; the high-first
  FRAMEGAP prologue ordering bug is the root of the merged silence.

## 2. Open questions

- Does the gap-gated one-shot arm on the true start burst (gap ~1790,
  bwidth ~260-350 ticks) and pass I6?
- Where exactly does the 114-tick overshoot live: the latch/read idiom
  or an unverified CH1 effective rate? Unmeasured.

## 3. Loose ends

- BITSAMP2, FRAMEGAP (1000/1400), and one-shot variants are probe-only,
  never anchored. Bytes exist in chat, not repo.
- Frame gap never cleanly isolated as a standalone reading; 3437/3474
  include idle + gap.

## 4. Suggested next scope

Run the gap-gated low-first one-shot. If st=3 with ones>=4, byte-identical
decode is achieved from CALL and the remaining work is the overshoot's
home. If st=2 persists with ripple>=1, the entry-phase model needs
reopening against the AGC history facts.

## 5. Ground truth

- docs/anchors/IRPING2.BAS / IRPING2.ASM
- docs/anchors/CH0CAL.ASM
- docs/anchors/ENVSHAPE.BAS
- docs/anchors/BASLOAD.BAS
