#!/usr/bin/env python3
"""pcjr-tools MCP server (v5).

Exposes three dispatch tools over the local PCjr reference strip, the
verified pcjr_asm_debug workbench, and the read-only repo grep engine:

    search_ref  mode=query|peek|stats
    debug_asm   command=selftest|parse|emit|decode|patch|check|branch|
                rel8|rel16|selfloc
    grep_repo   mode=query|read|grep_all|stats|roots

Each tool declares a required discriminator ("mode" / "command") so the
BDS MCP client never drops them. The reference strip and repo are loaded
read-only; nothing leaves this machine.

Endpoint:
    /mcp   streamable HTTP (FastMCP streamable_http_app)

Environment variables:
    PCJR_REF_DIR   Directory containing deepseek_reference.txt,
                   pcjr_ref_tool.py, pcjr_asm_debug.py, and
                   pcjr_repo_grep.py.
                   Defaults to <repo root>/refs (derived from this
                   file's location).
    PCJR_HOST      Bind host. Defaults to 127.0.0.1.
    PCJR_PORT_REF  Bind port. Defaults to 8765.

Register a single server named "pcjr-tools" pointing at
http://localhost:8765/mcp in Better DeepSeek.
"""
import json
import os
import sys
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

_SERVER_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SERVER_DIR.parent

HOST = os.environ.get("PCJR_HOST", "127.0.0.1")
PORT_REF = int(os.environ.get("PCJR_PORT_REF", "8765"))

REF_DIR = os.environ.get("PCJR_REF_DIR", str(_REPO_ROOT / "refs"))
REF_FILE = os.path.join(REF_DIR, "deepseek_reference.txt")
REFTOOL_FILE = os.path.join(REF_DIR, "pcjr_ref_tool.py")
ASM_FILE = os.path.join(REF_DIR, "pcjr_asm_debug.py")
GREP_FILE = os.path.join(REF_DIR, "pcjr_repo_grep.py")

sys.path.insert(0, REF_DIR)

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("Missing 'mcp' package. Install it with:", file=sys.stderr)
    print("  pip install -r requirements.txt", file=sys.stderr)
    raise

try:
    import pcjr_ref_tool as REFTOOL
    import pcjr_asm_debug as ASM
    import pcjr_repo_grep as GREP
except ImportError as exc:
    print("Missing pcjr_ref_tool.py, pcjr_asm_debug.py, or pcjr_repo_grep.py in PCJR_REF_DIR:", file=sys.stderr)
    print(f"  expected dir: {REF_DIR}", file=sys.stderr)
    print(f"  error: {exc}", file=sys.stderr)
    raise

from mcp.server.transport_security import TransportSecuritySettings

ALLOWED_BDS_ORIGIN = "moz-extension://12acc078-b84b-4db7-bb5d-ca3aab7eaf30"

mcp = FastMCP(
    "pcjr-tools",
    transport_security=TransportSecuritySettings(
        allowed_origins=[ALLOWED_BDS_ORIGIN],
        allowed_hosts=["127.0.0.1:8765", "localhost:8765"],
    ),
)

try:
    REFSTORE = REFTOOL.RefStore(REF_FILE)
except Exception as exc:
    print(f"ERROR: cannot load reference strip {REF_FILE}: {exc}", file=sys.stderr)
    sys.exit(1)

# --- search_ref ---------------------------------------------------------

@mcp.tool()
def search_ref(
    mode: str,
    query: Optional[str] = None,
    context: int = 3,
    max_pages: int = 1,
    start: Optional[int] = None,
    end: Optional[int] = None,
    verbose: Optional[bool] = None,
) -> str:
    """Search the IBM PCjr Technical Reference strip.

    mode:
        query  English prose search. Needs 'query' (optional: context, max_pages).
        peek   Raw entries by 1-based file position. Needs 'start' >= 1.
        stats  Diagnostic statistics. Optional 'verbose' (omit or true).
    """
    try:
        if mode == "query":
            if not query:
                return "ERROR: mode=query requires 'query'"
            return REFSTORE.query(query, context, max_pages)
        if mode == "peek":
            if start is None or start < 1:
                return "ERROR: mode=peek requires 'start' >= 1 (1-based entry index)"
            return REFSTORE.peek(start, end)
        if mode == "stats":
            return REFSTORE.stats(bool(verbose))
        return "ERROR: mode must be one of query|peek|stats"
    except ValueError as exc:
        return f"ERROR: {exc}"

# --- debug_asm ----------------------------------------------------------

class PatchItem(BaseModel):
    offset: int
    value: int

class BranchCheck(BaseModel):
    at: int
    target: int

