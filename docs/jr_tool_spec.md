# `jr` — PCjr bridge byte pipeline specification
**Version:** 1.0  
**Status:** normative draft (option A)  
**Audience:** implementer with no prior PyCJr context

This document is sufficient to implement the `jr` tool, its default rule
set, the loader template, and the self-verification fixtures. When prose
and a normative block disagree, the normative block wins:

- Section 4, the default `jr-rules.json`
- Section 5, the loader template
- Section 8, the fixtures

---

## 0. Conventions and reading guide

Writing rules for this spec:

1. Every lint rule cites a hardware fact: a `facts.md` heading, a session
   file, or a manual entry. No rule exists without evidence.
2. No byte pattern appears without its mnemonic equivalent. The reader
   must be able to translate bytes to instructions by eye.
3. Every failure message prints **expected vs found**. A bare "missing"
   message on correct-but-non-canonical code erodes trust.
4. No static check claims to prove hardware safety. The hardware stage
   gate is the only proof.

Terminology:

- **`R`** — result region offset from the code base.
- **ceiling** — maximum allowed code length in bytes.
- **stage** — development stage 1..6, matching the workflow Stage Gate.
- **`jr`** — the single CLI described in Section 3.
- **DATA block** — Cartridge BASIC `DATA &H..,&H..` lines terminated by
  a `-1` sentinel, the canonical pasteable machine-code carrier.

---

## 1. Thesis and history

`jr` is a byte pipeline for IBM PCjr bridge code. It assembles, lints a
set of *named* hardware invariants, emits pasteable Cartridge BASIC DATA,
and verifies the typed listing against the assembled image.

It is **not** a proof system. It is a checklist of the failures this
project has already paid for.

Four failures define the rule set:

1. **S1 v2 (2026-08-25).** A routine passed the old emission gate and
   rebooted the PCjr into BIOS on the first NMI. Static checks do not
   prove hardware safety; they only warn about named hazards.
2. **The +128 trap (2026-08-25).** `lea bp,[bp+128]` instead of `+122`
   shifts every result store six bytes high. The selfloc displacement is
   arithmetic nobody should do by hand.
3. **CH0CAL `38 D8` gap (2026-08-25).** A `cmp ax,bx` emitted ungated
   because the old decoder didn't cover it. An opcode whitelist is a
   proxy for hazards not yet named.
4. **ST2B ripple (2026-08-27).** Single-poll edge detection latched AGC
   ripple dips, producing trimodal spans. The defect was in the
   algorithm, not the bytes. `jr`'s job there is to rule out the byte
   layer so the human attacks the real variable.

Division of labor:

| Concern | Owner |
|---|---|
| Branch range, undefined/duplicate labels, malformed operands | UASM |
| Named PCjr invariants (entry, selfloc, retf, counter latch, NMI, budget) | `jr lint` |
| Retyped-listing drift, anchor migration | `jr verify`, `jr golden` |
| Algorithm/timing bugs, final safety proof | hardware stage gate |

---

## 2. Scope and boundaries

`jr` does:

- Assemble `.asm` to `.bin` via UASM `-bin`.
- Lint `.bin` against the rule table, gated by `--stage`.
- Emit Cartridge BASIC DATA and a generated loader, producing a complete
  `.bas` ready to paste.
- Verify a typed `.bas` against the assembled `.bin`.
- Extract a golden `.bin` from an existing anchor `.bas`.

`jr` does **not**:

- Prove hardware safety.
- Disassemble or decode. `jr dis` shells out to `ndisasm` for the human;
  the linter works on raw bytes, with one bounded ModRM parse for selfloc.
- Replace a general-purpose assembler. UASM assembles; `jr` does not own
  encoding.
- Catch algorithm/timing bugs. Those are the hardware gate's job.

---

## 3. Architecture

One CLI, `jr`, with subcommands:

