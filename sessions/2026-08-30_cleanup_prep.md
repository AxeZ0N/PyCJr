# Handoff — tooling cleanup and IRPING2 prep

## Verified this session
- BIOS .lst format fully characterized (see `bios_lst_format` fact):
  MASM-style .LST, six line types, PROC NEAR boundaries, `R` =
  relocatable operand, segment override in offset column.
- bios_grep whitespace collapse landed and is live on port 8765:
  `PROC NEAR` single-space now returns 119 hits (was 0). Returned text
  preserves original spacing. None-safe. Three regression tests added;
  grep_selftest and pytest pass.
- IRPING confirmed retired and never-anchored; `session_anchor_policy`
  stale (superseded). IRPING2_MIN designed as its replacement.
- IRPING2_MIN passed the emission gate: `jr build stage=5` clean,
  `jr dis` byte-exact, 56 bytes, all invariants confirmed.
- BASLOAD.BAS read: generic sentinel loader, no embedded IRPING copy.

## IRPING2_MIN — contract
{
"id": "IRPING2_MIN",
"source": "BASLOAD.BAS + IRPING2.ASM",
"expected": { "return": "RETURNED OK", "result_byte": 3 },
"regression": "self (transport-only); CH0CAL stays functional primary",
"recovery": "cold_power_cycle"
}

## IRPING2_MIN — ASM (new program, full listing)

; IRPING2.ASM - minimal transport sanity probe (supersedes IRPING)
; Detect BOTH a high and a low sample of 62h bit 6 in one finite
; masked poll. No timestamps, no decode, no counter. Pass: result=3.
; Origin: org 0, position-independent via selfloc.
; Facts: port C = 62h, IR bit 6 -> facts.md hardware_map;
;        NMI mask/clear/restore -> facts.md nmi_chain_detail.
; Stage: 5 (polling loop, NMI masked). Not a functional decode probe.

option casemap:none
option segment:use16

code segment
    assume cs:code
    org 0

start:
    push cs                  ; Rule 1 bridge: DS = CS
    pop  ds
    push bp                  ; preserve interpreter frame
    call get_ip
get_ip:
    pop  bp                  ; BP = entry + 6
    lea  bp, [bp + 128 - 6]  ; BP = entry + 128 = O+128 (Rule 4 selfloc)

    mov  byte ptr [bp], 0    ; result byte = 0

    mov  al, 00h
    out  0A0h, al            ; mask NMI (D7=0) before touching 62h
    in   al, 0A0h            ; dummy read: clear pending latch

    mov  cx, 0FFFFh          ; finite poll cap, no unbounded arm

poll_loop:
    in   al, 62h             ; 8255 port C
    test al, 40h             ; bit 6 = IR input
    jz   saw_low
    or   byte ptr [bp], 01h  ; saw_high
    jmp  check_done
saw_low:
    or   byte ptr [bp], 02h  ; saw_low
check_done:
    mov  al, [bp]
    cmp  al, 03h
    je   done                ; both edges seen -> early exit
    loop poll_loop

done:
    in   al, 0A0h            ; clear latch
    mov  al, 80h
    out  0A0h, al            ; restore NMI (D7=1) before RETF
    pop  bp
    retf

code ends
end start

## IRPING2_MIN — DATA block (jr build output, byte-exact)

1000 DATA &H0E,&H1F,&H55,&HE8,&H00,&H00,&H5D,&H8D,&H6E,&H7A,&HC6,&H46,&H00,&H00,&HB0,&H00
1010 DATA &HE6,&HA0,&HE4,&HA0,&HB9,&HFF,&HFF,&HE4,&H62,&HA8,&H40,&H74,&H06,&H80,&H4E,&H00
1020 DATA &H01,&HEB,&H04,&H80,&H4E,&H00,&H02,&H8A,&H46,&H00,&H3C,&H03,&H74,&H02,&HE2,&HE7
1030 DATA &HE4,&HA0,&HB0,&H80,&HE6,&HA0,&H5D,&HCB
1040 DATA -1

bin_hex: 0E1F55E800005D8D6E7AC6460000B000E6A0E4A0B9FFFFE462A8407406804E0001EB04804E00028A46003C037402E2E7E4A0B080E6A05DCB

