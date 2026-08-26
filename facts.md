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
## 2026-08-24 · grep_repo_read_mode · decision
grep_repo `read` mode landed stdlib-pure (no git, no subprocess).
Args: path (root-relative, required), max_lines (default 2000).
Return: {path, lines, text, truncated, total_lines}; text is 1-based
`line_no\tcontent` lines. Safety guard rejects absolute paths, `..`
traversal, non-root first component (facts.md|sessions|docs),
non-text suffix, and symlink escapes outside repo root. Modes are now
query|read|stats|roots. Server handler returns read results as JSON;
query mode still returns text.

## 2026-08-24 · grep_repo_read_verified · empirical
Three MCP probes + one workflow trace passed after server/BDS restart.
- read facts.md max_lines=10 → lines=10, truncated=true, total_lines=346
- read ../facts.md → "path traversal refused"
- read refs/pcjr_repo_grep.py → "path must start with one of [...]"
- Workflow: query gap2_1126 → fact at facts.md:302 + owner session →
  read sessions/2026-08-24_agc_profile_probe.md → cross-check consistent.
BDS refreshed its fingerprint; path/max_lines now in the schema.

## 2026-08-24 · grep_repo_history_paste_first · policy
No revs/read_rev/diff modes. History stays paste-first:
`git log -- <path>` then `git show REV:path`.
Rationale: facts.md and sessions/ are append-only with `supersedes:`,
so the working tree is already the archive; docs/ regenerate from
facts + sessions.
Re-open trigger: if facts.md or sessions/ shift to edit-in-place,
revisit revs/read_rev.

## 2026-08-24 · tool_call_discipline · policy
Observed: every MCP tool call re-injects full context (skills, memory,
MCP fingerprint), so call count is the dominant token cost.
Repo lookup rule: one clustered grep_repo query → one read of the
owning file → cross-check in-model → second call only on conflict.
Target: two tool round-trips per repo workflow; never re-run guard
probes in normal operation.

## 2026-08-24 · memory_selection_heuristic · analysis
The injected memory block contains the ENTIRE batch every turn: all
always keys plus all called keys. The keyword gate is not pruning in
practice because trigger tokens are ubiquitous in this project
(system prompt says "PCjr" constantly; carrier/timer/frame/read/tool
terms pervade session text). Conclusion: the always vs called level
distinction buys almost no token savings here. The only real token
lever is shorter VALUES, not level placement. Static audit (keyword
specificity, value length, pointer-not-full-spec) is the best proxy
until platform hit-rate telemetry exists.

## 2026-08-24 · memory_keyword_audit_due · open item
Mandatory future pass (not now): evaluate keyword selections for the
BDS memory batch. Identify generic tokens poisoning called keys
(read, tool, frame, carrier, port); rename keys or demote values to
pointers. Hit-rate measurement is not possible from inside the
session; needs a platform-level memory-audit view (BDS feature
request). Until then: static audit only.
## 2026-08-24 · grep_repo_read_fullrepo · decision
grep_repo `read` mode scope extended from the three fact-layer roots
to the whole repo (root-relative path, text suffixes only).
Supersedes the three-root rule in grep_repo_read_mode (2026-08-24).
Guards unchanged and verified: absolute path refused, `..` refused,
any hidden path component refused (.git/config test), symlink escape
refused, non-text suffix refused, max_lines truncation explicit.
Verified: read pycjr.py max_lines=30 -> 30 lines, truncated=true,
total_lines=554.

## 2026-08-24 · grep_repo_grep_all · decision
New mode `grep_all`: whole-repo regex search over text files (same
guard set as read), capped by max_matches (default 50). Returns
total_matches, returned, truncated, files_searched, text. `query`
stays fact-layer-only; the split keeps curated fact search clean
while grep_all locates code/config symbols (flags, defines, handlers).
Cap is mandatory under tool_call_discipline: observed 190 matches for
a generic token, returned 5, truncated=true.
Verified end-to-end over MCP after server/BDS restart.
## 2026-08-24 · pycjr_run_test_harness_contract · empirical
Live pycjr.py (root, 664 lines) implements `--run_test FILE` with
`nargs='?'`, plus `--spec`, `--arm`, `--post`, `--battery`. Trial file
grammar: `label, lead_us, on,off, on,off, ...`; `#` starts a comment,
blank lines are skipped. `build_probe_wave(lead, pairs)` emits lead
silence, then per pair an `on_us` 40 kHz carrier burst followed by
`off_us` silence; the final `off` is trailing. `run_battery` sequences
cls/run/enter/arm/wave/post. `run_suite` batches by `--battery`
(default 4). `bin/pycjr.py` is stale (`store_true`/`testing_macro`);
the live Pi file is authoritative for the harness.