```

jr build  SRC.asm   [options]   assemble -> lint -> emit .data + loader .bas
jr lint   FILE.bin  [options]   lint only
jr verify NAME.bas NAME.bin     parse .bas, byte-compare to .bin
jr golden NAME.bas [--out F]    parse .bas, write golden .bin
jr dis    FILE.bin              run ndisasm -b 16 (human listing)
jr data   FILE.bin              bytes -> DATA lines + -1 sentinel
jr parse  NAME.bas [--out F]    extract DATA from a typed listing -> .bin

```

### 3.1 Data flow

```

SRC.asm
| uasm -bin -Fl -Fo
v
SRC.bin
| jr lint (stage-gated rules)
v
SRC.data  (DATA lines + -1)
|

- loader template (Section 5) -> SRC.bas

typed SRC.bas
| jr parse
v
extracted.bin -> jr verify / jr golden

```

`build` runs lint **before** emitting `.data`/`.bas`. A failed lint leaves
no new `.data` or `.bas` artifact.

### 3.2 Dependencies

- Python 3, standard library only.
- `uasm` on PATH (or `--uasm /path/to/uasm`).
- `ndisasm` on PATH for `jr dis`.

No capstone. No Makefile. No MCP in the byte path.

### 3.3 UASM invocation and source skeleton

```

uasm -bin -Fl -Fo out.bin src.asm

```

UASM requires a segment wrapper even in `-bin` mode. The canonical source
skeleton:

```asm
option casemap:none
option segment:use16

code segment
    assume cs:code
    org 0

start:
    push cs
    pop  ds
    push bp
    call get_ip
get_ip:
    pop  bp
    lea  bp, [bp + N - 6]      ; N = result offset R (N-6 is the disp)
    ; ... routine body ...
    in   al, 0A0h              ; clear keyboard latch
    mov  al, 80h
    out  0A0h, al              ; re-enable NMI
    pop  bp
    retf

code ends
end start
```

`org 0` pins offset 0 to the first byte. The output `.bin` must have no
header and no padding.

### 3.4 One-time UASM padding self-test

On the first `jr build` run of a new installation, `jr` must prove the
UASM dialect produces unpadded output:

1. Assemble a source containing only `retf` (`CB`) with the segment
wrapper above.
2. Assert the output file is exactly one byte (`CB`).

If not, the implementation must report that UASM `-bin` is padding and
stop. This is a one-time check cached under the install's config dir.

---

## 4. Rules as data

The linter is a small engine over a rule list. The default rule list is
normative and reproduced in full below. An implementer may load an
override with `--rules FILE`, but must start from this default.

### 4.1 Rule schema

Each rule object has these fields:

| Field | Type | Meaning |
|---|---|---|
| `id` | string | unique rule name |
| `kind` | string | checker kind (below) |
| `pattern` | string | hex bytes, no separators |
| `min_stage` | int 1..6 | rule active iff `stage >= min_stage` |
| `severity` | `"error"` or `"warn"` | error blocks build; warn blocks only under `--strict` |
| `message` | string | expected-vs-found text |
| `rationale` | string | fact/session/manual citation |
| `config` | object | kind-specific options; may be omitted |

### 4.2 Checker kinds

- **`prefix`** — bytes must start with `pattern`. Fail if absent.
- **`suffix`** — bytes must end with `pattern`. Optional `config.cond`:
a list of hex substrings; if provided and none appears in the bytes,
the rule is inactive.
- **`absent`** — `pattern` must not appear anywhere in the bytes.
Fail with the offset of the first occurrence.
- **`count`** — count occurrences of `pattern`. `config.op` is `eq`, `le`,
or `ge`; compare to `config.value`. Used for the single-`retf` rule.
- **`before`** — if any `config.b` pattern appears in the bytes, then
`config.a` must appear before the first occurrence of any `b`. If no
`b` appears, the rule is inactive.
- **`selfloc`** — specialized check. Find `E8 00 00 5D`; parse the
following `lea bp,[bp+disp]` ModRM byte; compare the sign-extended
displacement to `R - 6`. `config.encodings` lists allowed forms,
default `["disp8","disp16"]`.
- **`budget`** — compare the file size in bytes to the ceiling passed on
the CLI. `config` is unused; the ceiling comes from `--ceiling`.

