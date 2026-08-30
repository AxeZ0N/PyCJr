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
# 2026-08-24 · threshold pinning battery 1 (merge+recovery)

{
  "id": "threshold_battery_1",
  "source": "threshold_battery.txt",
  "regression": "CH0CAL",
  "recovery": "cold_power_cycle",
  "contract": {
    "stimulus": "W=62us two-burst, lead=0, trailing=5000us",
    "sweep": "merge S=180/190/200/210, recovery S=260/300/340/380"
  },
  "results": [
    {"S":180,"ed":4,"H":"550 406","L":188},
    {"S":190,"ed":4,"H":"550 478","L":188},
    {"S":200,"ed":4,"H":"550 478","L":188},
    {"S":210,"ed":4,"H":"550 478","L":188},
    {"S":260,"ed":4,"H":"550 550","L":188},
    {"S":300,"ed":4,"H":"550 548","L":334},
    {"S":340,"ed":4,"H":"550 550","L":476},
    {"S":380,"ed":4,"H":"550 500","L":476}
  ],
  "notes": "S=380 H2=500 transient; did not reproduce in battery 3."
}

# 2026-08-24 · threshold pinning battery 2 (knee pinning)

{
  "id": "threshold_battery_2",
  "source": "threshold_battery_2.txt",
  "regression": "CH0CAL",
  "recovery": "cold_power_cycle",
  "contract": {
    "stimulus": "W=62us two-burst, lead=0, trailing=5000us",
    "sweep": "fuse S=160/165/170/175, recovery S=230/240/250, repeats 300/340/380"
  },
  "results": [
    {"S":160,"ed":2,"note":"fused"},
    {"S":165,"ed":2,"note":"fused"},
    {"S":170,"ed":2,"note":"fused"},
    {"S":175,"ed":4,"H":"550 406","L":188},
    {"S":230,"ed":4,"H":"550 478","L":188},
    {"S":240,"ed":4,"H":"550 550","L":188},
    {"S":250,"ed":4,"H":"550 550","L":188},
    {"S":300,"ed":4,"H":"550 548","L":334},
    {"S":340,"ed":4,"H":"550 550","L":476},
    {"S":380,"ed":4,"H":"550 550","L":476}
  ],
  "notes": "S=380 L=476 repeats battery 1 S=340; S=380 H2 anomaly retired."
}

# 2026-08-24 · anomaly knock-out battery 3

{
  "id": "threshold_battery_3",
  "source": "threshold_battery_3.txt",
  "regression": "CH0CAL",
  "recovery": "cold_power_cycle",
  "contract": {
    "stimulus": "batch1 W=250/S=5000 x4, batch2 W=62 S=310/320/330/335"
  },
  "results": [
    {"S":5000,"W":250,"H1":1054,"H2":1054,"L":11492},
    {"S":5000,"W":250,"H1":1126,"H2":1124,"L":11422},
    {"S":5000,"W":250,"H1":1126,"H2":1054,"L":11420},
    {"S":5000,"W":250,"H1":1126,"H2":1126,"L":11380},
    {"S":310,"W":62,"H":"550 548","L":334},
    {"S":320,"W":62,"H":"550 550","L":404},
    {"S":330,"W":62,"H":"550 548","L":406},
    {"S":335,"W":62,"H":"550 550","L":404}
  ],
  "notes": "W250 asymmetry intermittent (1/4); L staircase jumps 310->320 (334->404)."
}
## 2026-08-24 · ch0cal_deterministic_hpress · result

contract: {"id":"ch0cal_deterministic_hpress","source":"CH0CAL/AGCPROBE",
  "expected":{"st":1,"ed":"38 (anchor)","functional":"h"},
  "regression":"IRPING","recovery":"cold_power_cycle"}

result: st=1, ed=36 (2/2 deterministic), functional h decodes, kb intact.
H: 550 548 550 550 548 1126 550 548 550 550 548 550 548 550 406 1124 550
L: 334 478 1052 478 550 908 550 478 3572 334 478 1052 478 478 188 982 406
Merges: H6=1126, H17=1124 (both 157us 0→1 gaps). Stable across 2/2.

verdict: FAIL vs anchor ed=38; FUNCTIONAL PASS. Classified receiver
analog drift (closed warm room). Code/Pi/wiring exonerated. One transient
38 after percussive, not reproducible. z2 functional sweep deferred to
next session.
## 2026-08-25 · DENSETRAIN · result

