#!/usr/bin/env python3
"""Minimal JSON-RPC HTTP MCP server for the pcjr_byte workbench.

Stdlib only. Exposes the verified pure functions in pcjr_byte.py as MCP
tools. Listen on 127.0.0.1:8766 by default; the endpoint is /mcp.

Start locally:
    python3 refs/pcjr_byte_mcp.py
Then register in Better DeepSeek as server name "pcjr-byte" with URL
    http://localhost:8766/mcp
"""
import json
import os
import sys
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pcjr_byte as B

PORT = int(os.environ.get("PCJR_BYTE_PORT", "8766"))
HOST = "127.0.0.1"

TOOLS = [
    {
        "name": "selftest",
        "description": "Run all pcjr_byte stage gates against the frozen IRPING image.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "parse",
        "description": "Parse a Cartridge BASIC DATA block into a hex byte string (stops at -1).",
        "inputSchema": {
            "type": "object",
            "properties": {"text": {"type": "string", "description": "BASIC DATA lines"}},
            "required": ["text"],
        },
    },
    {
        "name": "emit",
        "description": "Emit a hex byte string as a Cartridge BASIC DATA block.",
        "inputSchema": {
            "type": "object",
            "properties": {"hex": {"type": "string", "description": "Hex bytes, e.g. 0E1F..."}},
            "required": ["hex"],
        },
    },
    {
        "name": "decode",
        "description": "Disassemble a hex byte string for the verified 8088 subset.",
        "inputSchema": {
            "type": "object",
            "properties": {"hex": {"type": "string", "description": "Hex bytes"}},
            "required": ["hex"],
        },
    },
    {
        "name": "patch",
        "description": "Apply (offset, value) patches and return a new DATA block.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "hex": {"type": "string", "description": "Hex bytes"},
                "patches": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "offset": {"type": "integer"},
                            "value": {"type": "integer"},
                        },
                        "required": ["offset", "value"],
                    },
                },
            },
            "required": ["hex", "patches"],
        },
    },
    {
        "name": "check",
        "description": "Compare a hex byte string to a reference; report first diff and length delta.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "hex": {"type": "string", "description": "Actual hex bytes"},
                "expected_hex": {"type": "string", "description": "Reference hex, default IRPING golden"},
            },
            "required": ["hex"],
        },
    },
    {
        "name": "rel8",
        "description": "Compute a short branch displacement (next-ip = insn+2).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "insn": {"type": "integer"},
                "target": {"type": "integer"},
            },
            "required": ["insn", "target"],
        },
    },
    {
        "name": "rel16",
        "description": "Compute a near call/jmp displacement (next-ip = insn+3).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "insn": {"type": "integer"},
                "target": {"type": "integer"},
            },
            "required": ["insn", "target"],
        },
    },
    {
        "name": "selfloc",
        "description": "Compute lea bp,[bp+disp16] after call get_ip / pop bp.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pop_offset": {"type": "integer"},
                "base": {"type": "integer", "description": "Result base offset, default 128"},
            },
            "required": ["pop_offset"],
        },
    },
]

def _text(s):
    return {"content": [{"type": "text", "text": s}], "isError": False}

def _err(code, message):
    return {"code": code, "message": message}

def dispatch(name, args):
    args = args or {}
    if name == "selftest":
        res = B.selftest()
        lines = [("PASS " if ok else "FAIL ") + k for k, ok in res.items()]
        lines.append("ALL_PASS " + str(all(res.values())))
        return _text("\n".join(lines))

    if name == "parse":
        out = B.parse(args["text"])
        return _text("".join(f"{b:02X}" for b in out))

    if name == "emit":
        data = list(bytes.fromhex(args["hex"]))
        return _text(B.emit(data))

    if name == "decode":
        data = list(bytes.fromhex(args["hex"]))
        return _text("\n".join(f"{off:04X}  {text}" for off, _, text in B.decode(data)))

    if name == "patch":
        data = list(bytes.fromhex(args["hex"]))
        patches = [(p["offset"], p["value"]) for p in args["patches"]]
        return _text(B.emit(B.patch(data, patches)))

    if name == "check":
        actual = list(bytes.fromhex(args["hex"]))
        expected_hex = args.get("expected_hex", B.GOLDEN_HEX)
        expected = list(bytes.fromhex(expected_hex))
        return _text(json.dumps(B.check(actual, expected), indent=2))

    if name == "rel8":
        return _text(json.dumps(B.rel8(args["insn"], args["target"])))

    if name == "rel16":
        return _text(json.dumps(B.rel16(args["insn"], args["target"])))

    if name == "selfloc":
        return _text(json.dumps(B.selfloc_disp(args["pop_offset"], args.get("base", 128))))

    return _err(-32602, f"unknown tool: {name}")

class Handler(BaseHTTPRequestHandler):
    server_version = "pcjr-byte-mcp/1.0"

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Private-Network", "true")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self._cors()
        self.end_headers()
        self.wfile.write(b"pcjr-byte MCP endpoint. Use POST JSON-RPC.\n")

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length) if length else b"{}"
            req = json.loads(raw.decode("utf-8") or "{}")
        except Exception:
            self._send_json(400, {"jsonrpc": "2.0", "id": None,
                                  "error": _err(-32700, "parse error")})
            return

        rid = req.get("id")
        method = req.get("method")

        if method == "initialize":
            result = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "pcjr-byte", "version": "1.0.0"},
            }
        elif method == "tools/list":
            result = {"tools": TOOLS}
        elif method == "tools/call":
            params = req.get("params") or {}
            name = params.get("name")
            args = params.get("arguments") or {}
            try:
                result = dispatch(name, args)
            except Exception as exc:
                self._send_json(200, {"jsonrpc": "2.0", "id": rid,
                                      "error": _err(-32000, f"{exc}\n{traceback.format_exc()}")})
                return
        elif method == "notifications/initialized":
            # Server-initiated notifications are not used; acknowledge silently.
            self.send_response(202)
            self._cors()
            self.end_headers()
            return
        else:
            self._send_json(200, {"jsonrpc": "2.0", "id": rid,
                                  "error": _err(-32601, f"method not found: {method}")})
            return

        self._send_json(200, {"jsonrpc": "2.0", "id": rid, "result": result})

    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        sys.stderr.write("pcjr-byte-mcp: " + fmt % args + "\n")

def main():
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    server.allow_reuse_address = True
    print(f"pcjr-byte MCP listening on http://{HOST}:{PORT}/mcp", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\npcjr-byte MCP stopped", flush=True)

if __name__ == "__main__":
    main()
