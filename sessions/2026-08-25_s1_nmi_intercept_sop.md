# Session — S1 NMI-intercept stub + deserializer SOP

Date: 2026-08-25
Scope: freeze the custom-deserializer design/test SOP, name the BASIC
harness, build the S1 NMI-intercept stub, pass the emission gate, hand
off the hardware run.

## Verified this session

- BASLOAD.BAS adopted as the PCjr-side BASIC harness identifier.
  Rule 3 "Sentinel Loader" heading is the loader-pattern name and
  stays unchanged; no SENTINEL program name exists. Pi-side
  pycjr_run_test_harness remains a distinct name.
- Anchor tiering: CH0CAL is the primary full-path regression for
  deserializer work. IRPING demoted to transport-only regression;
  frozen DATA stays in Rule 5. Additive, not a supersede.
- debug_asm subset extended (user tool edit): iret CF, push ax 50,
  pop ax 58, mov ax,[moffs16] A1, mov [moffs16],ax A3,
  mov ax,[bp+d8] 8B, mov byte [bp+d8],imm8 C6 /0, dec dx 4A,
  mov dx,imm16 BA, mov ax,imm16 B8. C6 46 d8 imm8 mis-decode
  ("db C6 / inc si") fixed.
- IRET manual-verified (BIOS KBDNMI, entry 338: IN AL,A0h then IRET);
  approved for the handler. No RETF substitute exists — RETF leaves
  FLAGS on the stack and corrupts the caller.
- S1 NMI-intercept stub designed, byte-minimized, and PASSED the
  emission gate: selfloc pop_offset=5 disp=0x007B, branch checks 4/4,
  full decode clean, 110 bytes, zero outside-subset fallbacks,
  handler at 0x61. Image frozen in Ground truth below.
- SOP frozen: contract-first, retrieve-before-emit, S0-S5 ladder,
  emission gate, CH0CAL/IRPING tiering, cold-recovery only.

## Open questions

- Hardware: does S1 return flag=1, status=0, keyboard intact?
  Outer wait count 24 (BA1800) is uncalibrated —
  `; VERIFY: wait_outer count against real arming window`.
- CH0CAL primary-regression pass criterion: confirm functional
  (h decodes, keyboard intact), not exact ed (ed=38 is environmental).
- Stock BIOS make-only / held-key behavior (manual 5-21..5-42):
  unverified. Needed before S5; not blocking S1-S4.

## Loose ends

- BASLOAD.BAS full listing is in Ground truth; not yet a repo file.
  Propose committing docs/anchors/BASLOAD.BAS on first hardware pass
  (needs an ingest-contract decision for a non-anchor harness file).
- SOP not yet filed as docs/custom_deserializer_sop.md; it lives in
  this session file. Propose a docs/ file if it outlives this session.
- selfloc pop_offset semantics trap: pop_offset is BP-after-pop, not
  the result target. Candidate one-line trap note for the test_workflow
  skill (proposal, not locked).
- 8C C8 (mov ax,cs) deliberately left out of the subset; push/pop path
  covers it. Add only if needed later.
- Project doc open-item list should gain a "custom deserializer"
  section; user-owned repo edit, not in this payload.

## Suggested next scope

- Hardware-run S1 (BASLOAD.BAS + S1 DATA block). Regression: IRPING,
  then CH0CAL. One keypress from the Pi during the window.
  Pass: RETURNED OK, flag=1, status=0, keyboard intact.
  On pass: S1 earns docs/anchors/S1.BAS + S1.ASM; advance to S2
  (CH0 latched read inside the NMI handler).

## Ground truth

Anchors by name:
- IRPING (frozen DATA, platform skill Rule 5)
- docs/anchors/CH0CAL.ASM
- docs/anchors/ENVSHAPE.BAS
- docs/anchors/AGCPROBE.BAS

New program (not yet anchored — no hardware pass): S1 NMI intercept.
Full listings below.

### S1.ASM (source)

; S1.ASM — INT 02h NMI intercept stub (110 bytes)
; Origin: loaded at VARPTR(A(0)); entered via far CALL O (Rule 1).
; Assumes: no DOS, CS=DS=SS=BASIC array segment (empirically validated
; by IRPING/CH0CAL anchors via [bp+disp] stores).
; Result map at O+128: [0]=flag, [2]=saved IVT offset, [4]=saved IVT
; segment, [6]=status (0=fired, 1=timeout).

        org 0
entry:
        push cs                  ; 0E        DS=CS
        pop ds                   ; 1F
        call get_ip              ; E8 0000   rel16 -> 0005
get_ip:
        pop bp                   ; 5D        BP=5
        lea bp,[bp+0x7B]         ; 8D AE 7B 00   BP=O+128
        mov al,0x00              ; B0 00
        out 0xA0,al              ; E6 A0     mask NMI (atomic swap)
        xor ax,ax                ; 31 C0
        push ax                  ; 50
        pop ds                   ; 1F        DS=0
        mov ax,[0x0008]          ; A1 0800   read IVT offset
        mov [bp+0x02],ax         ; 89 4602   save offset
        mov ax,[0x000A]          ; A1 0A00   read IVT segment
        mov [bp+0x04],ax         ; 89 4604   save segment
        mov ax,0x0061            ; B8 6100   handler offset
        mov [0x0008],ax          ; A3 0800   install offset
        push cs                  ; 0E
        pop ax                   ; 58        CS -> AX
        mov [0x000A],ax          ; A3 0A00   install segment
        push cs                  ; 0E
        pop ds                   ; 1F        restore DS=CS
        mov al,0x80              ; B0 80
        out 0xA0,al              ; E6 A0     enable NMI
        mov dx,0x0018            ; BA 1800   outer=24 ; VERIFY: calibrate