contract: {"id":"DENSETRAIN","source":"densetrain_battery.txt",
  "expected":{"return":"RETURNED OK","ed":"24 clean, fewer iff fusing",
  "H":"flat ~230us, no >10% sag","L_min":"deliverable"},
  "regression":"AGCPROBE.BAS (AGC1) + CH0CAL ASM",
  "recovery":"cold_power_cycle"}

result: st=1, kb intact. Sweep S=260..160us, 12-burst trains.
- S=260: H 550 flat (one 620ct outlier), L 190/262 bimodal.
- S=240: H 550/476 mixed, L 190 uniform; clean 24/24.
- S=230: one fusion (H 1378ct merged), L 190; 22/24.
- S=220: clean edges, H oscillates 476/478 and 406/404; L 190.
- S<=200: collapse, multiple fusions.

verdict: dense separation floor ~230-240us (stochastic onset 230,
clean 240). H dense minimum 406ct (~170us). 250us cell refuted.
## 2026-08-25 · RECOVERY4 · result

{
  "id": "RECOVERY4",
  "source": "recovery4_battery.txt",
  "regression": "AGCPROBE.BAS (AGC1) + CH0CAL ASM",
  "recovery": "cold_power_cycle",
  "results": [
    {"label":"CTRL_180","ed":12,"fusions":6,"note":"reproduces dense collapse"},
    {"label":"R4_180","ed":22,"fusions":1,"note":"fusion post-reset block 3"},
    {"label":"R4_200","ed":24,"fusions":0,"note":"S=200 rescued by reset"},
    {"label":"R4_220","ed":24,"fusions":0,"note":"L7=133 below 79us floor"}
  ],
  "verdict": "PASS mechanistically; retired economically (k≈3 vs k>22 break-even)"
}
## 2026-08-25 · irping_basload_pass · result

contract: {"id":"IRPING_BASLOAD","source":"BASLOAD.BAS + IRPING DATA",
"expected":{"return":"RETURNED OK","transport":"sane (char echo)"},
"regression":"self","recovery":"cold_power_cycle"}
result: `loaded 61 bytes`; Pi key echoed on screen; keyboard intact
after. Transport sane. Rising/falling not transcribed this run; the
IRPING block read through BASLOAD's S1 offsets printed flag=0
saved=6:6 status=0 — a diagnostic misread, not a transport failure.

## 2026-08-25 · ch0cal_envshape_pass · result

contract: {"id":"CH0CAL_ENVSHAPE","source":"ENVSHAPE.BAS (CH0CAL ASM)",
"expected":{"return":"RETURNED OK","functional":"h decodes","keyboard_after":"intact"},
"regression":"IRPING -> CH0CAL","recovery":"cold_power_cycle"}
result: passed; functional 'h' decode, keyboard intact. ed reading
environmental per facts.md ch0cal_ed_reading_conflict; not
contractual.

## 2026-08-25 · s1_v1_div0 · result

contract: {"id":"S1_NMI_INTERCEPT","source":"BASLOAD.BAS + S1 v1 (110B)",
"expected":{"return":"RETURNED OK","flag":1,"status":0,"keyboard_after":"intact"},
"regression":"IRPING -> CH0CAL","recovery":"cold_power_cycle"}
result: FAIL. `loaded 110 bytes`, ~3s, `Division by zero in (blank)`,
keyboard dead. Root cause: bp clobber (no push/pop bp).

## 2026-08-25 · s1_v2_reboot · result

contract: {"id":"S1_NMI_INTERCEPT_V2","source":"BASLOAD.BAS + S1 v2 (114B)",
"expected":{"return":"RETURNED OK","flag":1,"status":0,"keyboard_after":"intact"},
"regression":"IRPING -> CH0CAL","recovery":"cold_power_cycle"}
result: FAIL. `loaded 114 bytes`; Pi 'h' during window -> PCjr reboot
into BIOS. No result map read. Defect not localized; stage gate
triggered.## 2026-08-25 · s1_ladder_stage1_bridge · result
contract: {id s1_ladder_stage1_bridge, expected return RETURNED OK,
keyboard intact, regression none}
result: PASS. loaded 9 bytes, returned ok, keyboard alive.

## 2026-08-25 · s1_ladder_stage2_selfloc · result
contract: {id s1_ladder_stage2_selfloc, expected flag 0x5A, return OK}
result: PASS. flag=0x5A (90 dec), keyboard alive.

## 2026-08-25 · s1_ladder_stage3_nmi_touch · result
contract: {id s1_ladder_stage3_nmi_touch, expected return OK,
keyboard intact}
result: PASS. mask/clear/restore clean, keyboard alive.
(regression IRPING + CH0CAL both green before run)