## 2026-08-24 · threshold_pinning_battery_spec · decision
Threshold pinning battery: W=62 us, lead=0, trailing=5000 us.
Merge sweep S=180/190/200/210; recovery sweep S=260/300/340/380.
8 trials, default `--battery 4` -> two batches (merge, recovery).
Delivered as `threshold_battery.txt`; spec recorded here.

## 2026-08-24 · ground_truth_anchor_convention · policy
Every hardware-passed program gets `docs/anchors/<PROG>.BAS` and
`docs/anchors/<PROG>.ASM`. Session handoff gains a mandatory fifth
section, Ground truth, listing anchor paths. No listing present means
the session cannot close. DATA blocks must byte-match the ASM;
regenerate via `debug_asm`, never hand-roll. Retype path is
`docs/anchors/`, never back-issues of sessions.

## 2026-08-24 · agcprobe_anchor_restored · decision
AGCPROBE.BAS restored from user transcription; included in payload at
`docs/anchors/AGCPROBE.BAS`. DATA 1000-1100 byte-identical to the
ENVSHAPE block, matching the CH0CAL.ASM 100-byte image.

## 2026-08-24 · ch0cal_asm_anchor_restored · decision
CH0CAL.ASM included in payload at `docs/anchors/CH0CAL.ASM`; design
logic for the 100-byte image used by ENVSHAPE.BAS and AGCPROBE.BAS.

## 2026-08-24 · session_title_scope_policy · open item
Session sidebar titles are all "PCJr Session Start"; useless for
retrieval. The system prompt final line must instruct the first
assistant message to state the active scope explicitly so the platform
can use it as the session title. User to edit `bds/00_system_prompt.md`.
Until applied, titles remain generic.

## 2026-08-24 · ingest_payload_extension · decision
Payload contract extended to accept `docs/anchors/` files so
`unzip payload.zip` places anchors correctly. Update `jr-ingest.sh`
or the manual unzip path accordingly.
## 2026-08-24 · agc_h_ratio_staircase · empirical

PC6 demodulated envelope, W=62us two-burst probes. H2/H1 amplitude ratio
is quantized, not a smooth recovery ramp. Three discrete states only:

- fused (S <= 170us, ed=2)
- 0.74 compressed (S=175us, H2=406ct)
- 0.87 attenuated plateau (S=190–230us, H2=478ct)
- 1.00 full recovery (S >= 240us, H2=550ct)

Transitions are near-vertical. Suggests discrete AGC gain stages, not RC
decay. Supersedes: the (220,440) and (220,260) monotonic-recovery reading.
See 2026-08-24_threshold_pinning.md.

## 2026-08-24 · agc_fuse_threshold · empirical

Fuse boundary pinned to (170,175]us for W=62us. S=170 merges (ed=2),
S=175 resolves (ed=4, H2/H1=0.74). Stock zero2 (157us) is inside the
fused regime; this is the mechanical root of the 38-vs-40 edge count.

## 2026-08-24 · agc_full_recovery_threshold · empirical

Full H2 recovery pinned to (230,240]us for W=62us. S=230 reads 0.87,
S=240 reads 1.00. Stock zero1 (220us) resolves but attenuated; start
(310us) and one (377us) fully recovered. Custom decoder floor = 240us.

## 2026-08-24 · agc_l_staircase · empirical

L (low-time) is also quantized, not smooth. W=62us, S sweep 300–380us:
334ct at S=300/310, jumps to ~404ct at S=320/330/335, jumps to 476ct at
S=340/380. Steps ~30us. Mechanism unverified; consistent with discrete
receiver-side quantization or probe code-path latency. L = S − 180us
holds again at large S (W=250/S=5000: 11420–11492 vs 11502 predicted).

## 2026-08-24 · w250_asymmetry_retired · empirical

