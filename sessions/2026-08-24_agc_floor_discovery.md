# Handoff — AGC silence floor discovery (single scope)

Date: 2026-08-24
Scope: pin the KBDNMI decode mechanism against the observed ed=36, record
the z2 AGC-floor hypothesis, hand off the functional sweep.

## Verified this session

- Deterministic hpress spec built and verified: 20 carrier bursts,
  pulse-for-pulse equivalent to build_frame(0x23)+build_frame(0xA3).
  hpress spec returns ed=36, 2/2.
- Manual taps: 36, 2/2. One transient 38 after percussive contact,
  not reproducible.
- Both boxes hard-reset, Pi pigpiod restarted, breadboard reworked —
  no recovery. Code, Pi runtime, wiring exonerated.
- KBDNMI listing (entries 334-346) manual-verified: time-driven
  biphase decoder on CH1-latched half-bit samples of PC6. Bit valid iff
  halves opposite + odd parity. Phase/parity error → beep, no char.
  Inter-bit merges are functionally invisible to stock decode.
- Two stable merges in every 36 run: H6 (make b4→b5) and H17
  (break b6→b7). Both 157us 0→1 gaps. Break b4→b5 survives (L15=79us)
  because it follows the 1500us frame gap.

## Open questions

- Is zero_silence_2_us=157 the true AGC minimum resolvable silence?
- What is the exact functional margin below 157 before stock decode fails?
- Does the break frame fail before the make frame as predicted
  (2 short-gap sites vs 1)?

## Loose ends

- CRT vertical-hold roll: V-hold pot recovers on light touch
  (oxide/thermal, long on-stretch). Monitor-side, separate. Blocks raw
  transcription until resolved.
- AGCPROBE.BAS contract comment says ed>=4; line 190 tests ed>=3.
  Repo inconsistency, cosmetic.
- agc_biphase memory key superseded by kbdnmi_biphase.

## Suggested next scope (mandatory)

- Resolve CRT vertical hold. Then load AGCPROBE.BAS (AGC1).
- Functional z2 sweep: zero_silence_2 downward through 157,150,140,
  130,120,110,100,90,80us. One trial each, cold, CRT stable.
- Gate on FUNCTIONAL output only, never ed:
  'h' appears → pass; beep/no-char → single-bit error; wrong char →
  two-bit parity-pass error.
- Record per value: h / beep / wrong-char. First beep defines the floor.
- Contract: {"id":"z2_functional_sweep","metric":"functional_char",
  "regression":"AGCPROBE.BAS (AGC1)","recovery":"cold_power_cycle"}

## Ground truth

- docs/anchors/AGCPROBE.BAS
- docs/anchors/CH0CAL.ASM
- docs/anchors/ENVSHAPE.BAS
- IRPING (frozen DATA, platform skill Rule 5)