### 4.3 Stage gating

Rule `r` runs iff:

```
stage >= r.min_stage
```

`--stage` defaults to **6**. Stages 1–5 are explicit opt-downs for
incremental development.

### 4.4 Severity and exit

- `error` always fails the lint step.
- `warn` fails the lint step only with `--strict`; otherwise it prints a
`WARN:` line and the lint step passes.
- All messages print `expected` and `found` where meaningful. For
`absent` rules that match, the message prints the found offset and the
offending bytes.

### 4.5 Default rules JSON (normative)

```
{
  "version": "1.0",
  "rules": [
    {
      "id": "entry",
      "kind": "prefix",
      "pattern": "0E1F55",
      "min_stage": 1,
      "severity": "error",
      "message": "bridge entry: expected push cs / pop ds / push bp (0E 1F 55); found {prefix}",
      "rationale": "platform-skill Rule 1 bridge contract; S1 v1 BP clobber (2026-08-25)"
    },
    {
      "id": "retf-count",
      "kind": "count",
      "pattern": "CB",
      "min_stage": 1,
      "severity": "error",
      "config": {"op": "eq", "value": 1},
      "message": "exactly one far RETF (CB) required; found {count}, expected 1. An early RETF skips the mandatory NMI restore",
      "rationale": "platform-skill Rule 10: no early exit may skip keyboard re-enable"
    },
    {
      "id": "epilogue",
      "kind": "suffix",
      "pattern": "5DCB",
      "min_stage": 1,
      "severity": "error",
      "message": "bridge epilogue: expected pop bp / retf (5D CB); found {suffix}",
      "rationale": "platform-skill Rule 1: preserve BP, return via far RETF"
    },
    {
      "id": "no-int21h",
      "kind": "absent",
      "pattern": "CD21",
      "min_stage": 1,
      "severity": "error",
      "message": "INT 21h (CD 21) forbidden: DOS not assumed; found at offset {offset}",
      "rationale": "platform-skill Rule 10"
    },
    {
      "id": "no-iret",
      "kind": "absent",
      "pattern": "CF",
      "min_stage": 1,
      "severity": "warn",
      "message": "possible IRET (CF) at offset {offset}; confirm via 'jr dis'. IRET in the bridge is unverified (S1 v2). A CF immediate inside another instruction is a false positive",
      "rationale": "platform-skill Rule 7; S1 v2 reboot into BIOS (2026-08-25)"
    },
    {
      "id": "no-speaker",
      "kind": "absent",
      "pattern": "E661",
      "min_stage": 1,
      "severity": "warn",
      "message": "possible OUT 61h (E6 61) at offset {offset}; PCjr sound is TI SN76496, not the PC speaker. Confirm via 'jr dis'",
      "rationale": "platform-skill Rule 10"
    },
    {
      "id": "selfloc",
      "kind": "selfloc",
      "min_stage": 2,
      "severity": "error",
      "config": {"encodings": ["disp8", "disp16"]},
      "message": "selfloc: lea bp,[bp+{found_disp}] yields result offset {found_r}; expected displacement {expected_disp} (R - 6 = {expected_disp})",
      "rationale": "facts selfloc_pop_offset_semantics; +128 trap (2026-08-25)"
    },
    {
      "id": "budget",
      "kind": "budget",
      "min_stage": 3,
      "severity": "error",
      "message": "budget: size {found_size} exceeds ceiling {ceiling}",
      "rationale": "facts s4b1_raised_ceiling (180 bytes)"
    },
    {
      "id": "latch-read",
      "kind": "before",
      "min_stage": 4,
      "severity": "warn",
      "config": {
        "a": "B000E643",
        "b": ["E440", "E441", "E442"]
      },
      "message": "bare counter read {b_hex} without latch idiom mov al,0 / out 43h,al (B0 00 E6 43). CH0CAL latch/read idiom required; 41h reads are a keyboard hazard",
      "rationale": "platform-skill Rule 11: CH0CAL idiom; TIMER1 41h hazard"
    },
    {
      "id": "nmi-mask",
      "kind": "before",
      "min_stage": 5,
      "severity": "warn",
      "config": {
        "a": "B000E6A0",
        "b": ["E462"]
      },
      "message": "in al,62h (E4 62) without preceding mov al,0 / out 0A0h,al (B0 00 E6 A0). Polling 62h with NMI live is unsafe",
      "rationale": "platform-skill Rule 7: NMI must be masked before polling 62h"
    },
    {
      "id": "nmi-restore",
      "kind": "suffix",
      "pattern": "E4A0B080E6A05DCB",
      "min_stage": 5,
      "severity": "warn",
      "config": {
        "cond": ["E6A0", "E462"]
      },
      "message": "NMI restore missing: expected in al,0A0h / mov al,80h / out 0A0h,al / pop bp / retf (E4 A0 B0 80 E6 A0 5D CB) when A0h/62h is touched; found {suffix}",
      "rationale": "platform-skill Rule 10: restore NMI before RETF; 80h empirical (STAGE5)"
    }
  ]
}
```

