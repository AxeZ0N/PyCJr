# PyCJr

IBM PCjr (4860/4861) + Pi-driven IR keyboard link. Development toolkit,
BDS import package, MCP server, and durable project record in one repo.

## Directory map (v5 living repo)

| Path | Purpose |
|---|---|
| `bds/` | BDS import package (markdown only; the assistant reads this) |
| `facts.md` | Append-only fact journal (values; `supersedes:` lines) |
| `sessions/` | Append-only narrative per scope (`YYYY-MM-DD_scope.md`) |
| `docs/` | Compiled views / archive: test log, CH0 calibration, FAQ, changelog |
| `mcp/pcjr-tools.md` | Server ops: start, env, registration, tool surface |
| `mcp/pcjr_tools_server.py` | The live MCP server (`search_ref`, `debug_asm`, `grep_repo`) |
| `refs/` | Manual strip + Python drivers (verbatim, moved manually) |
| `bin/` | `jr-commit.sh`, `migrate_repo.py`, selftests, server launcher |

## What the assistant can and cannot see

- Sees: `bds/` (imported) + live MCP tools (`search_ref`, `debug_asm`,
  `grep_repo`).
- Does not see: `facts.md`, `sessions/`, `docs/`, `mcp/`, `refs/`,
  `bin/`. Those are for you. Bridge repo state via `grep_repo` calls or
  paste-first `git grep`.

## Session loop

1. Start: `git log --oneline -20` + paste latest `sessions/*.md`.
2. Work: skills govern; stage gates; contracts as now.
3. End: assistant proposes facts.md appends + session file + optional
   `docs/test_log.md` append. You approve, save, run
   `bin/jr-commit.sh "scope: <summary>" facts.md sessions/... docs/...`.
4. Next session: the handoff is already in git.

## One-time baseline commits (historical)

The repo was restaged with the `--setup` escape:

```bash
bin/jr-commit.sh --setup "machinery baseline" bin/... refs/... mcp/...
bin/jr-commit.sh --setup "refactor baseline" facts.md sessions/... bds/... docs/... README.md MANIFEST.md
```

Day-to-day commits stay narrow: `facts.md`, `sessions/`, `docs/` only.

## Single-source policy

`MANIFEST.md` is the canonical artifact inventory — every file labeled
with type, import target, version, and status. Consult it before adding
or moving anything.

Each fact has one owner; everywhere else points, never restates.

- Platform skill owns hardware facts + IR protocol.
- Workflow skill owns retrieval, tooling, stage gates, emission gate.
- Project doc owns always-active rules, assumptions, open items.
- `facts.md` owns single values (append-only; updates use `supersedes:`).
- `docs/ch0_calibration.md` owns CH0CAL method + defects.
- `docs/test_log.md` owns run history (volatile readings).
- `sessions/` owns per-scope narrative and decisions.

