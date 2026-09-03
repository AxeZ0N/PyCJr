# Handoff — jr lint v2: engine + config implemented, anchors found stale

Date: 2026-09-03
Scope: implement the jr lint v2 refactor through engine revamp,
config consolidation, and regression. No hardware run. Phases 4-5
deferred.

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
- Regression run: IRPING2 bytes under v2 bridge stage 6 fails with
  exactly two errors - entry `0E1F5506` vs found `0E1F55E8` and
  epilogue `075DCB` vs found `A05DCB`. No other rule fired. This is
  measured proof the opcode-aware checkers discriminate cleanly.

## Open questions

- Whether CH0CAL is stale in the same way as IRPING2. Strong
  suspicion by era; not measured this session.
- Whether the `handler`/`iret` shapes have ever been exercised end
  to end under v2 config. Phase 2 code is present but unrun against
  a conforming handler/iret routine.

## Loose ends

- Phase 4 (docs/jr_tool_spec.md §2/§4/§6/Stage Gate table,
  jr-manual.md, test_jr.py, test-workflow skill Stage Gate table)
  not done.
- Phase 5 (MCP schema shape/only/skip, retire rules, server
  restart) not done; user-applied.
- Two supersedes emitted this session (see facts.append.md).
- IRPING2 and CH0CAL anchors need Contract-A regeneration with a
  hardware run and a test_log entry - separate scope.

## Suggested next scope

Regenerate IRPING2 and CH0CAL anchors under Contract A (add
`push es` after `push bp`, `pop es` before `pop bp`, plus the
CH0CAL result-store reads), verify byte-match via `jr build` ->
`jr dis` -> `jr lint`, then hardware-verify and record in
`docs/test_log.md`. Do not fold into lint-v2 close.

## Ground truth

- `docs/anchors/IRPING2.BAS` / `IRPING2.ASM` - present, byte-
  consistent, but pre-Contract-A (stale; missing ES preservation).
- `docs/anchors/CH0CAL.BAS` / `CH0CAL.ASM` - flagged stale by era;
  not measured this session.
- No new anchors this session; no hardware run.
