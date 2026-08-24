# Handoff — threshold pinning (single scope)

Date: 2026-08-24
Scope: pin the W=62us burst-pair fuse and recovery thresholds at PC6,
resolve the W=250 asymmetry and the L-overshoot anomalies, close the
38-edge root cause.

## Verified this session

- CH0CAL anchor passed before every battery (three runs, three passes).
- Fuse: (170,175]us. Merge battery S=180–210 all ed=4; pinning battery
  S=160/165/170 ed=2, S=175 ed=4 (H2/H1=0.74).
- Recovery: (230,240]us. S=220/230 at 0.87, S=240+ at 1.00.
- H2/H1 staircase: only 0.74 / 0.87 / 1.00 across all S. Discrete AGC
  recovery states, not RC ramp.
- L staircase: 334 / ~404 / 476ct, jumps at 310→320 and 335→340, steps
  ~30us. Systematic (reproduced across two batteries).
- W=250/S=5000 asymmetry retired: four repeats, three symmetric.

## Open questions

- L staircase mechanism: receiver-side quantization vs probe code-path
  latency. Unverified.
- ed=2 merged-high width still unmeasured (BASIC ed>=3 gate blocks dump).
- Whether the quantized AGC is a discrete gain-stage ladder in the
  SN76496 receive path or an artifact of the demod comparator.

## Loose ends

- AGCPROBE ed>=2 dump variant not implemented (merged-high capture).
- W_c sweep 150/175/200/225 and N=12 train deferred from prior scope.
- bin/pycjr.py stale copy still needs sync or removal.
- refs/pcjr_repo_grep.py docstring still shows --run-test (hyphen).

## Suggested next scope

- Implement AGCPROBE ed>=2 variant; capture fused-pair merged-high
  width at S<=157us.
- Probe the L-staircase mechanism with a single-edge W-sweep under
  NMI-masked conditions.

## Ground truth

- CH0CAL.ASM -> docs/anchors/CH0CAL.ASM (design logic)
- ENVSHAPE.BAS -> docs/anchors/ENVSHAPE.BAS (frozen BASIC runner)
- AGCPROBE.BAS -> docs/anchors/AGCPROBE.BAS (probe capture variant)
- Agreement: ENVSHAPE.BAS and AGCPROBE.BAS DATA blocks byte-match
  CH0CAL.ASM; regenerate via debug_asm, never hand-roll.
