# PyCJr — pcjr-tools MCP Server (operational)

Repo-resident operational doc for the human. Not BDS-imported.

The assistant sees the live MCP tool surface directly via the BDS MCP
import, and reads the canonical dispatch tables in
`bds/10_skills/pcjr_test_workflow.md`. This file covers server
operations only — start, env, registration — and does not duplicate
those tables.

## Identity

- Server name: `pcjr-tools`
- URL: `http://localhost:8765/mcp`
- Entry point: `refs/pcjr_ref_mcp.py`
- Legacy alias: `pcjr-ref` (superseded; no longer used in docs/skills)

## Canonical dispatch (target of the rewrite)

- `search_ref` — searching tool; modes `query` | `peek` | `stats`.
- `debug_asm` — assembly workbench; command dispatch over the former
  `byte_*` family.

Full arg/command tables: see `bds/10_skills/pcjr_test_workflow.md`.
Do not maintain a second copy here.

## Environment

| Var | Default | Purpose |
|---|---|---|
| `PCJR_REF_DIR` | `$HOME/Code/Helpful/PCJR/refs` | Directory containing `deepseek_reference.txt`, `pcjr_ref_util.py`, `pcjr_byte.py` |
| `PCJR_HOST` | `127.0.0.1` | Bind host |
| `PCJR_PORT_REF` | `8765` | Bind port |

## Start

From the repo root:

```bash
PCJR_REF_DIR="$PWD/refs" python3 refs/pcjr_ref_mcp.py
```

Or use the provided launcher:

```
bin/start_pcjr_mcp.sh
```

## Byte self-check

```
bin/byte_selftest.sh
# equivalent:
python3 refs/pcjr_byte.py selftest
```

Run after every server restart to confirm the byte workbench gates all
pass against the frozen IRPING image.

## BDS registration

- Server name: `pcjr-tools`
- URL: `http://localhost:8765/mcp`
- Re-register in BDS after adding or renaming tools.

## Migration note

Live legacy tool names — `query_ref`, `peek_ref`, `stats_ref`,
`byte_selftest`, `byte_parse`, `byte_emit`, `byte_decode`,
`byte_patch`, `byte_check`, `byte_branches`, `byte_rel8`,
`byte_rel16`, `byte_selfloc` — are superseded by the `search_ref` /
`debug_asm` dispatch. Implement the dispatch before relying on the
canonical names in live calls; until then, the old names remain
callable.

