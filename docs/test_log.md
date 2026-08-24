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
## 2026-08-22 · ENVSHAPE26 · result
{
  "id": "ENVSHAPE26",
  "source": "ENVSHAPE26.BAS",
  "expected": { "return": "returned ok", "st": 1, "ed": 38, "in0": 0, "it": 61440, "nH": 19, "nL": 18, "mH": 572, "xh": "1124..1126", "mL": 745, "xl": "3500..3502", "keyboard_after": "intact" },
  "observed":  { "return": "returned ok", "st": 1, "ed": 38, "in0": 0, "it": 61440, "nH": 19, "nL": 18, "mH": 572, "xh": 1124, "mL": 745, "xl": 3502, "keyboard_after": "intact (presumed)" },
  "verdict": "PASS",
  "recovery": "cold_power_cycle"
}
## 2026-08-24 · AGCPROBE · result
{
  "id": "AGCPROBE",
  "source": "AGCPROBE.BAS + pycjr harness",
  "stimulus": "custom probe waves: burst-pair (W,S,W,S) and 8-burst train",
  "clock": "CH0 2.38636 MHz empirical",
  "keyboard_after": "intact (all runs)",
  "runs": [
    {"label":"G1_iso","spec":"62,5000,62,5000","ed":4,"H":[550,548],"L":[11566]},
    {"label":"G2_w25","spec":"25,5000,25,5000","ed":4,"H":[550,550],"L":[11420]},
    {"label":"G2_w40","spec":"40,5000,40,5000","ed":4,"H":[550,550],"L":[11420]},
    {"label":"G2_w62","spec":"62,5000,62,5000","ed":4,"H":[550,550],"L":[11564]},
    {"label":"G2_w125","spec":"125,5000,125,5000","ed":4,"H":[550,550],"L":[11636]},
    {"label":"G2_w250","spec":"250,5000,250,5000","ed":4,"H":[1126,1052],"L":[11422]},
    {"label":"G2_w500","spec":"500,5000,500,5000","ed":4,"H":[1702,1702],"L":[11420]},
    {"label":"G3_s1500","spec":"62,1500,62,1500","ed":4,"H":[550,548],"L":[3142]},
    {"label":"G3_s440","spec":"62,440,62,440","ed":4,"H":[550,550],"L":[620]},
    {"label":"G3_s220","spec":"62,220,62,220","ed":4,"H":[550,478],"L":[188]},
    {"label":"G3_s157","spec":"62,157,62,157","ed":2,"H":[],"L":[]},
    {"label":"G3_s80","spec":"62,80,62,80","ed":2,"H":[],"L":[]},
    {"label":"G3_s40","spec":"62,40,62,40","ed":2,"H":[],"L":[]},
    {"label":"G4_train","spec":"8x(62,440)","ed":16,"H":[550,550,548,550,550,548,550,550],"L":[620,694,694,620,694,622,620]}
  ],
  "notes": [
    "Battery-2 transcription header 'ed=5' was a slip; every line in that block carries 3 deltas = ed 4. Analyzed as ed=4.",
    "Pre-suite sanity run '2000,62,375' gave st=1 ed=2 it=61440, no H/L dump; single burst correctly blocked by the ed>=3 gate.",
    "Manual h-press (pre-suite): st=1 ed=34 in=0 it=61440, h decoded, H contains single 1450 ct (607 us) merge candidate; the first 55 ct value was a transcription error, corrected away.",
    "ed>=3 dump gate discarded merged-high width on S=157/80/40; next probe needs ed>=2 dump."
  ]
}
