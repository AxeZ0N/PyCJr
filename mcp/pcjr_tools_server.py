#!/usr/bin/env python3
"""
pcjr-tools MCP server — integrated guide for PCjr machine-code design. (v8)

This server exposes three tools that together support the full
PCjr Cartridge BASIC machine-code design and validation loop:

    search_ref   Query the digitized IBM PCjr Technical Reference strip.
    grep_repo    Search the PyCJr repository fact layer (facts.md, sessions/, docs/).
    jr           Assemble, lint, extract, and verify bridge machine code.

Use all three in concert:
  1. Retrieve manual facts with search_ref.
  2. Retrieve repo decisions with grep_repo.
  3. Build and validate machine code with jr.

All file paths in the jr tool are relative to the repository root.

--- search_ref ---
Search the IBM PCjr Technical Reference strip (noisy OCR).

mode:
    query   English prose search. Needs 'query'.
            Optional: context (default 3), max_pages (default 1).
    peek    Raw entries by 1-based file position. Needs 'start' >= 1.
            Optional: end.
    stats   Diagnostic statistics. Optional: verbose (omit or true).

--- grep_repo ---
Read-only repo search over facts.md, sessions/, and docs/ (plus whole
repo for read/grep_all). A match is evidence, not automatically a fact.

mode:
    query     Fact-layer regex search. Needs 'query'.
              Optional: context (default 2), literal (default false).
    stats     Fact-layer file/line counts.
    roots     Which fact-layer roots exist.
    read      Full file by root-relative path, whole repo (text only,
              hidden paths refused). Needs 'path'. JSON return.
    grep_all  Regex search across whole repo (text files only, hidden
              paths refused). Needs 'query'. JSON return; capped by
              max_matches (default 50).

--- jr ---
PCjr bridge machine-code pipeline: assemble, lint, extract, verify.

The routine must satisfy the bridge contract:
    - Entry prefix 0E 1F 55: push cs / pop ds / push bp
    - Epilogue 5D CB: pop bp / retf
    - Exactly one far RETF (CB)
    - Self-location: call get_ip / pop bp / lea bp,[bp+R-6]
    - Results stored at O+R; BASIC reads them via PEEK(VARPTR(A(0))+R)
    - If port A0h or 62h is touched, restore NMI before RETF with:
      IN AL,0A0h (clear latch), then OUT 0A0h,80h

command:
    build    Assemble SRC.asm with UASM, lint, then write SRC.bin,
             SRC.data, and SRC.bas next to src. Needs 'src'.
             Optional: stage (default 6), result (auto if omitted),
             ceiling (default 180), rules (path to JSON rule file),
             strict, uasm (default "uasm"), keep.
             On success returns JSON with keys: status, bin_hex,
             data_block, bas_source, errors, warnings.

    lint     Lint FILE.bin against the stage-gated rule set.
             Needs 'binfile'.
             Optional: stage (default 6), result (REQUIRED if selfloc
             rule is active), ceiling (default 180), rules, strict.
             Returns JSON: {"status": "pass"|"warn",
             "errors": [], "warnings": []}.
             A non-pass result is returned as an error string.

    verify   Compare .bas DATA bytes to .bin bytes. Needs 'bas' and 'bin'.
             Returns JSON: {"match": bool, "expected_size": int,
             "actual_size": int, "mismatches": [{"offset": int,
             "expected": int|null, "actual": int|null}]}.

    golden   Extract DATA bytes from .bas and write a binary file.
             Needs 'bas'. Optional: out (default NAME.golden.bin).

    dis      Disassemble FILE.bin with ndisasm. Needs 'binfile'.

    data     Emit BASIC DATA lines from FILE.bin. Needs 'binfile'.

    parse    Extract DATA bytes from .bas and return hex or write to
             'out'. Needs 'bas'. Optional: out.

Errors from jr are returned as: "ERROR (exit N):\n<message>".

--- Recommended design/validation workflow ---
  1. Retrieve before emit:
       - Use search_ref for manual facts (ports, bits, vectors).
       - Use grep_repo for repo facts/decisions and session ground truth.
  2. Construct bytes:
       - Prefer pjasm / debug_asm tools. Never hand-roll rel8/rel16.
       - Or assemble a complete source with jr build.
  3. Lint the generated binary:
       - jr lint FILE.bin --stage N --result R
       - If selfloc rule is active, result is required.
  4. Verify against anchors:
       - jr golden ANCHOR.BAS --out /tmp/anchor.bin
       - jr lint /tmp/anchor.bin --stage 6 --result R
       - jr verify ANCHOR.BAS ANCHOR.bin
  5. Gate each stage before advancing.
       - If a stage fails, fix only that stage and re-run.
       - If transport is suspect, regress with IRPING first.
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional

_SERVER_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SERVER_DIR.parent

HOST = os.environ.get("PCJR_HOST", "127.0.0.1")
PORT_REF = int(os.environ.get("PCJR_PORT_REF", "8765"))

REF_DIR = os.environ.get("PCJR_REF_DIR", str(_REPO_ROOT / "refs"))
REF_FILE = os.path.join(REF_DIR, "deepseek_reference.txt")
REFTOOL_FILE = os.path.join(REF_DIR, "pcjr_ref_tool.py")
GREP_FILE = os.path.join(REF_DIR, "pcjr_repo_grep.py")
JR_TOOLS_DIR = os.path.join(REF_DIR, "jr-tools")

# Add both refs and refs/jr-tools to sys.path
sys.path.insert(0, REF_DIR)
sys.path.insert(0, JR_TOOLS_DIR)

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("Missing 'mcp' package. Install it with:", file=sys.stderr)
    print("  pip install -r requirements.txt", file=sys.stderr)
    raise

try:
    import pcjr_ref_tool as REFTOOL
    import pcjr_repo_grep as GREP
    import jr as JR
except ImportError as exc:
    print("Missing pcjr_ref_tool.py, pcjr_repo_grep.py, or jr.py in PCJR_REF_DIR:", file=sys.stderr)
    print(f"  expected ref dir: {REF_DIR}", file=sys.stderr)
    print(f"  expected jr-tools dir: {JR_TOOLS_DIR}", file=sys.stderr)
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

# --- jr -----------------------------------------------------------------

@mcp.tool()
def jr(
    command: str,
    src: Optional[str] = None,
    binfile: Optional[str] = None,
    bas: Optional[str] = None,
    bin: Optional[str] = None,
    out: Optional[str] = None,
    stage: Optional[int] = None,
    result: Optional[int] = None,
    ceiling: Optional[int] = None,
    rules: Optional[str] = None,
    strict: bool = False,
    uasm: Optional[str] = None,
    keep: bool = False,
) -> str:
    """PCjr bridge byte pipeline (assemble, lint, verify, data, parse, dis).

    command:
        build    Assemble SRC.asm -> .bin, lint, emit .data and .bas.
                 Needs 'src'. Optional: stage, result, ceiling, rules,
                 strict, uasm, keep.
        lint     Lint FILE.bin. Needs 'binfile'. Optional: stage, result,
                 ceiling, rules, strict.
        verify   Compare .bas DATA to .bin. Needs 'bas' and 'bin'.
        golden   Extract bytes from .bas to a .bin file. Needs 'bas'.
                 Optional: out (default NAME.golden.bin).
        dis      Disassemble FILE.bin with ndisasm. Needs 'binfile'.
        data     Emit DATA lines from FILE.bin. Needs 'binfile'.
        parse    Extract bytes from .bas DATA. Needs 'bas'.
                 Optional: out (default stdout).
    """
    try:
        if command == "build":
            if not src:
                return "ERROR: command=build requires 'src'"
            with open(src, 'r') as f:
                asm_text = f.read()
            res = JR.build(
                asm_text,
                stage=stage if stage is not None else 6,
                result=result,
                ceiling=ceiling if ceiling is not None else 180,
                rules=rules,
                strict=strict,
                uasm=uasm or "uasm",
            )
            # Write outputs (same as CLI)
            base = os.path.splitext(src)[0]
            bin_path = base + ".bin"
            data_path = base + ".data"
            bas_path = base + ".bas"
            with open(bin_path, 'wb') as f:
                f.write(bytes.fromhex(res["bin_hex"]))
            with open(data_path, 'w') as f:
                f.write(res["data_block"])
            with open(bas_path, 'w') as f:
                f.write(res["bas_source"])
            return json.dumps(res, indent=2)

        elif command == "lint":
            if not binfile:
                return "ERROR: command=lint requires 'binfile'"
            with open(binfile, 'rb') as f:
                bin_hex = f.read().hex().upper()
            res = JR.lint(
                bin_hex,
                stage=stage if stage is not None else 6,
                result=result,
                ceiling=ceiling if ceiling is not None else 180,
                rules=rules,
                strict=strict,
            )
            return json.dumps(res, indent=2)

        elif command == "verify":
            if not bas or not bin:
                return "ERROR: command=verify requires 'bas' and 'bin'"
            with open(bas, 'r') as f:
                bas_text = f.read()
            with open(bin, 'rb') as f:
                bin_hex = f.read().hex().upper()
            res = JR.verify(bas_text, bin_hex)
            return json.dumps(res, indent=2)

        elif command == "golden":
            if not bas:
                return "ERROR: command=golden requires 'bas'"
            with open(bas, 'r') as f:
                bas_text = f.read()
            hex_out = JR.golden(bas_text)
            out_path = out if out else os.path.splitext(bas)[0] + ".golden.bin"
            with open(out_path, 'wb') as f:
                f.write(bytes.fromhex(hex_out))
            return f"golden: wrote {len(hex_out)//2} bytes to {out_path}"

        elif command == "dis":
            if not binfile:
                return "ERROR: command=dis requires 'binfile'"
            with open(binfile, 'rb') as f:
                bin_hex = f.read().hex().upper()
            return JR.dis(bin_hex)

        elif command == "data":
            if not binfile:
                return "ERROR: command=data requires 'binfile'"
            with open(binfile, 'rb') as f:
                bin_hex = f.read().hex().upper()
            return JR.data(bin_hex)

        elif command == "parse":
            if not bas:
                return "ERROR: command=parse requires 'bas'"
            with open(bas, 'r') as f:
                bas_text = f.read()
            hex_out = JR.parse(bas_text)
            if out:
                with open(out, 'wb') as f:
                    f.write(bytes.fromhex(hex_out))
                return f"parse: wrote {len(hex_out)//2} bytes to {out}"
            return hex_out

        else:
            return f"ERROR: unknown command '{command}'; valid: build|lint|verify|golden|dis|data|parse"

    except JR.JrError as exc:
        return f"ERROR (exit {exc.exit_code}):\n{exc}"
    except FileNotFoundError as exc:
        return f"ERROR: file not found: {exc}"
    except Exception as exc:
        return f"ERROR: {exc}"

def main() -> None:
    print("pcjr-tools MCP server")
    print(f"  reference strip: {REF_FILE}")
    print(f"  ref tool:        {REFTOOL_FILE}")
    print(f"  repo grep:       {GREP_FILE}")
    print(f"  jr module:       {os.path.join(JR_TOOLS_DIR, 'jr.py')}")
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
