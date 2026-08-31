# Handoff — ES-clobber bridge contract (single scope)

Date: 2026-08-31
Scope: locate the source of the bytes-corruption crashes on the NMI
ladder and fix the bridge contract.

## Verified this session

- Re-established the regression baseline: IRPING2 green (transport
  sane); L0DI clean (`m1=42`, `m2=43`).
- Falsified the BP-clobber theory. NMIPEEK (DI-based result base, BP
  restored right after self-location) still produced the bytes
  corruption + keyboard-dead signature. BP was not the killer.
- Isolated ES clobber. Controlled A/B on NMIPEEK:
  - no ES save -> corrupted every run;
  - `PUSH ES` / `POP ES` around the body -> clean pass every run.
- Confirmed the stock KBDNMI vector readback: `0F78:F000`
  (`saved=3960:61440`), matching the BIOS listing.
- Anchored NMIPEEK: `docs/anchors/NMIPEEK.BAS` / `NMIPEEK.ASM`.

## Open questions

- Why did the original N1-A (ES-clobbering) pass exactly once on
  hardware before corrupting? Recorded as `n1a_onepass_anomaly`.
- Does any other segment register need preservation across the bridge
  (SS already fixed; DS restored; CS unchanged)? Untested.

## Loose ends

- Rule 1 of `pcjr_cartridge_basic_asm` still says BP-only; it needs the
  ES addition from `es_clobber_bridge_contract`.
- The `jr` lint ruleset has no ES-preserve check yet. A `push/pop es`
  invariant should be considered for the bridge entry rule.
- The custom INT 02h dispatch question (original scope) remains open —
  it was superseded this session by the bridge-contract defect.

## Suggested next scope

Patch Rule 1 and the lint entry rule to require BP + ES preservation,
rebuild the N1-A probe under the corrected contract, and re-attempt the
masked-write/readback N1-A experiment. Only then return to the
custom-dispatch question.

## Ground truth

- docs/anchors/NMIPEEK.BAS / NMIPEEK.ASM — ES-preserved IVT read (new)
- docs/anchors/IRPING2.BAS / IRPING2.ASM — transport regression
- docs/anchors/CH0CAL.ASM / CH0CAL.bas — functional primary regression
