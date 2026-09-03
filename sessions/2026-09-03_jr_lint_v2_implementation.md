# Handoff — jr lint v2: engine + config implemented through Phase 3

Date: 2026-09-03
Scope: implement the jr lint v2 refactor through Phase 3 (config
consolidation, read-back). No hardware run.

## Closure marker

This session closed after Phase 3. Phases 4-5 of the spec remain
open and are the next scope. Phase 6 regression was attempted and
produced a measured conflict result (see below); it is not a lint-v2
defect.

## Verified this session

- Phase 0 closed: exact ndisasm renderings pinned via live `jr dis`
  on a synthetic red fragment: `CD21` -> `int 0x21`, `CF` -> `iret`,
  `E661` -> `out 0x61,al`, `8CCB` -> `mov bx,cs`. All three matcher
  strings match spec §13 expectations.
- Phase 1 landed and gated live: stage-0 legality, stage-0 status
  fix (`LINTING SKIPPED` string eliminated), dead-code deletion at
  the old lines 457-459, selfloc message text `R - 6` -> `R - entry`
  in all three rulesets.
- Phase 2 landed: `load_config`, `resolve_rules`, CHECKERS registry
  (prefix/suffix/opcode-count/opcode-absent/before/selfloc/budget),
  `decode()`/`dis()` split, `build` reorders disasm before lint,
  CLI shape/only/skip surface, `--rules` retired.
- Phase 3 landed and read-back verified: 17 rules, unique ids, all
  shape/preset/group references resolve, `version: 2`.

## Open questions

- Phase 4 doc/skill/test updates not done: `docs/jr_tool_spec.md`
  (§2/§4/§6/Stage Gate table), `refs/jr-tools/jr-manual.md`,
  `refs/jr-tools/test_jr.py`, and the test-workflow skill Stage Gate
  table (user-applied, per `skill_create_semantics`).
- Phase 5 MCP schema not done: add `shape`/`only`/`skip`, retire
  `rules`, restart server. User-applied.
- Whether CH0CAL is stale in the same way as IRPING2. Strong
  suspicion by era; not measured this session.
- Whether the `handler`/`iret` shapes have ever been exercised end
  to end under v2 config. Phase 2 code is present but unrun against
  a conforming handler/iret routine.

## Loose ends

- IRPING2 and CH0CAL anchors need Contract-A regeneration with a
  hardware run and a test_log entry. Deferred; not part of lint-v2
  completion. Do not fold into the Phase 4-5 finish scope.
- Two supersedes emitted this session (see facts.append.md).

## Suggested next scope

Finish the jr lint v2 spec: Phase 4 (docs/jr_tool_spec.md,
jr-manual.md, test_jr.py, test-workflow skill Stage Gate table
update - the skill update is user-applied), then Phase 5 (MCP schema
shape/only/skip, retire rules, user restarts server). Do not start
anchor regeneration in that session; keep it a separate follow-on
scope after Phase 4-5 close.

## Ground truth

- `docs/anchors/IRPING2.BAS` / `IRPING2.ASM` - present, byte-
  consistent, but pre-Contract-A (stale; missing ES preservation).
- `docs/anchors/CH0CAL.BAS` / `CH0CAL.ASM` - flagged stale by era;
  not measured this session.
- No new anchors this session; no hardware run.
