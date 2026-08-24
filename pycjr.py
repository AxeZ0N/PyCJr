#!/usr/bin/env python3
"""
PCjr stock IR keyboard emulator — integrated prototype.

Backend: reduced PCjrIRSender (frame/press/wave only, verified).
Outer layer: text input, atomic Shift handling, 50 chars/sec throttle.

Still stubs / intentionally omitted:
  - ANSI escape -> F-keys/arrows (ESC_MAP) : native PCjr codes unverified
  - Ctrl+Break                             : native sequence unverified
  - stateful make/break                    : out of scope by design
"""

import argparse
import time
import os
import pigpio

# ----------------------------------------------------------------------
# Verified scan tables
# ----------------------------------------------------------------------
SCAN = {
    "a": 0x1E,
    "b": 0x30,
    "c": 0x2E,
    "d": 0x20,
    "e": 0x12,
    "f": 0x21,
    "g": 0x22,
    "h": 0x23,
    "i": 0x17,
    "j": 0x24,
    "k": 0x25,
    "l": 0x26,
    "m": 0x32,
    "n": 0x31,
    "o": 0x18,
    "p": 0x19,
    "q": 0x10,
    "r": 0x13,
    "s": 0x1F,
    "t": 0x14,
    "u": 0x16,
    "v": 0x2F,
    "w": 0x11,
    "x": 0x2D,
    "y": 0x15,
    "z": 0x2C,
    "0": 0x0B,
    "1": 0x02,
    "2": 0x03,
    "3": 0x04,
    "4": 0x05,
    "5": 0x06,
    "6": 0x07,
    "7": 0x08,
    "8": 0x09,
    "9": 0x0A,
    " ": 0x39,
    "-": 0x0C,
    "=": 0x0D,
    "[": 0x1A,
    "]": 0x1B,
    ";": 0x27,
    "'": 0x28,
    "`": 0x29,
    "\\": 0x2B,
    ",": 0x33,
    ".": 0x34,
    "/": 0x35,
    "\n": 0x1C,
    "\r": 0x1C,
    "\t": 0x0F,
    "\b": 0x0E,
    "\x1b": 0x01,
    "\x7f": 0x0E,  # Backspace (DEL)
}

SHIFT = {
    "!": "1",
    "@": "2",
    "#": "3",
    "$": "4",
    "%": "5",
    "^": "6",
    "&": "7",
    "*": "8",
    "(": "9",
    ")": "0",
    "_": "-",
    "+": "=",
    "{": "[",
    "}": "]",
    ":": ";",
    '"': "'",
    "~": "`",
    "<": ",",
    ">": ".",
    "?": "/",
    "|": "\\",
}

# ----------------------------------------------------------------------
# Native PCjr F-key chords
# ----------------------------------------------------------------------
# F1-F10 are Fn + top-row digit scancodes. F11-F12 are standalone.
FKEY_SCANCODES = {
    1: 0x02,
    2: 0x03,
    3: 0x04,
    4: 0x05,
    5: 0x06,
    6: 0x07,
    7: 0x08,
    8: 0x09,
    9: 0x0A,
    10: 0x0B,
    11: 0x57,
    12: 0x58,
}

# ANSI F-key sequences -> F-key number.
ESC_FKEY_MAP = {
    b"\x1bOP": 1,
    b"\x1bOQ": 2,
    b"\x1bOR": 3,
    b"\x1bOS": 4,
    b"\x1b[15~": 5,
    b"\x1b[17~": 6,
    b"\x1b[18~": 7,
    b"\x1b[19~": 8,
    b"\x1b[20~": 9,
    b"\x1b[21~": 10,
    b"\x1b[23~": 11,
    b"\x1b[24~": 12,
}

