## 2026-08-31 · probe_b_axclobber_74

{
  "id": "probe_b_axclobber_74",
  "hypothesis": "H — chain via mov ax,imm / push ax / retf coexists",
  "falsifier": "F — BASIC corrupt or keyboard dead after chain",
  "clean_run": "S — loaded 74; RETURNED OK",
  "observed": "loaded 74, RETURNED OK, Syntax error in 160 on first key, KB dead, cursor flashing",
  "verdict": "no_result — flag never printed, IRPING2 unconfirmed; defect: AX clobbered by chain setup, transparent KBDNMI restore passed it to BASIC"
}

## 2026-08-31 · probe_b_allregs_86

{
  "id": "probe_b_allregs_86",
  "hypothesis": "H — all-registers-saved handler chains with SP preserved",
  "falsifier": "F — hard freeze or lost keystroke",
  "clean_run": "S — loaded 86; RETURNED OK",
  "observed": "loaded 86, RETURNED OK, hard freeze on first key, no cursor",
  "verdict": "no_result — 18-byte save frame perturbed stack depth/phase at KBDNMI entry"
}

## 2026-08-31 · probe_b_noop_bisect

{
  "id": "probe_b_noop_bisect",
  "hypothesis": "H — defect lives in handler non-zero work; a pure chain coexists",
  "falsifier": "F — zero-work redirect still hard-freezes or fails to echo",
  "clean_run": "S — loaded 57; RETURNED OK; INPUT prompt displayed",
  "observed": "passed: keyboard alive, keystroke echoed via INPUT",
  "verdict": "failed_to_disprove — F not observed; H survives one disproof attempt. IRPING2 status unconfirmed in report."
}
