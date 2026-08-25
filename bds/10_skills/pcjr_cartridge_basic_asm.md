# IBM PCjr Cartridge BASIC & 8088 Assembly — Canonical Verified Skill (v5)

## Activation

Use whenever the user requests code or design help for the IBM PCjr
(4860/4861), PCjr Cartridge BASIC, PCjr 8088 assembly, or the PyCJr
IR link.

- Repo is source of truth; BDS library is a runtime cache. Git wins on
  drift. Session-fresh readings live in `docs/test_log.md` and
  `facts.md`, never here.

## Target Platform

- CPU: Intel 8088 @ 4.77 MHz, 16-bit real mode
- BASIC: IBM Cartridge BASIC (PCjr-specific), NOT generic BASICA/GW-BASIC
- OS: optional PC-DOS 2.1; Cartridge BASIC runs from cartridge without DOS

## Primary Sources

1. IBM PCjr Technical Reference — November 1983, First Edition Revised.
   Digitized strip, accessed through the `pcjr-tools` MCP server
   (`search_ref` / `debug_asm`).
2. IBM PCjr BASIC Reference — June 1983.
3. Ralf Brown's Interrupt List (RBIL) Release 61.

The skill is a fast-path summary. The Technical Reference is the
authority, but the strip is noisy OCR. Label facts `manual-verified`,
`empirical`, `unverified`, or `conflict`.

## Manual Locator

| Topic | Manual Location |
|---|---|
| Processor, performance, 8259A interrupt controller | 2-13 to 2-16 |
| 64KB RAM, ROM subsystem | 2-17 to 2-19 |
| I/O channel, system board I/O | 2-21 to 2-29 |
| 8255 bit assignments | 2-30 |
| Cassette interface | 2-39 |
| Video/graphics subsystem, palette, lightpen | 2-43 to 2-74 |
| Beeper, sound, SN76496, audio tone generator | 2-85 to 2-89 |
| Infra-Red Link, receiver | 2-97 |
| Cordless keyboard, transmitter | 2-101 to 2-103 |
| Program cartridge and interface | 2-107 to 2-114 |
| Games interface, joystick | 2-119 to 2-122 |
| Serial port RS232 | 2-125 to 2-130 |
| System power supply | 2-135 |
| BIOS usage, vectors, memory map | 5-5 to 5-13 |
| Keyboard encoding and usage | 5-21 to 5-42 |
| BIOS cassette logic | 5-47 to 5-51 |
| ROM BIOS listing | Appendix A |
| Characters, keystrokes, color | Appendix C |

## Rule 1 — Machine-Code Bridge (Hard Rule)

Use exactly this contract. No exceptions:

```basic
DEF SEG          ' code segment
O = VARPTR(A(0)) ' offset
CALL O           ' far call
```

The called machine routine MUST:

- start with `PUSH CS` / `POP DS`
- preserve BP: `PUSH BP` at entry (after `POP DS`), `POP BP`
immediately before `RETF`. Clobbering BP corrupts the Cartridge
BASIC interpreter frame and yields `Division by zero in (blank)`
with a dead keyboard — unrecoverable, cold power-cycle only.
(empirical, 2026-08-25, S1 v1)
- end with far `RETF` (opcode `0CBh`)

Never emit `CALL ABSOLUTE` (it evaluates to 0 in Cartridge BASIC and
calls offset 0 — hangs the machine). Never emit `USR0` (black-screens
the PCjr).

## Rule 2 — Variable Ordering (Hard Rule)

- Pre-declare every scalar before `O = VARPTR(A(0))`.
- Creating any variable after `VARPTR` moves the array and invalidates `O`.
- `DEFINT` literals must not exceed 32767; use `DEFDBL` for values that
may overflow.

## Rule 3 — Sentinel Loader (Mandatory Pattern)

Never use a manual byte-count loader. A wrong count omits the final
`RETF` and hangs. Always terminate `DATA` with `-1`:

```
10 DEFINT A-Z
20 DIM A(70)
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
170 RI = PEEK(VARPTR(A(0)) + 130) + 256 * PEEK(VARPTR(A(0)) + 131)
180 FA = PEEK(VARPTR(A(0)) + 132) + 256 * PEEK(VARPTR(A(0)) + 133)
190 PRINT "status="; ST; " rising="; RI; " falling="; FA
200 END
1000 DATA ...  ' machine-code bytes here
1010 DATA -1
```