### 4.6 Canonical idiom policy

House style for bridge code: load AL with `mov al,imm`. `xor al,al`,
`sub al,al`, and `and al,0` are architecturally equivalent but
non-canonical. The linter's expected-vs-found messages flag them so the
byte stream stays uniform and machine-checkable. This is the same
reasoning as the mandatory exact mask and restore sequences.

---

## 5. Loader generation

`jr build` must generate the complete `.bas`. It does **not** merge a
frozen external `BASLOAD.BAS`; the loader is generated from the
normative template below so the tool is self-contained.

### 5.1 Invariant

```
R >= code_len
```

- `code_len` is the assembled `.bin` size in bytes.
- If the CLI did not pass `--result`, resolve:

```
if code_len <= 128: R = 128
else:               R = 180
```

- If `--result N` was passed, `R = N`.
- If `R < code_len`, `jr build` fails with exit code 5 before writing any
loader output.

### 5.2 Ceiling

`ceiling` defaults to `180`. If `code_len > ceiling`, the `budget` rule
fails (exit 4).

### 5.3 Loader template (normative)

Placeholders are substituted by `jr build`:

- `__DIM__` — `DIM` argument computed below.
- `__RESULT__` — `R`, inserted into all result PEEK offsets.

Computation for `__DIM__`:

```
needed = max(code_len, R + 6)   # code bytes and a 6-byte result region
dim    = (needed + 1) // 2 - 1  # integer array: 2 bytes per element
```

Template:

```
10 DEFINT A-Z
20 DIM A(__DIM__)
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
160 ST = PEEK(VARPTR(A(0)) + __RESULT__)
170 RI = PEEK(VARPTR(A(0)) + __RESULT__ + 2) + 256! * PEEK(VARPTR(A(0)) + __RESULT__ + 3)
180 FA = PEEK(VARPTR(A(0)) + __RESULT__ + 4) + 256! * PEEK(VARPTR(A(0)) + __RESULT__ + 5)
190 PRINT "status="; ST; " rising="; RI; " falling="; FA
200 END
```

The DATA block emitted by `jr data` is appended immediately after line
200, with its own line numbers starting at 1000. The final line must be
`DATA -1`.

### 5.4 Success output

`jr build` prints exactly one line on success:

```
PASS: SRC.asm -> SRC.bin (N bytes, R=NNN) -> SRC.bas
```

where `N` is `code_len` and `NNN` is the resolved `R`.

---

## 6. Subcommand reference

### `jr build SRC.asm [options]`

Assemble, lint at `--stage` (default 6), emit `SRC.data`, generate
`SRC.bas`.

Options:

