# Handoff — Tooling Build + Repo Refactor (single scope)

Date: 2026-08-22
Scope: Build the journal tooling (read path + write path) and refactor
the repo into the append-only "living repo" shape. No hardware, no
machine-code emission, no manual lookups this session unless a
fact-migration line is contested.

## 1. Decisions locked this session (do NOT re-litigate)

- No write MCP. A localhost server that can mutate the repo is
  rejected on security grounds. Write access belongs to the user, not
  any tool I can call.
- No new schema (JSON/JSONL). Append-only Markdown with grep-friendly
  headers. Future-proofing comes from less schema, not more.
- Read path is paste-first `git grep`. Zero new attack surface. A
  read-only repo bot is an optional escalation, not the default.
- BDS features stay in their lanes:
  - Skills = durable rules + hardware map + protocol + prohibitions.
  - Project doc = assumptions, always-active rules, open-item IDs.
  - Persona = voice.
  - Memory = hot cache/pointers only, NOT the ledger.
- Repo = source of truth. BDS library = runtime cache. Git wins.
- Memory hygiene: drop the `pcjr_` prefix on all keys. Keep `always`
  keys near-empty.

## 2. Four pending doc-sync items (first facts commit)

1. `carrier_high_us = 13`, `carrier_low_us = 12` — supersedes Rule 8.
   Source: pi_source_verified.
2. ENVSHAPE added to workflow anchor list.
3. `gap2_1126` = stretched envelope H (~471 us), NOT silence, NOT a
   440 us bit cell.
4. `open_3840` closed: 38-vs-40 variance = arming window
   (`for fl=1 to 100`) swallowed frame 1's leading start burst.

## 3. Target repo layout

```

PyCJr/
bds/                      # BDS import package
00_system_prompt.md
10_skills/*.md
20_persona/*.md
30_project/*.md
facts.md                  # append-only fact journal
sessions/                 # append-only narrative per scope
docs/                     # compiled views / archive, regenerable
mcp/  refs/  bin/  pyproject.toml

```

## 4. facts.md convention

Append-only. One fact per heading line. Updates append a new line with
`supersedes:` — never edit old lines.

## 5. Write path — jr-commit.sh (local, user-run)

One-step append+commit. Validates files under facts.md, sessions/, or
docs/ (plus a `--setup` escape for baseline commits). Rejects absolute
paths and `..`.

## 6. Read path — paste-first git grep (primary)

When a fact hasn't been spoken in the session, the assistant states the
grep command and you paste output. A match is evidence, not a clean fact.

Read-only repo bot (Option A) built this session: `grep_repo` MCP tool —
stdlib only, no git binary, no subprocess, fixed roots, loopback bind.

## 7. Session loop (end to end)

1. Start: `git log --oneline -20` + paste latest sessions/*.md handoff.
2. Work: skills govern; stage gates; contracts as now.
3. End: assistant proposes record payload — facts.md appends + session
   file + optional test_log append. You approve, save, run jr-commit.sh.
4. Next session: handoff is already in git.

## 8. Open questions / cheap tests

- skill_create overwrite semantics: update in place, or duplicate?
  Test on the smallest edit (add ENVSHAPE anchor).
- BDS `called` keyword trigger: substring, whole token, or underscore
  split? Two-key experiment in a throwaway turn.
- Repo vs library drift: repo-authoritative; sync after every
  skill_create via a matching repo overwrite.

## 9. Rejected ideas (do not resurrect)

- Write MCP / git-write bot. Rejected: attack surface.
- JSONL facts ledger. Rejected: schema gamble, grep-hostile.
- Value-free skills. Rejected: breaks self-sufficiency on memory miss.
- `pcjr_`-prefixed memory keys. Rejected: keyword matcher poison.

## 10. Baseline commit plan (two commits)

- Commit 1 (machinery): bin/jr-commit.sh, bin/migrate_repo.py,
  bin/grep_selftest.sh, refs/pcjr_repo_grep.py, mcp/pcjr-tools.md.
- Commit 2 (refactor): facts.md, sessions/, bds/* v5, docs/* slimmed,
  README.md, MANIFEST.md.

## Loose ends & contingencies (2026-08-22 close)

- docs/changelog.md: did not exist; created with a v5 entry.
- reconciliation: run bin/migrate_repo.py; it flags max_delta=3528
  stragglers and stale v4 version strings. Fix before committing.
- BDS memory migration is a separate manual track: the no-prefix batch
  still needs explicit approval; old `pcjr_*` keys must be removed by
  the user in the BDS memory UI. The assistant does not write memory
  silently.
- skill_create overwrite semantics test remains open; do it on the
  smallest edit before the big platform skill rewrite.

## Post-baseline wiring (2026-08-22, same session)

The two baseline commits were followed by a third wiring commit:

- `grep_repo` registered in `mcp/pcjr_tools_server.py` (v5; three tools).
- `bin/start_pcjr_mcp.sh` -> `mcp/pcjr_tools_server.py`.
- `bin/byte_selftest.sh` -> `refs/pcjr_asm_debug.py`.
- `bin/grep_selftest.sh` normalized to SCRIPT_DIR.
- All manual fallback commands corrected to `refs/pcjr_ref_tool.py`.
- Server `PCJR_REF_DIR` default derives from the server file location.
- MANIFEST v5 rewrite; README completed.
- `bin/pycjr.py`: `--cc` help = Fn+B; docstring/actual throttle aligned.

The earlier loose-end note "grep_repo requires server registration in
refs/pcjr_ref_mcp.py" is superseded: registration lives in
`mcp/pcjr_tools_server.py` and is already done.

## Ingest cycle test (2026-08-22)

- jr-ingest.sh added; first payload applied end to end.
- Write path verified: facts dedupe, docs append, session append, one commit.
- Remaining manual: add MANIFEST.md row for bin/jr-ingest.sh (not append-friendly; use jr-commit --setup), and delete the pcjr_ch0_clock_status memory key.
