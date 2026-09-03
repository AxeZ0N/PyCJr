# jr — PCjr Bridge Byte Pipeline

`jr` assembles PCjr bridge assembly, checks it against named hardware invariants, and packages it as pasteable Cartridge BASIC DATA statements. It does not prove hardware safety — that remains the hardware stage gate's job.

Specification: [`../../docs/jr_tool_spec.md`](../../docs/jr_tool_spec.md)

---

## Installation

**Requirements**

- Python 3 (standard library only)
- `uasm` on PATH (or `--uasm /path/to/uasm`)
- `ndisasm` on PATH for `jr dis`

**Setup**

1. Make the tool executable:
       chmod +x refs/jr
2. Optionally add `refs/` to PATH or create a symlink in `/usr/local/bin`.

**UASM self‑test**

On first `jr build`, a one‑time check confirms that UASM produces unpadded output. The result is cached in `~/.jr_cache`. If UASM is updated, delete the cache to force a retest.

---

## Quick Start

Create a bridge source `demo.asm` using the canonical skeleton:

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
        lea  bp, [bp + 128 - 6]      ; result offset R = 128
        ; ... routine body ...
        in   al, 0A0h              ; clear keyboard latch
        mov  al, 80h
        out  0A0h, al              ; re-enable NMI
        pop  bp
        retf

    code ends
    end start

Build it:

    jr build demo.asm

Output:

    PASS: demo.asm -> demo.bin (26 bytes, R=128) -> demo.bas

Inspect the emitted BASIC:

    jr data demo.bin

Verify a typed listing against the binary:

    jr verify demo.bas demo.bin

Output:

    verify: demo.bas matches demo.bin (26 bytes)

---

## Subcommand Reference

### `jr build SRC.asm [options]`

Assemble, lint, emit `SRC.data` and generate `SRC.bas`.

| Option       | Description                                      |
|--------------|--------------------------------------------------|
| `--stage N`  | Development stage (1–6, default 6)               |
| `--result R` | Explicit result offset (default: 128 if ≤128 bytes, else 180) |
| `--ceiling C`| Maximum allowed code length (default 180)        |
| `--rules F`  | Override rules JSON file                         |
| `--strict`   | Escalate warnings to errors                      |
| `--uasm P`   | Path to UASM executable                          |
| `--keep`     | Keep intermediate files on failure               |

Exit codes: `0` success, `1` usage, `2` UASM failure, `4` lint failure, `5` loader/emission failure.

### `jr lint FILE.bin [options]`

Lint only. Same options as `build` (except `--uasm`). Requires `--result` if `selfloc` rule is active.

Exit codes: `0` no errors (and no warnings under `--strict`), `4` otherwise.

### `jr verify NAME.bas NAME.bin`

Parse BASIC DATA and byte‑compare to binary.

Exit codes: `0` match, `6` mismatch, `7` parse error.

### `jr golden NAME.bas [--out FILE.bin]`

Extract bytes from a typed listing into a binary file. Default output `NAME.golden.bin`.

Exit codes: `0` success, `7` parse error.

### `jr dis FILE.bin`

Run `ndisasm -b 16 FILE.bin` for human inspection.

### `jr data FILE.bin`

Print DATA lines (uppercase hex, `&H` prefix) ending with `DATA -1`.

### `jr parse NAME.bas [--out FILE.bin]`

Extract DATA bytes from BASIC. Tolerates optional line numbers, `&H`/`&h`, comma/whitespace variation, multiple `DATA` per line (via `:`), trailing comments.

Exit codes: `0` success, `7` parse error.

---

## Rule Table

| ID           | Kind    | Stage | Severity | Checks |
|--------------|---------|-------|----------|--------|
| `entry`      | prefix  | 1     | error    | Must start with `push cs / pop ds / push bp` (`0E 1F 55`) |
| `retf-count` | count   | 1     | error    | Exactly one `CB` far return |
| `epilogue`   | suffix  | 1     | error    | Must end with `pop bp / retf` (`5D CB`) |
| `no-int21h`  | absent  | 1     | error    | No `INT 21h` (`CD 21`) |
| `no-iret`    | absent  | 1     | warn     | No `IRET` (`CF`) — may be false positive |
| `no-speaker` | absent  | 1     | warn     | No `OUT 61h` (`E6 61`) |
| `selfloc`    | selfloc | 2     | error    | `lea bp,[bp+disp]` displacement equals `R - entry` |
| `budget`     | budget  | 3     | error    | Code size ≤ ceiling (default 180) |
| `latch-read` | before  | 4     | warn     | Timer reads (40h/41h/42h) must be preceded by latch idiom (`B0 00 E6 43`) |
| `nmi-mask`   | before  | 5     | warn     | `in al,62h` must be preceded by NMI mask (`B0 00 E6 A0`) |
| `nmi-restore`| suffix  | 5     | warn     | If A0h/62h touched, must end with NMI restore + `pop bp / retf` |

**Canonical idiom:** Use `mov al,imm` (not `xor al,al`, `sub al,al`, or `and al,0`). The linter flags non‑canonical zeroing.

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0    | Success |
| 1    | Usage error |
| 2    | UASM assemble failure |
| 4    | Lint failure (error rule or `--strict` warning) |
| 5    | Build emission/loader failure (`R < code_len`, file I/O) |
| 6    | Verify/golden byte mismatch |
| 7    | Parse error |

---

## FAQ

**Why does my code pass lint but still fail on hardware?**  
Static checks only warn about named hazards. Algorithm and timing bugs are not detectable by byte analysis — always test on hardware.

**Can I use `xor al,al` instead of `mov al,0`?**  
No. The canonical idiom policy requires `mov al,imm` for uniformity and machine‑checkability.

**What does `WARN: possible IRET (CF)` mean?**  
The byte `CF` was found; it could be an `IRET` instruction or part of an immediate. Inspect with `jr dis`.

**How do I raise the budget ceiling?**  
Use `--ceiling N` (default 180). But if code exceeds 180 bytes, reconsider algorithm or split routine.

**What are stages?**  
Development stages 1–6 gate rules by maturity. Higher stages enable stricter checks. Default is 6; use `--stage` to lower for incremental work.

**What happens if `jr build` fails?**  
No new `.data` or `.bas` are written. Pre‑existing outputs are left untouched. Use `--keep` to retain intermediate files for debugging.
