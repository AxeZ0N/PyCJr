# Handoff — jr lint v2 refactor: spec authored, implementation deferred

Date: 2026-09-01
Scope: design and lock the `jr` lint v2 refactor; no implementation, no
config edits, no hardware run. Deliverable is one normative file,
`docs/jr_lint_v2_refactor_spec.md`, which the next session executes.

## Verified this session

- Read `refs/jr-tools/jr.py` in full (724 lines).
- Read all three rulesets: `jr_rules.json`, `jr_rules_handler.json`,
  `jr_rules_iret.json`.
- Read `docs/jr_tool_spec.md` and the latest session handoff
  (`skill_reconcile_int02_irping2`).
- Confirmed `jr_rules.json` is already Contract A (entry `0E1F5506`,
  epilogue `075DCB`, nmi-restore `…075DCB`).
- Confirmed selfloc logic in `jr.py` is already marker-derived
  (`entry = idx + 3`); only message text and spec prose are stale.
- Resolved conflicts C1–C11 into the consolidated spec.
- Locked decisions: strict stays optional and never implied by stage 6;
  `--rules` is retired entirely; A (opcode-aware `absent`) and B
  (`before` deferred, unchanged) are both approved.

## Open questions

- ndisasm exact rendering for `int 21`, `iret`, `out 61` must be pinned
  from a real `jr dis` run before opcode matchers are hardcoded.
  Spec §M.1; this is the retrieval gate for Phase 0.
- Severity escalation of `no-iret`/`no-speaker` to error is confirmed
  but remains a deliberate default-behavior change to flag in facts.

## Loose ends

- `jr_rules_handler.json` and `jr_rules_iret.json` deletion deferred to
  the implementing session.
- Supersedes for `jr_handler_ruleset_added` and `jr_iret_ruleset_added`
  deferred; they must be emitted in the implementing session's payload.
- MCP schema (`shape`/`only`/`skip`, retire `rules`) is user-applied and
  requires server restart; not repo-writable.
- `test_jr.py` and `jr-manual.md` updates deferred to implementation.

## Suggested next scope

Implement the refactor exactly per
`docs/jr_lint_v2_refactor_spec.md`: Phase 0 (pin ndisasm strings) →
Phase 1 (mechanical prep) → Phase 2 (engine) → Phase 3 (config v2) →
Phase 4 (docs/skill/tests) → Phase 5 (MCP, user-applied) → Phase 6
(regression on IRPING2/CH0CAL) → Phase 7 (close, with the two
supersedes and no test_log).

## Ground truth

- `docs/anchors/IRPING2.BAS` / `IRPING2.ASM` — transport regression
- `docs/anchors/CH0CAL.BAS` / `CH0CAL.BAS` — functional primary
  regression (note the repo listing shows the `.BAS`/`.bas` variant the
  latest reconciliation handoff cited; retype only from the anchor dir)
- No new anchors this session; no hardware run.
