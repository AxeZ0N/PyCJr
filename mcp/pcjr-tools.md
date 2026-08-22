# pcjr-tools — Server Ops + Tool Surface (v5)

Server: `pcjr-tools` at `http://localhost:8765/mcp` (loopback bind).

## Tools

| Tool | Mode / command | Purpose |
|---|---|---|
| `search_ref` | `query` \| `peek` \| `stats` | Manual strip search |
| `debug_asm` | command dispatch | 8088 byte workbench |
| `grep_repo` | `query` \| `stats` \| `roots` | Read-only repo fact search (Option A: stdlib, no git) |

### search_ref

```

mode: query   query, context(3), max_pages(1)
mode: peek    start, end (1-based; start>=1)
mode: stats   verbose (omit or true; never false)

```

### debug_asm

```

command: selftest|parse|emit|decode|patch|check|branch|rel8|rel16|selfloc

```

### grep_repo (new)

Schema:

```json
{
  "mode": "query",
  "query": "carrier_high_us|burst_us",
  "context": 2,
  "literal": false
}
```

- `query` — regex search over `facts.md`, `sessions/`, `docs/` (case-insensitive; `|` works).
- `stats` — file/line counts per root.
- `roots` — which roots exist.
- Zero-arg hazard: every `grep_repo` call MUST include `mode`.

## Registration (write once)

In `refs/pcjr_ref_mcp.py`, import the engine and register a third tool:

```
from pcjr_repo_grep import TOOL_SCHEMA, dispatch

# under your existing tool registration loop, add:
#   name="grep_repo", schema=TOOL_SCHEMA, handler=dispatch
```

Then restart the server. Self-test:

```
bin/grep_selftest.sh
```

## Security posture (do not weaken)

- Fixed roots: `facts.md`, `sessions/`, `docs/`. No `..`, no absolute paths.
- No git binary, no subprocess, stdlib only.
- Writes NEVER go through the server. Writes are user-owned via
`bin/jr-commit.sh` and `bin/migrate_repo.py`.

## Paste-first fallback

When the server is down, the assistant asks you to run and paste:

```
git grep -n -i -E -C2 "carrier_high_us|burst_us|gap2" -- facts.md sessions docs
```