@mcp.tool()
def debug_asm(
    command: str,
    mode: str = "all",
    text: Optional[str] = None,
    hex_bytes: Optional[str] = None,
    expected_hex: Optional[str] = None,
    patches: Optional[list[PatchItem]] = None,
    checks: Optional[list[BranchCheck]] = None,
    insn: Optional[int] = None,
    target: Optional[int] = None,
    pop_offset: Optional[int] = None,
    base: int = 128,
    wrap: int = 11,
) -> str:
    """8088 byte workbench (command dispatch). Byte construction source of truth.

    command:
        selftest  Run all stage gates against the frozen IRPING image.
        parse     Parse a BASIC DATA block -> hex bytes. Needs 'text'.
        emit      Emit hex bytes as a DATA block. Needs 'hex_bytes'.
        decode    Disassemble for the verified 8088 subset. Needs 'hex_bytes'.
        patch     Apply (offset,value) patches; returns DATA block.
                  Needs 'hex_bytes' and 'patches'.
        check     Compare to IRPING golden or 'expected_hex'. Needs 'hex_bytes'.
        branch    Verify (at,target) pairs against decoded displacements.
                  Needs 'hex_bytes' and 'checks'.
        rel8      Signed rel8 displacement. Needs 'insn' and 'target'.
        rel16     Signed rel16 displacement. Needs 'insn' and 'target'.
        selfloc   Full self-location instruction. Needs 'pop_offset' (base=128).
    """
    try:
        if command == "selftest":
            results = ASM.selftest()
            lines = [("PASS " if ok else "FAIL ") + name for name, ok in results.items()]
            lines.append("ALL_PASS " + str(all(results.values())))
            return "\n".join(lines)

        if command == "parse":
            if text is None:
                return "ERROR: command=parse requires 'text'"
            data = ASM.parse(text)
            return "".join(f"{b:02X}" for b in data)

        if command == "emit":
            if hex_bytes is None:
                return "ERROR: command=emit requires 'hex_bytes'"
            data = list(bytes.fromhex(hex_bytes))
            return ASM.emit(data, wrap=wrap)

        if command == "decode":
            if hex_bytes is None:
                return "ERROR: command=decode requires 'hex_bytes'"
            data = list(bytes.fromhex(hex_bytes))
            out = []
            for off, ln, text_ in ASM.decode(data):
                hx = "".join(f"{b:02X}" for b in data[off:off + ln])
                out.append(f"{off:04X}: {hx:<9} {text_}")
            return "\n".join(out)

        if command == "patch":
            if hex_bytes is None or patches is None:
                return "ERROR: command=patch requires 'hex_bytes' and 'patches'"
            data = list(bytes.fromhex(hex_bytes))
            patch_list = [(p.offset, p.value) for p in patches]
            return ASM.emit(ASM.patch(data, patch_list))

        if command == "check":
            if hex_bytes is None:
                return "ERROR: command=check requires 'hex_bytes'"
            actual = list(bytes.fromhex(hex_bytes))
            expected = (
                list(bytes.fromhex(expected_hex))
                if expected_hex
                else list(bytes.fromhex(ASM.GOLDEN_HEX))
            )
            return json.dumps(ASM.check_detail(actual, expected), indent=2)

        if command == "branch":
            if hex_bytes is None or checks is None:
                return "ERROR: command=branch requires 'hex_bytes' and 'checks'"
            data = list(bytes.fromhex(hex_bytes))
            check_list = [(c.at, c.target) for c in checks]
            return json.dumps(ASM.branch_checks(data, check_list), indent=2)

        if command == "rel8":
            if insn is None or target is None:
                return "ERROR: command=rel8 requires 'insn' and 'target'"
            b = ASM.rel8(insn, target)
            return json.dumps({
                "insn": insn, "target": target, "next_ip": insn + 2,
                "disp": target - (insn + 2), "bytes": b,
            }, indent=2)

        if command == "rel16":
            if insn is None or target is None:
                return "ERROR: command=rel16 requires 'insn' and 'target'"
            b = ASM.rel16(insn, target)
            return json.dumps({
                "insn": insn, "target": target, "next_ip": insn + 3,
                "disp": target - (insn + 3), "bytes": b,
            }, indent=2)

        if command == "selfloc":
            if pop_offset is None:
                return "ERROR: command=selfloc requires 'pop_offset'"
            return json.dumps(ASM.selfloc_full(pop_offset, base), indent=2)

        return "ERROR: unknown command; valid: selftest|parse|emit|decode|patch|check|branch|rel8|rel16|selfloc"
    except ValueError as exc:
        return f"ERROR: {exc}"

# --- grep_repo ----------------------------------------------------------

@mcp.tool()
def grep_repo(
    mode: str,
    query: Optional[str] = None,
    context: int = 2,
    literal: bool = False,
    path: Optional[str] = None,
    max_lines: int = 2000,
    max_matches: int = 50,
) -> str:
    """Read-only repo tool over the PyCJr repo.

    mode:
        query     Fact-layer regex search (facts.md, sessions/, docs/).
                  Needs 'query'.
        stats     Fact-layer file/line counts.
        roots     Which fact-layer roots exist.
        read      Full file by root-relative path, whole repo (text only,
                  hidden paths refused). Needs 'path'. JSON return.
        grep_all  Regex search across whole repo (text files only, hidden
                  paths refused). Needs 'query'. JSON return; capped by
                  max_matches.
    """
    try:
        result = GREP.dispatch(
            mode=mode,
            query=query,
            context=context,
            literal=literal,
            path=path,
            max_lines=max_lines,
            max_matches=max_matches,
        )
        if mode in ("read", "grep_all"):
            return json.dumps(result, indent=2)
        if isinstance(result, dict) and "text" in result:
            return result["text"]
        return json.dumps(result, indent=2)
    except Exception as exc:
        return f"ERROR: {exc}"

def main() -> None:
    print("pcjr-tools MCP server")
    print(f"  reference strip: {REF_FILE}")
    print(f"  ref tool:        {REFTOOL_FILE}")
    print(f"  asm debugger:    {ASM_FILE}")
    print(f"  repo grep:       {GREP_FILE}")
    print(f"  entries loaded:  {len(REFSTORE.pages)}")
    print(f"  endpoint:        http://{HOST}:{PORT_REF}/mcp")
    print("Press Ctrl+C to stop.")

    import uvicorn

    try:
        app = mcp.streamable_http_app()
        print("transport: streamable-http (/mcp)")
    except AttributeError:
        app = mcp.sse_app()
        print("transport: sse fallback (may not work with BDS)")

    uvicorn.run(app, host=HOST, port=PORT_REF)

if __name__ == "__main__":
    main()
