# PyCJr — Changelog

Ordered version history. Repo-resident; not BDS-imported.

## v4 — consolidation

- Renamed project doc `pcjrduino_project.md` -> `pycjr_project.md`;
  project branding `PCJrduino` -> `PyCJr`.
- Decided canonical MCP dispatch: `search_ref` (modes query/peek/stats)
  and `debug_asm` (command dispatch over the former `byte_*` family).
- NMI/keyboard latch clear resolved: dummy READ of `A0h`, manual-verified
  (entries 32/34/35, KBDNMI body 338).
- Added mandatory keyboard re-enable to hard prohibitions: dummy
  `IN A0h`, then `OUT A0h,80h`, before `RETF`; no early exit skips it.
- CH0 input clock closed as empirical 2.38636 MHz; retired 1.19318 MHz.
- CH0 clock single-sourced in platform skill Rule 6 (removed Rule 11
  restatement).
- Removed session readings from skills; Debug Anchor Rule now lists
  anchor identities only.
- Moved CH0CAL derived constants and defects to
  `docs/ch0_calibration.md`.
- Moved open items to `bds/30_project/pycjr_project.md`.
- Converted `docs/anchors_and_gates.md` -> `docs/test_log.md` (run
  history only; gates stay in the workflow skill).
- Dropped `docs/tooling_reference.md`; merged into `mcp/pcjr-tools.md`.
- Adopted single-source policy: one owner per fact, pointers elsewhere.
