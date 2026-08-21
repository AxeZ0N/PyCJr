#!/usr/bin/env python3
"""PCjr byte workbench. Pure stdlib. Prove all gates: python3 pcjr_byte.py selftest"""
import re
import sys

GOLDEN_HEX = ("0E1F55E800005D8DAE7A00BA6200EC2440B400894600"
              "89C6B9307531DB31FFBA6200EC244039F0740A85F674"
              "0347EB014389C6E2EA895E02897E045DCB")

GOLDEN_DATA = """1000 DATA &H0E,&H1F,&H55,&HE8,&H00,&H00,&H5D,&H8D,&HAE,&H7A,&H00
1010 DATA &HBA,&H62,&H00,&HEC,&H24,&H40,&HB4,&H00,&H89,&H46,&H00
1020 DATA &H89,&HC6,&HB9,&H30,&H75,&H31,&HDB,&H31,&HFF,&HBA,&H62
1030 DATA &H00,&HEC,&H24,&H40,&H39,&HF0,&H74,&H0A,&H85,&HF6,&H74
1040 DATA &H03,&H47,&HEB,&H01,&H43,&H89,&HC6,&HE2,&HEA,&H89,&H5E
1050 DATA &H02,&H89,&H7E,&H04,&H5D,&HCB
1060 DATA -1
"""


def parse(text):
    """BASIC DATA block -> byte list (stops at -1 sentinel)."""
    out = []
    for raw in text.splitlines():
        line = raw.strip().split("'")[0].strip()
        if not line:
            continue
        line = re.sub(r'^\d+\s+', '', line)
        if line.upper().startswith("DATA"):
            line = line[4:].lstrip()
        for tok in re.findall(r'&[Hh][0-9A-Fa-f]+|&[Oo][0-7]+|-?\d+', line):
            if tok.upper().startswith('&H'):
                v = int(tok[2:], 16)
            elif tok.upper().startswith('&O'):
                v = int(tok[2:], 8)
            else:
                v = int(tok, 10)
            if v == -1:
                return out
            if not (0 <= v <= 255):
                raise ValueError(f"out of byte range: {tok!r}")
            out.append(v)
    return out


def emit(data, start=1000, step=10, per=11):
    """byte list -> BASIC DATA block with sentinel."""
    lines, n = [], (len(data) + per - 1) // per
    for i in range(n):
        chunk = data[i * per:(i + 1) * per]
        lines.append(f"{start + i * step} DATA "
                     + ",".join(f"&H{b:02X}" for b in chunk))
    lines.append(f"{start + n * step} DATA -1")
    return "\n".join(lines)


def patch(data, patches):
    """Non-mutating (offset,value) edits; ValueError on bad input."""
    out = list(data)
    for off, val in patches:
        if not (0 <= off < len(data)):
            raise ValueError(f"offset out of range: {off}")
        if not (0 <= val <= 255):
            raise ValueError(f"value out of byte range: {val}")
        out[off] = val
    return out


def check(actual, expected):
    """Compare byte lists -> report dict."""
    a, e = list(actual), list(expected)
    first = next((i for i in range(min(len(a), len(e))) if a[i] != e[i]), None)
    if first is None and len(a) != len(e):
        first = min(len(a), len(e))
    return {"ok": len(a) == len(e) and first is None,
            "delta": len(a) - len(e), "first_diff": first}


def rel8(insn, target):
    """Short branch displacement bytes (next-ip = insn+2)."""
    disp = target - (insn + 2)
    if not (-128 <= disp <= 127):
        raise ValueError(f"rel8 out of range: {disp}")
    return [disp & 0xFF]


def rel16(insn, target):
    """Near call/jmp displacement bytes (next-ip = insn+3)."""
    if not (-32768 <= target - (insn + 3) <= 32767):
        raise ValueError("rel16 out of range")
    disp = (target - (insn + 3)) & 0xFFFF
    return [disp & 0xFF, (disp >> 8) & 0xFF]


def selfloc_disp(pop_off, base=128):
    """lea bp,[bp+disp16] after call get_ip / pop bp."""
    disp = base - pop_off
    if not (0 <= disp <= 0xFFFF):
        raise ValueError(f"selfloc out of range: {disp}")
    return [disp & 0xFF, (disp >> 8) & 0xFF]


REGS16 = ["ax", "cx", "dx", "bx", "sp", "bp", "si", "di"]
REG8 = ["al", "cl", "dl", "bl", "ah", "ch", "dh", "bh"]
EA0 = ["[bx+si]", "[bx+di]", "[bp+si]", "[bp+di]", "[si]", "[di]", None, "[bx]"]

