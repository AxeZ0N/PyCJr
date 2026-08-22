# PyCJr — Manifest (v5)

Canonical artifact inventory. Every repo artifact is labeled here.
The single source of truth for what exists, where it goes, and its state.

## Label fields

| Field | Values |
|---|---|
| type | system_prompt · skill · persona · project · doc · ref_data · driver · mcp_ops · script · config |
| import_target | project · skills · persona · mcp · none |
| version | v5 · verbatim · n/a |
| status | canonical · pending_user_move · user_owned · superseded |

## Repository artifacts

| Path | Type | Import target | Version | Status |
|---|---|---|---|---|
| `README.md` | doc | none | v5 | canonical |
| `MANIFEST.md` | doc | none | v5 | canonical |
| `facts.md` | doc | none | v5 | canonical |
| `pyproject.toml` | config | none | — | user_owned |
| `bds/00_system_prompt.md` | system_prompt | project | v5 | canonical |
| `bds/10_skills/pcjr_cartridge_basic_asm.md` | skill | skills | v5 | canonical |
| `bds/10_skills/pcjr_test_workflow.md` | skill | skills | v5 | canonical |
| `bds/20_persona/pcjr_hardware_engineer.md` | persona | persona | v5 | canonical |
| `bds/30_project/pycjr_project.md` | project | project | v5 | canonical |
| `docs/ch0_calibration.md` | doc | none | v5 | canonical |
| `docs/changelog.md` | doc | none | v5 | canonical |
| `docs/FAQ.md` | doc | none | v5 | canonical |
| `docs/project_state.md` | doc | none | v5 | canonical |
| `docs/test_log.md` | doc | none | v5 | canonical |
| `sessions/README.md` | doc | none | v5 | canonical |
| `sessions/2026-08-22_tooling_build_repo_refactor.md` | doc | none | v5 | canonical |
| `mcp/pcjr-tools.md` | mcp_ops | none | v5 | canonical |
| `mcp/pcjr_tools_server.py` | driver | mcp | v5 | canonical |
| `refs/deepseek_reference.txt` | ref_data | none | verbatim | pending_user_move |
| `refs/pcjr_ref_tool.py` | driver | none | v5 | canonical |
| `refs/pcjr_asm_debug.py` | driver | none | v5 | canonical |
| `refs/pcjr_repo_grep.py` | driver | mcp | v5 | canonical |
| `bin/byte_selftest.sh` | script | none | v5 | canonical |
| `bin/grep_selftest.sh` | script | none | v5 | canonical |
| `bin/jr-commit.sh` | script | none | v5 | canonical |
| `bin/migrate_repo.py` | script | none | v5 | canonical |
| `bin/pycjr.py` | driver | none | v5 | canonical |
| `bin/start_pcjr_mcp.sh` | script | none | v5 | canonical |

## Superseded artifacts (delete; do not re-import)

| Path | Superseded by |
|---|---|
| `pcjrduino/` (old generated tree) | `PyCJr/` |
| `bds/30_project/pcjrduino_project.md` | `bds/30_project/pycjr_project.md` |
| `docs/anchors_and_gates.md` | `docs/test_log.md` |
| `docs/tooling_reference.md` | `mcp/pcjr-tools.md` + `bds/10_skills/pcjr_test_workflow.md` |
| `refs/pcjr_ref_util.py` | `refs/pcjr_ref_tool.py` |
| `refs/pcjr_byte.py` | `refs/pcjr_asm_debug.py` |
| `refs/pcjr_ref_mcp.py` | `mcp/pcjr_tools_server.py` |

## Ownership notes (single-source policy)

- Hardware facts + IR protocol -> `pcjr_cartridge_basic_asm`.
- Retrieval, tooling, gates, emission gate -> `pcjr_test_workflow`.
- Always-active rules, assumptions, open items -> `pycjr_project`.
- Single values -> `facts.md` (append-only; updates use `supersedes:`).
- CH0CAL derivation + defects -> `docs/ch0_calibration.md`.
- Run history (volatile) -> `docs/test_log.md` + session handoff.
- Per-scope narrative -> `sessions/`.
- MCP ops -> `mcp/pcjr-tools.md`; live server -> `mcp/pcjr_tools_server.py`.
