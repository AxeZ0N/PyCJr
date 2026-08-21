# PyCJr Handoff Verification (v4)

Repo-resident verification checklist. Run at the start of a fresh session
and after any BDS import or MCP config change. Lives at
`docs/handoff_verification.md`; include it in the project-files import set
if you want it visible in the first message.

## 1. Import slot mapping (five-way split)

BDS imports these separately. Verify each slot points at the right file
and loads only that file's content — no duplication across slots.

| BDS slot | File | Must show | OK |
|---|---|---|---|
| System prompt | `bds/00_system_prompt.md` | PyCJr envelope; data policy; codegen/memory rules | |
| Persona | `bds/20_persona/pcjr_hardware_engineer.md` | PCjr hardware engineer voice; empirical posture | |
| Skill | `bds/10_skills/pcjr_cartridge_basic_asm.md` | Rules 1–12; bridge; hardware map; IRPING DATA | |
| Skill | `bds/10_skills/pcjr_test_workflow.md` | Retrieval; `search_ref`/`debug_asm`; gates; emission gate | |
| Project prompt | `bds/30_project/pycjr_project.md` | PyCJr rules; assumptions; session scope; open items | |
| Project files (concat) | `README.md`, `MANIFEST.md`, `docs/*` | Durable record: labels, CH0 calibration, test log | |

Project-files concat order: `README.md` -> `MANIFEST.md` ->
`docs/project_state.md` -> `docs/test_log.md` ->
`docs/ch0_calibration.md` -> `docs/changelog.md`.

## 2. MCP server

- Name: `pcjr-tools`
- URL: `http://localhost:8765/mcp`
- Expected tools after dispatch rewrite: `search_ref`, `debug_asm`.
- Legacy names (`query_ref`, `peek_ref`, `stats_ref`, `byte_*`) are
  superseded and may appear only in a migration note.
- Verify: server pings from BDS; tool list matches the skill tables.

## 3. Stale-name sweep (must be absent from imported content)

- `pcjr-ref` -> must be `pcjr-tools`
- `PCJrduino` -> must be `PyCJr`
- `pcjrduino_project.md` -> must be `pycjr_project.md`

## 4. Single-source checks

- Skills contain stable rules only; no volatile readings (`max_delta`,
  `gap1`/`gap2`, iteration counts) in skills, persona, or project prompt.
- Volatile readings live only in BDS memory
  (`pcjr_ch0_clock`, `pcjr_stage5_clean_anchor`, `pcjr_ch0cal_anchor`)
  and the per-session handoff.
- CH0 clock appears once, in the platform skill Rule 6 hardware map.
- Open items appear once, in the project prompt.

## 5. Acceptance criteria (no further changes needed when all pass)

1. Each slot loads exactly its expected file.
2. No stable fact is duplicated across slots.
3. No session reading is embedded in a skill or prompt.
4. Project files expose the manifest, test log, calibration, and
   changelog in order.
5. MCP server reachable and dispatch names in the skills match the live
   server.
6. First assistant message demonstrates: project named PyCJr, facts
   labeled `manual-verified` / `empirical` / `unverified` / `conflict`,
   and no stale `pcjr-ref` / `PCJrduino` references.

## 6. One-time manual actions (until done, item 2 and 5 are partially pending)

- Move into `refs/`: `deepseek_reference.txt`, `pcjr_ref_util.py`,
  `pcjr_byte.py`, `pcjr_ref_mcp.py`.
- Delete superseded: `docs/anchors_and_gates.md`,
  `docs/tooling_reference.md`, `bds/30_project/pcjrduino_project.md`,
  old `pcjrduino/` tree.
- Implement `search_ref` / `debug_asm` dispatch on `pcjr-tools`; restart;
  re-register in BDS.

## 7. Session opener (paste after imports)

```text
SESSION SCOPE: <one goal>
ASSETS: <this session's volatile readings and anchors>
MCP: pcjr-tools reachable? <yes/no>
RULINGS: <values to change or confirm>
```
