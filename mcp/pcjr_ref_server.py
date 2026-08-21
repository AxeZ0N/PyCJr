#!/usr/bin/env python3
"""pcjr-ref MCP server.

Exposes the local IBM PCjr Technical Reference strip and the verified
pcjr_byte workbench through MCP tools. The reference text and byte
functions never leave this machine; this server runs locally.

Endpoint:
    /sse    SSE transport used by Better DeepSeek

Environment variables:
    PCJR_REF_DIR   Directory containing deepseek_reference.txt,
                   pcjr_ref_util.py, and pcjr_byte.py.
                   Defaults to ~/Code/Helpful/PCJR/refs.
    PCJR_HOST      Bind host. Defaults to 127.0.0.1.
    PCJR_PORT_REF  Bind port. Defaults to 8765.

Note: byte tools are served on the same port as the reference tools.
Register a single server named "pcjr-ref" pointing at this endpoint.
"""

import json
import os
import subprocess
import sys

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("Missing 'mcp' package. Install it with:", file=sys.stderr)
    print("  pip install -r requirements.txt", file=sys.stderr)
    raise

from pydantic import BaseModel

HOST = os.environ.get("PCJR_HOST", "127.0.0.1")
PORT_REF = int(os.environ.get("PCJR_PORT_REF", "8765"))

REF_DIR = os.environ.get("PCJR_REF_DIR", os.path.expanduser("~/Code/Helpful/PCJR/refs"))
REF_FILE = os.path.join(REF_DIR, "deepseek_reference.txt")
UTIL_FILE = os.path.join(REF_DIR, "pcjr_ref_util.py")
BYTE_FILE = os.path.join(REF_DIR, "pcjr_byte.py")

# pcjr_byte lives next to pcjr_ref_util.py, not on the default sys.path.
sys.path.insert(0, REF_DIR)
try:
    import pcjr_byte as BYTE
except ImportError:
    print("Missing pcjr_byte.py in PCJR_REF_DIR:", file=sys.stderr)
    print(f"  expected: {BYTE_FILE}", file=sys.stderr)
    raise

from mcp.server.transport_security import TransportSecuritySettings

ALLOWED_BDS_ORIGIN = "moz-extension://12acc078-b84b-4db7-bb5d-ca3aab7eaf30"

mcp = FastMCP(
    "pcjr-ref",
    transport_security=TransportSecuritySettings(
        allowed_origins=[ALLOWED_BDS_ORIGIN],
        allowed_hosts=["127.0.0.1:8765", "localhost:8765"],
    ),
)

def _run_util(args: list[str]) -> str:
    """Run pcjr_ref_util.py with the supplied arguments and return stdout."""
    if not os.path.isfile(REF_FILE) or not os.path.isfile(UTIL_FILE):
        return (
            "ERROR: reference files not found.\n"
            f"Expected reference strip: {REF_FILE}\n"
            f"Expected utility:         {UTIL_FILE}\n"
            "Set PCJR_REF_DIR to the directory containing both files."
        )

    cmd = [sys.executable, str(UTIL_FILE), str(REF_FILE), *args]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=REF_DIR,
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        return "ERROR: pcjr_ref_util.py timed out after 30 seconds."

    if result.returncode != 0:
        return f"ERROR from pcjr_ref_util.py:\n{result.stderr.strip()}"

    output = result.stdout.strip()
    return output if output else "(no matches)"

@mcp.tool()
def query_ref(query: str, context: int = 3, max_pages: int = 1) -> str:
    """Search the IBM PCjr Technical Reference strip.

    Args:
        query: Term or phrase to search.
        context: Number of context lines around each match.
        max_pages: Maximum number of pages/entries to return.
    """
    return _run_util(
        ["query", query, "--context", str(context), "--max-pages", str(max_pages)]
    )

@mcp.tool()
def peek_ref(start: int = 0, end: int = 20) -> str:
    """Print raw reference entries by file position.

    Args:
        start: Starting entry index.
        end: Ending entry index.
    """
    return _run_util(["peek", str(start), str(end)])

@mcp.tool()
def stats_ref(verbose: bool = False) -> str:
    """Print diagnostic statistics.

    The heading list produced by --verbose is diagnostic only and is not
    an authoritative table of contents.

    Args:
        verbose: Include verbose heading diagnostic output.
    """
    return _run_util(["stats", "--verbose"] if verbose else ["stats"])