OP1 = {0x0E: "push cs", 0x1F: "pop ds", 0x55: "push bp", 0x5D: "pop bp",
       0xEC: "in al,dx", 0xCB: "retf"}

REL8 = {0x74: "je", 0x75: "jne", 0xEB: "jmp", 0xE2: "loop"}

IMM8 = {0x24: "and al,0x%02X", 0xB4: "mov ah,0x%02X",
        0xE4: "in al,0x%02X", 0xE6: "out 0x%02X,al",
        0xB0: "mov al,0x%02X"}

IMM16 = {0xBA: "mov dx,0x%04X", 0xB9: "mov cx,0x%04X"}

MNEMO = {0x89: "mov", 0x31: "xor", 0x39: "cmp", 0x85: "test"}

MNEMO8_RM_REG = {0x88: "mov"}   # MOV r/m8, r8
MNEMO8_REG_RM = {0x3A: "cmp"}   # CMP r8, r/m8


def _s8(v):
    return v - 256 if v >= 128 else v


def _s16(v):
    return v - 65536 if v >= 32768 else v


def _u16(lo, hi):
    return lo | (hi << 8)


def decode(data):
    """byte list -> [(offset, length, text)] for the verified subset."""
    out, off, n = [], 0, len(data)
    while off < n:
        b = data[off]
        start = off
        if b in OP1:
            off += 1
            text = OP1[b]
        elif 0x40 <= b <= 0x47:
            off += 1
            text = f"inc {REGS16[b - 0x40]}"
        elif b in REL8:
            text = f"{REL8[b]} 0x{(off + 2 + _s8(data[off + 1])) & 0xFFFF:04X}"
            off += 2
        elif b == 0xE8:
            next_ip = off + 3
            text = f"call 0x{(next_ip + _s16(_u16(data[off + 1], data[off + 2]))) & 0xFFFF:04X}"
            off += 3
        elif b in IMM8:
            text = IMM8[b] % data[off + 1]
            off += 2
        elif b in IMM16:
            text = IMM16[b] % _u16(data[off + 1], data[off + 2])
            off += 3
        elif 0xB8 <= b <= 0xBF:
            imm = _u16(data[off + 1], data[off + 2])
            off += 3
            text = f"mov {REGS16[b - 0xB8]},0x{imm:04X}"
        elif b == 0x8D or b in MNEMO or b in (0x88, 0x3A, 0x80):
            off, text = _modrm(data, off)
        else:
            text = f"db 0x{b:02X} ; outside verified subset"
            off += 1
        out.append((start, off - start, text))
    return out


def _modrm(data, off):
    opcode = data[off]
    m = data[off + 1]
    mod, reg, rm = (m >> 6) & 3, (m >> 3) & 7, m & 7
    p = off + 2

    if mod == 3:
        rm8 = REG8[rm]
        rm16 = REGS16[rm]
        mem = ""
    elif mod == 0:
        if rm == 6:
            disp = _u16(data[p], data[p + 1])
            p = off + 4
            mem = f"[0x{disp:04X}]"
        else:
            mem = EA0[rm]
    elif mod == 1:
        disp = data[p]
        p = off + 3
        base = EA0[rm]
        mem = f"[bp+0x{disp:02X}]" if rm == 6 else f"{base}+0x{disp:02X}"
    else:
        disp = _u16(data[p], data[p + 1])
        p = off + 4
        base = EA0[rm]
        mem = f"[bp+0x{disp:04X}]" if rm == 6 else f"{base}+0x{disp:04X}"

    def rm_oper(use8):
        if mod == 3:
            return rm8 if use8 else rm16
        return mem

    if opcode == 0x8D:
        return p, f"lea {REGS16[reg]},{mem}"
    if opcode in MNEMO:
        return p, f"{MNEMO[opcode]} {rm_oper(False)},{REGS16[reg]}"
    if opcode in MNEMO8_RM_REG:
        return p, f"{MNEMO8_RM_REG[opcode]} {rm_oper(True)},{REG8[reg]}"
    if opcode in MNEMO8_REG_RM:
        return p, f"{MNEMO8_REG_RM[opcode]} {REG8[reg]},{rm_oper(True)}"
    if opcode == 0x80:
        if reg == 7:
            imm = data[p]
            p += 1
            return p, f"cmp {rm_oper(True)},0x{imm:02X}"
        # Unsupported group /N: consume imm8 so the stream stays aligned.
        p += 1
        return p, f"db 0x80 ; group /{reg} unsupported"
    return p, f"db 0x{opcode:02X} ; outside verified subset"