W=250/S=5000 asymmetry (1126/1052) did not reproduce in four repeats:
three symmetric, one 72ct split. Intermittent edge-trigger jitter on the
soft falling edge of a W>=250us burst, not magnitude-dependent recovery.
Retired. H at W=250 wanders 1054–1126ct at identical stimulus.

## 2026-08-24 · demod_envelope_staircase · analysis

The entire PC6 demod envelope is quantized: H amplitude in three states,
L timing in discrete steps. Amplitude is therefore unusable as a signal
for a custom edge decoder; timing is the only reliable channel. Confirms
the earlier "timing only" design rule; upgrades it from hypothesis to
empirical fact.
## 2026-08-24 · agcprobe2_fused_voided · decision

AGCPROBE2 fused-HIGH battery results were fabricated by the prior
assistant and are voided and purged. No per-trial AGCPROBE2 values
exist on record. Valid this session: CH0CAL pre-pass caught 'h';
harness fired all six trials; AGCPROBE2 (AGCPROBE.BAS line 190
`if ed>=2 then 210`) was the runner; keyboard intact after. The
"All runs st=1 ed=2 H:1126 L:N/A" line is the CH0CAL gap2 anchor
reading, not a battery result. Next session must re-run
trials_high.txt and transcribe raw per-trial output in firing order.
## 2026-08-24 · kbdnmi_time_biphase_decoder · manual-verified

KBDNMI (Technical Reference entry 338) is a time-driven biphase
decoder, not an edge-driven one. After the start-bit trailing edge it
latches CH1 once, then samples PC6 at absolute half-bit offsets via
subroutine I30 (5 samples, majority vote ≥3 → 1). A bit is valid only
if its two half-samples are OPPOSITE (OFD8 CMP CL,AL / OFDB JE phase
error); then odd parity is required (OFEF AND BL,1 / OFF2 JZ parity
error). Either failure jumps to I9: beep, no character. Inter-bit gap
merges do not disturb the intra-bit biphase transition and are therefore
functionally invisible to stock decode. The frame gap (1500us) AGC
recovery explains why the first short gap after it survives while
mid-train gaps fuse.

## 2026-08-24 · ed_envelope_edge_not_decode · empirical

ed counts PC6 envelope edges via CH0 timestamps. It is a diagnostic,
not a decode result. Deterministic hpress spec (20 bursts, verified
pulse-for-pulse equivalent to build_frame(0x23)+build_frame(0xA3))
returned ed=36 2/2; manual taps 36 2/2. Two stable merges: H6=1126,
H17=1124, both 157us 0→1 gaps. H16=406 and L9=3572 (~1497us frame gap)
stable across runs. Stock still prints 'h'. Code, Pi runtime, pigpiod,
wiring, breadboard rework, and percussive contact all exonerated.
The 38→36 shift is receiver analog drift in a closed warm room.

## 2026-08-24 · z2_agc_floor_hypothesis · unverified

Hypothesis: stock zero_silence_2_us=157 sits at the AGC/demod minimum
resolvable silence. Envelope profile L=max(S−180, 79us) saturates to
~79us at S=157 — shorter than the demod's minimum pulse width. Likely
sizing order: set the tightest gap to the analog resolution floor, then
build the biphase/time decoder above it so decode is blind to merges.
No AGC datasheet in hand. KBDNMI mechanism is manual-verified; the
157us floor is unverified. Settled only by the functional z2 sweep.

## 2026-08-24 · ch0cal_ed_reading_conflict · conflict

Historical CH0CAL anchor reading: ed=38. Current deterministic + manual
reading: ed=36 (warm-room). Program bytes unchanged; reading shifted.
Anchor stands as ground truth for the program. The ed=38 expectation is
now environmental, not contractual.
## 2026-08-25 · densetrain_loaded_separation_floor · empirical

Dense pulse train (W=62us, 12 bursts, lead=0, trailing=5000us). Under
sustained AGC load the resolvable-silence floor rises above the isolated
two-burst merge band (157-170us):

- S=240us: clean, 24/24 edges.
- S=230us: one fusion of 11 gaps (stochastic onset).
- S=220us: clean in one run, severe H compression (406-478 ct).
- S<=200us: collapse, multiple fused gaps.

Safe dense design margin: inter-burst gap >= 240us.

## 2026-08-25 · densetrain_h_compression · empirical

