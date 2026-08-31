# Handoff — IVTWR-LOOP torn-vector race disproof (single scope)

Date: 2026-08-30
Scope: disprove the torn-vector race hypothesis behind int02_vector_write_ub.

## Verified this session

- IVTWR-LOOP built via jr build stage 6, pass, no warnings; jr dis clean.
- Mode A (NMI masked): RETURNED OK, mismatch=0, final=3960:61440, kb alive.
- Mode B (NMI enabled, held-key): RETURNED OK, mismatch=0, final=3960:61440,
kb alive.
- Falsifier observed on clean run: hypothesis DISPROVED.
- Supersede proposed: int02_write_act_safe over int02_vector_write_ub.

## Open questions

- NMI arrival mid-write inferred, not measured. Held-key traffic over
~30 ms loop makes it near-certain; exact event count unknown.
- Actual dispatch into a custom INT 02h handler: untested, separate
question, not pre-authorized.

## Loose ends

- Skill Rule 7 and Rule 9 still say the write kills the keyboard; need a
surgical patch if the supersede lands.
- IVTWR-LOOP not anchored (disproof probe).

## Suggested next scope

Skill patch for Rules 7/9 if supersede approved. Then, only if needed:
actual custom-handler dispatch test.

## Ground truth

- docs/anchors/IRPING2.ASM / IRPING2.BAS — transport regression
- docs/anchors/CH0CAL.ASM / CH0CAL.bas — functional primary regression
- No new anchors this session.