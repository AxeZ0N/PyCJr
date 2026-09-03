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
## 2026-08-26 · s1v2_polling_pass · empirical

S1V2.BAS, 71 bytes, loaded 71. flag=0, rising=17, falling=17,
keyboard intact. Bridge push cs / pop ds / push bp ... pop bp / retf
verified on hardware. bp-preserve correct; S1 v1's bp-clobber div0 is
not reproduced. DATA 1000-1070 byte-matches S1V2.ASM via debug_asm.

## 2026-08-26 · s2v1_ch0_poll_pass · empirical

S2V1.BAS, 106 bytes, loaded 106. st=1, edge count 22h (34) in the
34-38 normal band, keyboard intact. CH0 latch/read per edge inside a
masked-NMI poll loop is safe on hardware. 16-bit cmp (39 /r) used in
place of CH0CAL's 38 /r; all instructions inside the debug_asm subset.
DATA 1000-1100 byte-matches S2V1.ASM via debug_asm.

## 2026-08-26 · s3_raw_ring_retired · decision

Hand-transcription of a raw timestamp ring is retired. The one
attempted S3 transcription corrupted beyond recovery (out-of-range and
impossible tokens); hardware, ASM, and encoder were exonerated.
Recording rule: a decoder prints only the functional answer on the
machine (h / beep / wrong-char); never dump raw edge stamps for manual
copy. ed is a ring-size sanity check, not a decode gate.

## 2026-08-26 · base26_encoder_anchored · empirical

Base26 encoder reconstructed from the locked format and
hardware-verified via B26VEC.BAS: all 11 frozen vectors pass
(0->A ... 65535->DSYP). A=0, variable-width, no leading zeros,
A-Z only. This closes the missing-ENVSHAPE26-source gap.
supersedes: 2026-08-22 · base26_dump_locked · decision

## 2026-08-26 · ch0cal_cmp38_ungated · open item

CH0CAL.ASM contains 38 D8 (cmp al,bl), outside the debug_asm verified
subset. Architecturally valid and empirically sound (CH0CAL passed
hardware), but never passed the emission gate as currently defined.
S2 v1 re-derived the compare as 16-bit cmp bx,ax (39 /r), in-subset.
Resolution options, none urgent: extend debug_asm to 38 /r, re-anchor
CH0CAL with 39 /r, or leave flagged. Not a hardware defect.

## 2026-08-26 · cartridge_basic_float16 · empirical

DEFINT overflows above 32767: S3V1 hit "Overflow in 190" constructing
the 61440 iteration count from peek() intermediates. Any 16-bit
reconstruction needs the float suffix (!) on the variable and 256! as
the multiplier, as ENVSHAPE/AGCPROBE already do. BASLOAD-family report
lines print via hex$() per the standing output rule.

## 2026-08-26 · memory_batch_spec · decision

Memory generation is formalized. Propose the full batch and wait for
approval; one batch per turn; never write silently. Key naming:
lowercase snake_case, no pcjr_ prefix. Optimize keyword hit rate: pick
tokens the user will type when recalling the decision (base26, ch0cal,
polling); never build a called key from generic tokens (cpu, port,
frame, direction). Value budget: target ~200 chars, hard cap 300; a
value is a route to the ledger, not the ledger, and ends with the
pointer (-> sessions/<file>.md or -> facts <heading>). Do not duplicate
facts.md: if a heading already owns the value, reference it and add
only the retrieval hook. Prefer few called keys, one per decision
cluster. Keep always keys near-empty. Anti-patterns: duplicating a
facts.md heading body-for-body, values over 300 chars, pcjr_ prefix,
writing before approval, mixing memory tags with prose in one message.
## 2026-08-26 · s4_decode_spec_locked · decision

S4 decode spec locked: sample-based half-cell decoder, KBDNMI-verbatim
core (entry 93/94), targeting the Pi emitter's actual frame (pycjr.py
build_frame verified byte-consistent). Edge-gap classification is
retired as a decode primitive: the 0→1 inter-bit gap (157us) fuses
below the pinned (170,175]us AGC fuse band, so the edge sequence is
structurally lossy. The intra-bit mid-cell biphase transition survives
every merge and is the decode axis.

Locked parameters:
- 5× majority per half-cell (stock-verbatim, entry 93)
- CH0 latched timing, 220us half-cell grid (2.38636 MHz empirical)
- start: burst-first, 310us post-burst wait (entry 93/94)
- 8 data LSB-first + odd parity; biphase per entry 94
- stop bit omitted by Pi emitter; decoder never samples it
- 1× sampling retired for first build; 5× is the shipped config

Result map: [0]=status (0 ok / 1 parity / 2 phase / 3 timeout),
[2..]=scancode. BASIC prints char only.

## 2026-08-26 · start_phase_310_manual · manual-verified

Start bit is burst-first (logical-1 half) followed by a 310us silence
(entry 93/94). 310us is the precise manual value, not 1.5× (310/220 =
1.41× the half-cell). The extended silence is what makes the start bit
unique and pulls the first data-bit sample onto the nominal half-cell
center.

## 2026-08-26 · pi_stop_omission_source_verified · empirical

pycjr.py build_frame (lines 244-271) emits parity bit → 1500us frame
gap, no stop burst. Source-verified against repo. The 1500us gap IS the
stop period. Invisible to S4 decode because the stop bit is never
sampled (matches KBDNMI listing: parity → INT 48h, no 11th consume).

## 2026-08-26 · bare8_ceiling_revision · analysis

supersedes: 2026-08-25 · framing_only_2x · analysis

Bare-8 custom framing ceiling recalculated: 8×440us = 3.52ms CPU lock
+ 1.5ms frame gap (CPU free) ≈ 5.0-5.4ms wall/keypress → ~185-199
ch/s. Stock is 19.36ms/keypress (51.6/s). Gain ≈ 3.5-3.8×, not the
~2× committed in framing_only_2x. The earlier figure was a conservative
round from 60→120 emitter-throttle thinking; the 8×bit_time math
exposes the real ceiling. Bare-8 framing remains the S5 horizon, not
S4 scope.

## 2026-08-26 · s4_sampler_spacing_open · open item

Entry 93 says "samples each half-bit-sample 5 times" but does not
state the intra-sample spacing. The cadence lives in the KBDNMI listing
(entries 334-346), not the prose. At S4 code emission: retrieve-before-
emit to pin it. Travels as `; VERIFY: intra-sample spacing against
KBDNMI listing`. Non-blocking for the spec lock.
## 2026-08-26 · s4a_hardware_pass · empirical

