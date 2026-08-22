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
| `refs/` | Manual strip + Python drivers (verbatim, moved manually) |
| `bin/` | `jr-commit.sh`, `migrate_repo.py`, `grep_selftest.sh`, server launcher |

## What the assistant can and cannot see

- Sees: `bds/` (imported) + live MCP tools (`search_ref`, `debug_asm`,
  `grep_repo`).
- Does not see: `facts.md`, `sessions/`, `docs/`, `mcp/`, `refs/`,
  `bin/`. Those are for you. Bridge repo state via `grep_repo` calls or
  paste-first `git grep`.

## Two baseline commits (one-time)

```bash
bin/jr-commit.sh --setup "machinery baseline" bin/... refs/... mcp/...
bin/jr-commit.sh --setup "refactor baseline" facts.md sessions/... bds/... docs/... README.md MANIFEST.md
```

## Session loop

1. Start: `git log --oneline -20` + paste latest `sessions/*.md`.
2. Work: skills govern; stage gates; contracts as now.
3. End: assistant proposes facts.md appends + session file + optional
