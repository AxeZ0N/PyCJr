# 2026-08-25 — S1 IVT write UB (single scope)

Scope: stage-gated per-instruction ladder; find the S1 v2 reboot cause;
close the interrupt-driven deserializer path.

## Verified this session

- Stages 1-4 PASS on hardware: bridge push/pop bp, selfloc+one store
  (flag=0x5A at O+128), NMI mask/clear/restore, clean IVT read
  F000:0F78 (saved=3960:61440).
- Stage 4 fixed the S1 SOP DS bug: S1 SOP stored [bp+disp] with DS=0,
  writing 0000:0002/0000:0004. Ladder uses push cs/pop ds before every
  result store.
- Stage 5 (dummy 1111:2222) and 5c (no-op write of saved F000:0F78)
  both screen-clean but keyboard DEAD. 5c never held a bogus vector,
  so the write act itself is the trigger.
- Decision: writing INT 02h vector (0000:0008/000A) is undefined
  behavior on this machine. Interrupt-driven S1 frozen, no anchor.
- BASLOAD.BAS restored: x=0, sv!/sg! single precision, hex output.
  loaded-N stays decimal (gate).

## Open questions

- Mechanism of the IVT-write keyboard death: unknown. Not the DS bug
  (5c was DS-correct), not the transient value (5c no-op). Recorded as
  UB until a manual/logic-diagram lookup explains it.
- Prior successful custom hook (user memory): which vector? Repo has no
  hardware-passed interrupt-hook record; not needed for polling path.

## Loose ends

- S1 v1/v2 listings remain unanchored; interrupt-driven path retired.
- on_error_nmi_reenable pattern still untranscribed.
- deserializer_sop S0-S5 ladder presumed interrupt-driven from S1
  onward; needs rewrite around polling for S2+.

## Suggested next scope

Polling custom decoder. Stage 0 is proven: mask NMI, poll 62h bit 6,
CH0-latch each edge, store timestamp array, restore before RETF
(CH0CAL pattern). Then software decode: start + 8 data + parity + stop,
440us cell, blind to merges. No IVT write anywhere.

## Ground truth

Anchors by name:

- docs/anchors/BASLOAD.BAS (restored this session)
- docs/anchors/CH0CAL.ASM
- docs/anchors/ENVSHAPE.BAS
- docs/anchors/AGCPROBE.BAS
- IRPING (frozen DATA, platform skill Rule 5)

No new hardware-passed program this session; nothing new to anchor.