# Verified by measurement: these scancodes are accepted by the PCjr and
# translated correctly by KEY62-INT when sent as standalone make+break.
ESC_MAP = {
    b"\x1b[A": 0x48,
    b"\x1b[B": 0x50,
    b"\x1b[C": 0x4D,
    b"\x1b[D": 0x4B,
    b"\x1bOA": 0x48,
    b"\x1bOB": 0x50,
    b"\x1bOC": 0x4D,
    b"\x1bOD": 0x4B,
    b"\x1b[H": 0x47,
    b"\x1b[F": 0x4F,
    b"\x1b[5~": 0x49,
    b"\x1b[6~": 0x51,
    b"\x1b[2~": 0x52,
    b"\x1b[3~": 0x53,
    b"\x1bOP": 0x3B,
    b"\x1bOQ": 0x3C,
    b"\x1bOR": 0x3D,
    b"\x1bOS": 0x3E,
    b"\x1b[15~": 0x3F,
    b"\x1b[17~": 0x40,
    b"\x1b[18~": 0x41,
    b"\x1b[19~": 0x42,
    b"\x1b[20~": 0x43,
    b"\x1b[21~": 0x44,
    b"\x1b[23~": 0x57,
    b"\x1b[24~": 0x58,
}

# VERIFY: SHIFT_SCAN against previous working table if regenerated.
# Standard left Shift scancode.
SHIFT_SCAN = 0x2A
FN_SCAN = 0x54


# ----------------------------------------------------------------------
# Reduced sender — frame/press/wave only. Do not extend beyond this.
# ----------------------------------------------------------------------
class PCjrIRSender:
    def __init__(
        self,
        gpio=2,
        burst_us=62,
        start_silence_us=310,
        one_silence_us=377,
        zero_silence_1_us=220,
        zero_silence_2_us=157,
        frame_gap_us=1500,
        carrier_half_a=12,
        carrier_half_b=13,
    ):
        self.gpio = gpio
        self.pin = 1 << gpio
        self.burst_us = burst_us
        self.start_silence_us = start_silence_us
        self.one_silence_us = one_silence_us
        self.zero_silence_1_us = zero_silence_1_us
        self.zero_silence_2_us = zero_silence_2_us
        self.frame_gap_us = frame_gap_us
        self.carrier_half_a = carrier_half_a
        self.carrier_half_b = carrier_half_b
        self.pi = None

    def connect(self):
        self.pi = pigpio.pi()
        if not self.pi.connected:
            raise RuntimeError("pigpiod not running; run: sudo pigpiod")
        self.pi.set_mode(self.gpio, pigpio.OUTPUT)
        self.pi.write(self.gpio, 0)  # active-high idle = LED off
        return self

    def close(self):
        if self.pi is not None:
            self.pi.write(self.gpio, 0)
            self.pi.stop()
            self.pi = None

    # -- pulse primitives ------------------------------------------------
    def _idle_pulse(self, us):
        return pigpio.pulse(0, self.pin, us)

    def _led_on_pulse(self, us):
        return pigpio.pulse(self.pin, 0, us)

    def _silence(self, us):
        return [self._idle_pulse(us)]

    def _burst(self):
        pulses = []
        on = False
        remaining = self.burst_us
        half = self.carrier_half_a
        while remaining > 0:
            d = min(half, remaining)
            pulses.append(self._led_on_pulse(d) if on else self._idle_pulse(d))
            remaining -= d
            on = not on
            half = (
                self.carrier_half_b
                if half == self.carrier_half_a
                else self.carrier_half_a
            )
        return pulses

    # -- frame construction ----------------------------------------------
    def build_frame(self, scan):
        """start + 8 data bits + odd parity + trailing frame gap."""
        p = []
        p += self._burst()
        p += self._silence(self.start_silence_us)

        ones = 0
        for bit in range(8):
            if (scan >> bit) & 1:
                p += self._burst()
                p += self._silence(self.one_silence_us)
                ones += 1
            else:
                p += self._silence(self.zero_silence_1_us)
                p += self._burst()
                p += self._silence(self.zero_silence_2_us)

        parity_bit = 0 if (ones & 1) else 1
        if parity_bit == 0:
            p += self._silence(self.zero_silence_1_us)
            p += self._burst()
            p += self._silence(self.zero_silence_2_us)
        else:
            p += self._burst()
            p += self._silence(self.one_silence_us)

        p += self._silence(self.frame_gap_us)
        return p

    def key_press_pulses(self, scan):
        """make frame + break frame."""
        return self.build_frame(scan) + self.build_frame(scan | 0x80)

    # -- transport --------------------------------------------------------
    def send_wave(self, pulses):
        if not pulses:
            raise RuntimeError("empty wave pulse list")
        self.pi.wave_clear()
        added = self.pi.wave_add_generic(pulses)
        if added <= 0:
            raise RuntimeError(f"wave_add_generic failed: {added}")
        wid = self.pi.wave_create()
        if wid < 0:
            raise RuntimeError(f"wave_create failed: {wid}")
        self.pi.wave_send_once(wid)
        while self.pi.wave_tx_busy():
            time.sleep(0.005)
        self.pi.wave_delete(wid)

    def send_key_press(self, scan):
        self.send_wave(self.key_press_pulses(scan))


