# PCjr Design / Test Workflow (v5)

## Activation

Use whenever the user asks to test, validate, verify, debug, or regress
generated PCjr Cartridge BASIC or 8088 assembly, or whenever a
machine-code experiment needs a verification path.

- Repo is source of truth; BDS library is a runtime cache. Git wins on
  drift.

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
| debug_asm | command | dispatch table below | 8088 byte workbench |
| grep_repo | query | query, context (2), literal (false) | Repo fact search |
| grep_repo | stats | — | Repo file/line counts |
| grep_repo | roots | — | Which roots exist |

Usage:

```xml
<BDS:AUTO:MCP url="pcjr-tools" tool="search_ref" args='{"mode":"query","query":"8255 bit assignments","context":3,"max_pages":1}'></BDS:AUTO:MCP>
<BDS:AUTO:MCP url="pcjr-tools" tool="search_ref" args='{"mode":"peek","start":30,"end":36}'></BDS:AUTO:MCP>
<BDS:AUTO:MCP url="pcjr-tools" tool="grep_repo" args='{"mode":"query","query":"carrier_high_us|gap2","context":2}'></BDS:AUTO:MCP>
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
`mode`; `debug_asm` needs `command`; `grep_repo` needs `mode`.

### Repo read path — grep_repo (Option A) + paste-first git grep

`grep_repo` reads `facts.md`, `sessions/`, and `docs/` only. Stdlib
only, no git binary, no subprocess, fixed roots, loopback bind. A match
is evidence, not automatically a clean fact.

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

## ASM tool — debug_asm

Server: `pcjr-tools`. Single tool, `command` dispatch:

| Command ↕▾ ↕▾ ↕▾ | Args ↕▾ ↕▾ ↕▾ |
|---|---|
| −−−selftest | mode="all" (after server restart) |
| −−−parse | text |
| −−−emit | hex_bytes |
| −−−decode | hex_bytes |
| −−−patch | hex_bytes, patches=[{offset,value}] |
| −−−check | hex_bytes, expected_hex |
| −−−branch | hex_bytes, checks=[{at,target}] |
| −−−rel8 | insn, target |
| −−−rel16 | insn, target |
| −−−selfloc | pop_offset, base=128 |
| −−⚙ |  |
| −⚙ |  |
⚙

Example:

```
<BDS:AUTO:MCP url="pcjr-tools" tool="debug_asm" args='{"command":"decode","hex_bytes":"0E1F55E800005D8DAE7A00"}'></BDS:AUTO:MCP>
```

Zero-arg hazard: every `debug_asm` call MUST include `command`.

## Emission Gate (mandatory)

No machine code leaves a response unless its bytes were produced or
confirmed by `debug_asm selfloc` + `debug_asm rel8`/`rel16` +
`debug_asm branch` + `debug_asm decode` BEFORE the DATA block is emitted.
Hand-rolling a rel8 displacement is a process violation. The tool is the
construction source of truth, not a post-hoc checker.

The gate proves byte construction and branch displacements. It does
not prove hardware safety: S1 v2 passed selfloc, 3/3 branch checks,
and a clean decode, then rebooted the PCjr into BIOS on the first
NMI. Hardware behavior remains a separate stage gate.

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

| Stage ↕▾ ↕▾ ↕▾ | New risk ↕▾ ↕▾ ↕▾ | Pass condition ↕▾ ↕▾ ↕▾ |
|---|---|---|
| −−−1 Bridge stub | PUSH CS / POP DS / RETF | Returns RETURNED OK |
| −−−2 Self-location | call get_ip / pop bp | Writes a known byte at O+128 |
| −−−3 Result stores | Explicit stores O+128/130/132 | BASIC reads expected values |
| −−−4 IN from target port | Port access | Status changes as documented |
| −−−5 Polling loop | Edge counters | Edges observed on stimulus |
| −−−6 Full capture | Complete routine | All contract fields match |
| −−⚙ |  |  |
| −⚙ |  |  |
⚙

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

## Anchor Ground Truth and Retype Path

- Anchor ground truth lives in `docs/anchors/<PROG>.BAS` and
`docs/anchors/<PROG>.ASM`. To retype an anchor, read those files —
never back-issues of sessions.
- A program earns its anchor files in the same session it first passes
hardware. Never defer anchor file creation.
- DATA blocks must byte-match the ASM via `debug_asm`; hand-rolled
bytes are a process violation.