Under dense load H compresses from the isolated 550 ct (~230us) floor:
- S=240: H mixed 550/476 ct.
- S=230: H 478 ct with fusion artifacts.
- S=220: H oscillates 476/478 (~200us) and 406/404 (~170us).

The 406 ct (~170us) in-traffic minimum is reproduced deliberately; it is
partial-recovery attenuation, not the steady-state isolated floor.

## 2026-08-25 · dense_cell_250us_retired · analysis

supersedes: decode_floor_mechanism

The earlier 596 ct (~250us) custom decode floor (min-H 406 + min-L 190)
is an isolated/two-run artifact. In dense traffic the binding constraint
is separation, not pulse width: H ~200us + separation >= 230us gives a
dense cell of ~430us or more. The 250us cell is not achievable under
continuous load.

## 2026-08-25 · mary_gap_alphabet_retired · analysis

M-ary gap encoding is dead on this data. Measured L saturates at
190 ct (~79us) for every transmitted gap below ~S=260us, so a decoder
sees no alphabet in the usable dense range. Above 260us the ~30us
staircase steps would force an 8-level alphabet to span ~240us of
dynamic range with an average gap worse than a stock one-cell. The gap
alphabet cannot pay for itself.

## 2026-08-25 · framing_only_2x · analysis

With cell shrink and M-ary both refuted, the remaining gain over stock is
framing only: drop make+break, parity, stop bit, and the 4840us IBG.
Expected ~2x (~100-120 ch/s), same order as the current 60 ch/s
emulator. The stock CPU hostage removal is a separate, unmeasured lever.

## 2026-08-25 · periodic_recovery_gap · open item

Unverified: interleave a long AGC-reset silence (>=1500us) every few
symbols, keep inter-symbol gaps tight (180-220us) in between. Untested;
the one remaining analog idea that could restore partial cell shrink.
## 2026-08-25 · recovery4_reset_suppresses_fusion · empirical

RECOVERY4 (W=62us, 12-burst trains, reset 1500us after bursts 4/8,
trailing 5000us; AGCPROBE.BAS capture, CH0CAL ASM):

- CTRL_180 (no reset): ed=12, 6 fusions — reproduces dense-floor collapse.
- R4_180: ed=22, 1 fusion (post-reset block 3) — reset drops fusion 6→1.
- R4_200: ed=24, 0 fusions — S=200 collapse rescued by reset.
- R4_220: ed=24 clean (L7=133 anomaly, see session loose ends).

Reset L reads 3140/3142ct, matching the 1500us calibration (3142ct).

## 2026-08-25 · periodic_recovery_retired · analysis

Reset cost/sym = (W+S) + (R−S)/k. Win vs no-reset safe cell 302us/sym
requires R < 180 + 60k. At R=1500: k > 22 clean symbols per reset.
Measured grace k≈3 (fusion returned in block 3 of R4_180). Off by ~7×.
No operating point breaks even — small R amortizes but buys no grace;
large R buys grace but costs too much. Retired.

## 2026-08-25 · ibg_minimum_unmeasured · analysis

frame_gap_us=1500 is the empirical safe replacement for the 4840us
11-stop-bit IBG (manual entry 94); stock decodes at 1500us. It is NOT
proven the minimum possible IBG. The true AGC minimum below 1500us is
unmeasured (z2 sub-gap sweep 157→80 deferred). Say "1500 is the
verified safe replacement," not "smallest possible."

## 2026-08-25 · receiver_observables_binary · analysis

PC6 is one binary bit: demod outputs carrier-present HIGH / absent LOW
(manual-verified entry 92). There is no amplitude axis at PC6. A
three-state DC-on / DC-off / 40kHz scheme collapses: DC-on and DC-off
both produce zero carrier → both read LOW. Only OOK survives. AGCPROBE
duty-flat (W=25/40/62/125us all read 550ct) shows width is destroyed
too; amplitude would be destroyed harder.

## 2026-08-25 · modulation_alternatives_closed · analysis

NRZ: consecutive 1s become one merged H (AGC is a merge machine).
M-ary gap alphabet: retired (L saturates 190ct for gaps ≤260us).
Width modulation: dead (duty-flat).
Amplitude modulation: dead (PC6 binary, no amplitude path).
FM sub-carrier: dead (fixed 40kHz demod, manual entry 92).
Biphase is not the constraint; the AGC envelope (H_min~170us,
L_min~79us) is. A custom decoder frees the validity rule
(halves-opposite) for margin, not a smaller cell.

