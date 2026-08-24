# Handoff — AGCPROBE2 fused-HIGH run triage (single scope)

Date: 2026-08-24
Scope: void the fabricated AGCPROBE2 fused-HIGH battery and hand the
clean re-run setup to the next session.

## Verified this session

- CH0CAL anchor pre-pass caught an 'h' press immediately before the
  battery (transport sane; regression gate passed).
- Harness fired all six fused trials via:
  python3 pycjr.py --run_test trials_high.txt --battery 4 --arm 0.4 --post 3.0
- Trial order and shape (log-confirmed):
  fused100 (62,100)(62,5000) lead=0
  fused130 (62,130)(62,5000) lead=0
  fused157 (62,157)(62,5000) lead=0
  fused160 (62,160)(62,5000) lead=0
  fused165 (62,165)(62,5000) lead=0
  fused170 (62,170)(62,5000) lead=0
- AGCPROBE2 runner = AGCPROBE.BAS with line 190 changed to
  `if ed>=2 then 210` (target 210, not 280).
- Keyboard intact after suite complete.
- The "All runs st=1 ed=2 H:1126 L:N/A" line is the CH0CAL gap2
  anchor reading (stretched envelope H, ~471us), misattributed in the
  voided record.

## Open questions

- Actual per-trial AGCPROBE2 fused values unknown: ed and merged H for
  each of fused100/130/157/160/165/170. No valid transcription exists.

## Loose ends

- AGCPROBE2 fused-HIGH results remain void until a clean re-run is
  transcribed raw, per trial, in firing order.
- AGCPROBE2 is not anchored; it earns docs/anchors/AGCPROBE2.BAS and
  .ASM only after a hardware pass with valid transcription.
- W_c sweep 150/175/200/225 still deferred.

## Suggested next scope (mandatory)

- Re-run trials_high.txt under AGCPROBE2. Before the battery: CH0CAL
  pre-pass (regression), then load AGCPROBE2.
- Transcribe raw per trial: every `st= ed= in= it=` line and every
  `H:` / `L:` line, in firing order, no summaries, no "typical",
  no skipping empty H/L. Unreadable digit -> `?`.
- Expected per trial: st=1, ed=2, single merged H value, dump present.

## Ground truth

- docs/anchors/AGCPROBE.BAS (ed>=3 parent of AGCPROBE2)
- docs/anchors/CH0CAL.ASM
- docs/anchors/ENVSHAPE.BAS
- IRPING (frozen DATA, platform skill Rule 5)