- `--stage N`
- `--result R` — explicit result offset
- `--ceiling C` — default 180
- `--rules FILE` — override rules JSON
- `--strict` — escalate warnings to errors
- `--uasm PATH`
- `--keep` — keep intermediate files on failure (default removes them)

Exit: `0` success, `1` usage, `2` UASM failure, `4` lint failure,
`5` loader/emission failure.

### `jr lint FILE.bin [options]`

Lint only. Same stage/result/ceiling/rules/strict options.

Exit: `0` no errors (and no warnings under `--strict`), `4` otherwise.

### `jr verify NAME.bas NAME.bin`

Parse `NAME.bas`, extract bytes, byte-compare to `NAME.bin`.

Exit: `0` match, `6` mismatch, `7` parse error.

Output on match:

```
verify: NAME.bas matches NAME.bin (N bytes)
```

### `jr golden NAME.bas [--out FILE.bin]`

Parse `NAME.bas`, write extracted bytes. Default output is
`NAME.golden.bin`; `--out` overrides.

Exit: `0` success, `7` parse error.

### `jr dis FILE.bin`

Run `ndisasm -b 16 FILE.bin` and print output. This is a human listing,
not a machine-parse input.

### `jr data FILE.bin`

Print DATA lines for the bytes:

```
1000 DATA &H0E,&H1F,...
...
1005 DATA -1
```

Every value is emitted as `&H` followed by uppercase hex. No trailing
spaces. The final line is always `DATA -1`.

### `jr parse NAME.bas [--out FILE.bin]`

Extract DATA from a Cartridge BASIC listing. Tolerances required:

- optional line numbers
- `&H` / `&h` hex prefixes
- comma and whitespace variation
- multiple `DATA` statements on one line via `:`
- trailing comments after a `:` or `'`

Stop at the first `-1` sentinel. A malformed or truncated token is a
parse error with the source line number.

Default output is raw bytes to stdout; `--out` writes a binary file.

---

## 7. Exit codes

| Code | Meaning |
|---|---|
| 0 | success |
| 1 | usage error |
| 2 | UASM assemble failure |
| 4 | lint failure (error rule, or `--strict` warning) |
| 5 | build emission/loader failure (`R < code_len`, file I/O) |
| 6 | verify/golden byte mismatch |
| 7 | parse error |

---

## 8. Self-verification fixtures (normative)

Before `jr` is trusted, the implementer must run a self-test that covers
these fixtures. The fixtures and expected outcomes are part of this spec.

### F1 — IRPING passes

Hex bytes (61 bytes, frozen IRPING image):

```
0E1F55E800005D8DAE7A00
BA6200EC2440B400894600
89C6B9307531DB31FFBA62
00EC244039F0740A85F674
0347EB014389C6E2EA895E
02897E045DCB
```

Command:

```
jr lint irping.bin --result 128 --stage 6
```

Expected: `PASS` with zero errors and zero warnings.

### F2 — selfloc +128 trap fails

Hex bytes (minimal, `lea bp,[bp+128]` instead of `+122`):

```
0E1F55E800005D8DAE80005DCB
```

Command:

```
jr lint selfloc_bad.bin --result 128 --stage 6
```

Expected: exit `4`, message names `selfloc`, expected displacement `122`,
found displacement `128`.

### F3 — missing NMI restore fails

Hex bytes (touches A0h, no restore sequence):

```
0E1F55E800005D8DAE7A00B000E6A05DCB
```

Command:

```
jr lint nmi_missing.bin --result 128 --stage 5
```

Expected: exit `4` under `--strict`, or a `WARN` naming `nmi-restore`
without `--strict`. The suffix rule fires because `E6A0` is present but
the final bytes are only `5D CB`.

### F4 — non-NMI routine passes NMI rules

Hex bytes (selfloc present, no 62h or A0h access):

```
0E1F55E800005D8DAE7A005DCB
```

Command:

```
jr lint non_nmi.bin --result 128 --stage 5
```

Expected: `PASS`; `nmi-mask` and `nmi-restore` are inactive because
their conditions are absent.