## 2026-08-25 · keypress_loss_budget · analysis

Stock keypress (manual entry 94) = four 4840us chunks: make frame,
make IBG (11 stop bits), break frame, break IBG = 19360us. The cell
(440us) is 2.3% of that budget. The analog work pinned only the cell.
Remaining levers are design/software: framing-only (drop make+break,
parity, stop) ~2×, and the CPU hostage (KBDNMI ~4.8ms/frame majority
sampling). The 60ch/s throttle is policy, not hardware.

## 2026-08-25 · analog_phase_closed · decision

The AGC analog phase is closed. Four directions exhausted: cell shrink
(440us pinned), periodic recovery (uneconomical), clock scaling (CH1
granularity was never the limit), modulation alternatives (all dead).
Remaining throughput is framing + CPU hostage. Next scope: custom
deserializer (replace KBDNMI).
## 2026-08-25 · debug_asm_v5_decode · manual-verified

`debug_asm` v5 decode fixes the `C6` byte-stream desync: `C6 46 D8 07` was
decoded as four single-byte `db` entries; it now decodes as one 4-byte
`mov [bp+0xD8],0x07`. Root cause: `C6` was outside the verified subset and
fell to the 1-byte `db` fallback.

## 2026-08-25 · debug_asm_v5_opcodes · manual-verified

Added decode coverage: `iret` (CF), `dec r16` (48-4F), `push r16` (50-57),
`pop r16` (58-5F), moffs `mov ax,[abs]`/`mov [abs],ax` (A1/A3),
`mov r16,r/m16` (8B), `mov r/m8,imm8` (C6). `55`/`5D` moved from OP1 into
the push/pop ranges; IRPING decode_31 count unchanged.

## 2026-08-25 · debug_asm_v5_robustness · manual-verified

`decode`/`_modrm` are length-safe via `_need`; truncated trailing
instructions render `db ; truncated` instead of raising IndexError.
`branch_checks` is OOB-safe. Hex input accepts whitespace and optional
`0x` via `ASM._hex_or_error` (server routes through it). Selftest: 50
gates, ALL_PASS True. No hardware run this session.
## 2026-08-25 · basload_naming · decision
BASLOAD adopted as the PCjr-side BASIC harness identifier (the full
runner: scalar pre-declare + DIM A + sentinel loader + CALL O + O+128
result map). Rule 3 "Sentinel Loader" heading is the loader-pattern
name only and stays unchanged; no SENTINEL program name exists. The
Pi-side `pycjr_run_test_harness` (pycjr.py --run_test) remains a
distinct name.

## 2026-08-25 · ch0cal_primary_regression · decision
CH0CAL is the primary full-path regression for custom-deserializer
work. IRPING is demoted to transport-only regression; its frozen DATA
stays in platform skill Rule 5. The split is additive, not a replace-
ment: no `supersedes:` on the IRPING fact. CH0CAL pass criterion is
functional (h decodes, keyboard intact), not exact ed — ed=38 is
environmental, not contractual.

## 2026-08-25 · debug_asm_subset_s1 · empirical
debug_asm verified subset extended (user tool edit) for the S1
NMI-intercept build. Newly verified: iret CF (manual-verified, BIOS
KBDNMI entry 338 ends IN AL,A0h then IRET), push ax 50, pop ax 58,
mov ax,[moffs16] A1, mov [moffs16],ax A3, mov ax,[bp+d8] 8B,
mov byte [bp+d8],imm8 C6 /0, dec dx 4A, mov dx,imm16 BA,
mov ax,imm16 B8. Decoder bug fixed: C6 46 d8 imm8 previously emitted
"db C6 / inc si" instead of the 4-byte instruction. mov ds,ax 8E D8
and mov ax,cs 8C C8 deliberately NOT used; the push/pop path covers
both with fewer novel forms.

