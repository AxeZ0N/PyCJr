# Handoff — Session Conventions + Read Path (single scope)

Date: 2026-08-22
Scope: Close refactor loose ends, lock the handoff convention, and
set first-message read policy.

## 1. Decisions locked this session (do NOT re-litigate)

- Refactor close confirmed: migration clean, memory culled,
  skill_create semantics recorded, MANIFEST row added, ingest cycle
  passed end to end.
- Record payloads go through bin/jr-ingest.sh (COMMIT.txt +
  facts.append.md + sessions/*.md + optional
  docs/test_log.append.md). jr-commit.sh remains for setup/baseline
  commits.
- Memory is fluid. The repo (facts.md, docs) is the ledger; BDS
  memory carries hot pointers only. Memory key count is NOT pinned
  in facts.md.
- No dedicated handoff template file. De-facto structure locked;
  procedure stays copy-newest-and-rename (FAQ 19).
- First message = `git log --oneline -20` + latest sessions/*.md
  handoff ONLY. Repo READMEs are not concatenated.
- Session files reference applicable anchor BASIC/ASM by name; full
  listing only for a new program.
- called-keyword trigger: experiment done, functional for our use.
  No further action.

## 2. Pending doc-sync items

This close is a jr-ingest payload:

- facts.md: append `skill_create_semantics`, `handoff_template`,
  `session_anchor_policy`.
- sessions/: create `2026-08-22_session_conventions_readpath.md`;
  append Close block to
  `2026-08-22_tooling_build_repo_refactor.md`.
- Run: `bin/jr-ingest.sh <payload.zip>`.

## 3. Read path policy (open)

grep_repo roots remain facts.md, sessions/, docs/. Root README.md +
MANIFEST.md sit outside them. Decision pending:

- Option 1 (recommended): add both to grep_repo roots. Change lands
  in mcp/pcjr_tools_server.py; needs a wiring commit.
- Option 2: paste-first only via `git grep`.

## Meta-observations

Tooling/process notes that help the assistant or user. Not code- or
debug-specific. Record only what is not captured above.

- Confirm memory-shaped facts with the user before recording. My
  BDS-memory snapshot drifted this session; the user's memory UI is
  authoritative, not my cached view.
- MCP round-trips re-inject the full BDS header into context. Prefer
  paste-first git grep for a single targeted fact; reserve MCP calls
  for search_ref/debug_asm work that needs them.
- Record behavior, not just closure. When a cheap test closes, write
  the observed mechanism in the same session; "done/functional"
  without the what evaporates.

## Loose ends & contingencies (2026-08-22 close)

- Decide grep_repo root expansion (Option 1 vs 2).

## Suggested next scopes (hardware)

1. IRTEST edge probe. Verify timer-2 IR-test wrap against manual
   2-85..2-89; mask NMI, set A0h D6, finite poll 62h bit 6 with edge
   counters, restore 80h before RETF. Regression anchor: IRPING.
2. Full frame decoder (Phase 3). CH0-latch timestamp per PC6 edge;
   reconstruct 440 us bit cells; decode start + 8 data + parity +
   stop. Custom-decoder context only. Anchor: CH0CAL.
3. TIMER1 41h hazard root cause. Determine whether the keyboard break
   from a latched CH1 read is KBDNMI timer-read theft. NMI masked,
   one variable per iteration. Regression anchor: ENVSHAPE (keyboard
   intact), re-run before/after touching 41h. Unblocks the RAM
   demodulator passthrough.
