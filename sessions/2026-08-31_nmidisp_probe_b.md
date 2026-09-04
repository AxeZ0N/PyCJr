# Session — Probe B no-op redirect bisect

Date: 2026-08-31
Scope: determine whether a zero-work redirect into the stock KBDNMI chain
coexists with Cartridge BASIC, and pin the runtime INT 48h vector.

## Verified this session

- Runtime INT 48h = KEY62_INT at F000:10C6, manual-verified. KEY_SCAN_SAVE
  (F068) is POST-only; its stack-underflow HALT is not on the runtime path.
- KEY62_INT calls DDS itself (DS=0040h at 10C8); comment states "all
  registers are destroyed" by design, KBDNMI is the saving caller.
- KBDNMI entry contract: transparent save/restore; no ES read; DS only on
  the error path.
- No-op 57-byte redirect passes hardware: keyboard alive, keystroke echoed
  through INPUT after one IR key. Empirical.

## Open questions

- Did IRPING2 run immediately before the no-op pass? Status unconfirmed in
  the report; record when known.
- Does adding exactly ONE flag store back to the no-op break coexistence?
  The single-flag-store 69-byte stamped variant is built but unrun.
- What does the INT 9 processor do after KEY62_INT? STI at 10C6 re-enables
  interrupts mid-translation; the INT 9 body is unread.

## Loose ends

- The 69-byte and 70-byte stamped variants were built but skipped on
  hardware, superseded by the no-op bisect.
- Earlier handoff "ES=DATA" blocker was mislabeled and is corrected this
  session: no ES preload needed; the constraint is "do not clobber."
- KBDNMI comment says INT 41, code is CD 48 (INT 48h). Unresolved, low
  priority; disassembly wins.

## Suggested next scope

Single-variable iteration: take the no-op and add exactly one flag store
(the 69-byte stamped handler is the pre-built candidate). Freeze → the
nonzero-work hypothesis gains a second survival. Pass → the flag store was
never the defect and the earlier failures were the heavier register-save
frames. Read the INT 9 processor body before further chain work.

## Ground truth

- docs/anchors/NMIDISPB.BAS / NMIDISPB.ASM — Probe B no-op redirect,
  hardware-passed 2026-08-31.
- docs/anchors/NMIDISP.BAS / NMIDISP.ASM — Probe A custom dispatch,
  hardware-passed 2026-08-31.
- docs/anchors/IRPING2.BAS / IRPING2.ASM — transport regression.