## 2026-08-25 · s1_nmi_intercept_contract · decision
S1 contract frozen. id S1_NMI_INTERCEPT, source BASLOAD.BAS + S1.ASM,
expected {return RETURNED OK, flag 1, status 0, keyboard_after intact},
regression IRPING -> CH0CAL, recovery cold_power_cycle. Result map at
O+128: [0]=flag, [2]=saved IVT offset word, [4]=saved IVT segment
word, [6]=status (0 fired / 1 timeout). Handler installs at INT 02h
(0000:0008) and returns via IRET. Stage ladder S0-S5 frozen in
2026-08-25_s1_nmi_intercept_sop.md.

## 2026-08-25 · s1_emission_gate_pass · empirical
S1 110-byte image passed the emission gate. selfloc pop_offset=5
disp=0x007B (lea bp,[bp+0x007B]); branch checks 4/4 (call 2->5,
je 0x39->0x44, loop 0x3B->0x35, jne 0x3E->0x32); full decode clean,
zero outside-subset fallbacks; handler at offset 0x61. Outer wait
count BA1800 (24) flagged `; VERIFY:` for hardware calibration. No
hardware run yet — S1 is NOT anchored.

## 2026-08-25 · selfloc_pop_offset_semantics · analysis
debug_asm selfloc `pop_offset` is the value BP holds AFTER `pop bp`
(the offset of the next instruction byte), NOT the result target;
`base` is the result target. S1 has no push bp, so pop bp lands at
offset 5 and pop_offset=5. Passing 128 as pop_offset silently produced
disp=0 — a self-consistent but wrong LEA that the gate cannot catch
from the output alone. Always derive pop_offset from the instruction
layout, never reuse the result offset.

## 2026-08-25 · deserializer_sop_frozen · decision
Custom-deserializer design/test SOP frozen: contract-first, retrieve
before emit, S0-S5 stage ladder (S0 IRPING, S1 NMI intercept stub,
S2 CH0-in-NMI, S3 one-frame edge capture, S4 gap classify + decode,
S5 make/break + consumer), emission gate via debug_asm, CH0CAL primary
/ IRPING transport-only regression, cold-recovery only. Full text in
2026-08-25_s1_nmi_intercept_sop.md.
## 2026-08-25 · basic_bp_preserve_contract · empirical

Any machine code entered via `CALL O` from Cartridge BASIC must
preserve bp across the call (push bp at entry after `pop ds`, pop bp
immediately before `retf`). Clobbering bp corrupts the interpreter
frame and yields `Division by zero in (blank)` with a dead keyboard —
unrecoverable, cold power-cycle only. S1 v1 violated this; IRPING and
CH0CAL already obey it. Promoted into platform skill Rule 1 via the
skill patch in this payload.

## 2026-08-25 · iret_bridge_status · analysis

IRET (CF) is architecturally the only correct NMI-return primitive:
RETF leaves FLAGS on the stack and corrupts the caller (manual-
verified, BIOS KBDNMI entry 338 ends IN AL,A0h then IRET). Empirically,
no `CALL O` bridge program using IRET has passed hardware — S1 v2,
the only IRET-bearing program run, rebooted into BIOS with cause
undiagnosed. Label discipline: `manual-verified` means present in the
manual/BIOS listing, not safe in our bridge path. IRET stays
`unverified` in the bridge until the per-instruction ladder anchors
it. Corrects the "approved for the handler" note in
`debug_asm_subset_s1`.

## 2026-08-25 · basload_loaded_byte_discriminator · analysis

BASLOAD prints `loaded N bytes` where N is the actual machine-code
length. N is the primary discriminator between DATA blocks: IRPING =
61, S1 v1 = 110, S1 v2 = 114. Earlier "S1 timeouts" were IRPING (61
bytes) finishing through BASLOAD's S1 result-map offsets, not S1
timeouts. Always gate on the printed byte count before arming.

## 2026-08-25 · on_error_nmi_reenable · open item

User reports that when the BASIC interpreter survives a machine-code
return but NMI is left masked, an `ON ERROR GOTO` handler can
re-enable the keyboard (IN AL,A0h then OUT A0h,80h). Exact BASIC
pattern and recovery-stub location not yet transcribed. Plan: capture
the working pattern and fold it into BASLOAD as a standard recovery
path. Applies only when the interpreter frame is intact; a bp clobber
bypasses ON ERROR entirely.

## 2026-08-25 · s1_stage_gate_decision · decision

