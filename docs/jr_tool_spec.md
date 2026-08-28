# `jr` — PCjr bridge byte pipeline specification

**Version:** 1.0 (implemented)
**Status:** normative — matches the shipped `refs/jr-tools/jr.py` and
`refs/jr-tools/jr_rules.json`, with the inline-first MCP surface
(asm_text / bin_hex / bas_text) added 2026-08-28.
**Audience:** implementer with no prior PyCJr context.

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

### 3.0 Inline surface (2026-08-28, MCP)

The MCP `jr` tool accepts inline string inputs in addition to file paths.
Inline is preferred for development; file inputs only for persistence.

| Param | Replaces | Carries |
|---|---|---|
| `asm_text` | `src` path | full UASM source text |
| `bin_hex` | `binfile` path | raw bytes as uppercase hex, no `0x`/`&H` |
| `bas_text` | `bas` path | full typed BASIC listing |

`build` accepts `asm_text` OR `src`; `lint`/`dis`/`data` accept `bin_hex`
OR `binfile`; `parse` accepts `bas_text` OR `bas`.

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

### 4.2 Default rule set (matches refs/jr-tools/jr_rules.json v1.0)

| id | kind | min_stage | severity | notes |
|---|---|---|---|---|
| entry | prefix `0E1F55` | 1 | error | bridge entry |
| retf-count | count `CB` == 1 | 1 | error | exactly one far RETF |
| epilogue | suffix `5DCB` | 1 | error | pop bp / retf |
| no-int21h | absent `CD21` | 1 | error | DOS not assumed |
| no-iret | absent `CF` | 1 | warn | possible IRET; confirm via dis |
| no-speaker | absent `E661` | 1 | warn | PCjr sound is SN76496 |
| selfloc | selfloc (disp8/disp16) | 2 | error | R-6 displacement |
| budget | budget | 3 | error | ceiling 180 |
| latch-read | before (latch then 40/41/42 read) | 4 | warn | CH0CAL idiom; 41h hazard |
| nmi-mask | before (mask A0 then IN 62) | 5 | warn | poll 62h only masked |
| nmi-restore | suffix (conditional) | 5 | warn | restore NMI before RETF |

Normalized patterns for the `before`/`suffix` `config` fields are the
actual byte sequences in `jr_rules.json`:

- `latch-read`: `a = B000E643`, `b = [E440, E441, E442]`
- `nmi-mask`: `a = B000E6A0`, `b = [E462]`
- `nmi-restore`: pattern `E4A0B080E6A05DCB`, cond `[E6A0, E462]`

The authoritative copy is the JSON file; this table is the summary. When
they disagree, the JSON wins.

## 5. Loader template

The generated `.bas` uses the float16-safe loader (verified
2026-08-28):

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

`__DIM__` is sized to cover the code length plus the result region;
`__RESULT__` is the result offset (default 128). The `256!` multiplier is
mandatory — Cartridge BASIC's `DEFINT` overflows above 32767.

## 6. Stage gating

`jr lint --stage N` activates every rule whose `min_stage <= N`. Rules
with `severity: "warn"` block only under `--strict`. `build` defaults to
`stage=6` when no `stage` is given (empirical, 2026-08-28) — pass
`stage=1` explicitly for a bare bridge stub.

## 7. Exit codes

- `0` success
- `4` lint failure (invariant violated)
- other codes per `jr.py` `JrError.exit_code` (UASM failure, parse
  errors, missing executables, etc.)

## 8. Fixtures

Fixtures are the known-good anchor bytes. The normative fixture set is:

- IRPING stage-5 DATA (61 bytes) — golden regression artifact.
- S4B1_ST2 — known-good stage-6 capture binary.

Each fixture must assemble, lint, and re-derive its DATA byte-exact.
When a fixture disagrees with this spec, the fixture's `.bin` is the
authority; this spec must be corrected to match.

## 9. Security / process invariants

- No writes through the MCP server; `jr` file-output commands run under
  the user's own invocation (CLI) or write only into the repo working
  tree the user owns.
- The tool never invokes a network, never imports capstone, never shells
  beyond `uasm` and `ndisasm`.

## 10. Migration note (2026-08-28)

`jr` supersedes `debug_asm` (`refs/pcjr_asm_debug.py`) and `pjasm`
(`refs/pcjrasm.py`) as the MCP byte-pipeline surface. `facts.md`
`jr_mcp_pipeline` records the transition; superseded facts:

- `pjasm_mcp_tool`
- `pjasm_r8_extension`
- `pjasm_selftest_merge`
- `pjasm_bracket`
- `pjasm_boundary`
- `asm_debug`

Historical references elsewhere are append-only records, not current API.
