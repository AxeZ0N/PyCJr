# PyCJr — Project State (durable record)

Repo-resident durable record. Not BDS-imported. BDS loads the `bds/`
package; this file backs it.

## Provenance

| Item | URL |
|---|---|
| PCjr BASIC manual | https://archive.org/details/pcjr-basic |
| Tech Ref PDF (secondary) | https://www.minuszerodegrees.net/manuals/IBM/IBM%204860%20(PCjr)%20-%20Technical%20Reference.pdf |

The digital-born `refs/deepseek_reference.txt` (479 entries) supersedes
the PDF for lookups; the PDF is the provenance copy.

## File inventory

| Path | Purpose |
|---|---|
| `bds/` | BDS import package: system prompt, skills, persona, project doc |
| `docs/project_state.md` | This file |
| `docs/test_log.md` | Regression/probe run history |
| `docs/ch0_calibration.md` | CH0CAL derivation, derived constants, defects |
| `docs/changelog.md` | Version history |
| `refs/deepseek_reference.txt` | Manual strip (verbatim, user-moved) |
| `refs/pcjr_ref_util.py` | Reference query utility (verbatim) |
| `refs/pcjr_byte.py` | Byte workbench (verbatim) |
| `refs/pcjr_ref_mcp.py` | MCP server entry (verbatim) |
| `mcp/pcjr-tools.md` | Server ops, env, registration, tool surface |
| `bin/` | Server start + selftest scripts |

## Reference tooling (pointer only)

Server: `pcjr-tools` at `http://localhost:8765/mcp`. Canonical dispatch:
`search_ref` (searching) and `debug_asm` (assembly tools). Full surface,
env vars, and registration steps live in `mcp/pcjr-tools.md`. Do not
duplicate those tables here.

## Hardware state (pointer only)

Stable hardware facts live in `bds/10_skills/pcjr_cartridge_basic_asm.md`
Rule 6 (hardware map) and Rule 7 (NMI rules). CH0 clock is empirical and
owned by the skill's hardware map; do not restate values here.

## Research log

- Phase 1 closed: raw IR at `62h` bit 6 verified empirically; PC6
  manual-verified (entry 33).
- Phase 2 closed (CH0CAL): CH0 latched-read edge timestamps verified.
  Safe path `OUT 43h,00h` -> `IN 40h`. Details in
  `docs/ch0_calibration.md`.
- Open items are owned by `bds/30_project/pycjr_project.md`.

## Session hygiene

Each session has one defined scope. Volatile readings — edge counts,
max_delta, gap counts, iteration counts, pass results — live in
`docs/test_log.md` and the session handoff, never in this file or the
skills. When a session scope is done, recommend a new session.
