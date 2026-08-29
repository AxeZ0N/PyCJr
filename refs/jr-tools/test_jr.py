#!/usr/bin/env python3
"""Self-verification tests for jr tool (Spec Section 8)."""

import os
import sys
import subprocess
import tempfile
import shutil
import filecmp

JR_PATH = os.path.join(os.path.dirname(__file__), "jr")

def run_jr(args, cwd):
    """Run jr tool, return (returncode, stdout, stderr)."""
    proc = subprocess.run(
        [sys.executable, JR_PATH] + args,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return proc.returncode, proc.stdout, proc.stderr

def write_bytes(path, hexstr):
    with open(path, "wb") as f:
        f.write(bytes.fromhex(hexstr))

def test_f1_irping_passes(tmpdir):
    hex_bytes = ("0E1F55E800005D8DAE7A00"
                 "BA6200EC2440B400894600"
                 "89C6B9307531DB31FFBA62"
                 "00EC244039F0740A85F674"
                 "0347EB014389C6E2EA895E"
                 "02897E045DCB")
    bin_path = os.path.join(tmpdir, "irping.bin")
    write_bytes(bin_path, hex_bytes)
    rc, stdout, stderr = run_jr(["lint", "irping.bin", "--result", "128", "--stage", "6"], tmpdir)
    assert rc == 0, f"F1 failed: rc={rc}, stderr={stderr}"
    assert "PASS" in stdout
    print("F1 PASS")

def test_f2_selfloc_trap_fails(tmpdir):
    hex_bytes = "0E1F55E800005D8DAE80005DCB"
    bin_path = os.path.join(tmpdir, "selfloc_bad.bin")
    write_bytes(bin_path, hex_bytes)
    rc, stdout, stderr = run_jr(["lint", "selfloc_bad.bin", "--result", "128", "--stage", "6"], tmpdir)
    assert rc == 4, f"F2 expected rc=4, got {rc}"
    assert "selfloc" in stderr
    assert "expected displacement 122" in stderr
    assert "128" in stderr
    # or more specifically:
    assert "lea bp,[bp+128]" in stderr
    print("F2 PASS")

def test_f3_missing_nmi_restore(tmpdir):
    hex_bytes = "0E1F55E800005D8DAE7A00B000E6A05DCB"
    bin_path = os.path.join(tmpdir, "nmi_missing.bin")
    write_bytes(bin_path, hex_bytes)
    # without --strict: should be WARN and rc=0
    rc, stdout, stderr = run_jr(["lint", "nmi_missing.bin", "--result", "128", "--stage", "5"], tmpdir)
    assert rc == 0, f"F3 (non-strict) expected rc=0, got {rc}"
    assert "WARN" in stderr
    assert "NMI restore" in stderr
    # with --strict: should be rc=4
    rc2, _, stderr2 = run_jr(["lint", "nmi_missing.bin", "--result", "128", "--stage", "5", "--strict"], tmpdir)
    assert rc2 == 4, f"F3 (strict) expected rc=4, got {rc2}"
    assert "NMI restore" in stderr2
    print("F3 PASS")

def test_f4_non_nmi_passes(tmpdir):
    hex_bytes = "0E1F55E800005D8DAE7A005DCB"
    bin_path = os.path.join(tmpdir, "non_nmi.bin")
    write_bytes(bin_path, hex_bytes)
    rc, stdout, stderr = run_jr(["lint", "non_nmi.bin", "--result", "128", "--stage", "5"], tmpdir)
    assert rc == 0, f"F4 expected rc=0, got {rc}"
    assert "PASS" in stdout
    print("F4 PASS")

def test_f5_data_roundtrip(tmpdir):
    hex_bytes = ("0E1F55E800005D8DAE7A00"
                 "BA6200EC2440B400894600"
                 "89C6B9307531DB31FFBA62"
                 "00EC244039F0740A85F674"
                 "0347EB014389C6E2EA895E"
                 "02897E045DCB")
    bin_path = os.path.join(tmpdir, "irping.bin")
    write_bytes(bin_path, hex_bytes)
    # generate DATA file
    rc, data_out, _ = run_jr(["data", "irping.bin"], tmpdir)
    assert rc == 0
    data_file = os.path.join(tmpdir, "irping.data")
    with open(data_file, "w") as f:
        f.write(data_out)
    # parse it back
    parsed_bin = os.path.join(tmpdir, "roundtrip.bin")
    rc, _, stderr = run_jr(["parse", "--out", "roundtrip.bin", "irping.data"], tmpdir)
    assert rc == 0, f"parse failed: {stderr}"
    # compare
    assert filecmp.cmp(bin_path, parsed_bin), "roundtrip mismatch"
    print("F5 PASS")

def test_f6_uasm_padding_selftest(tmpdir):
    # Create asm source with only retf in canonical skeleton
    asm_src = os.path.join(tmpdir, "trivial.asm")
    with open(asm_src, "w") as f:
        f.write("""\
option casemap:none
option segment:use16

code segment
    assume cs:code
    org 0
start:
    retf
code ends
end start
""")
    out_bin = os.path.join(tmpdir, "trivial.bin")
    lst_file = os.path.join(tmpdir, "trivial.lst")
    uasm = "uasm"  # assume on PATH
    cmd = ["uasm", "-bin", f"-Fl={lst_file}", "-Fo", out_bin, asm_src]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    assert proc.returncode == 0, f"UASM failed: {proc.stderr}"
    with open(out_bin, "rb") as f:
        data = f.read()
    assert len(data) == 1 and data[0] == 0xCB, f"padding check failed: got {data.hex()}"
    print("F6 PASS")

def main():
    with tempfile.TemporaryDirectory() as tmpdir:
        test_f1_irping_passes(tmpdir)
    with tempfile.TemporaryDirectory() as tmpdir:
        test_f2_selfloc_trap_fails(tmpdir)
    with tempfile.TemporaryDirectory() as tmpdir:
        test_f3_missing_nmi_restore(tmpdir)
    with tempfile.TemporaryDirectory() as tmpdir:
        test_f4_non_nmi_passes(tmpdir)
    with tempfile.TemporaryDirectory() as tmpdir:
        test_f5_data_roundtrip(tmpdir)
    with tempfile.TemporaryDirectory() as tmpdir:
        test_f6_uasm_padding_selftest(tmpdir)
    print("All tests passed.")

if __name__ == "__main__":
    main()