## IRPING2_MIN — runnable BASIC (jr-generated loader)

10 DEFINT A-Z
20 DIM A(66)
30 I = 0 : O = 0 : X$ = "" : B = 0 : D = 0
40 ST = 0 : RI = 0 : FA = 0
50 I = 0
60 READ D
70 IF D = -1 THEN 110
80 POKE VARPTR(A(0)) + I, D
90 I = I + 1
100 GOTO 60
110 PRINT "Loaded "; I; " bytes. Press Enter to CALL..."
120 INPUT X$
130 O = VARPTR(A(0))
140 CALL O
150 PRINT "RETURNED OK"
160 ST = PEEK(VARPTR(A(0)) + 128)
170 RI = PEEK(VARPTR(A(0)) + 130) + 256! * PEEK(VARPTR(A(0)) + 131)
180 FA = PEEK(VARPTR(A(0)) + 132) + 256! * PEEK(VARPTR(A(0)) + 133)
190 PRINT "status="; ST; " rising="; RI; " falling="; FA
200 END

1000 DATA &H0E,&H1F,&H55,&HE8,&H00,&H00,&H5D,&H8D,&H6E,&H7A,&HC6,&H46,&H00,&H00,&HB0,&H00
1010 DATA &HE6,&HA0,&HE4,&HA0,&HB9,&HFF,&HFF,&HE4,&H62,&HA8,&H40,&H74,&H06,&H80,&H4E,&H00
1020 DATA &H01,&HEB,&H04,&H80,&H4E,&H00,&H02,&H8A,&H46,&H00,&H3C,&H03,&H74,&H02,&HE2,&HE7
1030 DATA &HE4,&HA0,&HB0,&H80,&HE6,&HA0,&H5D,&HCB
1040 DATA -1

Gate on printed `loaded 56 bytes` before arming. Pass = `status= 3`.
Arming-swallow property: the Enter key is itself IR; its tail edges
can set both bits, so result=3 proves the link lives, not that a
specific test key was the source. For a distinct-key test, send a
second key after Enter. BASLOAD.BAS also works (fl reads O+128) but
its sv/sg/st lines read stale bytes IRPING2 does not write.

## Open questions
- Does `search_ref` grep mode carry the same OCR-whitespace
  false-negative? Prose backend is pcjr_manual.py; whitespace there is
  justified/hyphenated prose, and query ranked mode shares the matcher.
  Own decision; do not sweep into the BIOS change blindly.
- Are there fully-resolved opcode operands without the `R` suffix
  anywhere in the .lst? Not seen in sampled lines.

## Loose ends
- `docs/jr_tool_spec.md` section 8 fixture names IRPING (61 bytes);
  update to IRPING2_MIN after it passes hardware (open item).
- Platform skill Rule 5 still says "IRPING ... DATA block lives in
  docs/anchors/"; re-import the skill with IRPING2_MIN wording after
  the hardware pass.
- `test_greps.py` docstring still says `python3 -m pytest test_usage.py`
  (stale filename). Cosmetic, pre-existing.
- `compile_pattern` compiles non-hex queries as raw regex with no
  re.escape (metachars like `*`/`?` misbehave). Pre-existing,
  unrelated to whitespace. Next tooling scope.
- facts.md heading hygiene (bare headings, enum drift) pending.
- mcp/test_mcp_jr_smoke.py fixture errors (6 collection errors) pending.
- ENVSHAPE.BAS has no .ASM (BASIC-only delay sweep, likely fine).

## Suggested next scope
- Hardware: run IRPING2_MIN on the PCjr. Expect `loaded 56 bytes`
  then `status= 3` with keyboard intact. If pass: anchor
  IRPING2.BAS/.ASM in the SAME session, update jr_tool_spec section 8
  and skill Rule 5, close the `irping2_transport_regression` decision.
- Then, one of: search_ref whitespace tolerance, smoke-test fixture
  cleanup, or facts.md heading hygiene.

## Ground truth
- No machine-code anchors this session (tooling + emission-gate only).
- IRPING2_MIN is NOT an anchor yet: emission gate passed, hardware
  stage gate not run. Anchor files are created only after a hardware
  pass.
