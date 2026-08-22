# pcjr-tools — Server Ops + Tool Surface (v5)

Server: `pcjr-tools` at `http://localhost:8765/mcp` (loopback bind).

## Tools

| Tool | Mode / command | Purpose |
|---|---|---|
| `search_ref` | `query` \| `peek` \| `stats` | Manual strip search |
| `debug_asm` | command dispatch | 8088 byte workbench |
| `grep_repo` | `query` \| `stats` \| `roots` | Read-only repo fact search (stdlib, no git) |

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

### grep_repo

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

## Registration (already wired)

`grep_repo` is registered in `mcp/pcjr_tools_server.py` (v5). It imports
the engine from `refs/pcjr_repo_grep.py`. No manual edit needed.

If you rebuild the server from scratch:

```
import pcjr_repo_grep as GREP

@mcp.tool()
def grep_repo(mode: str, query: Optional[str] = None,
              context: int = 2, literal: bool = False) -> str:
    ...
```

Then restart:

```
bin/start_pcjr_mcp.sh
```

Self-test:

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

For the manual strip, the fallback is the `search_ref` dispatch; when the
server is down, paste the output of the ref tool (or ask the assistant
for the exact command for your checkout).

