# PCjr Design / Test Workflow (v6)

## Activation

Use whenever the user asks to test, validate, verify, debug, or regress
generated PCjr Cartridge BASIC or 8088 assembly, or whenever a
machine-code experiment needs a verification path.

- Repo is source of truth; BDS library is a runtime cache. Git wins on
  drift.
- v6 change: the `jr` tool replaces `debug_asm` and `pjasm` as the
  single MCP byte-pipeline surface. Inline inputs are preferred; file
  inputs only for persistence. Stage-gated lint maps to
  `refs/jr-tools/jr_rules.json` `min_stage` values.

## Loop Order (always)

1. Spec first. Every routine declares its contract before code is generated.
2. Retrieve before emit. Use the Retrieval Protocol below.
3. Generate in stages. Bridge stub -> self-location -> result stores ->
   one `IN` from target port -> polling loop -> full capture.
4. Gate each stage. Do not advance until the previous stage returns the
   expected result.
5. Regress first when transport is suspect. Run IRPING first.
6. Record the result. Every run emits a result block.
7. Recover cold. On hang, cold power-cycle. Never assume Ctrl+Alt+Del.

## Retrieval Protocol (mandatory)

The assistant has no local shell. Reference lookups use the MCP server
or a user-pasted command output.

### MCP server

Server: `pcjr-tools`
Endpoint: `http://localhost:8765/mcp`

| Tool | Mode | Arguments | Purpose |
|---|---|---|---|
| search_ref | query | query, context (3), max_pages (1) | English prose search |
| search_ref | peek | start, end (1-based) | Raw entries by file position |
| search_ref | stats | verbose (omit or true) | Diagnostics only |
| grep_repo | query | query, context (2), literal (false) | Repo fact search |
| grep_repo | read | path | Full file, whole repo, root-relative |
| grep_repo | grep_all | query | Regex across whole repo |
| jr | command (below) | build/lint/verify/golden/dis/data/parse | Bridge byte pipeline |

Note on notation: this document writes MCP invocations with square
brackets, e.g. `[BDS:AUTO:MCP ...]`, so it is never parsed as a live
tool call. In actual use, replace the outer square brackets with angle
brackets.

Usage (shown bracketed):

```
[BDS:AUTO:MCP url="pcjr-tools" tool="search_ref" args='{"mode":"query","query":"8255 bit assignments","context":3,"max_pages":1}']
[BDS:AUTO:MCP url="pcjr-tools" tool="search_ref" args='{"mode":"peek","start":30,"end":36}']
[BDS:AUTO:MCP url="pcjr-tools" tool="grep_repo" args='{"mode":"query","query":"carrier_high_us|gap2","context":2}']
```

Traps:

- `stats` heading list is diagnostic only. It is NOT an authoritative
table of contents.
- Never pass `"verbose": false`. The BDS MCP client drops the request
before transmission. Omit the field or pass true.
- `peek` is 1-based. `start=0` returns an application error.
- `query` (search_ref) searches English prose, not register tables. Use
`peek` for register/port/BIOS facts. Appendix A is the full BIOS dump.
- Every MCP call MUST include its required field: `search_ref` needs
`mode`; `grep_repo` needs `mode`; `jr` needs `command`.

### Repo read path — grep_repo (Option A) + paste-first git grep

`grep_repo` `query` searches the fact layer (`facts.md`, `sessions/`,
`docs/`); `read` and `grep_all` span the whole repo (text only, hidden
paths refused, symlink/absolute/`../` escapes refused). A match is
evidence, not automatically a clean fact.

When MCP is unavailable, ask the user to run and paste:

```
git grep -n -i -E -C2 "carrier_high_us|burst_us|gap2" -- facts.md sessions docs
```

### Fallback mode: command + paste (manual strip)

When MCP is unavailable for the manual, ask the user to run and paste:

```
REF LOOKUP NEEDED
Run:
python3 refs/pcjr_ref_tool.py refs/deepseek_reference.txt query "<term>" --context 3 --max-pages 1
Paste output.
```

Command reference:

```
python3 refs/pcjr_ref_tool.py refs/deepseek_reference.txt query "<term>" --context 3 --max-pages 1
python3 refs/pcjr_ref_tool.py refs/deepseek_reference.txt peek 30 35
python3 refs/pcjr_ref_tool.py refs/deepseek_reference.txt stats --verbose
```

