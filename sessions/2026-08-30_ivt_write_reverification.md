# Handoff — INT 02h IVT-write UB re-verification (single scope)

Date: 2026-08-30
Scope: Reopen the int02_vector_write_ub decision as unproven; spec a
readback-gated quiescent-write disproof probe; no hardware run this session.

## 1. Verified this session

- The 2026-08-25 UB decision rests on ladder stages 5/5c whose listings are
  absent from the repo. Only facts.md and session notes record them; no ASM
  or DATA survives.
- The 5c inference is circular: "never held a bogus vector" was never
  verified by readback. No byte-exactness, word-order, or two-word-completion
  check was performed.
- S1.ASM (full listing in sessions/2026-08-25_s1_nmi_intercept_sop.md,
  Ground truth section) implements the write correctly: OUT A0h,00h mask,
  offset word first, segment second, masked restore.
- The three 2026-08-25 failures are distinct: S1 v1 = BP clobber (bridge);
  S1 v2 = reboot in arming window, never root-caused; ladder 5/5c = the only
  runs attributed to "the write act," with no surviving listings.
- CLI/STI in the bridge is safe to the level of "a NOP-containing routine
  returns cleanly" only; nothing beyond the bridge is proven by it.

## 2. Open questions

- Does a masked, CLI-held, byte-exact two-word restore of the stock vector
  leave the keyboard intact? Unverified; this is the open disproof.

Disproof contract:

{
"id": "ivt_write_quiescent",
"hypothesis": "H — a masked, CLI-held, byte-exact two-word restore of the
stock vector to 0000:0008/000A leaves the keyboard intact.",
"falsifier": "F — keyboard dead with readback == F000:0F78 confirmed at
O+128/130 before the keyboard gate.",
"clean_run": "S — IRPING2 green; readback matches; BASIC returns; keyboard
functional after.",
"verdict": "pending"
}

- Mechanism if H fails: torn-vector window between the two stores, or NMI
  live during a store. Neither measured.
- Does the 8255 PC0 latch still set when NMI is masked (A0h D7=0)? Unverified;
  make-or-break for the PC0-seeded clone, separate from this probe.

## 3. Loose ends

- Ladder stage 5/5c DATA blocks exist only in chat history, if anywhere.
- S1 v2 reboot cause still unrooted; the ladder pivot abandoned it.
- int02_vector_write_ub in facts.md stands unmodified until the probe runs.

## 4. Suggested next scope

Build and run the stage-5c replica via jr build at stage 6: bridge prologue,
selfloc, OUT A0h,00h, CLI, save 0008/000A, no-op restore both words in IVT
order, readback both words to O+128/130, IN AL,A0h clear, OUT A0h,80h, STI,
POP BP, RETF. Regression IRPING2 first. Pass = keyboard intact with readback
confirmed; then narrow Rule 7 and reopen the custom INT 02
