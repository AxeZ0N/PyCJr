# Handoff — Envelope Sweep + BUSY100CAL (single scope)

Date: 2026-08-22
Scope: Characterize the 38-vs-40 question with a delay sweep, attempt
to calibrate the BASIC arming delay, and decide the next stage.

## 1. Decisions locked this session (do NOT re-litigate)

- 38 is the true envelope shape of one h make+break. 40 target retired.
- open_3840 refuted: arming window is not the cause of the missing 2
  edges. New candidate = envelope burst-pair merge (hypothesis).
- BUSY100CAL aborted: CH0 single-wrap timer cannot resolve interpreted
  BASIC delays. Multi-wrap ASM only, if ever needed.
- A0 mask/unmask in BASIC is keyboard-safe (Stage 2 passed).
- Wait-for-edge ASM arm is the next stage; the BASIC delay it replaces
  is documented-dead code, not worth further calibration.

## 2. Stage gate record (BUSY100CAL)

- S0  ON ERROR GOTO: PASS via Out of DATA (err 4). 1/0 does NOT trap.
- S1  INP/OUT + CH0 latch/read: PASS (lo=12 hi=205).
- S2  A0 mask/unmask: PASS, keyboard intact.
- S3  float-loop sweep: PASS mechanically, data rejected (float loop
      variable + wrap folds).
- S4  wrap-flag sweep: data rejected; jitter spans multiple 27.5ms
      wraps, single flag undercounts, min-on-raw-dt bug. Aborted.

## 3. Pending doc-sync items (this payload)

- facts.md appends above.
- Anchor listings committed to docs/anchors/ (ENVSHAPE.BAS,
  CH0CAL.ASM) via normal git add + commit.
- BDS memory: envshape anchor updated, busycal_aborted and
  basic_error_handling added; pcjr_doc_sync_pending removed in UI
  (no memory_delete tool).

## 4. Meta-observations

- 1/0 raises no trappable BASIC error on this interpreter. Use Out of
  DATA for any ON ERROR GOTO test.
- ON ERROR GOTO lingers after END and re-enters the handler on prompt
  typos. Always clear with ON ERROR GOTO 0 before END.
- A 27ms wrap timer is the wrong instrument for interpreted-BASIC
  delays. Stop patching, switch tool (ASM multi-wrap) or drop the
  measurement.

## 5. Loose ends & contingencies

- Wait-for-edge ASM arm: spec, stage-gate, and regress against
  ENVSHAPE. Expect ed=38, now deterministic vs Enter->h timing.
- Envelope merge hypothesis: confirm/refute with H/L dump; unverified.
- IRTEST edge probe (A0h D6 timer-2 wrap) still open, low risk.

## 6. Suggested next scopes

1. Wait-for-edge ASM arm on frozen CH0CAL (confirm 38, kill >1s
   sensitivity). Anchor: ENVSHAPE.
2. Envelope merge hypothesis: H/L dump at 0.5s vs >1s, one variable.
3. IRTEST edge probe. Anchor: IRPING.
