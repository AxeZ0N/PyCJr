# Handoff — KBDNMI CH1 verbatim clone (single scope)

Date: 2026-08-28
Scope: Resolve the 544/310 conflict using CH1 verbatim, test fixed-grid decode hypothesis, close on failed disproof.

## 1. Verified this session

- CH1 clock = 14.31818/12 = 1.19318 MHz via the 526-tick half-cell constant resolving to exactly 440.8 us. Resolves `kbdnmi_comment_conflicts`; the listing comment "310 us" is wrong. 544 ticks = 456.1 us.
- BITSAMP CH1-verbatim (NMI masked, KBDNMI I30 copied, 544-tick wait, bit0 first-half 5x majority): h -> bit=1 3/3, keyboard intact. Correct decode.
- trail-sample delta 658/658/660 ticks, deterministic to 1 tick.
- The CH0 clock conversion was a real confound: same nominal 456 us target, CH0 read LOW, CH1 reads HIGH.
- CH1 latch/read with NMI masked is keyboard-safe 3/3.

## 2. Open questions

- Why ones=3, not 5? Sample sits on the ragged edge of bit0 HIGH. Where exactly does 544+114 ticks land?
- Why does the CH1 wait loop overshoot 114 ticks (~96 us) while CH0 overshot 77 counts (~32 us)? Shorter loop, more overshoot - unexplained.
- Is the confirmed trailing edge (rej=1 every run) the true demod trailing edge, or one ripple late?
- Is t_r (burst start -> PC6 rise) state-dependent? If yes, no fixed trailing-edge offset can be robust.

## 3. Loose ends

- BITSAMP.BAS/.ASM exist this session but are NOT anchored (thin margin, unexplained overshoot). Do not promote without the overshoot resolved.
- The receiver-chain waveform model (AGC=slow memory, demod=min-pulse one-shot) is a consistency check only, unverified.
- The Visualizer widget is speculative; it cannot produce evidence.

## 4. Suggested next scope

- Instrument the wait-loop cost directly: measure wall-clock per iteration on CH1 vs CH0, pin the overshoot source before trusting any fixed offset.
- Edge-sync probe: arm on start burst, latch CH0 on bit0's own rising edge, 5x majority relative to that edge - removes reliance on the trailing-edge reference entirely.
- IR-test loopback (A0h D6=1): on-board AGC profile via the receiver's own diode, isolates receiver board from Pi emitter. Open item #3.
- Higher-resolution W-sweep to test the min-pulse one-shot model (flat H vs truly linear).

## 5. Ground truth

- IRPING (platform Rule 5 DATA) — regression artifact, not run this session.
- docs/anchors/BASLOAD.BAS
- docs/anchors/CH0CAL.ASM
- docs/anchors/ENVSHAPE.BAS

No new anchors this session. BITSAMP is probe-only.