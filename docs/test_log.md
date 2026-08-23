# PyCJr — Test Log (regression/probe run history) (v5)

Repo-resident run history. Not BDS-imported. Rules (stage gates,
emission gate, debug anchor rule) live in
`bds/10_skills/pcjr_test_workflow.md`; values and single-fact anchors
live in `facts.md`; this file records run entries and baselines.

## Run entry template

```

date: YYYY-MM-DD
id: <probe id>
source: <FILE.BAS / artifact>
contract: <expected fields>
observed: <actual fields>
keyboard_after: <intact | broken | not applicable>
regression: <IRPING | last known-good>

```

## Known-good baselines (recorded data, not rules)

### IRPING (golden regression artifact)

- Frozen 61-byte raw IR edge sampler; DATA lives in the platform skill
  Rule 5, not here.
- Expected pass: `rising>0`, `falling>0`, `status=0` or `64`.
- Role: run first when transport behavior is suspect.

### SHAPE3 Stage 3

- Recorded: `status=1`, `edges=2`, `init=0`.
- Role: early-stage known-good.

### STAGE5 clean

- Recorded: `status=1`, `edges=40`, `init=0`, keyboard intact.
- Recorded `max_delta=3456` at edge 20 (session reading; see note).
- Note: edge count varies 38-40 across clean runs. Root cause resolved:
  arming window swallowed frame 1's leading start burst
  (`facts.md` `open_3840`).

### CH0CAL

- Recorded pass: `st=1`, `ed=38`, `in=0`, `it=61440`, keyboard intact.
- gap1: `3428` @ 1500us, `23704` @ 10000us, `47636` @ 20000us.
- gap2: `1126` counts (~472 us) = stretched envelope H, not silence, not
  a bit cell. See `facts.md` `gap2_1126`.
- Derivation and defects: `docs/ch0_calibration.md`.

### ENVSHAPE

- Recorded clean: `st=1`, `ed=38`, `in=0`, `it=61440`, `nh19 nl18`,
  keyboard intact. Added to workflow anchor list.

## Superseded readings (do not reuse)

- STAGE5 earlier readings `edges=38` / `max_delta=2592` are superseded by
  the STAGE5 clean baseline above.
- `max_delta=3528` appears in some notes; the recorded anchor value is
  `3456`. Flag any file still carrying 3528 for reconciliation
  (`bin/migrate_repo.py` scans for this).

## 2026-08-22 baseline

```

date: 2026-08-22
id: repo_baseline
source: tooling_build_repo_refactor
contract: living-repo layout + grep_repo + jr-commit.sh
observed: facts.md seeded; anchors migrated; docs slimmed
keyboard_after: not applicable
regression: not applicable

```

### BUSY100CAL (aborted)

- S0 pass: Out of DATA traps, ERR 4. 1/0 no trap.
- S1 pass: CH0 lo=12 hi=205, INP/OUT confirmed.
- S2 pass: A0 mask/unmask, keyboard intact.
- S3/S4 data rejected: n=0 reps 50776/49808/53624; n=5 -> 64 (wrap
  fold); n=10 -> 20256 (wrap fold); wrap-flag run still multi-wrap
  ambiguous. Aborted, tool unfit. See facts.md busy100cal_aborted.

### ENVSHAPE delay sweep

- ed=38 flat 0.2..1.0s. >1s ed=18 (truncation). 40 retired.
  open_3840 refuted; merge hypothesis open.
## 2026-08-22 · ENVSHAPE26 · result
{
  "id": "ENVSHAPE26",
  "source": "ENVSHAPE26.BAS",
  "expected": { "return": "returned ok", "st": 1, "ed": 38, "in0": 0, "it": 61440, "nH": 19, "nL": 18, "mH": 572, "xh": "1124..1126", "mL": 745, "xl": "3500..3502", "keyboard_after": "intact" },
  "observed":  { "return": "returned ok", "st": 1, "ed": 38, "in0": 0, "it": 61440, "nH": 19, "nL": 18, "mH": 572, "xh": 1124, "mL": 745, "xl": 3502, "keyboard_after": "intact (presumed)" },
  "verdict": "PASS",
  "recovery": "cold_power_cycle"
}
