# NMIDISP Probe A — 2026-08-31

## Contract

{
  "id": "nmidisp_a",
  "source": "NMIDISP.BAS",
  "expected": { "installer_return": "RETURNED OK", "dispatch_flag": 1 },
  "regression": "IRPING2",
  "recovery": "cold_power_cycle"
}

## Result

{
  "id": "nmidisp_a",
  "loaded": 72,
  "installer_return": "RETURNED OK",
  "observed": "status=1 rising=0 falling=0 (status field = dispatch flag)",
  "dispatch_flag": 1,
  "keyboard": "dead (expected: KBDNMI replaced, scancodes discarded)",
  "cursor": "blinking (IF restored, INT 08h alive)",
  "regression": "IRPING2 status=3 (pass)",
  "verdict": "clean run — dispatch observed; coexistence survived one disproof attempt"
}

## Control

{
  "id": "nmidisp_a_control",
  "stimulus": "none",
  "loaded": 72,
  "dispatch_flag": 0,
  "regression": "IRPING2 status=3 (pass)",
  "verdict": "clean — no spurious NMI in the window"
}
