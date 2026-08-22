# PyCJr — Facts Journal (append-only)

Rules:
- Append only. One fact per heading line.
- Updates append a new line with `supersedes:`; never edit old lines.
- Grep target:
  git grep -n -i -E -C2 "carrier_high_us|burst_us|gap2" -- facts.md sessions docs

## 2026-08-22 · carrier_high_us = 13 · empirical · pi_source_verified
Burst 62us; carrier 13us high / 12us low. Supersedes Rule 8 "12 high / 13 low".

## 2026-08-22 · ch0_clock = 2.38636 MHz · empirical
14.31818/6 = CPU/2. Slope: 1500us->3428, 10000us->23704, 20000us->47636.

## 2026-08-22 · poll_quant = 72ct = 30.17us · empirical
F000h polling budget ~1.85s.

## 2026-08-22 · gap2_1126 = stretched envelope H · empirical
1126 ct ~471us. NOT silence. NOT a 440us bit cell.

## 2026-08-22 · open_3840 resolved · empirical
38-vs-40 variance = arming window (for fl=1 to 100) swallowed frame 1 start burst.

## 2026-08-22 · envshape_anchor · empirical
ENVSHAPE clean: st=1 ed=38 in0=0 it=61440 nh19 nl18, kb intact. Added to anchors.

## 2026-08-22 · stage5_clean_anchor · empirical
STAGE5: st=1 edges=40 init=0 max_delta=3456 at_edge=20, kb intact. 38/40 variance closed.

## 2026-08-22 · ch0cal_anchor · empirical
CH0CAL: st=1 ed=38 in0=0 it=61440, kb intact. gap1: 3428/23704/47636.
## 2026-08-22 · ingest_payload · decision · tooling
One-step append+commit via bin/jr-ingest.sh <payload.zip>. Payload = COMMIT.txt + facts.append.md + docs/*.append.md + sessions/*.md. Repo files never overwritten.
## skill_create_semantics
Observed 2026-08-22: skill_create on an existing name with a
different usage creates a duplicate; table glyphs (↕▾) are mangled
to (−). Policy: re-import repo skill files instead of skill_create
for platform-skill edits.

## handoff_template
No sessions/TEMPLATE.md. De-facto structure: # Handoff — <Scope>
(single scope) with Date/Scope, Decisions locked, Pending doc-sync
items, domain sections, Meta-observations, Loose ends &
contingencies. Procedure: copy newest handoff and rename (FAQ 19).

## session_anchor_policy
Session files reference applicable anchor BASIC/ASM by name; full
listing only for a new program. Known anchors: IRPING, SHAPE3 St3,
STAGE5, CH0CAL, ENVSHAPE.
## 2026-08-22 · envshape_sweep_38 · empirical
Delay sweep (Enter->h, 0.2..1.0s in 0.1 steps): ed=38 flat across the
band. >1s: ed=18 (truncation). The missing 2 edges are not a timing
loss. 38 = true envelope shape of one h make+break. 40 target RETIRED.
supersedes: open_3840

## 2026-08-22 · open_3840_refuted · conflict
open_3840 (arming window swallowed frame 1 start burst) refuted by the
sweep: 38 holds at delays where nothing can be swallowed. New candidate
for the missing 2 edges: demodulated-envelope burst-pair merge — 62us
burst reads ~230us high at PC6, and zero-silence 220/157us lets a burst
falling edge collide with the next rising edge. hypothesis, unverified.
supersedes: open_3840

## 2026-08-22 · on_error_linger · empirical
Cartridge BASIC ON ERROR GOTO stays armed after END. Direct-mode error:
ERL=65535, error code reported normally. Clear with ON ERROR GOTO 0
before END. 1/0 does NOT trap (no BASIC-level error raised); Out of
DATA (err 4) traps reliably. Use Out of DATA for handler tests.

## 2026-08-22 · busy100cal_aborted · decision · tooling
CH0 single-wrap timing (65536 ct = 27.47 ms @ empirical 2.38636 MHz)
is unfit for measuring interpreted-BASIC delays. Jitter spans multiple
wraps; a single wrap flag undercounts, and min-on-raw-dt is wrong under
wrap. If the line-130 delay is ever needed, measure from ASM with a
multi-wrap counter, never from BASIC. Stage gates passed S0 (trap via
Out of DATA), S1 (INP/OUT + CH0 read), S2 (A0 mask/unmask, kb intact).

## 2026-08-22 · width80_rejected · empirical
WIDTH 80 works in Cartridge BASIC but is unreadable on this monitor.
Stay at 40-col with paged, fixed-width output. `; VERIFY: WIDTH 80
support against PCjr BASIC Reference`.

## 2026-08-22 · anchors_archived · decision · tooling
ENVSHAPE.BAS + CH0CAL.ASM archived as ground-truth anchors
(skill_create: "ENVSHAPE Anchor", "CH0CAL Anchor"). Repo is source of
truth: full listings now live at docs/anchors/ENVSHAPE.BAS and
docs/anchors/CH0CAL.ASM.
## 2026-08-22 · stock_throughput_retired · empirical + analysis
86 ch/s retired as a link figure: INT 16h drain of a pre-filled
buffer with KBDNMI masked; producer absent; unit ambiguous (system
type-ahead vs keyboard MPU buffer).
supersedes: Rule 8 "stock ceiling ~86 chars/sec".

## 2026-08-22 · emitter_throttle_60 · policy
60 ch/s = emitter throttle (sleep 1/max_cps) to bound NMI CPU tax.
Not a ceiling; disappears with the CPU floor under a custom path.

## 2026-08-22 · stock_two_floors · manual-verified + empirical
Serial floor: 440us cell, 11-bit frame, 4840us IBG (entry 94).
CPU floor: KBDNMI ~4.8ms/frame hostage (220us half-cell, 5x
majority, entry 93) + KBINT consumer cost.

## 2026-08-22 · nmi_one_per_frame · manual-verified
NMI fires once per frame on start-bit leading edge (entry 93).
Keypress = make + break = 2 NMIs. Typematic rate unverified
(; VERIFY: against PCjr keyboard docs).

## 2026-08-22 · wired_port_not_faster · manual-verified
Cable shares biphase serial + 11 stop bits (entry 94) and the same
flip-flop -> PC0 latch -> NMI path (entry 95). Bypasses only the
photodiode/amp/demod front-end.

## 2026-08-22 · pc6_demod_envelope · manual-verified
PC6 = demodulated envelope: photodiode -> amp -> amp w/AGC ->
demodulator -> BO3 I.R. KBD DATA (entry 92). 40 kHz carrier
mandatory (entry 92). 62us burst -> H ~230us typ / ~471us max.
Upgrades the earlier empirical label; PC6 is not the raw carrier.

## 2026-08-22 · memory_matcher_semantics · analysis
BDS 'called' memory keys split on underscores and fire per token
(FAQ §20). Explains pcjr_* acting like always.

## 2026-08-22 · envelope_floor_open · open item
Full H/L delta dump never transcribed (only summary stats +
gap2_1126). Open: stretch distribution, merge distance, min assert
width. Custom PC6 decode floor = stretch + merge, unmeasured.
