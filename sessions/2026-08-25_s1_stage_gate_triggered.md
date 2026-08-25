# 2026-08-25 — S1 stage gate triggered (single scope)

Date: 2026-08-25
Scope: close S1 hardware bring-up on catastrophic failure; anchor the
BASLOAD harness; freeze the per-instruction verification plan.

## Verified this session

- Regression: BASLOAD + IRPING passed (61-byte block, transport sane,
keyboard intact after).
- Regression: ENVSHAPE + CH0CAL passed (functional 'h' decode,
keyboard intact; ed reading environmental, not contractual).
- S1 v1 (110 bytes): `loaded 110 bytes`; ~3s after 'h' ->
`Division by zero in (blank)`, dead keyboard. Root cause: bp
clobber (no push/pop bp around selfloc).
- S1 v2 (114 bytes): emission-gate full pass (selfloc pop_offset=6
disp=0x7A, 3/3 branches, decode clean), `loaded 114 bytes`; Pi 'h'
during window -> PCjr reboot into BIOS.
- Stage gate triggered; S1 scope closed. No S1 hardware pass, so no
S1 anchor.
- BASLOAD.BAS earned its anchor (two programs passed through it this
session: IRPING 61B, CH0CAL via ENVSHAPE).
- Skill edits F1-F5 shipped as `skill_patch.diff` in this payload;
applied manually via `git apply`, not through jr-ingest.

## Open questions

- Which exact instruction/sequence in S1 v2 causes the BIOS reboot?
Candidates: NMI enabled with a pending/stale latch, vector install
segment arithmetic, handler DS assumption, or iret on a malformed
stack.
- Did the handler fire and iret into garbage, or did the reboot happen
before the handler? Unobserved.
- What does the saved INT 02h vector read on this machine? Expected
F000:xxxx; never captured cleanly.

## Loose ends

- S1 v1 (110B) and S1 v2 (114B) listings recorded in Ground truth;
neither anchored.
- ON ERROR GOTO NMI re-enable pattern not yet transcribed.
- `wait_outer=24` still uncalibrated; must be calibrated once S1
actually fires without rebooting.
- Skill patch F1-F5 pending manual apply + review. F1 (bp preserve) and
F2 (iret status) are mandatory; F3/F4 are BASLOAD consistency; F5
lands in pcjr_test_workflow.md (emission gate does not prove
hardware safety; S1 v2 is the canonical counterexample).

## Suggested next scope

Per-instruction hardware verification ladder. Start from a known-good
bridge and add one risk class per stage, gating each on the PCjr:

1. Bridge stub: push cs / pop ds / push bp / call get_ip / pop bp /
retf — returns RETURNED OK, keyboard intact, no bp clobber.
2. - selfloc (lea bp,[bp+disp]) and one result store — BASIC reads a
known byte at O+128.
3. - NMI mask/clear/restore: out A0h,00h / in A0h / out A0h,80h —
returns with keyboard alive.
4. - read IVT 0000:0008 / 0000:000A into O+130/O+132 — BASIC prints a
sane F000:xxxx saved vector.
5. - write IVT then immediately restore — returns, no reboot, no
keyboard loss.
6. - enable NMI with a minimal flag-only handler (iret) — fires only
on a real Pi key; flag=1, status=0.
7. Recombine into full S1 and gate.

Each stage: BASLOAD, verify `loaded N bytes`, IRPING then CH0CAL
before any NMI-touching stage, one variable per iteration, cold
recovery on any hang/reboot.

## Ground truth

Anchors by name:

- docs/anchors/BASLOAD.BAS (new this session — generic harness, no
data lines)
- IRPING (frozen DATA, platform skill Rule 5)
- docs/anchors/CH0CAL.ASM
- docs/anchors/ENVSHAPE.BAS
- docs/anchors/AGCPROBE.BAS

New program (not anchored — no hardware pass): S1 v2, 114 bytes.

### S1 v2 ASM (114 bytes, emission-gate-passed, hardware-failed)