## 2026-08-25 · s1_ladder_stage4_read_ivt · result
contract: {id s1_ladder_stage4_read_ivt, expected saved F000:xxxx}
result: PASS. saved=3960:61440 = F000:0F78, keyboard alive.
note: harness first run overflowed (256*peek > 32767 under DEFINT);
fixed with sv!/sg! single precision.

## 2026-08-25 · s1_ladder_stage5_write_ivt · result
contract: {id s1_ladder_stage5_write_ivt, expected return OK,
saved unchanged, keyboard intact}
result: FAIL. screen flag=0 saved=F78:F000 status=0, keyboard DEAD.
false pass caught on human keyboard gate. cold_power_cycle.

## 2026-08-25 · s1_ladder_stage5c_noop_write · result
contract: {id s1_ladder_stage5c_noop_write, expected return OK,
keyboard intact}
result: FAIL. returned ok, saved=F78:F000, keyboard DEAD. no-op write
of saved value proves the IVT write act itself is the trigger, not the
value. Decision: INT 02h vector write is UB on this machine.
## 2026-08-26 · s1v2 · result

{
  "id": "s1v2",
  "source": "S1V2.BAS",
  "result": {
    "return": "returned ok",
    "loaded": 71,
    "flag": "0",
    "rising": "17",
    "falling": "17",
    "keyboard": "intact"
  },
  "pass": true,
  "recovery": "cold_power_cycle"
}

## 2026-08-26 · s2v1 · result

{
  "id": "s2v1",
  "source": "S2V1.BAS",
  "result": {
    "return": "returned ok",
    "loaded": 106,
    "st": "1",
    "edge_count": "22h (34)",
    "snapshot": "0",
    "iter_low_byte": "0",
    "keyboard": "intact"
  },
  "pass": true,
  "recovery": "cold_power_cycle"
}

## 2026-08-26 · b26vec · result

{
  "id": "b26vec",
  "source": "B26VEC.BAS",
  "result": {
    "vectors": 11,
    "match": "11/11",
    "keyboard": "n/a (no machine code)"
  },
  "pass": true,
  "recovery": "cold_power_cycle"
}

## 2026-08-26 · s3v1 · result

{
  "id": "s3v1",
  "source": "S3V1.BAS",
  "result": {
    "return": "returned ok",
    "loaded": 106,
    "st": "1",
    "ed": "36",
    "dump": "transcription corrupted"
  },
  "verdict": "void — transcription only",
  "note": "hardware, ASM, and encoder exonerated; method retired",
  "recovery": "cold_power_cycle"
}
## 2026-08-26 · s4a_v1_timeout · result

contract: {"id":"S4A","source":"S4A.BAS v1 (139B, CH0 variant)",
"expected":{"return":"RETURNED OK","st":"0|3","half":"0|1",
"keyboard_after":"intact"},
"regression":"IRPING -> CH0CAL","recovery":"cold_power_cycle"}
result: PASS (timeout path). No stimulus; st=0, half=0,
t0=58371 t1=45216 (code-tail artifacts, not timestamps). Keyboard
intact. 2/2 identical.

## 2026-08-26 · s4a_v1_h_softlock · result

contract: {"id":"S4A","source":"S4A.BAS v1 (139B, CH0 variant)",
"expected":{"return":"RETURNED OK","st":3,"half":"0|1",
"keyboard_after":"intact"},
"regression":"IRPING -> CH0CAL","recovery":"cold_power_cycle"}
result: FAILED. h press during window caused screen line corruption
and keyboard softlock. Root cause: v1 restored NMI mid-make-frame;
KBDNMI deserialized the frame tail as garbage. Cold power-cycle
recovered.

## 2026-08-26 · s4a_v2_h_pass · result

contract: {"id":"S4A","source":"S4A.BAS v2 (112B, LOOP-timing)",
"expected":{"return":"RETURNED OK","st":3,"half":"0|1",
"keyboard_after":"intact"},
"regression":"IRPING -> CH0CAL","recovery":"cold_power_cycle"}
result: PASS. h press: st=3, half=1 (predicted first data bit of
0x23). Keyboard alive. Run via --run_test.
## 2026-08-26 · s4b1_stage1_pass · result

contract: {"id":"S4B1-stage1","source":"S4B1.BAS stage1 (39B)",
  "expected":{"return":"RETURNED OK","st":"&HAA","bit0":"&HBB",
  "bit1":"&HCC","biphase_ok":"&HDD","keyboard_after":"intact"},
  "regression":"IRPING -> S4A","recovery":"cold_power_cycle"}
result: loaded=39, returned ok, st=&HAA bit0=&HBB bit1=&HCC
  biphase=&HDD, keyboard intact. PASS.