### Reading search results

The strip contains OCR/scan artifacts:

- `I` may be `1`; `O` may be `0`.
- Columns may be misaligned; page headers may interrupt body text.
- A single result is evidence, not a clean fact.

If a queried value conflicts with an empirical result:

1. Do not silently override either source.
2. Run a second query with different wording.
3. If the conflict remains, mark it `conflict` and describe both sources.
4. Do not emit code depending on the conflicting value without a
`; VERIFY:` tag or an explicit user decision.

### Retrieval Gate

Before emitting any port, mode, segment, or vector value:

1. Locate the manual section (Manual Locator in the platform skill).
2. Query through `search_ref`, or ask the user for a manual lookup.
3. Clean result -> `manual-verified`.
4. Hardware evidence only -> `empirical`.
5. Neither -> `unverified`, tagged
`; VERIFY: value against PCjr Technical Reference`.

Never claim the assistant ran the util locally. Never pass an unverified
value without the tag.

## jr tool — bridge byte pipeline

Server: `pcjr-tools`. Single tool, `command` dispatch. Backed by
`refs/jr-tools/jr.py`; UASM assembles, NDISASM disassembles. Inline
inputs are preferred for development; file inputs only for persistence.
All inline inputs are strings without `0x`/`&H` prefixes.

| Command | Args | Purpose |
|---|---|---|
| build | asm_text (or src path); stage (default 6), result (auto), ceiling (180), strict, uasm, keep | UASM assemble -> lint -> `bin_hex`/`data_block`/`bas_source` |
| lint | bin_hex (or binfile); stage, result, ceiling, strict | lint-only against jr_rules.json |
| verify | bas, bin | byte-compare .bas DATA to .bin |
| golden | bas; out | extract DATA from .bas -> .bin |
| dis | bin_hex (or binfile) | NDISASM `-b 16` human listing |
| data | bin_hex (or binfile) | emit DATA lines + `-1` sentinel |
| parse | bas_text (or bas); out | extract hex from .bas |

UASM requires a segment wrapper even in `-bin` mode. The canonical
skeleton (jr_tool_spec section 3.3):

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
    lea  bp, [bp + N - 6]      ; N = result offset R (disp = N - 6)
    ; ... routine body ...
    in   al, 0A0h
    mov  al, 80h
    out  0A0h, al
    pop  bp
    retf

