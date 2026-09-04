# Handoff — Contract A bridge + tooling repair (single scope)

Date: 2026-08-31
Scope: freeze Contract A bridge, repair the two jr tooling defects it
exposed, build NMIPEEK2.

## Verified this session

- Contract A frozen (user decision): `PUSH ES` immediately after
  `PUSH BP`; entry `0E 1F 55 06`, epilogue `07 5D CB`. See
  `contract_a_bridge_frozen`.
- Repaired `refs/jr-tools/jr_rules.json` — truncated `nmi-restore`
  restored; entry/epilogue/nmi-restore all carry the ES contract.
- Repaired `refs/jr-tools/jr.py` selfloc — displacement now derived
  from marker index, not hardcoded 6.
- Built NMIPEEK2: stage 6 lint pass, 46 bytes, 0 errors, 0 warnings.
  Disasm reviewed: entry correct, `lea bp,[bp+0x79]` gives result base
  entry+128, ES/NMI preserved, `07 5D CB` epilogue.
- No hardware run this session.

## Open questions

- Does NMIPEEK2 pass hardware under Contract A? Expected status=42,
  rising=3960, falling=61440, keyboard alive.
- `n1a_onepass_anomaly` still open — original N1-A's single unexplained
  clean pass.
- Does the repo skill file carry the full Rule 1 Contract A text, or
  did the paste truncate at the Rule 1 header as seen in BDS?

## Loose ends

- NMIPEEK v1 (pre-Contract A ES placement) remains ground truth but now
  violates the frozen entry bytes. Decide: leave as historical anchor or
  rebuild under Contract A.
- `jr_rules.json` rationale cites Rule 10/11; emitted skill text ends at
  Rule 9. Numbering drift to reconcile.
- `jr.py` selfloc message template still says "(R - 6 = ...)" —
  cosmetic, now misleading under Contract A. Patch message text.

## Suggested next scope

Hardware run of NMIPEEK2 (IRPING2 regression first). On clean pass,
create NMIPEEK2.BAS / NMIPEEK2.ASM anchors same session, then decide
NMIPEEK v1 fate. Only then return to the deferred custom INT 02h
dispatch question.

## Ground truth

- docs/anchors/NMIPEEK.BAS / NMIPEEK.ASM — pre-Contract A IVT read (v1)
- docs/anchors/IRPING2.BAS / IRPING2.ASM — transport regression
- docs/anchors/CH0CAL.ASM / CH0CAL.bas — functional primary regression
