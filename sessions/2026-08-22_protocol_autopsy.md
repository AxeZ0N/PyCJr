# 2026-08-22 — Protocol Autopsy (single scope)

Scope: retrieve the KBDNMI listing and audit the stock IR protocol —
CPU floor, stop-bit rationale, comment conflicts, parallel-decode
feasibility, and the one-way paste target.

## Verified this session

- KBDNMI body (entry 338) CLI 0F76 -> STI 0FF4, no yield point.
  5-sample start-bit majority; CH1 reads via 43h/41h; biphase 2-sample
  compare; odd parity; INT 48h dispatch.
- Stop-bit rationale: entry 94 — 11 stop bits = processor bandwidth for
  other interrupts. manual-verified.
- CH0 = only maskable timer IRQ (TOD, 18.2 Hz); CH1 CPU-read; CH2
  audio. Keyboard arrives on the NMI pin.
- Stock CPU floor: 4.4 ms/frame, 5.28 ms free tail, ~19.4 ms/keypress.
- Rejected: interrupt/parallel decode — no free timer IRQ, single-task
  cartridge.
- Locked target: one-way paste speed; 1500 us gap already banked (1.5x).

## Open questions

- Three listing/comment conflicts: DX=544 vs "310 us"; DX=526 vs "next
  half bit"; stop bit listed but never sampled.
- biphase-as-AGC hypothesis unverified; AGC profile probe required
  before dropping biphase.
- ENVSHAPE26 line-3 token 5 visual confirmation ("vc" vs "bc").

## Loose ends

- Cooperative CH0 scheduling feasible (~2100 cycles/cell budget) but
  not a build item.
- No hardware run this session; no test_log append.

## Suggested next scope

- AGC profile probe: burst-silence-burst envelope measurement, or
  ENVSHAPE26 re-run to settle the n=1 envelope values first.