code ends
end start
```

Examples (shown bracketed; see Retrieval Protocol notation note):

```
[BDS:AUTO:MCP url="pcjr-tools" tool="jr" args='{"command":"build","asm_text":"option casemap:none\noption segment:use16\ncode segment\n    assume cs:code\n    org 0\nstart:\n    push cs\n    pop  ds\n    push bp\n    pop  bp\n    retf\ncode ends\nend start\n","stage":1}']
[BDS:AUTO:MCP url="pcjr-tools" tool="jr" args='{"command":"dis","bin_hex":"0E1F555DCB"}']
```

Zero-arg hazard: every `jr` call MUST include `command`.

Trap (empirical, 2026-08-28): `jr build` defaults to `stage=6`. A bare
stage-1 bridge stub without selfloc trips the selfloc rule (min_stage 2)
and fails exit 4. Pass `stage=1` explicitly for early stages.

`jr build` success returns a float16-safe generated loader: auto-sized
`DIM A(...)` (code + result region) and `256!` multipliers in lines
170/180. No hand-assembly of the loader.

## Emission Gate (mandatory)

No DATA block leaves a response unless its bytes were produced by
`jr build` at the target stage and the human reviews `jr dis`. UASM
owns instruction encoding and branch range; `jr lint` enforces the
named bridge invariants (entry/selfloc/retf/NMI/budget); `jr dis` is
the review step for flagged warnings (possible IRET `CF`, possible
`OUT 61h`) and for confirming branch targets.

Hand-rolling any byte or displacement is a process violation. UASM is
the construction source of truth, `jr lint` the invariant checker,
NDISASM the review source.

The gate proves construction and named invariants. It does not prove
hardware safety: S1 v2 passed the old gate then rebooted the PCjr into
BIOS on the first NMI. Hardware behavior remains a separate stage gate.

## Test Contract (mandatory)

Every generated routine ships with a contract block:

```
{
  "id": "probe_id",
  "source": "FILE.BAS",
  "expected": { "return": "RETURNED OK", "...": "..." },
  "regression": "IRPING",
  "recovery": "cold_power_cycle"
}
```

Fields generalize per routine. Do not copy IRPING's rising/falling
expectations into a timer, video, or sound routine.

## Stage Gate (mandatory)

`jr build stage=N` activates every rule whose `min_stage <= N`. `.` =
error (blocks build); `!` = warn (blocks only under `strict=true`).
Rule ids and thresholds are normative in `refs/jr-tools/jr_rules.json`.

| Stage | New risk | Lint rules active | Hardware pass condition |
|---|---|---|---|
| 1 Bridge stub | PUSH CS / POP DS / PUSH BP / RETF | entry. retf-count. epilogue. no-int21h. no-iret! no-speaker! | Returns RETURNED OK |
| 2 Self-location | call get_ip / pop bp / lea | + selfloc. | Writes a known byte at O+R |
| 3 Result stores | Explicit stores O+128/130/132 | + budget. (ceiling 180) | BASIC reads expected values |
| 4 IN from target port | Port access | + latch-read! | Status changes as documented |
| 5 Polling loop | 62h reads, NMI mask/restore | + nmi-mask! nmi-restore! | Edges observed on stimulus |
| 6 Full capture | Complete routine | + strict=true (warns become errors) | All contract fields match |

`R` = result region offset (default 128). `jr build` auto-derives
`result` if omitted; `jr lint` REQUIRES `result` when the selfloc rule
is active.

If a stage fails, the defect is in the bytes added in that stage.
Fix only that stage, then re-run.

## Anti-Patterns (never)

- Emitting code without a contract block.
- Advancing a stage without passing the previous gate.
- Burying an unverified port/segment value without the `; VERIFY:` tag.
- Skipping IRPING when transport behavior looks wrong.
- Assuming any recovery other than cold power-cycle.
- Telling the assistant to run local `pcjr_ref_tool.py` commands — the
assistant cannot.
- Trusting a manual value without search_ref output or pasted output.
- Treating a noisy OCR match as a clean manual fact.
- Silently overwriting an empirical fact with a single garbled query.
- Unbounded arm on 62h bit 6. Mechanism: KBDNMI de-serializes after the
first edge when NMI is active. Use a finite loop, mask NMI
(OUT A0h,00h), restore 80h before RETF.
- Allowing a capture to swallow the arming keystroke. PCjr Enter emits an
IR make/break frame; INPUT consumes before CALL O, but early capture
can catch it. Add a delay or wait-for-edge.
- Running `jr build` at stage 6 on a stage-1 stub without passing
`stage=1` — the selfloc rule (min_stage 2) rejects it, not a bug.

## Debug Anchor Rule

Before debugging a failing capture, re-run the last known-good probe with
identical stimulus. If the anchor passes, the transport is sane and the
defect is in the changed code. If the anchor fails, run IRPING first.
Change only one variable per iteration.

Known anchors — identity only. Recorded readings live in the session
handoff, `facts.md`, and `docs/test_log.md`, never here:

- IRPING — golden regression artifact (DATA in platform skill Rule 5).
- SHAPE3 Stage 3 — known-good early stage.
- STAGE5 clean — known-good capture with keyboard intact.
- CH0CAL — known-good CH0 timestamp capture.
- ENVSHAPE — known-good envelope capture with keyboard intact.
- AGCPROBE — known-good envelope probe capture (AGCPROBE.BAS, CH0CAL ASM).
- DEC1_ST2A — known-good PC0 polling gate.

## Anchor Ground Truth and Retype Path

- Anchor ground truth lives in `docs/anchors/<PROG>.BAS` and
`docs/anchors/<PROG>.ASM`. To retype an anchor, read those files —
never back-issues of sessions.
- A program earns its anchor files in the same session it first passes
hardware. Never defer anchor file creation.
- DATA blocks must byte-match the ASM via `jr build` (UASM emits
`.data`/`.bas`); hand-rolled bytes are a process violation.