outer:
        mov cx,0xFFFF            ; B9 FFFF
inner:
        cmp byte [bp+0x00],0x01  ; 80 7E 0001
        je fired                 ; 74 09     -> 0044
        loop inner               ; E2 F8     -> 0035
        dec dx                   ; 4A
        jne outer                ; 75 F2     -> 0032
        mov byte [bp+0x06],0x01  ; C6 460601 timeout status
fired:
        mov al,0x00              ; B0 00     mask NMI for restore
        out 0xA0,al              ; E6 A0
        xor ax,ax                ; 31 C0
        push ax                  ; 50
        pop ds                   ; 1F        DS=0
        mov ax,[bp+0x02]         ; 8B 4602   reload saved offset
        mov [0x0008],ax          ; A3 0800
        mov ax,[bp+0x04]         ; 8B 4604   reload saved segment
        mov [0x000A],ax          ; A3 0A00
        push cs                  ; 0E
        pop ds                   ; 1F
        in al,0xA0               ; E4 A0     clear latch (Rule 10)
        mov al,0x80              ; B0 80
        out 0xA0,al              ; E6 A0     restore NMI
        retf                     ; CB

handler:                         ; offset 0x61
        push cs                  ; 0E
        pop ds                   ; 1F
        in al,0xA0               ; E4 A0     clear latch
        mov al,0x80              ; B0 80
        out 0xA0,al              ; E6 A0     restore NMI
        mov byte [bp+0x00],0x01  ; C6 460001 flag=1
        iret                     ; CF

### S1 hex image (DATA block for BASLOAD.BAS)

1000 DATA &H0E,&H1F,&HE8,&H00,&H00,&H5D,&H8D,&HAE,&H7B,&H00
1010 DATA &HB0,&H00,&HE6,&HA0,&H31,&HC0,&H50,&H1F,&HA1,&H08
1020 DATA &H00,&H89,&H46,&H02,&HA1,&H0A,&H00,&H89,&H46,&H04
1030 DATA &HB8,&H61,&H00,&HA3,&H08,&H00,&H0E,&H58,&HA3,&H0A
1040 DATA &H00,&H0E,&H1F,&HB0,&H80,&HE6,&HA0,&HBA,&H18,&H00
1050 DATA &HB9,&HFF,&HFF,&H80,&H7E,&H00,&H01,&H74,&H09,&HE2
1060 DATA &HF8,&H4A,&H75,&HF2,&HC6,&H46,&H06,&H01,&HB0,&H00
1070 DATA &HE6,&HA0,&H31,&HC0,&H50,&H1F,&H8B,&H46,&H02,&HA3
1080 DATA &H08,&H00,&H8B,&H46,&H04,&HA3,&H0A,&H00,&H0E,&H1F
1090 DATA &HE4,&HA0,&HB0,&H80,&HE6,&HA0,&HCB,&H0E,&H1F,&HE4
1100 DATA &HA0,&HB0,&H80,&HE6,&HA0,&HC6,&H46,&H00,&H01,&HCF
1110 DATA -1

### BASLOAD.BAS (generic harness)

1 ' BASLOAD.BAS — generic sentinel-loader harness (S1 build)
2 ' Loads machine code from DATA, CALLs it, reads the O+128 result map.
3 ' S1 contract: {"id":"S1_NMI_INTERCEPT","source":"BASLOAD.BAS + S1.ASM",
4 '   "expected":{"return":"RETURNED OK","flag":1,"status":0,
5 '   "keyboard_after":"intact"},"regression":"IRPING -> CH0CAL",
6 '   "recovery":"cold_power_cycle"}
10 DEFINT A-Z
20 DIM A(110)
30 I = 0 : O = 0 : D = 0 : X$ = ""
40 FL = 0 : SV = 0 : SG = 0 : ST = 0
50 I = 0
60 READ D
70 IF D = -1 THEN 110
80 POKE VARPTR(A(0)) + I, D
90 I = I + 1
100 GOTO 60
110 PRINT "Loaded "; I; " bytes. Press Enter, then send one key..."
120 INPUT X$
130 O = VARPTR(A(0))
140 CALL O
150 PRINT "RETURNED OK"
160 FL = PEEK(VARPTR(A(0)) + 128)
170 SV = PEEK(VARPTR(A(0)) + 130) + 256 * PEEK(VARPTR(A(0)) + 131)
180 SG = PEEK(VARPTR(A(0)) + 132) + 256 * PEEK(VARPTR(A(0)) + 133)
190 ST = PEEK(VARPTR(A(0)) + 134)
200 PRINT "flag="; FL; " saved="; SV; ":"; SG; " status="; ST
210 END