org 0
entry:
push cs                  ; 0E
pop ds                   ; 1F
push bp                  ; 55        preserve interpreter BP
call get_ip              ; E8 0000
get_ip:
pop bp                   ; 5D        BP = entry offset + 6
lea bp,[bp+0x7A]         ; 8D AE 7A 00   BP = O+128 (6+122)
mov al,0x00              ; B0 00
out 0xA0,al              ; E6 A0     mask NMI
in al,0xA0               ; E4 A0     clear pending latch
xor ax,ax                ; 31 C0
push ax                  ; 50
pop ds                   ; 1F        DS = 0
mov ax,[0x0008]          ; A1 0800
mov [bp+0x02],ax         ; 89 4602
mov ax,[0x000A]          ; A1 0A00
mov [bp+0x04],ax         ; 89 4604
mov ax,0x0065            ; B8 6500   handler offset
mov [0x0008],ax          ; A3 0800
push cs                  ; 0E
pop ax                   ; 58
mov [0x000A],ax          ; A3 0A00   handler segment = CS
push cs                  ; 0E
pop ds                   ; 1F
mov al,0x80              ; B0 80
out 0xA0,al              ; E6 A0     enable NMI
mov dx,0x0018            ; BA 1800   outer=24
outer:
mov cx,0xFFFF            ; B9 FFFF
inner:
cmp byte [bp+0x00],0x01  ; 80 7E 0001
je fired                 ; 74 09     -> 0x47
loop inner               ; E2 F8     -> 0x38
dec dx                   ; 4A
jne outer                ; 75 F2     -> 0x35
mov byte [bp+0x06],0x01  ; C6 460601 timeout
fired:
mov al,0x00              ; B0 00
out 0xA0,al              ; E6 A0
xor ax,ax                ; 31 C0
push ax                  ; 50
pop ds                   ; 1F        DS = 0
mov ax,[bp+0x02]         ; 8B 4602   restore offset
mov [0x0008],ax          ; A3 0800
mov ax,[bp+0x04]         ; 8B 4604   restore segment
mov [0x000A],ax          ; A3 0A00
push cs                  ; 0E
pop ds                   ; 1F
in al,0xA0               ; E4 A0
mov al,0x80              ; B0 80
out 0xA0,al              ; E6 A0     restore NMI
pop bp                   ; 5D        restore interpreter BP
retf                     ; CB

handler:                         ; offset 0x65
push cs                  ; 0E
pop ds                   ; 1F
in al,0xA0               ; E4 A0
mov al,0x80              ; B0 80
out 0xA0,al              ; E6 A0
mov byte [bp+0x00],0x01  ; C6 460001 flag=1
iret                     ; CF

### S1 v2 DATA

1000 data &h0e,&h1f,&h55,&he8,&h00,&h00,&h5d,&h8d,&hae,&h7a,&h00
1010 data &hb0,&h00,&he6,&ha0,&he4,&ha0,&h31,&hc0,&h50,&h1f,&ha1
1020 data &h08,&h00,&h89,&h46,&h02,&ha1,&h0a,&h00,&h89,&h46,&h04
1030 data &hb8,&h65,&h00,&ha3,&h08,&h00,&h0e,&h58,&ha3,&h0a,&h00
1040 data &h0e,&h1f,&hb0,&h80,&he6,&ha0,&hba,&h18,&h00,&hb9,&hff
1050 data &hff,&h80,&h7e,&h00,&h01,&h74,&h09,&he2,&hf8,&h4a,&h75
1060 data &hf2,&hc6,&h46,&h06,&h01,&hb0,&h00,&he6,&ha0,&h31,&hc0
1070 data &h50,&h1f,&h8b,&h46,&h02,&ha3,&h08,&h00,&h8b,&h46,&h04
1080 data &ha3,&h0a,&h00,&h0e,&h1f,&he4,&ha0,&hb0,&h80,&he6,&ha0
1090 data &h5d,&hcb,&h0e,&h1f,&he4,&ha0,&hb0,&h80,&he6,&ha0,&hc6
1100 data &h46,&h00,&h01,&hcf
1110 data -1