### F5 — DATA round-trip identity

For the F1 bytes:

```
jr data irping.bin > irping.data
jr parse --out roundtrip.bin <(cat loader_prefix irping.data)
cmp irping.bin roundtrip.bin
```

Expected: `cmp` reports no difference. The exact command shape may vary;
the contract is that `parse(data(x)) == x` for every fixture byte list.

### F6 — UASM padding self-test

Assemble a source containing only `retf` in the canonical skeleton.
Expected output file length is exactly `1` and byte `CB`.

---

## 9. Failure-mode map

| Bug class | Caught by | Rule/stage |
|---|---|---|
| Hand-rolled rel8 error | UASM | assemble |
| Undefined/duplicate label | UASM | assemble |
| Malformed operand | UASM | assemble |
| Wrong selfloc constant (+128 trap) | `selfloc` | stage 2 |
| BP clobbered / missing push-pop | `entry`, `epilogue` | stage 1 |
| Early RETF skips NMI restore | `retf-count` | stage 1 |
| IRET in bridge | `no-iret` (warn) | stage 1 |
| INT 21h with no DOS | `no-int21h` | stage 1 |
| PC speaker toggle | `no-speaker` (warn) | stage 1 |
| Bare 40h/41h/42h read | `latch-read` | stage 4 |
| 62h poll with NMI live | `nmi-mask` | stage 5 |
| Missing NMI restore | `nmi-restore` | stage 5 |
| Budget overflow | `budget` | stage 3 |
| `R < code_len` overlap | build invariant | emission |
| Retyped-listing drift | `verify` | post-paste |
| Anchor byte drift | `golden` + `cmp` | regression |
| AGC ripple / timing bug | hardware stage gate | not statically provable |

---

## 10. Implementation notes

These notes resolve the non-obvious mechanics.

### 10.1 Hex normalization

All pattern/config hex strings are case-insensitive and separator-free.
The parser strips `&H`, `0x`, spaces, commas, and line numbers before
decoding.

### 10.2 `selfloc` parse

1. Locate `E8 00 00 5D`.
2. Read the next byte `modrm`.
3. If `modrm == 0x6E`: read one displacement byte, sign-extend to 16-bit.
4. If `modrm == 0xAE`: read two displacement bytes, little-endian.
5. Otherwise fail with the found `modrm` byte.
6. Check the allowed `encodings` list; fail if the found form is absent.
7. Compare `disp` to `R - 6`. Report `found_r = 6 + disp` in the message
to make the arithmetic explicit.

### 10.3 `count` checker

`config.op` and `config.value` determine the comparison. For the default
`retf-count` rule, count every `CB` byte. If the count is `1`, pass;
otherwise fail. No attempt is made to distinguish opcode bytes from
immediate bytes.

### 10.4 Atomic build output

`build` writes `.data` and `.bas` only after lint passes. On any failure,
previously existing outputs are left untouched, and newly generated
partial files are removed unless `--keep` is set.

### 10.5 UASM dialect

The canonical source skeleton in Section 3.3 is mandatory for `jr build`
input. UASM's A2082 error means instructions were placed outside a
`segment` block; the skeleton prevents this.

---

## 11. Repo integration

Proposed file layout:

```
refs/
  jr                  # executable Python entry point
  jr_rules.json       # default rules (copy of Section 4.5)
  loader_template.bas # template from Section 5.3 (optional convenience)
docs/
  jr_tool_spec.md     # this document
  test_jr.py          # self-verification runner for Section 8
```

### Add-a-rule workflow

1. Record the new hazard in `facts.md` with a heading and status.
2. Add one rule object to `jr_rules.json`; include `rationale` pointing
at the facts.md heading.
3. Add a fixture to `docs/test_jr.py` that triggers the rule.
4. Run the full self-test; all existing fixtures must still pass.

### Remove/disable a rule

Delete the object, or set a `"disabled": true` field the engine honors.
The default `jr-rules.json` in this spec has no disabled rules.

---

*End of specification.*

