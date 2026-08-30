# Handoff — KBDNMI I30 sync-reference re-scope

Date: 2026-08-30
Scope: Clone KBDNMI timing, read I30 body, retire loop-cost, raise
sync-reference-phase hypothesis. IRPING2 transport anchor landed.

## 1. Verified this session

- IRPING2_MIN hardware pass: `loaded 56 bytes`, `RETURNED OK`,
  `status= 3`, keyboard intact. Transport sanity confirmed.
- IRPING2 anchored: `docs/anchors/IRPING2.BAS` + `IRPING2.ASM`,
  custom runner (no rising/falling lines), 56-byte DATA byte-exact.
- I30 body read from `bios_grep` (3410–3448): latch `40h` = CH1,
  two NOPs, two `IN 41h`; wait loop is a PLL — overshoot carried
  forward (`SUB CX,DX` / `ADD DI,CX`), does not accumulate.
- Loop cost ruled out: ~70 cycles ≈ 17.5 CH1 ticks per iteration
  vs 114–116 tick overshoot ≈ 6.5× granularity.
- 5-sample majority (`CMP AH,3`) starts AT the 544-tick point,
  runs forward ~38 µs; not centered.

## 2. Open questions

- Does the clone seed DI from the same phase as KBDNMI's I6 sync?
  The overshoot is deterministic (±1 tick) → systematic
  reference-phase offset, not noise.
- Where exactly does KBDNMI capture DI relative to the carrier-off
  transition?

## 3. Loose ends

- Platform skill Rule 5 still says IRPING; update to IRPING2
  regression, re-import per `skill_create_semantics`.
- `docs/jr_tool_spec.md` §8 fixture names IRPING (61 bytes);
  update to IRPING2.
- `wait_overshoot_ch1_anomaly` superseded in facts; loop-cost
  hypothesis retired.

## 4. Suggested next scope

Continue the sync-reference hypothesis. Static retrievals first,
no hardware run until one matches.

```json
{
"id": "sync_reference_phase",
"hypothesis": "H — the clone's DI clock capture sits ~114 CH1 ticks later than KBDNMI's reference edge (start-burst geometry), producing the bit0 first-half overshoot; later bits self-heal via the I30 PLL carry-forward.",
"falsifier": "F — the 114-116 tick overshoot is NOT accounted for by a ~95.5 us frame feature (start burst / gap / carrier-off geometry) found in ir_protocol_frozen or the listing.",
"clean_run": "S — static retrieval only; IRPING2 transport regression passes before any hardware probe.",
"verdict": "pending"
}
```

Retrieval order:

1. `bios_grep` peek 0F80–0FB9 (lines before `MOV DI,AX`) — locate
KBDNMI's clock capture relative to the I6 sync transitions.
2. `grep_repo` `ir_protocol_frozen` — pull start-burst duration and
gap geometry; check whether ~95.5 µs matches a frame feature.
3. If matched → hypothesis survives to hardware; if not → supersede
and re-open the reference-timing question.

Do NOT build the 5x sampler until the edge is shown stable.

## 5. Ground truth

- docs/anchors/IRPING2.BAS
- docs/anchors/IRPING2.ASM
- docs/anchors/BASLOAD.BAS
- docs/anchors/CH0CAL.ASM
- docs/anchors/ENVSHAPE.BAS

# Handoff — KBDNMI I30 sync-reference re-scope

Date: 2026-08-30
Scope: Clone KBDNMI timing, read I30 body, retire loop-cost, raise
sync-reference-phase hypothesis. IRPING2 transport anchor landed.

## 1. Verified this session

- IRPING2_MIN hardware pass: `loaded 56 bytes`, `RETURNED OK`,
  `status= 3`, keyboard intact. Transport sanity confirmed.
- IRPING2 anchored: `docs/anchors/IRPING2.BAS` + `IRPING2.ASM`,
  custom runner (no rising/falling lines), 56-byte DATA byte-exact.
- I30 body read from `bios_grep` (3410–3448): latch `40h` = CH1,
  two NOPs, two `IN 41h`; wait loop is a PLL — overshoot carried
  forward (`SUB CX,DX` / `ADD DI,CX`), does not accumulate.
- Loop cost ruled out: ~70 cycles ≈ 17.5 CH1 ticks per iteration
  vs 114–116 tick overshoot ≈ 6.5× granularity.
- 5-sample majority (`CMP AH,3`) starts AT the 544-tick point,
  runs forward ~38 µs; not centered.

## 2. Open questions

- Does the clone seed DI from the same phase as KBDNMI's I6 sync?
  The overshoot is deterministic (±1 tick) → systematic
  reference-phase offset, not noise.
- Where exactly does KBDNMI capture DI relative to the carrier-off
  transition?

## 3. Loose ends

- Platform skill Rule 5 still says IRPING; update to IRPING2
  regression, re-import per `skill_create_semantics`.
- `docs/jr_tool_spec.md` §8 fixture names IRPING (61 bytes);
  update to IRPING2.
- `wait_overshoot_ch1_anomaly` superseded in facts; loop-cost
  hypothesis retired.

## 4. Suggested next scope

Continue the sync-reference hypothesis. Static retrievals first,
no hardware run until one matches.

```json
{
"id": "sync_reference_phase",
"hypothesis": "H — the clone's DI clock capture sits ~114 CH1 ticks later than KBDNMI's reference edge (start-burst geometry), producing the bit0 first-half overshoot; later bits self-heal via the I30 PLL carry-forward.",
"falsifier": "F — the 114-116 tick overshoot is NOT accounted for by a ~95.5 us frame feature (start burst / gap / carrier-off geometry) found in ir_protocol_frozen or the listing.",
"clean_run": "S — static retrieval only; IRPING2 transport regression passes before any hardware probe.",
"verdict": "pending"
}
```

Retrieval order:

1. `bios_grep` peek 0F80–0FB9 (lines before `MOV DI,AX`) — locate
KBDNMI's clock capture relative to the I6 sync transitions.
2. `grep_repo` `ir_protocol_frozen` — pull start-burst duration and
gap geometry; check whether ~95.5 µs matches a frame feature.
3. If matched → hypothesis survives to hardware; if not → supersede
and re-open the reference-timing question.

Do NOT build the 5x sampler until the edge is shown stable.

## 5. Ground truth

- docs/anchors/IRPING2.BAS
- docs/anchors/IRPING2.ASM
- docs/anchors/BASLOAD.BAS
- docs/anchors/CH0CAL.ASM
- docs/anchors/ENVSHAPE.BAS