S1 NMI-intercept scope closed on catastrophic failure. Next scope:
per-instruction hardware verification ladder, one risk class per
stage, each gate must pass on the PCjr before advancing. Regression:
IRPING then CH0CAL before any NMI-touching stage. Full ladder in
2026-08-25_s1_stage_gate_triggered.md.

## 2026-08-25 · payload_skill_patch_extension · decision

Payload may now carry `skill_patch.diff`: a unified diff for the two
bds/10_skills files (F1-F5 this session). It is applied manually via
`git apply skill_patch.diff` and reviewed with `git diff -- bds/`,
NOT through bin/jr-ingest.sh. Full overwrite files are never emitted
in the payload; the patch carries only surgical hunks.
## 2026-08-25 · int02_vector_write_ub · decision
Writing the INT 02h vector (0000:0008/000A) is undefined behavior on
this machine. Stage 5 (dummy 1111:2222) and stage 5c (no-op write of
saved value) both returned clean on screen but killed the keyboard;
5c never had a bogus vector at any instant, isolating the write act
itself. Never install an NMI handler via IVT write.
supersedes: 2026-08-25 · s1_nmi_intercept_contract (install premise)

## 2026-08-25 · s1_ladder_residue · empirical
Per-instruction ladder, stage-gated on hardware: stages 1-4 PASS
(bridge push/pop bp, selfloc+store, NMI mask/clear/restore, clean IVT
read F000:0F78). Stage 4 proved DS-switch discipline fixes the S1 SOP
save bug (DS=0 during [bp+disp] store wrote 0000:0002/0000:0004).
Stages 5/5c FAIL keyboard-dead -> IVT write UB. Reusable residue:
mask NMI -> poll 62h bit 6 -> CH0-latch timestamps -> restore before
RETF.

## 2026-08-25 · basload_anchor_restore · decision
docs/anchors/BASLOAD.BAS restored: line 30 x=0 (was x="" type
mismatch under defint); sv!/sg! single-precision readback (DEFINT
256*peek overflowed on BIOS segment F000); line 200 prints flag/saved/
status in hex. loaded-N count stays decimal — it is a gate, not a value.
## 2026-08-25 · deserializer_sop_polling_v2 · decision

Custom-deserializer SOP rewritten for polling. The interrupt-driven half is
retired; no IVT write appears anywhere in the ladder. Ladder v2:

- S0 IRPING — transport-only regression, unchanged.
- S1 polling probe stub — mask NMI (OUT A0h,00h), dummy IN AL,A0h to clear
  the latch, finite poll of 62h bit 6, restore (OUT A0h,80h), RETF.
- S2 CH0-in-poll-loop — CH0 latched read per edge, timestamp array.
- S3 one-frame edge capture.
- S4 gap classify + software decode (440us cell; start + 8 data + parity +
  stop; odd parity).
- S5 make/break + consumer.

S1/S2 reuse the hardware-verified ladder residue from
2026-08-25_s1_ivt_write_ub.md (stages 1-4 pass: bridge, selfloc, NMI
mask/clear/restore, clean IVT read). CH0CAL remains the primary regression;
IRPING stays transport-only. Two flags carried: arming-swallow (wait-for-
first-edge discipline), and stock make-only/held-key behavior unverified
(blocks nothing before S5). S1 v2 body choice (verbatim IRPING edge-counter
body vs first-edge-only stub) left open.

supersedes: 2026-08-25 · deserializer_sop_frozen (interrupt-driven S1-S5 ladder)

## 2026-08-25 · s1_frozen_image_bp_violation · conflict

The frozen 110-byte S1 image recorded in 2026-08-25_s1_nmi_intercept_sop.md
and summarized in s1_emission_gate_pass omits push bp at entry and pop bp
before retf, violating the bp-preserve contract (Rule 1). Its self-location
(call get_ip / pop bp / lea bp,[bp+0x7B]) clobbers the interpreter frame
pointer; this is the S1 v1 that hardware-failed with Division by zero.
Corrected image is S1 v2, 114 bytes: push bp at entry, pop bp before retf,
selfloc pop_offset=6 disp=0x7A; full listing in
2026-08-25_s1_stage_gate_triggered.md. Both images are obsolete — the
interrupt-driven path is retired by the INT 02h IVT-write UB finding — but
the record must not leave a Rule-1-violating image as the frozen S1.

supersedes: 2026-08-25 · s1_emission_gate_pass (110-byte image as frozen S1)
