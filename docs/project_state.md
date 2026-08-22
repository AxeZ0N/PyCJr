# PyCJr — Project State (durable record) (v5)

Repo-resident durable record. Not BDS-imported. BDS loads the `bds/`
package; this file backs it.

## Provenance

| Item | URL |
|---|---|
| PCjr BASIC manual | https://archive.org/details/pcjr-basic |
| Tech Ref PDF (secondary) | https://www.minuszerodegrees.net/manuals/IBM/IBM%204860%20(PCjr)%20-%20Technical%20Reference.pdf |

The digital-born `refs/deepseek_reference.txt` (479 entries) supersedes
the PDF for lookups; the PDF is the provenance copy.

## File inventory (pointer)

See `README.md` and `MANIFEST.md`. Do not duplicate the table here.

## Facts and sessions

- Values: `facts.md` (append-only; updates use `supersedes:`).
- Narrative: `sessions/YYYY-MM-DD_scope.md`.
- Run history: `docs/test_log.md`.

## Hardware state (pointer only)

Stable hardware facts live in `bds/10_skills/pcjr_cartridge_basic_asm.md`
Rule 6 (hardware map) and Rule 7 (NMI rules). CH0 clock is empirical and
owned by the skill's hardware map; do not restate values here.

## Research log (pointer)

- Phase 1 closed: raw IR at `62h` bit 6 verified empirically; PC6
  manual-verified (entry 33). See `facts.md`.
- Phase 2 closed (CH0CAL): CH0 latched-read edge timestamps verified.
  Safe path `OUT 43h,00h` -> `IN 40h`. See `docs/ch0_calibration.md`.
- Open items are owned by `bds/30_project/pycjr_project.md`.

## Session hygiene

Each session has one defined scope. Volatile readings — edge counts,
max_delta, gap counts, iteration counts, pass results — live in
`facts.md`, `docs/test_log.md`, and the session handoff, never here or
in the skills. When a session scope is done, recommend a new session.
