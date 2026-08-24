# Handoff — grep_repo read tool (single scope)

Date: 2026-08-24
Scope: design + implement + verify stdlib-pure `read` mode for the
grep_repo MCP tool. No hardware runs.

## Verified this session

- `read` mode landed in refs/pcjr_repo_grep.py: args path + max_lines
  (default 2000); returns path/lines/text/truncated/total_lines with
  1-based line numbering.
- Safety guard verified over MCP:
  - read facts.md max_lines=10 → lines=10, truncated=true, total_lines=346
  - read ../facts.md → ERROR: path traversal refused
  - read refs/pcjr_repo_grep.py → ERROR: path must start with one of
    [facts.md, sessions, docs]
- Real workflow traced in two tool calls: query gap2_1126 → locate fact
  at facts.md:302 + owner session → read the handoff → cross-check
  consistent. No conflict found.
- Option 2 locked: read is stdlib-pure (no git, no subprocess); no
  revs/read_rev modes. History stays paste-first.
- BDS client cached the updated schema after restart; fingerprint now
  includes path + max_lines.
- Memory-selection heuristic recorded: entire memory batch (always +
  called) is injected every turn; keyword gate not pruning because
  trigger tokens are ubiquitous. Only shorter values help. See facts.

## Open questions

- Memory keyword audit: mandatory future pass to evaluate always vs
  called hit behavior and rename keys carrying generic tokens.
  Measurement requires platform telemetry; not possible in-session.
- Platform context re-injection after every MCP call is a BDS-level
  cost; repo-side mitigation is tool_call_discipline + shorter memory
  values, not a code change.

## Loose ends

- pcjr_test_workflow skill read-path table still lists grep_repo as
  query|stats|roots only. Needs a doc update to add read (path,
  max_lines) and retrieval usage examples.
- ENVSHAPE repo-listing dollar-drop correction (carried from
  2026-08-24_agc_profile_probe.md) remains unapplied. Not this scope.

## Suggested next scope

- Mandatory: memory keyword audit (generic-token check, pointer values,
  always vs called evaluation). Static only until platform telemetry.
- Update pcjr_test_workflow read-path table + retrieval examples to
  include read mode.
- Return to deferred hardware scope: threshold pinning batteries
  (merge S=180/190/200/210; recovery S=260/300/340/380).