S4A (frame-sync + first half-cell sampler, 112B) passed on hardware:
st=3, half=1 on Pi 'h' (0x23; LSB-first first data bit = 1, so half=1
is the predicted value, stronger than the contract's "0|1"). Keyboard
alive. Bridge, selfloc, NMI mask/restore, finite arm, rising+trailing
edge sync, 5x majority, and end-quiet wait verified together in one
run. Timeout path (no stimulus) st=0 clean on the v1 variant.

## 2026-08-26 · s4a_midframe_return_defect · empirical

S4A v1 (139B) returned to BASIC immediately after the first half-cell
sample, restoring NMI while the rest of the make frame was still
arriving. KBDNMI deserialized the frame tail as a garbage scan code ->
screen line corruption + keyboard softlock. Cold power-cycle recovered.
Fix (v2): end-quiet wait polls PC6 for 400 consecutive quiet samples,
any burst resets the count, before NMI is restored. The wait completes
in the post-keypress silence, masking the entire press including the
break frame - BIOS never buffers the key. Desirable for S4B.

## 2026-08-26 · s4a_loop_timing_substitution · decision

S4A uses LOOP-constant delays (CX=90 start-phase, CX=190h end-quiet)
instead of the CH0-latched grid the S4 spec called for. CH0 word-imm
CMP (81 /7 iw) did not fit the 128-byte code ceiling and is also a
debug_asm decode bug. LOOP timing is deterministic on the 8088; the
risk is calibration accuracy, not drift. S4A passes with these
constants for one h run. S4B decision pending: LOOP vs extending
debug_asm for CH0. Scopes only S4A; the locked S4 spec is unchanged
for later stages unless the user locks a revision.

## 2026-08-26 · code_region_128_ceiling · analysis

Machine code invoked via CALL O must end at offset <= 128 or it
overlaps the result region (BASIC PEEKs at O+128). S4A v2 is 112 bytes;
S4A v1's CH0 idiom was 139 bytes and overlapped. Hard constraint for
all future stages.

## 2026-08-26 · debug_asm_rel8_branch_gate · decision

debug_asm rel8 returns the displacement via next_ip semantics; branch
validates (at,target) pairs against decoded displacements. Emission
gate order is selfloc -> rel8/branch -> decode. Hand-rolled rel8 is a
process violation; three S4A drafts with hand-rolled displacements
failed decode and were rejected before reaching hardware. This closes
the ch0cal_cmp38_ungated-class gap: every new stage now runs the full
per-branch gate.
## 2026-08-26 · pjasm_v6_table_driven · decision

pjasm = refs/pcjrasm.py, encode-only. One instruction table drives
five encoder kinds (fixed/reg16/imm8/rel/modrm+grp); no per-opcode
branches. Decoder deliberately lives in refs/pcjr_asm_debug.py, not
here. IRPING assembles byte-exact, 61 bytes.

## 2026-08-26 · grp1_81_pjasm_encode · decision

81 /7 iw is two pjasm rows: (cmp,rm,imm) and (cmp,r16,imm). Encode
verified byte-exact. debug_asm decode still FAILs on 81 (P1 fail-fast,
no decode row). S4B CH0 grid unblocked on encode side only.

## 2026-08-26 · modrm_bp_irregularity · analysis

mod=0 rm=6 means disp16, not [bp]; [bp] is forced to mod=1 disp8=0;
LEA bp,[bp+disp] must always emit mod=2 disp16. The size=60 defect was
the generic encoder shrinking LEA to mod=1. Encoded as LEA16 special.

## 2026-08-26 · pjasm_debug_integration · decision

refs/test_pjasm_integration.py proves the local boundary: pjasm output
-> debug_asm decode/branch_checks/check. 9/9. No MCP, no anchors, no
hardware.
## 2026-08-26 · debug_asm_v53_81_decode · decision
supersedes: 2026-08-26 · grp1_81_pjasm_encode · decision

`debug_asm` v5.3 adds `81 /7 iw` decode to the verified subset.
`cmp r/m16,imm16` decodes for both memory and register forms:
`81 7E 00 DC 00` -> `cmp [bp+0x00],0x00DC`, `81 F8 DC 00` ->
`cmp ax,0x00DC`. Unsupported group /N still halts decode (P1
fail-fast). The gate decode-fail fixture `gd` switches from `81` to
`63` so it still exercises the fail path after `81` became decodable.
Selftest ALL_PASS True (MCP-verified). This closes the S4B CH0-grid
gap: the `81 /7 iw` compare required for the 220us CH0 grid now
passes the full emission gate.

## 2026-08-26 · pjasm_mcp_tool · decision

`pcjr-tools` now exposes a fourth tool, `pjasm`, with
`command=assemble|selftest`. It imports `refs/pcjrasm.py` as `PJASM`
and keeps the encode-only boundary: `assemble` returns
`size`, `budget_left`, `hex`, and `data_block`; `selftest` runs Stage
A/B/D + IRPING byte-exact (57/57 ALL_PASS True, MCP-verified).
Decoder stays in `refs/pcjr_asm_debug.py` via `debug_asm`. The MCP
server imports `pcjrasm.py` from `PCJR_REF_DIR`, so the file must
ship alongside the other refs.
## 2026-08-26 · s4b1_raised_ceiling · decision

Machine-code ceiling raised from 128 to 180 bytes. Result region moves
from O+128 to O+180; selfloc LEA displacement becomes 174 (0xAE) because
`lea bp,[bp+174]` = entry+180. BASIC PEEKs at `VARPTR(A(0))+180..187`.
Verified via debug_asm selfloc (base=180 -> disp 174, 8D AE AE 00) and
hardware stage-1 sentinel pass. Stage code must end at offset <= 180.

## 2026-08-26 · ch0_down_counter · empirical

8253 CH0 counts DOWN. Elapsed between a latching read at time A and a
later latching read at time B is `A - B`, positive. Three runs measured
the start-burst envelope high as 526, 578, and 600 counts (220.4, 242.2,
251.4 us). Latch path per CH0CAL: `mov al,0 / out 43h,al / in al,40h` (lo)
`/ in al,40h` (hi). Never bare IN on a counter port.

## 2026-08-26 · s4b1_stage3b_boundary · empirical

S4B1_ST3B (180B instrumented probe) passed hardware clean: st=3,
rise=0xC330, trail=0xC0D8, burst=0x258 (600 counts = 251.4us), half=0,
keyboard intact. Fixed 740-count (0x2E4 = 310us) anchor from the start
burst trailing edge samples the start-silence/bit0 boundary and
flip-flops: S4A (LOOP CX=90, same nominal offset) returned half=1 for
'h', stage3b (CH0 anchor) returned half=0. Run-to-run envelope variance
(~30us) moves the sample point across the boundary. Fixed grid retired
as a decode primitive.

## 2026-08-26 · fixed_ch0_grid_retired · decision

S4B's locked CH0 fixed-grid decode approach is retired. The AGC envelope
stretches the nominal 62us start burst to ~220-250us with ~30us run
variance, so no fixed timing offset from the start burst reaches bit0's
center reliably. Next decode attempt must be edge-driven: detect bit0's
own rising edge and sample relative to that edge, per bit.

## 2026-08-26 · pjasm_operand_rules · analysis

pjasm (refs/pcjrasm.py) operand constraints observed this session:
rejects `mov byte [bp+n],imm` (use load/store pairs), rejects `jb`
(use `jc`), rejects `out dx,al` (use `out imm,al`), rejects trailing-h
literals `0AAh` (use `0xAA` or decimal), rejects `in al,0A0h` written as
`0A0h` literal (use `0xA0`), enforces rel8 range -128..127 (use a
two-hop jmp for distant targets). `81 /7 iw` (cmp r/m16,imm16) encodes
and decodes correctly.
## 2026-08-27 · dec1_st1_hw_pass · empirical

DEC1_ST1 two-edge span probe passed hardware 2/2. Run 1: flag=2,
r0/r1 = 0xCDD0:0xCA54, span 0x037C = 892 counts = 373.8 us. Run 2:
flag=2, r0/r1 = 0xBB46:0xB7C8, span 0x037E = 894 counts = 374.6 us.
Keyboard intact both runs. Repeatability ~2 counts (~0.84 us), matching
the recorded short-term H/L repeatability floor. loaded-106 gate
observed on both runs. Anchored.

## 2026-08-27 · dec1_first_edge_bit0_inference · analysis

DEC1_ST1 span 892/894 counts matches the ENVSHAPE26 bit0 cell
(H 550 + L 332 = 882 counts) within the recorded run-to-run envelope
variance. The start burst (~220-251 us stretched per S4B1_ST3B) was
swallowed by the arming window, so DEC1's first detected rising edge
is bit0, not the start bit. The measured span is the bit0->bit1
rising-edge cell. Inference, not proven: a three-latch variant or an
explicit pre-wait would pin edge identity.

## 2026-08-27 · pjasm_bracket_spacing · analysis

pjasm rejects spaces inside memory operands: `lea bp,[bp + 122]` fails
with `unsupported r/m operand`, while `lea bp,[bp+122]` assembles.
Extends pjasm_operand_rules (2026-08-26), which covered literal forms
and opcode names but not bracket spacing.
## 2026-08-27 · dec1_st2a_pc0_latch · empirical

DEC1_ST2A passed hardware 1/1: PC0 (`62h` bit 0, manual-verified
"Keyboard Latched") is readable through the polling bridge. Arming =
mask NMI (`OUT A0h,00h`), clear latch (dummy `IN A0h`), finite arm on
PC0. At capture, PC6 read `40h` (HIGH), sanity-confirming the latch
corresponds to a keyboard-data rising edge. Keyboard intact after
restore `80h`. loaded-57 gate observed.

## 2026-08-27 · dec1_st2b_trimodal_span · empirical

DEC1_ST2B (single-poll start-burst trailing edge via CH0) produced 8
stimulus spans in 3 modes: 334 ct (140 us, 1x), 520 ct (218 us, 2x),
572/574 ct (240 us, 5x). No-stimulus control clean (`status=0`),
ruling out Enter-tail contamination. CH0 is a down counter; span =
t0 - t1 (mod 65536). The earlier first-pass wrap analysis was wrong and
is retracted. The 240 us mode matches the known stretched start-burst
envelope (S4B1_ST3B 220-251 us); 140/218 are sub-envelope, consistent
with single-poll detection latching brief LOW ripple excursions inside
the envelope HIGH.

## 2026-08-27 · dec1_st2b_single_poll_ripple · analysis

Root cause of the ST2B trimodal span: single-poll "wait first falling
edge" has no confirmation step. KBDNMI (BIOS entry 338) uses
single-poll for the candidate edge, then requires 4 consecutive LOW
samples (`MOV CX,4`) before trusting it; any bounce back HIGH ->
sync error, frame discarded. ST2B omitted that confirmation and
therefore latched ripple dips (~22 us gap between 240 and 218 modes).
Fix: port the 4x-consecutive-LOW confirmation before trusting the
trailing edge.

## 2026-08-27 · pjasm_missing_r8_shapes · decision

pjasm v6.0 (refs/pcjrasm.py) table is narrower than the stated
pjasm_boundary implied. Missing shapes needed for a 1:1 KBDNMI-core
port: `test r8,imm`, `xor r8,r8`, `shr r8,1`, `inc r8`, `dec r8`,
`or r8,r8`, `xchg ah,al`, `jnb`. A faithful KBDNMI core (5x majority
halves, opposite-halves, odd parity via r8 bit ops) is not expressible
in pjasm today. Decision (user): extend pjasm with the missing r8
shapes; those opcodes are known to run on this hardware. Next session =
pjasm extension, then ST2C KBDNMI-core on CH0.
## 2026-08-27 · pjasm_r8_extension · decision
pjasm v6.1 adds eight KBDNMI-core r8 shapes: test r8,imm (F6 /0 ib,
register-only), xor r8,r8 (32 /r), shr r8,1 (D0 /5 ib, imm=1 only),
inc r8 (FE /0), dec r8 (FE /1), or r8,r8 (0A /r), xchg r8,r8
(86 /r), jnb/jnc (73 rel8). Byte-matched to the KBDNMI listing where
observable: xor ah,ah = 32E4, or bh,al = 0AF8, xchg ah,al = 86E0.
Group ops reject memory operands at table lookup; shr rejects imm != 1.
supersedes: pjasm_missing_r8_shapes

## 2026-08-27 · pjasm_selftest_merge · decision
ASM.selftest() is the only entry point the pcjr-tools MCP handler
calls. Every stage gate must live inside selftest()'s return dict.
A Stage E placed in a separate function wired only into main() is
invisible to the MCP route (drift discovered and fixed this session).
## 2026-08-28 · jr_api_refactor · decision
jr core logic extracted to jr.py: build, lint, verify, golden, dis, data, parse pure functions; JrError with exit_code; CLI wrapper thin; all side effects limited to subprocess and cache. test_jr.py passes all fixtures.

## 2026-08-28 · jr_mcp_integration · decision

MCP server imports jr.py directly (no subprocess). Smoke-tested via MCP: jr data, lint, parse, golden, lint on S4B1_ST2 anchor; all pass.

## 2026-08-28 · jr_mcp_docstring · decision

jr tool docstring reworked with bridge contract, defaults, output shapes, error format, workflow. Top-level merged docstring covers search_ref, grep_repo, jr.

## 2026-08-28 · jr_build_atomicity · decision

build CLI no longer deletes existing outputs on failure; writes only after lint passes.

## 2026-08-28 · jr_parse_comment_sentinel · decision

parse_bas_content now tolerates trailing comments after -1 sentinel; negative result args raise usage error.
## 2026-08-28 · jr_mcp_pipeline · decision

`jr` is now the single byte-pipeline tool registered on `pcjr-tools`
(server v8). `debug_asm` and `pjasm` are retired and not registered.
Seven commands: build, lint, verify, golden, dis, data, parse. Backing:
`refs/jr-tools/jr.py`; UASM assembles, NDISASM disassembles, both on
PATH. Inputs are inline-first: `asm_text` / `bin_hex` / `bas_text`
replace `src` / `binfile` / `bas` for development; file inputs only for
persistence. Construction gate is: `jr build` (UASM, at target stage) ->
`jr dis` (NDISASM review) -> `jr lint` (named invariants). Never
hand-roll bytes. References: `docs/jr_tool_spec.md`,
`refs/jr-tools/jr_rules.json`.

supersedes:

- pjasm_mcp_tool
- pjasm_r8_extension
- pjasm_selftest_merge
- pjasm_bracket_spacing
- pjasm_operand_rules
- pjasm_missing_r8_shapes

## 2026-08-28 · jr_mcp_inline_surface · empirical

Verified live against `pcjr-tools` (2026-08-28):

- `jr dis` with `bin_hex` "0E1F555DCB" returns NDISASM text
(push cs / pop ds / push bp / pop bp / retf).
- `jr build` with `asm_text` + `stage:1` returns status pass,
`bin_hex` 0E1F555DCB, `data_block`, and a float16-safe generated
`bas_source` (auto-sized `DIM`, `256!` multipliers).
- Omitting the UASM segment wrapper raises A2082 "Must be in segment
block". Canonical skeleton = `docs/jr_tool_spec.md` section 3.3
(option casemap:none / option segment:use16 / code segment ... code
ends / org 0).
- `jr build` defaults to `stage=6`; a bare stage-1 stub fails exit 4 on
the selfloc rule (min_stage 2). Pass `stage=1` explicitly for early
stages.
- Lint thresholds read from `jr_rules.json`: entry / retf-count /
epilogue / no-int21h (1), selfloc (2), budget (3), latch-read (4),
nmi-mask / nmi-restore (5). warn rules block only under `strict=true`.
## 2026-08-28 · ch1_clock_clean_12th · analysis

14.31818/12 = 1.19318 MHz. The listing's 526-tick half-cell constant
resolves to 526/1.19318 = 440.8 us, matching the 440 us half-cell
exactly. Therefore 544 ticks = 456.1 us, and the listing comment
"544 = 310 us" is wrong (authoring/OCR slip). "310 us" is the emitter's
start_silence duration, a distinct quantity from KBDNMI's
post-trailing-edge wait. The /12 clean divisor is the tiebreaker.
supersedes: kbdnmi_comment_conflicts

## 2026-08-28 · ch1_544_verbatim_bitsamp · empirical

BITSAMP CH1-verbatim: NMI masked, KBDNMI I30 timing copied (mov al,40h
/ out 43h / in 41h / in 41h), wait target 544 ticks, bit0 first-half
5x majority. h (scancode 23h, bit0=1 biphase HIGH-first) -> bit=1 3/3,
keyboard intact. ones=3 (2 of 5 polls LOW) - correct decode, thin margin.
trail-sample delta 658/658/660 ticks (551.8/553.5 us), deterministic
to 1 tick. Failed disproof of the CH0 clock-conversion confound.
Not anchored: margin too thin, overshoot unexplained.

## 2026-08-28 · wait_overshoot_ch1_anomaly · open item

CH1-verbatim wait loop overshoots the 544-tick target by 114-116 ticks
(~96 us). CH0 build overshot 77 CH0 counts (~32 us). The CH1 loop is
shorter (mov cx,di vs push di/pop cx) yet overshoots more - backwards
from cycle-count prediction, unexplained. This is why ones=3 not 5.
Blocks robust decode until understood.

## 2026-08-28 · ch1_masked_read_safe · empirical

CH1 latch/read (mov al,40h / out 43h / in 41h / in 41h) with NMI masked
(OUT A0h,00h) left keyboard intact 3/3. Consistent with timer1_hazard
(active NMI is the risk); masking isolates the probe. Does not supersede.

## 2026-08-28 · receiver_chain_waveform_model · analysis

Black-box spitball: AGC = slow gain memory (release 220-440 us,
H-compression under load). Demod = min-pulse one-shot (flat H=230 us
for W<=125 us). PC6 trailing edge = one-shot expiry, not carrier-off
plus decay. t_r (burst start -> PC6 rise) unmeasured, suspected
state-dependent. No internal test points; manual is block-diagram only.
Consistency check only, not evidence.
## 2026-08-29 · hardware_map · manual-verified

Moved from platform skill v5 Rule 6. Authoritative register map for the
PCjr 4860/4861.

| Register | Address | Purpose | Status |
|---|---|---|---|
| PORT_A | 60h | 8255 Port A output | Confirmed + manual-verified |
| PORT_B | 61h | 8255 Port B output | Confirmed + manual-verified |
| PORT_C | 62h | 8255 Port C input | Confirmed + hardware-verified |
| CMD_PORT | 63h | 8255 control | Confirmed |
| TIMER0 | 40h | 8253 CH0, input 2.38636 MHz (14.31818/6 = CPU/2) | Confirmed; clock empirical |
| TIMER1 | 41h | 8253 CH1, keyboard de-serialize, 1.1925 MHz when A0h D5=0 | manual-verified (entries 31/34) |
| TIMER2 | 42h | 8253 CH2, sound source, IR test 40 kHz when A0h D6=1 | manual-verified (entries 31/34) |
| TIM_CTL | 43h | 8253 control | Confirmed |
| NMI_PORT | A0h | NMI mask / control | Confirmed + manual-verified |
| INTA00 | 20h | 8259 PIC | Confirmed |
| INTA01 | 21h | 8259 PIC | Confirmed |

8253 decode: A6=1, A1/A0 select 40h-43h. Manual `Hex Range` print
(40-47) is a formatting conflict; 44h-47h alias unverified.
`; VERIFY: 44h-47h decode against PCjr Technical Reference`.

Latch commands via 43h: CH0=00h, CH1=40h,
## 2026-08-29 · document_pipeline_design · decision
PCjr manual pipeline (pcjr_manual_pipeline.py) merges page segmentation, continuous page axes, and figure-region segmentation. Manual page ID is the canonical key for all pipeline records.

## 2026-08-29 · page_axes_contract · decision
Each page emits three continuous axes: toc_frac, listing_frac, figureish. No hard page-type enum; downstream thresholds its own cutoffs.

## 2026-08-29 · figure_region_segmentation · decision
Figure regions seed from language-model score <= -9.0 only. The structural multiplier was removed after it erased schematic part numbers. listing pages with listing_frac >= 0.30 are skipped. Regions require length >= 3 and low-line fraction >= 0.6.

## 2026-08-29 · listing_axis_false_positive_video_pages · open item
2-61 and 2-62 (Video Subsystem diagrams) report listing_frac ~0.4 despite being figures, not BIOS listings. is_listing_line matches some scan-line labels. Axis label is wrong for downstream though region suppression is unaffected.

## 2026-08-29 · segmented_output_default_gap · open item
pipeline run writes pages.jsonl by default, but marked page output still requires --seg-out. Decision pending: default pages.seg.txt beside pages.jsonl with --no-seg to suppress.

## 2026-08-29 · figureish_label_dominant_connector_caveat · analysis
Label-dominant connector layout pages have figureish near 0 because LM rates English labels as prose. Dense line art is detected; sparse label layouts are not. Known limitation, not a defect.
## 2026-08-29 · mcp_tool_surface_v9 · decision
search_ref gains grep mode (line-attributed hits; pages.jsonl joined as
meta). New tool bios_grep serves refs/ibm_pcjr-bios.lst. grep_repo modes
renamed by scope: facts, all, files, ls, read, facts_headings, stats,
roots. Stray path param dropped. jr unchanged.
supersedes: 2026-08-24 · grep_repo_grep_all

## 2026-08-29 · manual_port_spelling · empirical
Prose manual spells ports as bare hex: grep 'A0h' = 0 hits, grep 'A0'
~70 hits. Grep bare digits for register facts; do not include the h
suffix. Documented as a retrieval trap in the platform skills.

## 2026-08-29 · search_ref_peek_file_order · decision
search_ref peek indexes are strip-file order, not physical page order;
peek(1) = B-47. Accepted. peek is raw access only; locate content via
query/grep.

## 2026-08-29 · bios_lst_header_block · empirical
refs/ibm_pcjr-bios.lst begins with an ASCII IBM header of ~25 lines;
listing labels start past line 25. bios_grep grep/peek cover the whole
file including the header, which can match header-text queries.

## 2026-08-29 · facts_headings_status_field3 · decision
facts_headings parse: date=field1, name=field2, status=field3; a fourth
and later field is provenance, preserved as extra[]. Fixes the
parts[-1] bug that mislabeled the status of 4+ field headings.

## 2026-08-29 · mcp_server_v9_backend_paths · decision
Server v9 loads refs/pcjr_technical_reference.txt via
tech_ref_sanitize.segment_pages (Appendix A excluded), joins
refs/pages.jsonl as metadata only, serves refs/ibm_pcjr-bios.lst via
BiosStore. Archived pcjr_ref_tool.py / pcjr_repo_grep.py logic was
re-derived into fresh modules, never imported.

## 2026-08-29 · bds_memory_critical_only · policy
BDS memory writes are restricted to critical, ultra-relevant facts
only. Broad memories get injected far too often and accelerate
hallucination. Prefer facts.md / sessions/ as the ledger; BDS memory is
a hot pointer at most.
refines: memory_batch_spec

## 2026-08-29 · facts_heading_hygiene · open item
facts.md contains three bare headings (skill_create_semantics,
handoff_template, session_anchor_policy), one status outside the enum
(listing-verified), and compound statuses (empirical + analysis,
manual-verified + empirical). Normalize headings or extend the enum.
## 2026-08-30 · bios_lst_format · manual-verified

The flat BIOS listing `refs/ibm_pcjr-bios.lst` (served by `bios_grep`)
is a MASM-style `.LST`, OCR'd by GloriousCow 2026 from Technical
Reference Appendix A. 11511 lines. Column layout by line type:

- Header block: lines 1-7 banner (line 6 marks the ASM source column);
  lines 9-25 A-3 page banner + EQUATES header. Content starts line 26.
- EQU: `= VVVV ... LABEL EQU value ; comment`. The `= VVVV` column is
  the equate VALUE (60H -> 0060), not an offset.
- Directive (SEGMENT/ORG/LABEL/PROC/ENDP): 4-hex offset in col 0,
  blank opcode-bytes column, directive right-aligned. Routines open
  `PROC NEAR` and close `ENDP` — NEAR even for BIOS entries (farness
  via the IVT far pointer, not a FAR proc).
- Code: `OOOO BB BB ... [LABEL] MNEM OPERANDS ; comment`. Offset,
  opcode bytes (2 hex each), optional label, mnemonic, operands.
- Segment override appears IN the offset column: `06DC 26: C7 ...`.
- Local labels are numeric-colon in the label column (`L13:`, `D3:`).
- Data: `DW OFFSET label` / `DB` carry bytes in the opcode column.
- `R` suffix on an operand = relocatable (symbol not resolved).
- Comment-only lines: full-width `;`, no offset/bytes.

Unverified: whether a fully-resolved operand ever appears WITHOUT the
`R` suffix (all sampled memory operands were relocatable). Addresses
are relative to segment ABS0 (SEGMENT AT 0) and DATA_AREA at 0400.

## 2026-08-30 · bios_grep_whitespace_tolerance · manual-verified

`refs/pcjr_bios.py::BiosStore.grep` now collapses whitespace runs to
single spaces in both needle and haystack before matching, via
`_collapse_ws = " ".join((s or "").split())`. Matching uses the
collapsed form; the returned `text` field keeps the original
column-aligned line.

Trap that motivated it: grep was whitespace-sensitive. Single-space
`"PROC NEAR"` returned 0 hits (truncated=false, a false no-match)
against the listing's `PROC    NEAR` (four spaces). Multi-word
single-space greps false-negatived. A capped result was never a true
no-match; this one was a true no-match and still wrong.

Live probe after the change: `"PROC NEAR"` returns 119 total_hits
(first hits lines 1096 `BITS_ON_OFF PROC NEAR`, 1480 `Q35 PROC NEAR`).
`(s or "")` restores the pre-existing null-query contract (`query=None`
returns `{"error": "empty pattern"}`, not an AttributeError).

Regression tests added to `test_greps.py`:
`test_bios_grep_whitespace_collapse`, `test_bios_grep_preserves_column_spacing`,
`test_bios_grep_proc_near_corpus`. Module docstring line 13 updated.

## 2026-08-30 · irping2_transport_regression · decision

IRPING is retired. It never had anchor files in `docs/anchors/`; its
61-byte DATA existed only in history (byte-exact per pjasm selftest,
57/57 ALL_PASS). The `session_anchor_policy` claim that IRPING is a
"known anchor" was stale.

Replacement: IRPING2_MIN, a minimal transport-only both-edge detector
for port 62h bit 6. Mask NMI (OUT A0h,00h), dummy IN AL,0A0h to clear
the latch, finite poll (CX=0FFFFh), set saw_high (bit0) on bit set /
saw_low (bit1) on bit clear, early-exit when result byte = 3, restore
NMI (OUT A0h,80h), RETF. Result byte at O+128; pass value 3. 56 bytes.

`jr build stage=5` passed (errors [], warnings []); `jr dis` reviewed
byte-exact. All invariants confirmed: entry 0E1F55, selfloc +0x7A
(=122, no +128 trap), exactly one CB, no CD21/CF/E661, NMI masked
before 62h poll, NMI restored before RETF. This is emission-gate pass
ONLY — not hardware-verified. IRPING2 earns anchor files in the
session where the PCjr returns result_byte=3.

`ch0cal_primary_regression` architecture stands: CH0CAL is still the
functional primary; the named transport-only regression is now
IRPING2_MIN instead of IRPING.

supersedes: session_anchor_policy

## 2026-08-30 · jr_tool_spec_fixture_stale · open item

`docs/jr_tool_spec.md` section 8 still names "IRPING stage-5 DATA
(61 bytes)" as a normative fixture. IRPING is retired and its DATA is
not in the repo. Update the fixture entry to IRPING2_MIN after (and
only after) IRPING2_MIN passes hardware. Open until then.
## 2026-08-30 · irping2_min_hw_pass · empirical

IRPING2_MIN hardware pass: `loaded 56 bytes`, `RETURNED OK`,
`status= 3`, keyboard intact. Transport sanity confirmed (both
polarities of 62h bit 6 sampled in one finite masked poll). The
generic loader's rising/falling fields read 0 because the probe
writes only O+128; they are meaningless on this probe and are
dropped from the anchor runner.

## 2026-08-30 · irping2_anchor · empirical

IRPING2 anchored: `docs/anchors/IRPING2.BAS` (custom runner, no
rising/falling lines) + `docs/anchors/IRPING2.ASM`. DATA block is
56 bytes, byte-exact from `jr build stage=5`; runner-only edit, no
re-emission of bytes. This is the new transport regression probe,
replacing IRPING.

## 2026-08-30 · irping_regression_superseded · decision

`supersedes: irping_regression (platform skill Rule 5)`

IRPING (61 bytes) retired as the transport regression. Replacement
is IRPING2_MIN/IRPING2 (56 bytes, status=3 pass). Pending repo
edits by user: (1) platform skill Rule 5 wording IRPING →
IRPING2, re-import per `skill_create_semantics`; (2)
`docs/jr_tool_spec.md` §8 fixture name IRPING → IRPING2.

## 2026-08-30 · i30_wait_loop_pll · analysis

Manual-verified from `bios_grep` (listing lines 3410–3448). The I30
wait loop is a phase-locked loop, not a dumb countdown: on exit
`SUB CX,DX` then `ADD DI,CX` carries the overshoot forward into the
next wait. Overshoot does NOT accumulate across half-bits. The
5-sample majority window (`CMP AH,3`) starts AT the 544-tick point
and runs forward ~38 µs; it is not centered on the midpoint. Latch
command is `40h` = latch CH1, two `IN AL,41h` reads, two NOPs.

## 2026-08-30 · overshoot_loop_cost_ruled_out · analysis

`supersedes: wait_overshoot_ch1_anomaly`

Loop-cost hypothesis disproven by arithmetic from the listing body.
Wait-loop iteration is ~70 cycles ≈ 17.5 CH1 ticks; the observed
overshoot is 114–116 ticks ≈ 6.5× loop granularity. Loop cost
cannot produce it. Because the I30 PLL carries overshoot forward,
the disturbance is one-time on bit0's first-half sample only —
consistent with ones=3 while h→bit=1 still decodes 3/3. The
overshoot is a systematic (±1 tick) reference error, not loop cost
and not noise.

## 2026-08-30 · sync_reference_phase_hypothesis · open item

H: the clone seeds DI (the reference clock capture) ~114 CH1 ticks
(~95.5 µs) later than KBDNMI's reference edge from the I6
carrier-off sync, so the 544-tick first wait starts late by a fixed
frame-feature amount. Later bits self-heal via the I30 PLL
carry-forward.

F: the 114–116 tick overshoot is NOT accounted for by a ~95.5 µs
feature (start burst / gap / carrier-off geometry) in
`ir_protocol_frozen` or the listing.

Continuation order (next session): (1) `bios_grep` peek lines
0F80–0FB9 to locate KBDNMI's clock capture relative to the I6 sync;
(2) `grep_repo` `ir_protocol_frozen` for burst/gap geometry. No
hardware run until one static retrieval matches. IRPING2 is the
transport regression gate. Do not build the 5x sampler until the
edge is shown stable.
## 2026-08-30 · kbdnmi_overshoot_hardware_intrinsic · empirical

CH1 wait-loop overshoot of the 544-tick target is 114-116 ticks (658/660
delta) across three independent entry strategies: no-CLI re-arm, CLI
frame-gap sync, and CLI one-shot. Within-build jitter is 1-2 ticks;
cross-build spread is 10 ticks (~8 us). Interrupts, entry phase, and loop
code are all excluded. The residual lives in the CH1 latch/read idiom or
an unverified CH1 effective rate, neither yet measured.
supersedes: wait_overshoot_ch1_anomaly

## 2026-08-30 · kbdnmi_entry_phase_variance · empirical

The I6 trailing-edge verify sees a ripple whose width depends on arm
strategy, proving the demod envelope state at I3 differs with AGC history.
FRAMEGAP re-arm (scans data LOWs before accepting frame gap): ripple 3-4,
bwidth 551 us - silence merged HIGH. One-shot (first LOW->HIGH): ripple 1-2,
bwidth 462 us - a data edge. Same Pi frame, different entry state.

## 2026-08-30 · oneshot_armed_mid_frame · empirical

One-shot build latched 552 CH1 ticks (462.6 us) from rise to I3 exit,
equal to one full bit (440 us) plus ~22 us. It armed on a data edge,
not the start burst. ripples 1-2 on I6 corroborate a false trailing
edge. One-shot without a frame boundary is insufficient.

## 2026-08-30 · gap_gated_low_first_pending · open item

Gap-gated one-shot built (300 bytes, R=320): wait LOW first, measure
LOW duration, accept as frame gap only if >= 1400 ticks (1173 us), then
treat next rise as start burst, no re-scan. Fixes FRAMEGAP's high-first
ordering bug. Awaiting hardware run to confirm gap ~1790 and bwidth in
the stretched-burst band.
## 2026-08-30 · int02_write_quiescent_reopen · analysis

The 2026-08-25 decision `int02_vector_write_ub` rests on ladder stages 5/5c
whose listings are absent from the repo, and on the circular claim that
stage 5c "never held a bogus vector" (no readback was performed; the write
was never verified byte-exact, IVT-ordered, or two-word). The full S1.ASM in
`sessions/2026-08-25_s1_nmi_intercept_sop.md` implements the write correctly:
`OUT A0h,00h` mask, offset word first (`A3 0800`), segment second (`A3 0A00`),
masked restore. S1 v1 failed on BP clobber (bridge defect, not the write); S1
v2 rebooted in the arming window and was never root-caused before the ladder
pivot. Mechanism candidate: torn-vector window between the two 16-bit stores,
or NMI live during a store — not the write act itself. Rule 7 stands
unmodified pending the `ivt_write_quiescent` disproof probe (readback-gated).
## 2026-08-30 · nmi_ptr_bios_word_only · manual-verified

bios_grep confirms NMI_PTR (ABS0 SEGMENT AT 0, label at 0008) is a WORD
label. Every write in the BIOS listing targets only the offset word via
C7 06 0008: 04D3=0F78 (POST init), 06B6=F815 (RAM-test temp handler D11),
06DC=0F78 (POST reset). The segment word at 000A is never written by the
BIOS. Contrast KEY62_PTR (0120), which does get its segment explicitly:
PUSH CS / POP AX / A3 0122. The BIOS treats NMI_PTR as a word, not a far
vector. Source: bios_grep lines 68, 1344, 1631, 1649.

## 2026-08-30 · stock_nmi_vector_empirical · empirical

READONLY probe (pure BASIC DEF SEG 0 + PEEK(8..11); no machine code
required) on a fresh boot reads 0000:0008 = 3960 (0F78), 0000:000A =
61440 (F000). Stock INT 02h vector at Cartridge BASIC runtime is
F000:0F78 on a clean boot, matching the BIOS POST write at 04D3. The
segment half is populated despite no BIOS write to 000A.

## 2026-08-30 · ivt_write_quiescent_sameboot · empirical

Same-boot probe (BASIC pre-read + IVTWR asm write probe + BASIC
post-read) on a fresh boot: pre = wr-readback = post = 3960:61440
(F000:0F78), RETURNED OK, keyboard fine. Clean run per contract
ivt_write_quiescent_sameboot; falsifier NOT observed. Verdict:
failed_to_disprove — the hypothesis survived one disproof attempt.
Not proven, not promoted to empirical fact. One clean
counter-observation to the premise of the 2026-08-25
int02_vector_write_ub decision, which remains unmodified.

## 2026-08-30 · ivt_zero_vector_session_residue · conflict

Earlier IVTWR run (same DATA bytes, non-fresh boot) read 0000:0000
from 0008/000A with keyboard fine. Later READONLY and same-boot probes
on fresh boots read F000:0F78. Two observations conflict. Leading
explanation (unverified): session residue — the machine had been up
through the day's KBDNMI experiments, the vector was already 0000:0000
before IVTWR ran, so its "no-op restore" was in fact a real write.
Untested; not promoted.

## 2026-08-30 · nmi_chain_detail_pointer_drift · open item

Rule 7 and the project doc point to facts.md heading nmi_chain_detail.
facts_headings (196 entries) has no such heading; hardware_map (line
1318) exists. Pointer drift — the NMI dispatch chain detail is not
stored under the name the rules reference. Needs either a facts.md
entry or a Rule 7 pointer correction.
## 2026-08-30 · ivt_write_safe_active_nmi · empirical

IVTWR-LOOP: 1024× byte-exact write/readback of saved vector (3960:61440)
to 0000:0008/000A. Mode 0 (NMI masked) and mode 1 (NMI enabled, held-key
stimulus) both RETURNED OK, mismatch=0, final vector 3960:61440, keyboard
alive. Fresh boot each mode. Build: jr build stage 6, pass, no warnings.

## 2026-08-30 · ivtwr_torn_vector_race_disproved · empirical

H = "IVT write is harmless quiescent; fatal only under active keyboard
NMI (torn-vector race)." F = "Mode B completes with keyboard alive and
mismatch=0." F observed on clean run (mode A clean first). Verdict:
DISPROVED. Caveat: NMI arrival mid-write inferred from held-key traffic,
not measured directly.

## 2026-08-30 · int02_write_act_safe · decision

supersedes: 2026-08-25 · int02_vector_write_ub

The INT 02h IVT write act (0000:0008/000A) is safe on a fresh boot:
quiescent and active-NMI 1024× write/readback loops, mismatch=0, vector
intact, keyboard alive. The 2026-08-25 kill is attributed to the known
code defects (S1 DS=0 store bug writing 0000:0002/0000:0004; S1 v1 BP
violation) whose listings were unverified, not to the write act itself.
Custom INT 02h handler dispatch remains untested and is not pre-authorized
by this decision.
## 2026-08-31 · skill_int02_patch_pending · open item

`bds/10_skills/pcjr_cartridge_basic_asm.md` Rule 7 (line ~136) and
Rule 9 (line ~165) still carry the 2026-08-25 claim that writing the
INT 02h IVT kills the keyboard. Superseded by `int02_write_act_safe`.
Patch spec emitted 2026-08-31: replace with a pointer to
`int02_write_act_safe`; Rule 9 residual guardrail becomes "custom
INT 02h handler dispatch — untested, not pre-authorized." Apply, then
re-import per `skill_create_semantics`.

## 2026-08-31 · faq_s17_irping_stale · open item

`docs/FAQ.md` §17 ("When should I run IRPING?") still names the retired
IRPING transport probe. Update heading and body to IRPING2 now that
`irping_regression_superseded` is committed and IRPING2 is anchored
(`docs/anchors/IRPING2.BAS` / `IRPING2.ASM`). Not previously tracked.

## 2026-08-31 · byte_selftest_irping_golden_stale · open item

`bin/byte_selftest.sh` line 2 comment says "vs IRPING golden." IRPING
DATA is retired and absent from the repo. Decide whether to retire the
script (pjasm-era, likely dead after the `jr` transition) or update the
golden reference. Not previously tracked.
## 2026-08-31 · jr_handler_ruleset_added · decision

New `refs/jr-tools/jr_rules_handler.json` — NMI chain-handler lint class.
Entry `0E 1F 55` (push cs / pop ds / push bp), epilogue `5D 53 50 CB`
(pop bp / push bx / push ax / retf far-jump to KBDNMI), `retf-count == 1`,
no latch-read/nmi-mask/nmi-restore rules (observer touches no port).
Invoked as `jr build --rules refs/jr-tools/jr_rules_handler.json`.
Rationale: bridge class demands `5D CB` RETF-to-BASIC; chain handler
exits by far jump, not RETF. Distinct machine shape needs distinct rules.

## 2026-08-31 · jr_iret_ruleset_added · decision

New `refs/jr-tools/jr_rules_iret.json` — NMI IRET-handler lint class.
Entry `0E 1F 55`, `retf-count == 0` (no CB), exactly one `CF`
(iret-has-iret), epilogue `5D CF` (pop bp / iret), plus no-int21h,
no-speaker, selfloc R-6, budget. Invoked as
`jr build --rules refs/jr-tools/jr_rules_iret.json`.
Rationale: NMI entry pushes FLAGS/CS/IP; only IRET restores the frame.
RETF in an NMI handler is a corruption, not a return.

## 2026-08-31 · jr_retf_count_cb_false_positive · analysis

`retf-count` (scans for `CB`) false-positives on `8C CB` = `mov bx, cs`.
The register field for BX in the `MOV r16, Sreg` encoding is `CB` as a
data byte, not a RETF opcode. First hit 2026-08-31 in N1-A wrapper.
Workaround: `push cs / pop bx` (`0E 5B`) avoids the byte. Same class as
documented `no-iret`/`no-speaker` CF/E661 false positives; rule message
should warn about `8C CB` specifically. Open item: patch message text.

## 2026-08-31 · kbdnmi_ch1_latch_conflict · conflict

ROM BIOS KBDNMI at `0FAB` executes `OUT TIM_CTL,40h` then
`IN AL,TIMER+1` (latch + read CH1) while the NMI latch is still set —
the exact operation platform-skill Rule 6 names as the keyboard-killing
hard hazard. BIOS does this stock on every keystroke. Sources: BIOS
listing `0FAB..0FB9` (manual-verified) vs skill Rule 6 (policy claim).
The skill line is over-broad or context-dependent; do not cite it
against CH1 reads until resolved. Does not block N1 ladder (observer
touches neither A0h latch nor 41h).

## 2026-08-31 · basload_256_multiplier_drift · open item

`docs/anchors/BASLOAD.BAS` lines 170/180 use bare `256*peek(...)` under
`DEFINT A-Z`. Correct float16-safe idiom per jr-tool spec §5 is `256!`.
The drift only survives because observed segment high bytes are small.
Anchors used this session; not silently fixed. Decision needed: patch
BASLOAD.BAS or leave as historical anchor.

## 2026-08-31 · n1a_masked_write_pass · empirical

N1-A (112-byte self-restoring bridge) passed on a clean substrate after
the paste/environment fix: mask NMI → save 0000:0008 → write CS:0000 →
readback → verify offset+segment → restore → unmask → RETF. `verify=1`,
keyboard alive, IRPING2 green before and after. Second independent pass
of the INT 02h write act; consistent with `int02_write_act_safe`.
This decision has no supersede — it extends the write-act evidence,
it does not authorize custom dispatch.

## 2026-08-31 · nmi_custom_dispatch_hostile · analysis

Three custom-dispatch runs, three `no_result` outcomes, no clean pass:
- N1-B0: 18-byte self-loc IRET handler. Screen corruption, dead keyboard.
- N1-B1: 2-byte `E4 A0 CF` handler. Screen clean, keyboard dead.
- N1-B2: no-key control of N1-B1. Identical failure to N1-B1.

Reducing the handler to bare latch-clear+IRET did not clear the
keyboard death — defect is upstream of the handler body, in dispatch or
wrapper. Screen corruption DID clear when the self-loc body went away.
NOT a disproof: all three runs are contaminated (`no_result`). The
disproof question remains open. Boundary is sharp and recorded: masked
write act passes (N1-A); every unmasked-fire variant has failed.
Surviving hypothesis untested: frame completion by KBDNMI is mandatory,
so swallowing a key without chaining desyncs the receiver. See
sessions/2026-08-31_nmi_dispatch_ladder.md.
</BDS:create_file>
<BDS:create_file fileName="sessions/2026-08-31_nmi_dispatch_ladder.md">

```markdown
# Handoff — NMI custom-dispatch ladder (single scope)

Date: 2026-08-31
Scope: prove, by disproof, whether a custom INT 02h handler can safely fire on the PCjr.

## Verified this session

- Bridge ladder re-proven from clean substrate after paste/environment
  freeze: L0 alive, loader, CALL, selfloc (result=42), A0h round-trip (result=43).
- N1-A passed: masked INT 02h write/readback/restore, `verify=1`, keyboard alive, IRPING2 green before/after. Second empirical pass of the write act.
- Two new jr rulesets: `jr_rules_handler.json` (chain class), `jr_rules_iret.json` (IRET class). Both pasted, server restarted, builds passed.
- N1-B0/B1/B2 all `no_result`: see test_log. No clean dispatch pass.
- `jr build --stage 2 --rules jr_rules_iret.json` correctly proved selfloc R-6 on the corrected (CLI-dropped) handler.

## Open questions

- Is the N1-B keyboard death caused by (a) unserviced NMI frame desync, or (b) a wrapper defect independent of dispatch? N1-B2 no-key control failed identically to N1-B1 — does NOT cleanly isolate; need N1-B3 stock-vector control.
- Does background IR traffic exist even with no key pressed (idle/heartbeat/AGC edges)? Untested; would explain N1-B2 if true.
- Is frame completion by KBDNMI mandatory? Surviving hypothesis, untested. If true, chain-to-KBDNMI is the only viable custom path.
- Is `8C CB` (`mov bx,cs`) a `retf-count` false positive to patch in the rule message? (analysis recorded, message text not patched.)
- CH1 latch conflict: resolve skill Rule 6 against BIOS `0FAB` stock behavior.

## Loose ends

- `jr_rules_iret.json` has no class for the 2-byte bare `E4 A0 CF` handler used in N1-B1/B2; reviewed by dis only, flagged as process note, not gated.
- N1-B3 (stock-vector-live wrapper control) designed but NOT emitted — pending clean anchor report after the freeze.
- BASLOAD.BAS `256*` drift and `jr_retf_count_cb_false_positive` are open items recorded in facts.
- No anchors earned this session; no anchor files emitted.

## Suggested next scope

Cold power-cycle, re-run IRPING2 + N1-A to confirm clean machine. Then
N1-B3: same wrapper, skip install (keep stock KBDNMI vector live through
the delay), press a key. Splits wrapper-defect vs dispatch-defect in one
run. If N1-B3 survives, next is the chain-to-KBDNMI probe. If it fails,
bisect inside the wrapper.

## Ground truth

- docs/anchors/IRPING2.BAS / IRPING2.ASM — transport regression
- docs/anchors/CH0CAL.ASM / CH0CAL.bas — functional primary regression
- No new anchors this session.
## 2026-08-31 · es_clobber_bridge_contract · empirical

ES must be preserved across the Cartridge BASIC machine-code bridge.
Controlled A/B, this session:

- DI-based NMIPEEK without an ES save corrupted BASIC on every run —
  `bytes` corruption signature, keyboard alive but frozen on string
  operations (Enter/parse).
- The same routine with `PUSH ES` after self-location and `POP ES`
  before `RETF` passed cleanly on repeated runs: `returned ok`,
  `m1=42`, `saved=3960:61440` (stock KBDNMI `0F78:F000`), keyboard
  alive and echoed.

ES clobber explains the original N1-A crash signature and the
nondeterminism (byte-identical rebuild passed once, then corrupted —
timing, not bytes). This fact extends `basic_bp_preserve_contract` to
BP + ES; Rule 1 of the platform skill must be revised accordingly.

supersedes: basic_bp_preserve_contract

## 2026-08-31 · nmipeek_anchor_pass · empirical

NMIPEEK passed hardware: masked read of the INT 02h vector with ES
preserved and a DI-based result base. Observed `returned ok`,
`m1=42`, `saved=3960:61440` (`0F78:F000`), keyboard alive and echoed.
Ground truth: `docs/anchors/NMIPEEK.BAS` / `docs/anchors/NMIPEEK.ASM`.

## 2026-08-31 · bp_clobber_theory_falsified · empirical

Hypothesis "the N1-B/N1-A crash signature is caused by KBDNMI
clobbering BP while BP holds the result base" is disproved. A DI-based
variant (NMIPEEK, BP restored immediately after self-location, all
stores through DI) still produced the same bytes-corruption signature.
BP was not the killer; ES clobber is. See `es_clobber_bridge_contract`.

## 2026-08-31 · n1a_onepass_anomaly · open item

The original N1-A (112 bytes, no ES save) passed exactly once on
hardware, then corrupted on a byte-identical rebuild. Under the
ES-clobber contract it is expected to corrupt reliably; the single
clean pass is unexplained. Do not cite N1-A as ground truth until the
anomaly is resolved.
## 2026-08-31 · contract_a_bridge_frozen · decision

Bridge entry contract frozen as Contract A, implementing the Rule 1
revision instructed by `es_clobber_bridge_contract`:

- Entry: `PUSH CS` / `POP DS` / `PUSH BP` / `PUSH ES` — bytes `0E 1F 55 06`
- Epilogue: `POP ES` / `POP BP` / `RETF` — bytes `07 5D CB`
- `PUSH ES` lands immediately after `PUSH BP`; `POP ES` immediately before `POP BP`.
- Selected over Contract B (push-ES-at-first-use, as in NMIPEEK v1) for
  uniform, unconditional, trivially-lintable semantics.
- Consequence: `get_ip` moves from offset 6 to offset 7; selfloc
  displacement becomes `R - 7`, not `R - 6`.

## 2026-08-31 · jr_rules_json_truncation · analysis

`refs/jr-tools/jr_rules.json` was truncated on disk: the `nmi-restore`
rule lost its `config`, `message`, and `rationale`, and the file ended
mid-structure at line 107 (tab-indented `}` at 106, bare `}` at 107).
The MCP server rejected every build at char 3725 before UASM ran —
identical error across three distinct `asm_text` payloads, localizing
the defect to the ruleset, not the assembly. Cause: paste lost the
tail. Fix: re-emitted the file wholesale. Lesson: read back and verify
long JSON after any paste.

## 2026-08-31 · jr_selfloc_hardcoded_offset · analysis

`jr.py` selfloc computed `expected_disp = R - 6` with a hardcoded 6,
assuming the old 3-byte bridge entry. Contract A's 4-byte entry shifts
`get_ip` to offset 7, so the correct displacement is `R - 7`. The
checker rejected correct Contract A code (`lea bp,[bp+121]` — found_r
127 vs expected 122). Fix: derive the entry offset from the located
marker — `entry = idx + 3`, `expected_disp = R - entry`,
`found_r = entry + disp`. Contract-proof: passes under both 3-byte and
4-byte entries. Requires MCP restart (module import).

## 2026-08-31 · nmipeek2_built_unverified · open item

NMIPEEK2 (masked INT 02h vector read under Contract A) built and
lint-passed at stage 6: 46 bytes, 0 errors, 0 warnings. Entry
`0E 1F 55 06`, selfloc `lea bp,[bp+0x79]` (disp 121) giving result base
entry+128, epilogue `07 5D CB`. NOT hardware-passed; not ground truth;
no anchor files until it passes. Expected on a clean hardware run:
status=42 (marker), rising=3960 (KBDNMI offset), falling=61440 (KBDNMI
segment), keyboard alive; regression IRPING2.
## 2026-08-31 · nmidisp_dispatch_observed · empirical

NMIDISP Probe A: a custom INT 02h vector installed from the BASIC
bridge dispatched on a single real IR keystroke and returned clean.
Flag went 0 -> 1; BASIC printed the result line after the handler
(interpreter intact past the IRET); keyboard dead by design (stock
KBDNMI replaced, scancodes discarded); cursor still blinking (IF
restored, INT 08h timer IRQ alive). Control run with no keystroke
printed flag=0. IRPING2 status=3 passed before each run. First clean
custom INT 02h dispatch in project history; the three prior no_result
crashes (2026-08-30) were pre-Contract A and pre-jr-tooling-repair
artifacts, not evidence the path is unusable.

## 2026-08-31 · nmidisp_basic_coexistence · analysis

A minimal NMI handler — push ds/ax/bp, set one flag byte at the result
region, pop bp/ax/ds, iret — survived one disproof attempt: BASIC
executed PEEK/PRINT after the handler returned and the cursor kept
blinking, consistent with restored IF and intact interpreter state.
NOT empirical, NOT manual-verified, NOT proven. Repeats plus the
KBDNMI chain (Probe B) are required before any coexistence claim is
promoted. The clean control run (flag=0, no spurious NMI in the window)
weakens but does not eliminate the spurious-source concern.

## 2026-08-31 · rule9_nmidisp_carveout · decision

Rule 9 prohibition on custom INT 02h handler dispatch was lifted for
the NMIDISP (Probe A) scope only, by user decision 2026-08-31. The
prohibition remains on the books for all other scopes and for Probe B
(no-op redirect -> JMP FAR F000:0F78) until separately authorized.
## 2026-08-31 · int48_runtime_vector · manual-verified

The runtime INT 48h (hex) vector is KEY62_INT at F000:10C6, not
KEY_SCAN_SAVE at F000:F068. Exactly two writes to KEY62_PTR (IVT offset
0120h) exist in the BIOS listing:

- 04D9: MOV KEY62_PTR, OFFSET KEY_SCAN_SAVE — "POD INT HANDLER"; POST
  diagnostic only.
- 07C9: MOV KEY62_PTR, OFFSET KEY62_INT — "62 KEY CONVERSION"; installed
  in the "SET UP OTHER INTERRUPTS AS NECESSARY" block after the vector
  table copy loop (F7A).

The 07C9 write supersedes the F068 stub before the runtime keyboard path
is live. KBDNMI's success path (INT 48h at 0FF7) therefore reaches
KEY62_INT at runtime, not the POST stub.

## 2026-08-31 · kbdnmi_entry_contract · manual-verified

KBDNMI (F000:0F78) entry contract, from a full routine read (0F78–1003):

- Pushes SI, DI, AX, BX, CX, DX, DS, ES in that order and pops in reverse.
  Save/restore is transparent: whatever register value is present on entry
  is faithfully restored on IRET. A clobbered GPR therefore passes straight
  back to the interrupted program.
- Does NOT read ES in its body. The push at 0F80 and pop at 0FF9 bracket
  no ES dereference.
- Does NOT set DS on the success path. Only the error path (I9 at 1004)
  calls DDS to set DS=0040h.
- Success path (0FF7 INT 48h) relies on the INT 48h target to establish
  its own DS.

supersedes: handoff assumption that KBDNMI requires ES=DATA on entry.

## 2026-08-31 · key62_int_ds_self · manual-verified

KEY62_INT (F000:10C6) calls DDS (138B) at 10C8, establishing DS=0040h
itself before any buffer write. Its header comment states the register
contract explicitly: "IT IS ASSUMED THAT THIS ROUTINE IS CALLED FROM THE
NMI DESERIALIZATION ROUTINE AND THAT ALL REGISTERS WERE SAVED IN THE
CALLING ROUTINE. AS A CONSEQUENCE ALL REGISTERS ARE DESTROYED." KBDNMI is
the saving caller. KEY62_INT contains no halt path (no OUT 0A0h,0 / no
CALL E_MSG) in its first ~40 bytes.

## 2026-08-31 · probe_b_noop_chain_pass · empirical

The 57-byte zero-work redirect (installer + one far-indirect jmp handler)
passes hardware: keyboard alive, keystroke echoed via INPUT after a single
IR key. The handler touches no register, stores no flag, and at KBDNMI
start SP is byte-identical to a stock NMI entry. See test_log
probe_b_noop_bisect.

## 2026-08-31 · probe_b_nonzero_work_defect · analysis

Hypothesis: the Probe B defect lives in the handler's non-zero work (flag
store, register saves, added cycles perturbing KBDNMI phase or stack),
not in the stock chain. The no-op pass means this hypothesis SURVIVED one
disproof attempt — it is not proven, not verified, not empirical.

Supporting observations, in run order:
- 74-byte AX-clobber variant → "Syntax error in 160" (AX corruption passed
  through KBDNMI's transparent save/restore into BASIC).
- 86-byte all-registers variant → hard freeze, no cursor (18-byte save
  frame perturbed stack depth at KBDNMI entry).

Both signatures vanish when the handler does zero work.
## 2026-09-03 · jr_lint_v2_refactor_spec · decision

The `jr` lint v2 refactor spec plus implementation plan is authored and
locked. Full normative content and explicit next-session instructions
live in `docs/jr_lint_v2_refactor_spec.md`; that file is the source of
truth for the implementing session. No code, no config, no file
deletions, no fact supersedes were performed this session — all are
deferred to the implementing session per that spec.