Canonical harness: docs/anchors/BASLOAD.BAS (no machine code, no
DATA lines; append a program's DATA at 1000+). Gate every run on the
printed `loaded N bytes` count; it discriminates DATA blocks. Size
the array to cover code length + 128 for the result region.

## Rule 4 — Position-Independent Result Storage (Mandatory)

Never store machine-code results at a hardcoded DS offset. Locate the
entry point at runtime:

```
    call get_ip              ; E8 00 00
get_ip:
    pop  bp                  ; 5D  BP = entry offset + 6
    lea  bp, [bp + 128 - 6]  ; 8D AE 7A 00  BP = entry offset + 128
```

Results go at `O+128`, matching `PEEK(VARPTR(A(0))+128)` in BASIC.

## Rule 5 — IRPING Regression Artifact

IRPING is the frozen 61-byte raw IR edge sampler that first verified
port `62h` bit 6. Re-run it first whenever hardware behavior changes or
new machine code misbehaves. If IRPING passes, the transport is sane and
any new bug is in the new code, not the link.

IRPING stage-5 DATA (61 bytes, 30000 loops):

```
1000 DATA &H0E,&H1F,&H55,&HE8,&H00,&H00,&H5D,&H8D,&HAE,&H7A,&H00
1010 DATA &HBA,&H62,&H00,&HEC,&H24,&H40,&HB4,&H00,&H89,&H46,&H00
1020 DATA &H89,&HC6,&HB9,&H30,&H75,&H31,&HDB,&H31,&HFF,&HBA,&H62
1030 DATA &H00,&HEC,&H24,&H40,&H39,&HF0,&H74,&H0A,&H85,&HF6,&H74
1040 DATA &H03,&H47,&HEB,&H01,&H43,&H89,&HC6,&HE2,&HEA,&H89,&H5E
1050 DATA &H02,&H89,&H7E,&H04,&H5D,&HCB
1060 DATA -1
```

Expected pass: send one key from the Pi during the window; `rising>0`
and `falling>0`, `status=0` or `64`.

## Rule 6 — Hardware Map with Verification Status

| Register ↕▾ ↕▾ ↕▾ | Address ↕▾ ↕▾ ↕▾ | Purpose ↕▾ ↕▾ ↕▾ | Status ↕▾ ↕▾ ↕▾ |
|---|---|---|---|
| −−−PORT_A | 60h | 8255 Port A output | Confirmed + manual-verified |
| −−−PORT_B | 61h | 8255 Port B output | Confirmed + manual-verified |
| −−−PORT_C | 62h | 8255 Port C input | Confirmed + hardware-verified |
| −−−CMD_PORT | 63h | 8255 control | Confirmed |
| −−−TIMER0 | 40h | 8253 counter 0 (CH0). Input clock 2.38636 MHz (14.31818/6 = CPU/2), empirical | Confirmed; clock empirical |
| −−−TIMER1 | 41h | 8253 counter 1 (keyboard de-serialize; 1.1925 MHz clk when A0h D5=0) | manual-verified (entries 31/34) |
| −−TIMER2 | 42h | 8253 counter 2 (sound source; IR test 40 kHz when A0h D6=1) | manual-verified (entries 31/34) |
| −−TIM_CTL | 43h | 8253 control | Confirmed |
| −−NMI_PORT | A0h | NMI mask / control | Confirmed + manual-verified |
| −−INTA00 | 20h | 8259 PIC | Confirmed |
| −−INTA01 | 21h | 8259 PIC | Confirmed |
| −⚙ |  |  |  |
| −⚙ |  |  |  |
⚙

Note: empirical values above are last-known. Session-fresh readings live
in `docs/test_log.md` and `facts.md`; BDS memory supersedes if loaded.

8253-5 decode: A6=1, A1/A0 select 40h-43h. Manual `Hex Range` print
(40-47) is a formatting conflict; 44h-47h alias unverified.
`; VERIFY: 44h-47h decode against PCjr Technical Reference`

Latch commands via 43h: CH0=00h, CH1=40h, CH2=80h (SC=D7/D6,
RL=D5/D4=00). NEC uPD8253; no 8254 read-back.

### 8255 Port A (60h) — output

Manual text: PA0-PA7 are "Reserved for Keystroke Storage".
Status: manual-verified.

### 8255 Port B (61h) — output

Manual text:

- PB0 `+Timer2 Gate (Speaker)`
- PB1 `+Speaker Data`
- PB2 `+Alpha (-Graphics)`
- PB3 `+Cassette Motor Off`
- PB4 `+Disable Internal Beeper and Cassette Motor Relay`
- PB5 `SPKR Switch 0`
- PB6 `SPKR Switch 1`
- PB7 `Reserved`

Status: manual-verified. OCR may have mangled the exact `+`/`-`
prefixes; read with caution.

### 8255 Port C (62h) — input

Manual text:

- PC0 `Keyboard Latched`
- PC1 `-Internal MODEM Card Installed`
- PC2 `-Diskette Drive Card Installed`
- PC3 `-64KB Memory and Display Expansion Installed`
- PC4 `Cassette Data In`
- PC5 `Timer Channel 2 Output`
- PC6 `+Keyboard Data` — hardware-verified raw IR bit
- PC7 `-Keyboard Cable Connected`

Status: PC6 = empirical + manual-verified. PC0 = `Keyboard Latched`.

### NMI mask / control register (A0h) — output

```
Write to Port A0
D7 = ENA NMI
D6 = IR TEST ENA
D5 = SEL CLK1 INPUT
D4 = +Disable HRQ
```

Status: manual-verified.

## Rule 7 — NMI Rules

- Keyboard NMI vectors through interrupt `02h` at `0000:0008` -> KBDNMI.
manual-verified (BIOS listing, entries 233/338).
- Keyboard latch = 8255 PC0. Set on the first rising edge of the keyboard
data stream (manual-verified, entry 32); entry 35 reads "set by any
key being pressed." Same physical latch.
- The latch causes NMI only if A0h D7 (Enable NMI) = 1 (manual-verified,
entry 34).
- Clear = dummy READ of port A0h. No data is presented to the CPU during
this read (manual-verified, entries 32/34/35; KBDNMI body entry 338
does `IN AL,0A0h` before `IRET`). Clear before another NMI can be
received. RESOLVED.
- NMI mask bits live at A0h, NOT at 8255 Port A 60h.
- Normal operating value: OUT A0h,80h (D7=1, D6=0, D5=0, D4=0).
Manual-derived + empirical (STAGE5 restore 80h, keyboard fine after).
- A0h D5: 0 = 1.1925 MHz clk to timer 1 (keyboard de-serialization);
1 = timer 0 output as clk to timer 1 (time-of-day overflow catch
during masked diskette ops). manual-verified (entry 34).
- IRET (CF) is architecturally the only correct NMI-return primitive:
RETF leaves FLAGS on the stack and corrupts the caller
(manual-verified, BIOS KBDNMI entry 338 ends IN AL,A0h then IRET).
Empirically, no CALL O bridge program using IRET has yet passed
hardware; S1 v2 rebooted into BIOS with cause undiagnosed. IRET
stays `unverified` in the bridge until the per-instruction ladder
anchors it.

## Rule 8 — IR Protocol Frozen Facts

These are empirical. Cross-check against the manual before changing the
emulator.

- Pi driver is active-high: pin LOW = LED off/idle, pin HIGH = LED on.
- Carrier 40 kHz: 13 us high / 12 us low; burst ~62 us.
(Supersedes the earlier 12/13 swap; see `facts.md` `carrier_high_us`.)
- Emitter timings (silence between bursts, not burst duration):
`start_silence_us=310`, `one_silence_us=377`,
`zero_silence_1_us=220`, `zero_silence_2_us=157`,
`frame_gap_us=1500` (safe floor). One/zero cell ~439 us,
start ~372 us.
- Frame spec (manual-verified, entry 94): bit cell 440 us (OCR `ps`),
start + 8 data + parity + stop = 11 bits, odd parity, 40 kHz burst,
50% duty, burst ~62.5 us (noisy diagram), 11 stop bits after scan
~4840 us.
- Stop bit = logical 1, 440 us (manual entry 94). The emitter omits the
stop burst; the 1500 us frame_gap serves as the stop period. Stock
receiver decodes; stop carrier not required (inference, unverified).
- Parity always odd. `none` fails (9th bit required). Odd/even both
empirically work; odd is conservative.
- Every keypress = make frame + break frame (break = scancode | `80h`).
`h` = `23h`/`A3h`.
- Stock ceiling ~86 chars/sec with assembly `INT 16h` drain. Pure
`INKEY$` drains too slowly for dense bursts.
- `SHIFT_SCAN=2Ah` verified. `FN_SCAN=54h` verified.
PCjr Ctrl+Break = Fn+B (`54h`+`30h`).
- Emitter invariants: always make+break, no typematic, no lock-state
tracking, atomic Shift, one key per wave.

## Rule 9 — Development Methodology

Build incrementally, one risk class per stage:

1. Bridge stub (`PUSH CS` / `POP DS` / `RETF`)
2. Self-location + one array write
3. Three explicit result stores
4. One `IN` from target port
5. Polling loop with edge counters
6. Full capture

If a stage hangs, the defect is in the bytes added in that stage.
Cold power-cycle is the reliable recovery; never assume Ctrl+Alt+Del
recovers. Flag unverified values with
`; VERIFY: value against PCjr Technical Reference`.

## Rule 10 — Failure Mode Prohibitions

Never emit:

- `CALL ABSOLUTE` or `USR0`
- CGA planar/bitplane code (PCjr 16-color video is packed-pixel,
2 pixels/byte)
- `OUT 61h` PC speaker toggles (sound is TI SN76496)
- `INT 21h` unless DOS is confirmed loaded
- IBM PC ROM addresses (`F6000`, etc.); PCjr regions are `F0000`
(Cassette BASIC), `E8000` (cartridge selects), `FFFFF`
(BIOS/diagnostics)
- Count-based machine-code loaders
- Hardcoded DS offsets for results
- Variables created after `VARPTR(A(0))`
- Any machine-code path that returns without re-enabling the keyboard

Mandatory keyboard re-enable before `RETF` (no early exit may skip it):
dummy `IN AL,0A0h` (clear latch), then `OUT 0A0h,80h` (restore NMI).
80h is empirical (STAGE5: keyboard fine after restore).

## Rule 11 — Research Track State

- Phase 1 closed: raw IR at `62h` bit 6 verified empirically; PC6
manual-verified (entry 33: cable if attached, else IR receiver).
- Phase 2 closed (CH0CAL): CH0 latched-read edge timestamps work.
Safe path: `OUT 43h,00h` (latch CH0) -> `IN 40h`. No bare `IN` on any
counter port.
- CH0 input clock: EMPIRICAL 2.38636 MHz. Single source in Rule 6 map;
do not restate elsewhere. Manual strip is silent; do not promote to
manual-verified.
- TIMER1 `41h` HAZARD: never latch/read `41h` with keyboard NMI active
(A0h D7=1). T2 empirical: latched CH1 read broke the keyboard (beep,
no chars). KBDNMI reads `41h` each keystroke (manual, entry 338).
Mechanism (BIOS timer read stolen during de-serialization) is
hypothesis.
- Keyboard dispatch chain (manual-verified 233/338): IR -> NMI INT02
= KBDNMI de-serializes (samples 62h bit 6, reads 41h), then INT 48h
KEY62-INT translates 62->83 key, OUT 60h + INT 09h KBINT buffers.
KBDNMI -> KEY62-INT -> KBINT.

Derived constants (poll-loop quantization, F000h budget, gap readings)
and open items live outside this skill; see the project doc and
`docs/ch0_calibration.md`.

## Rule 12 — Manual Lookups

Manual lookups use the Retrieval Protocol in `pcjr_test_workflow`.

The digitized manual is authoritative but noisy. If a query conflicts
with measured behavior, record both and do not silently override either.
Never claim a manual value was verified without search_ref output or
pasted user output.

## Anchors

Anchor ground truth lives in `docs/anchors/`, never in this skill.

- ENVSHAPE.BAS  -> docs/anchors/ENVSHAPE.BAS   (frozen BASIC runner)
- CH0CAL.ASM    -> docs/anchors/CH0CAL.ASM     (design logic)
- AGCPROBE.BAS  -> docs/anchors/AGCPROBE.BAS   (probe capture variant)
- BASLOAD.BAS   -> docs/anchors/BASLOAD.BAS    (generic harness, no data lines)

Agreement rule: DATA blocks in `.BAS` must byte-match the corresponding
`.ASM`. Regenerate via `debug_asm`, never hand-roll.