# ----------------------------------------------------------------------
# Emulator outer layer
# ----------------------------------------------------------------------
class PCjrEmulator(PCjrIRSender):
    """Outer character layer. Inherits transport and frame building."""

    def __init__(self, chars_per_sec=50):
        super().__init__()
        self.char_interval_s = 1.0 / max(1, chars_per_sec)
        self._last_char_time = 0.0

    # -- character layer --------------------------------------------------
    def send_char(self, ch, use_enter_delay=True):
        """Send one character as an atomic make+break sequence.

        Shift is pressed and released inside the same wave, so an
        interrupted send cannot leave Shift stuck on the PCjr.
        """
        if ch in SCAN:
            self.send_key_press(SCAN[ch])
            if ch == '\n': time.sleep(0.5)
            return

        if ch.isupper() and ch.lower() in SCAN:
            base = SCAN[ch.lower()]
        elif ch in SHIFT and SHIFT[ch] in SCAN:
            base = SCAN[SHIFT[ch]]
        else:
            raise ValueError(f"No scan code mapping for character: {ch!r}")

        self.send_wave(
            self.build_frame(SHIFT_SCAN)  # Shift make
            + self.key_press_pulses(base)  # key make+break
            + self.build_frame(SHIFT_SCAN | 0x80)  # Shift break
        )

    def send_text(self, text):
        """Send text with conservative pacing; one key at a time."""
        for ch in text:
            self.send_char(ch)
            self._throttle()

    # -- pacing -----------------------------------------------------------
    def _throttle(self):
        now = time.monotonic()
        wait = self._last_char_time + self.char_interval_s - now
        if wait > 0:
            time.sleep(wait)
        self._last_char_time = time.monotonic()

    def send_ansi_escape(self, seq):
        """Send one ANSI terminal escape sequence.

        F-keys use the native Fn+digit chord via send_fkey().
        Other sequences use the measured ESC_MAP scancodes.
        """
        if isinstance(seq, str):
            seq = seq.encode("latin-1")

        if seq in ESC_FKEY_MAP:
            self.send_fkey(ESC_FKEY_MAP[seq])
            return

        try:
            scan = ESC_MAP[seq]
        except KeyError:
            raise KeyError(f"Unknown ANSI escape sequence: {seq!r}") from None
        self.send_key_press(scan)

    def send_scan(self, scan):
        """Send one raw make+break scancode, bypassing the character tables."""
        self.send_key_press(scan)

    def _modifier_tap(self, mod_scan, tap_scan):
        """Press mod_scan, tap tap_scan, release mod_scan. Atomic."""
        self.send_wave(
            self.build_frame(mod_scan)
            + self.key_press_pulses(tap_scan)
            + self.build_frame(mod_scan | 0x80)
        )

    def send_ctrl_break(self):
        """Ctrl+Break = Fn+B on the PCjr. Verified."""
        self._modifier_tap(FN_SCAN, SCAN["b"])

    def send_fkey(self, n):
        """Send F-key n (1-12).

        F1-F10 use the native Fn+digit chord.
        F11-F12 use verified standalone scancodes.
        """
        if n not in FKEY_SCANCODES:
            raise ValueError(f"Unsupported function key: F{n}")

        scan = FKEY_SCANCODES[n]
        if n <= 10:
            self._modifier_tap(FN_SCAN, scan)
        else:
            self.send_key_press(scan)

    def testing_macro(self, code: int, delay_after_enter: int, delay_between_codes: int):
        """
        Press enter, wait then send a single frame. Wait, then send it again.
        code: int = scancode / hex / int to encode just make sure it's a byte
        delay_after_enter: int = seconds
        delay_between_codes: int = micro seconds
        """
        # The wave builder will append delay_between_codes at the end of the sequence
        original_frame_gap_us = self.frame_gap_us
        self.frame_gap_us = delay_between_codes 


        test_frames = self.build_frame(code) + self.build_frame(code)
        # Reset delay
        self.frame_gap_us = original_frame_gap_us

        self.send_char('\n')
        time.sleep(delay_after_enter)
        self.send_wave(test_frames)




