# PyCJr

IBM PCjr (4860/4861) + Pi-driven IR keyboard link. Development toolkit,
BDS import package, MCP server, and durable project record in one repo.

## Directory map

| Path | Purpose |
|---|---|
| `bds/` | BDS import package (markdown only; the assistant reads this) |
| `docs/` | Durable record: project state, test log, CH0 calibration, changelog |
| `mcp/pcjr-tools.md` | Server ops: start, env, registration (human-facing) |
| `refs/` | Manual strip + Python drivers (verbatim, moved manually) |
| `bin/` | Server launcher + byte-workbench selftest |

## What the assistant can and cannot see

- Sees: `bds/` (imported) + the live MCP tool surface (`search_ref`,
  `debug_asm` once implemented).
- Does not see: `docs/`, `mcp/`, `refs/`, `bin/`. Those are for you.
  Bridge volatile state to the assistant via the session handoff.

## Keys to the label scheme

`MANIFEST.md` is the canonical artifact inventory — every file labeled
with type, import target, version, and status. Consult it before adding
or moving anything.

The single-source policy: each fact has one owner; everywhere else
points, never restates.

- Platform skill owns hardware facts and IR protocol.
- Workflow skill owns retrieval, tooling, stage gates, emission gate.
- Project doc owns always-active rules, assumptions, open items.
- `docs/ch0_calibration.md` owns CH0CAL-derived constants and defects.
- `docs/test_log.md` owns run history (volatile readings).