# --- pcjr_byte workbench tools -------------------------------------------
# These wrap the verified pure functions in pcjr_byte.py. Run
# byte_selftest after a server restart to prove the import is healthy.

class BytePatch(BaseModel):
    offset: int
    value: int

@mcp.tool()
def byte_selftest(mode: str="all") -> str:
    """Run all pcjr_byte stage gates against the frozen IRPING image.

    Returns PASS/FAIL for every gate plus an ALL_PASS summary line.
    """
    results = BYTE.selftest()
    lines = [("PASS " if ok else "FAIL ") + name for name, ok in results.items()]
    lines.append("ALL_PASS " + str(all(results.values())))
    return "\n".join(lines)

@mcp.tool()
def byte_parse(text: str) -> str:
    """Parse a Cartridge BASIC DATA block into hex bytes (stops at -1 sentinel)."""
    data = BYTE.parse(text)
    return "".join(f"{b:02X}" for b in data)

@mcp.tool()
def byte_emit(hex_bytes: str) -> str:
    """Emit a hex byte string as a Cartridge BASIC DATA block with -1 sentinel."""
    data = list(bytes.fromhex(hex_bytes))
    return BYTE.emit(data)

@mcp.tool()
def byte_decode(hex_bytes: str) -> str:
    """Disassemble a hex byte string for the verified 8088 subset.

    Unknown opcodes are printed as db 0xNN and never guessed.
    """
    data = list(bytes.fromhex(hex_bytes))
    return "\n".join(f"{off:04X}  {text}" for off, _, text in BYTE.decode(data))

@mcp.tool()
def byte_patch(hex_bytes: str, patches: list[BytePatch]) -> str:
    """Apply (offset, value) patches and return a new DATA block.

    Non-mutating; out-of-range offsets or byte values raise an error.
    """
    data = list(bytes.fromhex(hex_bytes))
    patch_list = [(p.offset, p.value) for p in patches]
    return BYTE.emit(BYTE.patch(data, patch_list))

@mcp.tool()
def byte_check(hex_bytes: str, expected_hex: str = "") -> str:
    """Compare a hex byte string to a reference.

    Reports ok, length delta, and first divergent offset. If expected_hex
    is empty, the frozen IRPING golden is used.
    """
    actual = list(bytes.fromhex(hex_bytes))
    expected = (
        list(bytes.fromhex(expected_hex))
        if expected_hex
        else list(bytes.fromhex(BYTE.GOLDEN_HEX))
    )
    return json.dumps(BYTE.check(actual, expected), indent=2)

@mcp.tool()
def byte_rel8(insn: int, target: int) -> str:
    """Compute a signed rel8 displacement (next IP = insn + 2)."""
    return json.dumps(BYTE.rel8(insn, target))

@mcp.tool()
def byte_rel16(insn: int, target: int) -> str:
    """Compute a signed rel16 displacement (next IP = insn + 3)."""
    return json.dumps(BYTE.rel16(insn, target))

@mcp.tool()
def byte_selfloc(pop_offset: int, base: int = 128) -> str:
    """Compute lea bp,[bp+disp16] after call get_ip / pop bp."""
    return json.dumps(BYTE.selfloc_disp(pop_offset, base))

@mcp.tool()
def byte_branches(data: [int], checks: [list]) -> str:
    """Verify (insn_addr, target) pairs against decoded displacements."""
    return json.dumps(BYTE.branch_checks(data, checks))

def main() -> None:
    print("pcjr-ref MCP server")
    print(f"  reference strip: {REF_FILE}")
    print(f"  utility:         {UTIL_FILE}")
    print(f"  byte tool:       {BYTE_FILE}")
    print(f"  endpoint:        http://{HOST}:{PORT_REF}")
    print("Press Ctrl+C to stop.")

    import uvicorn

    try:
        app = mcp.streamable_http_app()
        print("transport: streamable-http")
    except AttributeError:
        app = mcp.sse_app()
        print("transport: sse fallback (may not work with BDS)")

    uvicorn.run(app, host=HOST, port=PORT_REF)

if __name__ == "__main__":
    main()
