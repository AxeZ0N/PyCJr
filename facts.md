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
## 2026-08-22 · base26_dump_locked · decision
Base26 dump format LOCKED. Alphabet `ABCDEFGHIJKLMNOPQRSTUVWXYZ` — all 26
letters, none dropped, `A`=0. Variable-width, no leading zeros,
space-delimited, fixed 6 tokens per line, max 4 symbols (26^4 = 456,976
covers 16-bit). Encoder = 2000 subroutine, wrap = 3000/3040. Verified on
hardware via ENVSHAPE26. Supersedes the base34 proposal, which was
rejected pre-ingest (letters-only; digits cost more than they save at
touch-typing speed).

## 2026-08-22 · cartridge_basic_not_equal_operator · empirical
Cartridge BASIC not-equal is `<>`, never `!=`. `IF V!=0 THEN` parses the
`!=` as an `=` equality test and inverts the branch, silently zeroing the
encoded output. Verified on hardware. Line 2000 uses `if v!<>0 then 2030`.

## 2026-08-22 · envshape26_hardware_pass · empirical
ENVSHAPE26 = frozen CH0CAL ASM (100 bytes, byte-for-byte) + base26 dump.
One-keypress run: st=1, ed=38, in0=0, it=61440 (paste shows "6144" —
transcription drop; loop is fixed 0F000h), nh=19, nl=18, mh=572, xh=1124,
ml=745, xl=3502. Keyboard intact presumed (clean completion; "Ok" omitted
in paste — confirm). Dump = 7 lines, 6 tokens + 1 trailing.

## 2026-08-22 · stretch_merge_confirmed_two_runs · empirical
Two independent runs (one base34, one base26 — encoding change did not
change the physics) agree on the envelope: H (burst) mean 572 counts =
239.7 us; max H 1124-1126 counts (~471 us); recurring short H 406 counts
= 170.2 us (min-assert lower bound). L (silence) min 190 counts = 79.6 us
(merge-distance lower bound); frame-gap max 3500-3502 counts (~1467 us,
just under the 1500 us emitter floor). Decode-floor lower bound =
406 + 190 = 596 counts ~ 250 us.

## 2026-08-22 · envshape26_line3_token · open item
Dump line 3 token 5 was transcribed `bc` (28 counts), which contradicts
the printed mH=572. Mean reconciliation requires `vc` (548): 548*5 with
the other H values sums to 10870, mean 572. `b`/`v` are adjacent keys —
transcription slip. Corrected line 3 = `ve vc ve sk vc fes`.
Re-read on the next run to confirm.
## 2026-08-22 · kbdnmi_pinned_span · listing-verified

KBDNMI (entry 338) pins the CPU from CLI 0F76 to STI 0FF4, no yield
point. Start bit: 5-sample majority >=3 (CX=5). Trailing-edge hunt:
CX=50 watchdog. CH1 latched reads via 43h/41h (0FAB). 8 data bits x2
biphase samples, opposite-half compare (0FC9). Parity x2, odd check
(0FE1). MOV AL,BH / INT 48h (0FF5).

## 2026-08-22 · stock_cpu_floor · analysis

Exclusive CPU per frame = 10 cells x 440 us = 4.4 ms (start+8
data+parity). Per byte 3.52 ms. Free tail = stop + 11 stop bits = 12
cells = 5.28 ms. Per scancode 9.68 ms; per keypress (make+break) 19.36
ms. Hard floor for receiver-only designs: CPU is the de-serializer - no
FIFO/8042/8251 between PC6 and RAM.

## 2026-08-22 · stop_bits_reason · manual-verified

Entry 94: eleven stop bits are inserted "to allow some processor
bandwidth between keystrokes to honor other types of interrupts, such
as serial and time-of-day." CPU-service headroom, not RF/AGC.

## 2026-08-22 · kbdnmi_comment_conflicts · conflict

Entry 338 listing vs comments: (a) 0FC6 BA 0220 = 544 -> 456 us at
1.1925 MHz, comment says "310 us"; (b) 0FCC BA 020E = 526 -> 441 us =
one full cell, comment says "next half bit"; (c) listing samples parity
then jumps straight to INT 48h - the manual's 11th (stop) bit is never
consumed. Three discrepancies recorded, none resolved.

