# Handoff — skill reconciliation: int02 write-act + IRPING2 stale-text patch specs

Date: 2026-08-31
Scope: emit surgical patch specs so the two skills match the committed
decisions `int02_write_act_safe` and `irping_regression_superseded`.
No hardware run; documentation/edit scope only.

## Verified this session

- Read latest handoff (ivtwr_loop_race) + git log; confirmed
  `int02_write_act_safe` supersede committed at HEAD (a9ee710).
- Retrieved exact skill text via grep_repo; confirmed Rule 7 and Rule 9
  are stale w.r.t. `int02_write_act_safe`.
- Full-repo sweeps `0000:0008` and `IRPING`; isolated every stale spot.
- Facts layer is already consistent: `irping2_transport_regression`,
  `irping2_min_hw_pass`, `irping2_anchor`, `irping_regression_superseded`
  all present; only bds/ skills and docs/bin carry stale text.
- Emitted two patch specs for user application:
  (a) int02 — Rule 7 line ~136, Rule 9 line ~165;
  (b) IRPING2 — Rule 5 block, plus five spots in pcjr_test_workflow
  (Loop Order, Test Contract template, generalization note,
  Anti-Patterns, Debug Anchor Rule).

## Open questions

- Custom INT 02h handler dispatch remains untested and not
  pre-authorized; unchanged by this session.
- bin/byte_selftest.sh: retire outright vs update golden — undecided.

## Loose ends

- Patch specs not yet applied; user applies and re-imports per
  `skill_create_semantics`.
- `jr_tool_spec_fixture_stale` open item remains (unblocks now that
  IRPING2 passed hardware).
- FAQ §17 and byte_selftest.sh were not previously tracked; now
  recorded as open items in this payload.

## Suggested next scope

Apply both patch specs, re-import the two skills, commit. Then close
the three stale-reference open items (jr_tool_spec §8, FAQ §17,
byte_selftest.sh). After that, only if separately authorized: the
custom INT 02h handler dispatch test.

## Ground truth

- docs/anchors/IRPING2.ASM / IRPING2.BAS — transport regression
- docs/anchors/CH0CAL.ASM / CH0CAL.bas — functional primary regression
- No new anchors this session; no hardware run.
