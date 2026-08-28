# 2026-08-28 · jr_tooling_transition

## Verified this session

- `jr` is the only registered byte-pipeline MCP tool (verified from
`pcjr_tools_server.py` v8 and the live MCP fingerprint):
build/lint/verify/golden/dis/data/parse. `debug_asm` and `pjasm` are
NOT registered. Registered tools: `search_ref`, `grep_repo`, `jr`.
- Inline inputs live-verified: `jr dis bin_hex` decoded 0E1F555DCB;
`jr build asm_text` + `stage:1` returned `bin_hex`/`data_block`/
`bas_source` (see facts `jr_mcp_inline_surface`).
- UASM segment wrapper mandatory; A2082 otherwise. Canonical skeleton
in `docs/jr_tool_spec.md` section 3.3.
- `jr build` defaults to `stage=6`; the selfloc gate (min_stage 2)
rejects a bare stub at exit 4 unless `stage=1` is passed.
- `jr_rules.json` read in full: 11 rules; error vs warn severity;
`min_stage` thresholds (see facts `jr_mcp_inline_surface`).
- Manual peek entries 30-36 (8255 bits, A0h bits, NMI latch,
de-serialization) corroborate the platform-skill hardware map — no
drift.

## Open questions

- None blocking on the tooling transition. ST2C (KBDNMI-core on CH0)
remains unspecced — next scope.

## Loose ends

- `pcjr_payload_generation.md` still says `jr-build` (hyphen) in the
ground-truth line; must be `jr build`.
- Repo docs emitted as fixed drafts (manual apply): `README.md`,
`mcp/pcjr-tools.md`, `mcp/pcjr_tools_server.py` docstring (line ~95
"Prefer pjasm / debug_asm"), `docs/jr_tool_spec.md`.
- `facts.md` and `sessions/` retain append-only `debug_asm`/`pjasm`
history by design; the transition is recorded via `supersedes:` in
fact `jr_mcp_pipeline`, not retro-edits.

## Suggested next scope

1. Apply the repo-doc fixes and the payload-skill `jr-build` fix;
commit via `bin/jr-commit.sh`.
2. Then spec ST2C on the jr pipeline: KBDNMI-core, N=4 trailing confirm,
5x majority halves, opposite-halves, odd parity, target 23h. Gate:
`jr build stage=6` -> `jr dis`.

## Ground truth

No new anchors this session; existing anchors remain valid by name:
IRPING, SHAPE3, STAGE5, CH0CAL, ENVSHAPE, AGCPROBE, DEC1_ST2A (anchor
files `docs/anchors/DEC1_ST2A.BAS` / `DEC1_ST2A.ASM`).