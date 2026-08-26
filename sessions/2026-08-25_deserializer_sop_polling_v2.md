# 2026-08-25 — Deserializer SOP v2 (polling) + S1 frozen-image correction

Date: 2026-08-25
Scope: rewrite the custom-deserializer S0-S5 ladder around polling after the
INT 02h IVT-write UB close; correct the frozen S1 image record to the
bp-preserving v2. Record-only session, no hardware run.

## Verified this session

- Repo grep confirmed deserializer_sop_frozen still carries the
  interrupt-driven ladder (S1 NMI intercept, S2 CH0-in-NMI).
- Frozen 110-byte S1 image in 2026-08-25_s1_nmi_intercept_sop.md omits
  push bp/pop bp — it is the S1 v1 that div0'd on hardware. Corrected
  image is S1 v2 (114B) in 2026-08-25_s1_stage_gate_triggered.md.
- Ladder v2 locked for polling: S0 IRPING, S1 polling probe stub,
  S2 CH0-in-poll-loop, S3 one-frame edge capture, S4 gap classify +
  software decode, S5 make/break + consumer. No IVT write anywhere.

## Open questions

- S1 v2 body: verbatim IRPING edge-counter body plus NMI mask (lower risk,
  proven), or a smaller first-edge-only stub (less code, adds branch logic).
  Proposal defaults to verbatim; not locked.
- Stock BIOS make-only / held-key behavior (manual 5-21..5-42) still
  unverified; needed before S5, blocks nothing before.

## Loose ends

- S1 v1 (110B) and v2 (114B) listings remain unanchored; interrupt-driven
  path retired, do not resurrect.
- on_error_nmi_reenable pattern still untranscribed; irrelevant to the
  polling path but leave open for completeness.
- deserializer_sop memory key still points at the pre-pivot SOP; refresh in
  the memory batch for this close.

## Suggested next scope

- Build S1 v2 polling stub (BASLOAD.BAS + DATA). Gate: loaded-N byte count,
  emission gate via debug_asm, then hardware with IRPING -> CH0CAL
  regression. Pass: RETURNED OK, rising/falling >0, keyboard intact.
- On S1 v2 pass: advance S2 (CH0 latch per edge inside the poll loop).

## Ground truth

Anchors by name:

- IRPING (frozen DATA, platform skill Rule 5)
- docs/anchors/BASLOAD.BAS
- docs/anchors/CH0CAL.ASM
- docs/anchors/ENVSHAPE.BAS
- docs/anchors/AGCPROBE.BAS

No new hardware-passed program this session; nothing new to anchor.
