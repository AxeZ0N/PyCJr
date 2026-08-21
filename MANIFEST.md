# PyCJr — Manifest

Canonical artifact inventory. Every repo artifact is labeled here.
The single source of truth for what exists, where it goes, and its state.

## Label fields

| Field | Values |
|---|---|
| type | system_prompt · skill · persona · project · doc · ref_data · driver · mcp_ops · script |
| import_target | project · skills · persona · mcp · none |
| version | v4 · verbatim · n/a |
| status | canonical · pending_user_move · user_owned · superseded |

## Repository artifacts

| Path | Type | Import target | Version | Status |
|---|---|---|---|---|
| `README.md` | doc | none | v4 | canonical |
| `MANIFEST.md` | doc | none | v4 | canonical |
| `pyproject.toml` | project config | none | — | user_owned |
| `bds/00_system_prompt.md` | system_prompt | project | v4 | canonical |
| `bds/10_skills/pcjr_cartridge_basic_asm.md` | skill | skills | v4 | canonical |
| `bds/10_skills/pcjr_test_workflow.md` | skill | skills | v4 | canonical |
| `bds/20_persona/pcjr_hardware_engineer.md` | persona | persona | v4 | canonical |
| `bds/30_project/pycjr_project.md` | project | project | v4 | canonical |
| `docs/project_state.md` | doc | none | v4 | canonical |
| `docs/test_log.md` | doc | none | v4 | canonical |
| `docs/ch0_calibration.md` | doc | none | v4 | canonical |
| `docs/changelog.md` | doc | none | v4 | canonical |
| `mcp/pcjr-tools.md` | mcp_ops | none | v4 | canonical |
| `refs/MOVE_VERBATIM.md` | doc | none | n/a | canonical |
| `refs/deepseek_reference.txt` | ref_data | none | verbatim | pending_user_move |
| `refs/pcjr_ref_util.py` | driver | none | verbatim | pending_user_move |
| `refs/pcjr_byte.py` | driver | none | verbatim | pending_user_move |
| `refs/pcjr_ref_mcp.py` | driver | none | verbatim | pending_user_move |
| `bin/start_pcjr_mcp.sh` | script | none | v4 | canonical |
| `bin/byte_selftest.sh` | script | none | v4 | canonical |

## Superseded artifacts (delete; do not re-import)

| Path | Superseded by |
|---|---|
| `pcjrduino/` (old generated tree) | `PyCJr/` |
| `bds/30_project/pcjrduino_project.md` | `bds/30_project/pycjr_project.md` |
| `docs/anchors_and_gates.md` | `docs/test_log.md` |
| `docs/tooling_reference.md` | `mcp/pcjr-tools.md` + `bds/10_skills/pcjr_test_workflow.md` |

## Ownership notes (single-source policy)

- Hardware facts + IR protocol -> `pcjr_cartridge_basic_asm`.
- Retrieval, tooling, gates, emission gate -> `pcjr_test_workflow`.
- Always-active rules, assumptions, open items -> `pycjr_project`.
- CH0CAL derivation + defects -> `docs/ch0_calibration.md`.
- Run history (volatile) -> `docs/test_log.md` + session handoff.
- MCP ops -> `mcp/pcjr-tools.md`.