## 2026-08-22 · no_free_timer_irq · manual-verified

Only maskable timer IRQ: CH0->IRQ0->INT 08h (time-of-day, 18.2 Hz =
1193180/65536). CH1 (41h) is CPU-read-only - KBDNMI polls it, never
interrupt-driven (entry 338, subroutine I30). CH2 (42h) = audio/PC5, no
interrupt output. Keyboard arrives on the NMI pin (INT 02h), not the
8259; no NMI->timer chaining on this board.

## 2026-08-22 · biphase_agc_hypothesis · analysis

Hypothesis: biphase is load-bearing as AGC DC-balance (every 440 us
cell carries exactly one burst -> ~50% duty), not as self-clocking
(KBDNMI times with CH1, listing-verified). Mechanism unverified. Do not
drop biphase without the AGC profile probe (burst-silence-burst envelope
measurement).

## 2026-08-22 · parallel_decode_non_goal · decision

Interrupt-driven parallel decode rejected: no free timer IRQ;
single-task Cartridge BASIC has no concurrent workload to protect.
Cooperative CH0-latched scheduling is feasible (~2100 cycles/cell
budget, sample ~30-50 cycles) but is a solution in search of a problem
here. Not a build item.

## 2026-08-22 · paste_throughput_target · decision

Actual PyCJr goal: one-way paste speed into Cartridge BASIC. Levers in
hand: 1500 us frame gap (banked, 1.5x vs 11-stop-bit stock), dense
per-event encoding, cooperative CH0 decoder. Decoder was replaceable but
non-binding; transmitter was the immutable floor; PyCJr is the first
owner of both ends.

## 2026-08-24 · agc_h_response_two_regime · empirical
Controlled Pi probe (CH0-latched PC6, 2.38636 MHz empirical clock).
H = high envelope after a 40 kHz carrier burst of width W, S=5000 us:
- W 25/40/62/125 us : H = 550 ct = 230 us (floor)
- W = 250 us       : H = 1126 / 1052 ct = 472 / 441 us
- W = 500 us       : H = 1702 ct = 713 us (~W + 210 us)
Transition width W_c between 125 and 250 us. Refutes both
"constant stretch" and "H = W" models.

## 2026-08-24 · agc_l_two_regime_offset_floor · empirical
L = measured low between two W=62 us bursts, vs programmed silence S:
- S = 220 us  : L = 188 ct = 79 us (floor dominates)
- S = 440 us  : L = 620 ct = 260 us (~S - 180 us)
- S = 1500 us : L = 3142 ct = 1317 us (~S - 183 us)
- S = 5000 us : L = 11420-11636 ct = 4786-4876 us (~S - 124..215 us)
Model: L = max(S - ~180 us, ~79 us). The 79 us floor matches the
repo two-run min-L 190 ct = 79.6 us. Offset is W-independent
(S=5000 flat across the W sweep); no conservation violation.

## 2026-08-24 · agc_w250_h_asymmetry · empirical
W=250 pair at S=5000: H1=1126 ct (472 us) vs H2=1052 ct (441 us),
a 31 us gap at identical stimulus. W=500 pair is symmetric
(1702/1702). Magnitude-dependent recovery suspected; unverified.
Single datapoint that breaks the clean two-regime model.

## 2026-08-24 · demod_stretcher_model · analysis
Unified model from the H and L regimes:
- min output high ~230 us (floor)
- high extension ~200 us beyond W for W >= ~250 us
- low release delay ~180 us
- min output low ~79 us
Consistent with a minimum-pulse-width pulse-stretching demod stage.
The L release delay is independent of W.

## 2026-08-24 · agc_merge_threshold · empirical
Burst-pair W=62 us edge count vs silence S:
- S = 220 us : ed=4, L=188 ct = 79 us, H2/H1 = 478/550 = 0.87
- S = 157 us : ed=2 (merged)
- S = 80 us  : ed=2 (merged)
- S = 40 us  : ed=2 (merged)
Merge threshold between 157 and 220 us. ed=2 trials produced no dump
(ed>=3 gate); merged-high width unmeasured this scope.

## 2026-08-24 · agc_recovery_threshold · empirical
H2/H1 amplitude ratio: 0.87 at S=220 us, 1.0 at S=440 us.
Full amplitude recovery between 220 and 440 us (assumed monotonic;
the in-between curve is unverified).

