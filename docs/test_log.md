# PyCJr — Test Log (regression/probe run history)

Repo-resident run history. Not BDS-imported. Rules (stage gates,
emission gate, debug anchor rule) live in
`bds/10_skills/pcjr_test_workflow.md`; this file records only results.

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
- Note: edge count varies 38-40 across clean runs. Open item:
  38-vs-40 edge variance root cause (owned by the project doc).

### CH0CAL

- Recorded pass: `st=1`, `ed=38`, `in=0`, `it=61440`, keyboard intact.
- gap1: `3428` @ 1500us, `23704` @ 10000us, `47636` @ 20000us.
- gap2: `1126` counts (~472 us).
- Derivation and defects: `docs/ch0_calibration.md`.

## Superseded readings (do not reuse)

- STAGE5 earlier readings `edges=38` / `max_delta=2592` are superseded by
  the STAGE5 clean baseline above.
- `max_delta=3528` appears in some notes; the recorded anchor value is
  `3456`. Flag any file still carrying 3528 for reconciliation.