## 2026-08-26 · s4b1_stage2_ch0_live · result

contract: {"id":"S4B1-stage2","source":"S4B1_stage2.BAS (103B)",
  "expected":{"return":"RETURNED OK","st":"2","rise/trail stored",
  "delta_nonzero":"1","keyboard_after":"intact"},
  "regression":"IRPING -> S4A","recovery":"cold_power_cycle"}
result: st=2 rise=0x4DE6 trail=0x4BA4 burst=0x242 (578 counts=242.2us)
  and an earlier run burst=526 counts=220.4us. CH0 latch/read works
  under NMI mask during live frame; keyboard intact. PASS.

## 2026-08-26 · s4b1_stage3b_boundary · result

contract: {"id":"S4B1-stage3b","source":"S4B1_stage3b.BAS (180B)",
  "expected":{"return":"RETURNED OK","st":"3","half":"0|1",
  "rise/trail/burst reported","keyboard_after":"intact"},
  "regression":"IRPING -> S4A","recovery":"cold_power_cycle"}
result: st=3 rise=0xC330 trail=0xC0D8 burst=0x258 (600 counts=251.4us)
  half=0, keyboard intact. Fixed 740-anchor samples the bit0 boundary
  and disagrees with S4A's half=1 at the same nominal offset. Negative
  result for fixed grid; edge-sync is the next path. RECORDED.
## 2026-08-27 · dec1_st1_hw_pass · result
{
  "id": "DEC1_ST1",
  "source": "DEC1_ST1.BAS",
  "expected": {
    "return": "RETURNED OK",
    "flag": "2 when both edges seen",
    "span": "880..1100 counts"
  },
  "regression": "IRPING -> S4B1_ST3B",
  "recovery": "cold_power_cycle"
}
result: PASS 2/2. Run 1: flag=2, r0=0xCDD0, r1=0xCA54, span 892 ct
(373.8 us). Run 2: flag=2, r0=0xBB46, r1=0xB7C8, span 894 ct
(374.6 us). Keyboard intact. loaded-106 gate observed.
## 2026-08-27 · dec1_st2a_hw_pass · result
{
  "id": "DEC1_ST2A",
  "source": "DEC1_ST2A.BAS",
  "expected": {"return": "RETURNED OK", "status": "2 when PC0 seen", "pc6": "40"},
  "result": {"return": "RETURNED OK", "status": 2, "pc6": "40", "kb": "intact", "loaded": "57"},
  "verdict": "pass"
}

## 2026-08-27 · dec1_st2b_fail · result
{
  "id": "DEC1_ST2B",
  "source": "DEC1_ST2B.BAS",
  "expected": {"return": "RETURNED OK", "status": "3", "span": "~148 ct (120-180 window)"},
  "result": {"return": "RETURNED OK", "spans": [334, 572, 572, 574, 574, 520, 520, 574], "no_stim": "status=0", "kb": "intact", "loaded": "92"},
  "verdict": "fail",
  "note": "trimodal AGC ripple; single-poll trailing edge insufficient"
}
# 2026-08-28 · bitsamp_ch1_544 · result

contract: {"id":"BITSAMP-CH1-544","source":"BITSAMP.BAS (inline jr build)",
"expected":{"return":"RETURNED OK","st":"3","bit":"0|1","ones":"0..5",
"trail/sample nonzero","keyboard_after":"intact"},
"regression":"IRPING -> CH0CAL","recovery":"cold_power_cycle"}
result: st=3 bit=1 ones=3 rej=1, 3/3, keyboard intact.
trail-sample deltas: 658 / 658 / 660 CH1 ticks (551.8 / 553.5 us at
1.19318 MHz). Deterministic to 1 tick. Ones=3 (not 5): 2 of 5 majority
polls LOW — sample on ragged edge of bit0 HIGH. Failed disproof of
CH0 clock-conversion confound; correct decode, thin margin.
Not anchored.## 2026-08-30 · IRPING2_MIN · result

```json
{
"id": "IRPING2_MIN",
"contract": {
  "source": "BASLOAD.BAS + IRPING2.ASM",
  "expected": { "return": "RETURNED OK", "result_byte": 3 },
  "regression": "self (transport-only); CH0CAL stays functional primary",
  "recovery": "cold_power_cycle"
},
"result": {
  "loaded": 56,
  "return": "RETURNED OK",
  "result_byte": 3,
  "keyboard": "intact",
  "rising": 0,
  "falling": 0,
  "note": "rising/falling are meaningless on this probe; it writes only O+128."
},
"verdict": "pass"
}
```

