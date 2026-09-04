# Handoff — jr lint v2 phase 4-5: docs, tests, MCP surface, boundary fix

Date: 2026-09-04
Scope: finish the jr lint v2 refactor through Phase 4 (docs/tests/skill)
and Phase 5 (MCP schema). No hardware run. Prior session closed after
Phase 3.

## Verified this session

- Phase 4 landed: `docs/jr_tool_spec.md` v2 (Contract-A skeleton with
  `R − 7` selfloc arithmetic, v2 config schema, shape rule sets, stage
  gate table with stage 0 row, strict orthogonal),
  `refs/jr-tools/jr-manual.md` (`--shape`/`--only`/`--skip`,
  `--rules` retired, `R − 7` quick-start), and
  `refs/jr-tools/test_jr.py` updated and passing 10/10.
- Fixture correction measured: Contract-A entry offset is 7, so
  selfloc disp = 121 (`79 00`); the prior fixtures carried 122. F2
  expected-disp assertion updated to 121.
- F9 drift measured: `--rules` argparse returns rc=2, not rc=1; the
  engine's friendly `use --shape` message is unreachable on the CLI
  path.
- Phase 5 landed: MCP `jr` schema now exposes `shape`/`only`/`skip`
  and no `rules`; both build and lint call sites patched.
- shape=None boundary bug found and fixed: `shape=shape or "bridge"`
  at both call sites. Verified pass on a bare lint call after the fix.

## Open questions

- Whether `handler`/`iret` shapes have been exercised end-to-end under
  the v2 config. Phase 2 code is present but unrun against a
  conforming handler/iret routine.
- Whether the engine guard diagnostic (`--stage is valid only for
  shape=bridge` when shape is None) should be tightened, or left alone
  after the boundary fix.
- Whether `--rules` retirement should be brought to spec behavior
  (friendly error) or the spec updated to match the measured
  argparse rc=2 + MCP silent-drop reality.

## Loose ends

- IRPING2 and CH0CAL anchors are pre-Contract-A/stale. Phase 6
  regression relint against v2 is not yet done; Contract-A anchor
  regeneration is a separate follow-on with a hardware run and
  test_log entry.
- CH0CAL staleness not measured; strong suspicion by era.
- Two supersedes emitted this session (`jr_handler_ruleset_added`,
  `jr_iret_ruleset_added`) point at deleted files.
- Test-workflow skill Stage Gate table correction was emitted as a
  separate correction file earlier; the skill re-import is
  user-applied per `skill_create_semantics`.

## Suggested next scope

Close the jr-tools refactor: Phase 6 regression — relint IRPING2 and
CH0CAL against the v2 config and record pass/fail; resolve the
`--rules` retirement drift (either implement a friendly argparse error
or update the spec to the measured behavior); optionally exercise
`handler`/`iret` shapes end-to-end; optionally tighten the engine
guard diagnostic.

Then a separate follow-on: Contract-A anchor regeneration for IRPING2
and CH0CAL with a hardware run and test_log entry. Do not fold into
the Phase 6 session unless separately authorized.

## Ground truth

- `docs/anchors/IRPING2.BAS` / `IRPING2.ASM` — pre-Contract-A (stale;
  missing ES preservation).
- `docs/anchors/CH0CAL.BAS` / `CH0CAL.ASM` — flagged stale by era; not
  measured.
- No new anchors this session; no hardware run.
