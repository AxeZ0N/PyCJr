# Handoff — pjasm v6.1 r8 extension

Date: 2026-08-27
Scope: extend pjasm with the KBDNMI-core r8 shapes and make the
extension visible through the MCP route. Tooling-only; no hardware
run.

## Verified this session

- pjasm v6.1 adds eight shapes: test r8,imm (F6 /0 ib), xor r8,r8
  (32 /r), shr r8,1 (D0 /5 ib), inc r8 (FE /0), dec r8 (FE /1),
  or r8,r8 (0A /r), xchg r8,r8 (86 /r), jnb/jnc (73 rel8).
- Byte-matched against KBDNMI listing: xor ah,ah 32E4; or bh,al 0AF8;
  xchg ah,al 86E0.
- selftest() now merges A+B+D+E; ASM.selftest() returns the full set.
- MCP server green end-to-end: ALL_PASS True with e_* gates present.
- Fixed b_rel8_loop expectation literal 0x3E -> 0xEA (disp = -22).

## Open questions

- MCP tool description string still reads "Stage A/B/D"; update to
  A/B/D/E server-side (cosmetic only).
- Budget impact of the new shapes on ST2C not yet measured.

## Loose ends

- The first v6.1 draft left Stage E in a separate stage_e_selftest()
  wired only into main(); the MCP handler (which calls selftest()
  directly) never saw it. Root cause of the apparent stale-server
  behavior. Corrected by merging the stages.

## Suggested next scope

Emit ST2C: KBDNMI-core on CH0, N=4 trailing confirmation, 5x majority
halves, opposite-halves, odd parity, target 23h for `h`. Regression:
IRPING -> S4B1_ST3B -> DEC1_ST2A.

## Ground truth

- No new hardware anchors this session (tooling-only scope).
- Existing anchors unchanged.
