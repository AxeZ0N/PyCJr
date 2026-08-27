# Handoff — pjasm MCP tool + debug_asm 81 /7 iw decode (single scope)

## Verified this session

- `pjasm` tool live on pcjr-tools: `assemble` and `selftest` both
  reachable; `selftest` ALL_PASS True (57/57), IRPING byte-exact.
- `debug_asm` v5.3 `81 /7 iw` decode confirmed at MCP level:
  `81 7E 00 DC 00` -> `cmp [bp+0x00],0x00DC` and
  `81 F8 DC 00` -> `cmp ax,0x00DC`.
- `debug_asm selftest` ALL_PASS True after the `iret` OP1 row was
  manually restored (my re-emit had dropped `0xCF: iret`).
- Emission gate holds: golden IRPING round-trip, branch audit, and
  fail-fast decode gates all still pass with `81` in the subset.

## Open questions

- Whether S4B should now proceed to hardware with the CH0 grid, or
  whether the LOOP-constant path (S4A) remains the chosen timing
  mechanism for the next stage.
- Whether `pjasm` should become the anchor regeneration path (Stage F)
  remains undecided.

## Loose ends

- The `iret` decode row lives in `OP1` and is required by selftest;
  my emitted file dropped it and the user restored it by hand. Re-typing
  the asm file must keep `0xCF: "iret"` in `OP1`.
- No `docs/test_log.append.md` for this session: no hardware run, only
  MCP-level tool tests.

## Suggested next scope

S4B CH0-grid hardware run (now unblocked on both encode and decode),
gated by IRPING regression first. OR Stage C prover. OR Stage F
anchor replay via pjasm. Gate each.

## Ground truth

- refs/pcjr_asm_debug.py
- refs/pcjrasm.py
- mcp/pcjr_tools_server.py
- IRPING (frozen DATA, platform skill Rule 5)