## 2026-08-24 · agc_probe_repeatability · empirical
Two independent runs of the same 62/5000 pair: H 550/548 vs 550/550
and L 11566 vs 11564. Short-term repeatability <=2 ct (~0.8 us) on
both H and L.

## 2026-08-24 · agc_duty_insensitive_8train · empirical
8-burst 50% train (W=62/S=440 us, ~3.5 ms): H flat 548-550 ct
(~230 us) across all eight, no tail sag. L 620-694 ct (260-291 us),
within poll quantization. Duty-insensitive over the tested horizon.

## 2026-08-24 · biphase_agc_duty_weakened · analysis
8-cell 50% train H equals sparse-pair H. AGC envelope is not
duty-sensitive over ~3.5 ms, weakening the biphase-as-AGC
duty-balance hypothesis. Not refuted over the full 11-bit frame
(~4.8 ms). Do not drop biphase without an N=12 train.
Extends biphase_agc_hypothesis; does not supersede it.

## 2026-08-24 · stock_zero_silences_map · analysis
Measured thresholds map onto stock emitter silences:
- zero_silence_1 = 220 us : at recovery floor, second burst attenuated.
- zero_silence_2 = 157 us : below merge threshold, bursts fuse.
- start_silence = 310 us : below observed full recovery (440 us), so
  stock traffic never reaches a fully recovered second burst (assuming
  monotonic recovery in 220-440 us). Amplitude is never a reliable
  stock signal; timing only.
This is the empirical root of the 38-vs-40 edge count and the 1450 ct
manual-press merge candidate. Stock decode survives because KBDNMI is
sample-based, not edge-based (entry 93).

## 2026-08-24 · gap2_1126_controlled_repro · empirical
W=250 controlled run produced H=1126 ct, matching the frozen
gap2_1126. A merged zero-silence pair presents ~250 us effective
stimulus and yields the same H. Extends gap2_1126; does not supersede.

## 2026-08-24 · decode_floor_mechanism · analysis
Repo custom decode floor 596 ct (~250 us) = min-H 406 ct + min-L
190 ct from two-run traffic. Controlled probe confirms the L component
(79 us floor). Isolated H floor is 230 us but in-traffic H compresses
(S=220: 200 us; repo min: 170 us) under recovery attenuation. The
170 us in-traffic minimum remains to be pinned; mechanism partial.

## 2026-08-24 · edge_completeness_not_decode_criterion · analysis
KBDNMI decodes by fixed-offset sampling (entry 93: wait 310 us, then
sample every 220 us half-bit, 5-sample majority), not edge
reconstruction. A manual press captured ed=34 and still decoded 'h'.
Edge count is a capture artifact, not a decode requirement.

## 2026-08-24 · ir_receiver_board_geometry · manual-verified
Entry 92: receiver card 57.15 x 63 mm, separate board, component-side
down, two snap-in standoffs, 8-pin rear connector, front photodiode
aperture, on-board diagnostic IR transmitter. Signal chain: photodiode
-> first amp -> second amp w/AGC -> demodulator -> BO3 I.R. KBD DATA.

## 2026-08-24 · ir_receiver_connector_pinout · manual-verified
Entry 93, 8 pins: A01 12V in, A02 GND, A03 GND shield,
A04 I.R. TEST FREQ in, B01 GND, B02 5V in, B03 I.R. KBD DATA out,
B04 GND.

## 2026-08-24 · ir_receiver_app_notes_truncated · conflict
Digitized manual page 2-98 cuts the application-notes sentence
mid-text. No manufacturer or part number anywhere in the strip.
Datasheet lookup impossible from the manual alone.

## 2026-08-24 · agc_profile_probe_decision · decision
No part-number datasheet exists in the manual; AGC profile must come
from hardware probing. Physical inspection fallback: the receiver is a
separate board, so its part number can be read visually if the probe
proves insufficient.

## 2026-08-24 · envshape_skill_dollar_drop · conflict
BDS ENVSHAPE anchor listing dropped $ on x$/h$/l$/hx$ and mangled
continuation lines (x="", h="", l=""). Under defint a-z these throw
"Type mismatch" at line 30. Corrected in BDS runtime cache; the repo
skill listing must get the same fix to survive a cache rebuild.
