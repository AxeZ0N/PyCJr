# PyCJr — Repo (v5 living repo)

PCjr machine-code bridge and Pi-driven IR keyboard link. This README is
a pointer to the living layout; hard values live in `facts.md`, skills
live in `bds/`, narrative lives in `sessions/`.

## Layout

| Path | What it is |
|---|---|
| `facts.md` | Append-only fact journal (values; `supersedes:` lines) |
| `sessions/` | Append-only narrative per scope (`YYYY-MM-DD_scope.md`) |
| `docs/` | Compiled views / archive: test log, CH0 calibration, FAQ, changelog |
| `mcp/pcjr-tools.md` | Server ops: start, env, registration, tool surface |
| `mcp/pcjr_tools_server.py` | The live MCP server (`search_ref`, `grep_repo`, `jr`) |
| `refs/` | Manual strip + Python drivers (verbatim, moved manually) |
| `bin/` | `jr-commit.sh`, `migrate_repo.py`, selftests, server launcher |
| `bds/` | Import package: system prompt, skills, persona, project doc |

## What the assistant sees

- Sees: `bds/` (imported) + live MCP tools (`search_ref`, `grep_repo`,
  `jr`).

## Tool surface (authoritative)

The registered MCP tools on `pcjr-tools`:

- `search_ref` — manual strip (query / peek / stats)
- `grep_repo` — read-only repo search (query / read / grep_all / stats / roots)
- `jr` — bridge byte pipeline (build / lint / verify / golden / dis / data / parse)

`debug_asm` and `pjasm` are retired. They are not registered on the live
server; `jr` (UASM + NDISASM) is the single construction/lint/review
surface. Historical references to them in `facts.md` and `sessions/` are
append-only records of what was true then, not current API.

## Ingest

User runs `bin/jr-ingest.sh <payload.zip>`. Payload contract lives in
`facts.md` `ingest_payload` and `docs/FAQ.md` (sections 7 and 21).
Repo wins over the BDS cache on any drift.
