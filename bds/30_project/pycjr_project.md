# PyCJr Project (v4)

This project targets the IBM PCjr 4860/4861 and the Pi-side IR sender
(pigpio, GPIO18, 40 kHz carrier). No DOS is loaded by default; machine
code runs through the Cartridge BASIC bridge.

## Always-active rules

- Skills `pcjr_cartridge_basic_asm` and `pcjr_test_workflow` are
  authoritative. If they are not present in context, re-request them
  before emitting code.
- The IBM PCjr Technical Reference (via `pcjr-tools` MCP) is the
  hardware authority. The strip is noisy OCR.
- Label every hardware fact: `manual-verified`, `empirical`,
  `unverified`, or `conflict`. Never pass an unverified
  port/segment/vector value without a `; VERIFY:` tag.
- On hang, cold power-cycle. Never assume Ctrl+Alt+Del recovers.
- Never emit the prohibited constructs listed in the platform skill.
- When IR transport behavior is suspect, run IRPING first.
- Ask before generating full files or running a new experiment.

## Assumptions

- All PCjr keyboard input arrives via the IR module. Pi passthrough:
  press or held key both emit make/break; held repeats frames. No
  physical keyboard involved; same input channel.
- Default: no DOS. BIOS interrupts only unless DOS is confirmed.

## Session scope policy

Long PyCJr sessions degrade performance and debug efficiency. Each
session must have a defined scope. When the scope is done, recommend
starting a new session.

## Hardware state (pointer)

Stable hardware facts live in `pcjr_cartridge_basic_asm` Rule 6 and
Rule 7. Do not restate values here; point to the skill. CH0 clock is
empirical and owned by the skill's hardware map.

## Open items (this file is the owner)

1. 38-vs-40 edge variance root cause.
2. Timer-2 IR-test wrap verification (manual 2-85..2-89).
3. IR-test edge probe (mask NMI, A0h 40h, finite poll PC6).
4. RAM demodulator chaining unrecognized frames to the stock path.

## Volatile measurements

Per-session readings — edge counts, max_delta, gap counts, iteration
counts, pass results — belong in the session handoff and
`docs/test_log.md`, not in this file or the skills. Update the handoff
as experiments progress.