def branch_checks(data, checks):
    """Verify (insn_addr, target) pairs against decoded displacements."""
    reports = []
    for at, target in checks:
        b = data[at]
        if b in REL8:
            rel = _s8(data[at + 1])
            actual = (at + 2 + rel) & 0xFFFF
        elif b == 0xE8:
            rel = _s16(_u16(data[at + 1], data[at + 2]))
            actual = (at + 3 + rel) & 0xFFFF
        else:
            reports.append({
                "at": at, "target": target, "actual": None, "ok": False,
                "error": f"opcode 0x{b:02X} is not a supported branch",
            })
            continue
        reports.append({"at": at, "target": target, "actual": actual,
                        "ok": actual == target})
    return {"ok": all(r["ok"] for r in reports), "checks": reports}


def selftest():
    """All stage gates against the frozen IRPING image."""
    g = list(bytes.fromhex(GOLDEN_HEX))
    d = parse(GOLDEN_DATA)
    e = emit(g)
    dec = decode(g)
    p = patch(g, [(0x19, 0x00), (0x1A, 0x01)])
    return {
        "parse_61": len(d) == 61 and d[0] == 0x0E and d[-1] == 0xCB,
        "parse_full": d == g,
        "emit_exact": e == GOLDEN_DATA.strip(),
        "emit_roundtrip": parse(e) == g,
        "decode_61": sum(ln for _, ln, _ in dec) == len(g),
        "decode_31": len(dec) == 31,
        "decode_test_si_si": dec[20][2] == "test si,si",
        "decode_out_imm8": decode([0xE6, 0x43])[0][2] == "out 0x43,al",
        "decode_in_imm8": decode([0xE4, 0x40])[0][2] == "in al,0x40",
        "decode_latch_path": ([t for _, _, t in decode(
            [0xE6, 0x43, 0xE4, 0x40, 0xE4, 0x40])] ==
            ["out 0x43,al", "in al,0x40", "in al,0x40"]),
        "decode_b0_latch_setup": ([t for _, _, t in decode(
            [0xB0, 0x00, 0xE6, 0x43, 0xE4, 0x40, 0xE4, 0x40])] ==
            ["mov al,0x00", "out 0x43,al", "in al,0x40", "in al,0x40"]),
        "decode_88_c3": decode([0x88, 0xC3])[0][2] == "mov bl,al",
        "decode_88_46": decode([0x88, 0x46, 0x00])[0][2] == "mov [bp+0x00],al",
        "decode_3a_c3": decode([0x3A, 0xC3])[0][2] == "cmp al,bl",
        "decode_80_fb_00": decode([0x80, 0xFB, 0x00])[0][2] == "cmp bl,0x00",
        "decode_b8_0100": decode([0xB8, 0x01, 0x00])[0][2] == "mov ax,0x0001",
        "decode_inc_si": decode([0x46])[0][2] == "inc si",
        "branch_audit": branch_checks(
            list(bytes.fromhex(GOLDEN_HEX)),
            [(0x27, 0x0033), (0x2E, 0x0031), (0x33, 0x001F)],
        )["ok"],
        "patch_len61": len(p) == 61,
        "patch_19_1A": p[0x19] == 0x00 and p[0x1A] == 0x01,
        "check_good": check(g, g)["ok"],
        "check_drop": check(g[:0x23] + g[0x24:], g)["first_diff"] == 0x23,
        "rel_call": rel16(0x03, 0x0006) == [0x00, 0x00],
        "rel_je": rel8(0x27, 0x0033) == [0x0A],
        "rel_loop": rel8(0x33, 0x001F) == [0xEA],
        "selfloc": selfloc_disp(6, 128) == [0x7A, 0x00],
    }


def main(argv):
    if not argv or argv[0] == "selftest":
        all_pass = True
        for name, ok in selftest().items():
            if not ok:
                all_pass = False
            print(("PASS" if ok else "FAIL"), name)
        print("ALL_PASS", all_pass)
        return
    cmd, data = argv[0], None
    if cmd in ("parse", "dis", "patch", "check"):
        data = parse(sys.stdin.read())
    if cmd == "parse":
        print(f"bytes={len(data)}")
        print("".join(f"{b:02X}" for b in data))
        print(emit(data))
    elif cmd == "dis":
        for off, ln, text in decode(data):
            print(f"{off:04X}  {text}")
    elif cmd == "patch":
        p = [(int(s.split('=')[0], 0), int(s.split('=')[1], 0)) for s in argv[1:]]
        print(emit(patch(data, p)))
    elif cmd == "check":
        print(check(data, list(bytes.fromhex(GOLDEN_HEX))))
    else:
        print("usage: pcjr_byte.py selftest|parse|dis|patch off=val ...|check")


if __name__ == "__main__":
    main(sys.argv[1:])
