# Handoff — pjasm v6.0 A/B/D + integration (single scope)

## Verified this session

- Stage A: IRPING byte-exact, size 61, 3/3.
- Stage B: rel8/rel16/selfloc derivation pinned, 12/12.
- Stage D: table-driven encoder, 81 /7 iw rows, all encode gates pass.
- Local integration: 9/9 via refs/test_pjasm_integration.py.
- LEA16 special forces mod=2 disp16 (fixes size=60 cascade).
- Four D-stage defects fixed: LEA, mov ah/al expectation, disp16
test, cmp r8,imm test logic.

## Open questions

- debug_asm 81 decode still absent; S4B CH0 grid is encode-side only.
- Whether pjasm should become the anchor regeneration path (Stage F).

## Loose ends

- Decoder cut from pjasm; decode remains debug_asm's job.
- mov ah,al canonical form is 88 C4 (rm8,r8); documented in table.
- Integration test files live in refs/, not docs/anchors/.

## Suggested next scope

Stage C prover (hard-rule checks), OR debug_asm 81 decode extension,
OR Stage F anchor replay. Gate each.

## Ground truth

- refs/pcjrasm.py
- refs/test_pjasm_integration.py
- refs/pcjr_asm_debug.py (unchanged authority)
- IRPING (frozen DATA, platform skill Rule 5)