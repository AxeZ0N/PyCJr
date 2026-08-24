# Handoff — AGC Profile Probe (single scope)

Date: 2026-08-24
Scope: controlled Pi-side envelope probing of the PCjr IR demod AGC
stage. Frozen CH0CAL ASM + compact AGCPROBE BASIC + Pi harness.

## Verified this session

- AGCPROBE harness + compact BASIC body worked end-to-end after two
  fixes: string $ suffix on x$/h$/l$ (Type mismatch at line 30) and
  single-line dump (multi-line scrolled off screen).
- ASM stayed byte-for-byte frozen. DATA 1000-1100 = ENVSHAPE.
- H envelope is two-regime: 230 us floor for W <= 125 us, then tracks
  ~W + 200 us for W >= 250 us. W_c open between 125 and 250 us.
- L envelope is two-regime: L = max(S - ~180 us, ~79 us). 79 us floor
  matches repo min-L; the ~180 us release delay is W-independent.
- Merge threshold in (157, 220) us. Recovery threshold in (220, 440) us.
- Short-term repeatability <=2 ct on H and L across repeated specs.
- W=250 pair asymmetry: H1=1126 vs H2=1052 at identical stimulus;
  unmodeled, flagged.
- Duty-insensitive over 8-cell train (~3.5 ms); biphase-as-AGC weakened,
  not refuted over the full 11-bit frame.
- gap2_1126 reproduced under control at W=250.
- Stock zero-silences mapped: 220 at recovery floor, 157 merges,
  start_silence 310 also below full recovery; stock amplitude is
  never reliable, timing only.
- Unified demod model: ~230 us min high, ~200 us high extension,
  ~180 us low release, ~79 us min low.
- Decode-floor mechanism partially explained: L component exact;
  in-traffic min-H 170 us still below isolated 230 us floor, open.
- Receiver manual facts recorded: geometry, 8-pin pinout, app-notes
  truncation. No manufacturer/part number; physical inspection is the
  datasheet fallback.

## Open questions

- W_c transition band: sweep 150/175/200/225 us.
- W=250 H asymmetry mechanism: magnitude-dependent recovery, or
  quantization artifact? Single datapoint.
- In-traffic min-H 170 us vs isolated 230 us: recovery attenuation
  compression? Needs tight-silence battery with ed>=2 dump.
- Full 11-bit frame duty test: N=12 or N=16 train (~4.8-7 ms).
- Recovery curve between 220 and 440 us: monotonicity assumed, not
  measured.
- Exact release delay and min-L floor: confirm max() model with a
  tighter S sweep.

## Loose ends

- AGCPROBE body + trials matrix emitted; user transcription complete.
- ed>=3 dump gate discarded merged-high data on S=157/80/40 trials.
  Next probe needs an ed>=2 dump to capture merged envelope width.
- ENVSHAPE skill dollar-drop: BDS runtime cache fixed; repo listing
  still needs the correction applied.
- Gate-0 keypress regression was manual only; not rerun under Pi
  control this scope.

## Suggested next scope

- Threshold pinning, two batteries:
  merge S=180/190/200/210; recovery S=260/300/340/380.
- W_c sweep (150/175/200/225) and the N=12 train.
- ed>=2 dump variant of AGCPROBE for merged-high capture.