import select
import sys
import termios
import tty


def _read_escape_sequence(fd):
    """Read an ANSI escape sequence starting with ESC (already consumed)."""
    seq = b"\x1b"
    while True:
        ready, _, _ = select.select([fd], [], [], 0.5)
        if not ready:
            break
        try:
            b = os.read(fd, 1)
        except OSError:
            break
        if not b:
            break
        seq += b
        if seq in ESC_MAP:
            return seq
        if not any(k.startswith(seq) for k in ESC_MAP):
            break

    return seq


def stdin_passthrough(emu):
    """Stream stdin to the PCjr.

    TTY mode:
      Ctrl+C       exit locally (does not send)
      Ctrl+B       send PCjr Ctrl+Break (Fn+B)
      Esc/ANSI     arrows, nav, F-keys via ESC_MAP
      everything   sent as text with the emulator throttle
    """
    fd = sys.stdin.fileno()

    if not sys.stdin.isatty():
        data = sys.stdin.buffer.read()
        emu.send_text(data.decode("ascii", errors="replace"))
        return

    print("Begin typing", flush=True)

    old_attrs = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)

        while True:
            ready, _, _ = select.select([fd], [], [], None)
            if not ready:
                continue
            b = os.read(fd, 1)
            if not b:
                break

            # Local controls, never sent to the PCjr.
            if b == b"\x03":  # Ctrl+C: exit passthrough
                break
            if b == b"\x02":  # Ctrl+B: PCjr Ctrl+Break
                emu.send_ctrl_break()
                continue

            # ANSI escape sequence: arrows, nav, F1-F12.
            if b == b"\x1b":
                seq = _read_escape_sequence(fd)
                try:
                    emu.send_ansi_escape(seq)
                except KeyError:
                    # Bare Esc or unknown sequence. Bare Esc is mapped in SCAN.
                    if seq == b"\x1b":
                        emu.send_char("\x1b")
                continue

            ch = b.decode("ascii", errors="replace")
            if ch:
                emu.send_char(ch)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_attrs)
        emu.close()


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="PCjr stock IR keyboard emulator")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--char", help="send exactly one character")
    group.add_argument("--text", help="send a text payload")
    group.add_argument("--scan", help="send one raw scancode as hex, e.g. 48")
    group.add_argument(
        "--escape", help="send one ANSI escape sequence as hex, e.g. 1b5b41"
    )
    group.add_argument("--cc", action="store_true", help="Send Ctrl+C to PCJr")
    group.add_argument(
        "--stdin", action="store_true", help="stream stdin to the PCjr interactively"
    )
    group.add_argument("--fkey", type=int, help="send F1-F12 (1-12)")
    group.add_argument("--run_test", action="store_true", help="Runs hardcoded test frames")

    args = parser.parse_args()

    emu = PCjrEmulator(chars_per_sec=60)
    emu.connect()
    try:
        if args.stdin:
            stdin_passthrough(emu)
            return
        if args.char is not None:
            if len(args.char) != 1:
                raise SystemExit("--char expects exactly one character")
            emu.send_char(args.char)
        elif args.run_test:
            emu.testing_macro(0x23, 0.5, 1500)
        elif args.scan is not None:
            emu.send_key_press(int(args.scan, 16))
        elif args.escape is not None:
            emu.send_ansi_escape(bytes.fromhex(args.escape))
        elif args.cc:
            emu.send_ctrl_break()
        elif args.fkey is not None:
            emu.send_fkey(args.fkey)
        else:
            emu.send_text(args.text)
    finally:
        emu.close()


if __name__ == "__main__":
    main()
