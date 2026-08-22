# Handoff — Throughput Rethink (single scope)

Date: 2026-08-22
Scope: Retire stale throughput numbers; bound the bottleneck chain;
identify which receiver characteristics are missing before a custom
decoder can be specced.

## 1. Verified this session

- 86 ch/s retired: INT 16h drain of a pre-filled buffer with KBDNMI
  masked; producer path absent; unit ambiguous (system type-ahead vs
  keyboard MPU buffer).
- 60 ch/s = emitter throttle policy (sleep 1/max_cps), not a ceiling.
- Two stock floors: serial (440us cell, 4840us IBG) + CPU (KBDNMI
  ~4.8ms/frame hostage + KBINT consumer). Manual entries 93/94.
- NMI = 1 per frame on start-bit leading edge; make+break = 2 per
  keypress. Typematic rate unverified.
- Wired port shares the serial protocol + latch/NMI path; not faster.
  Bypasses only the photodiode/amp/demod front-end.
- PC6 = demodulated envelope; 40 kHz carrier mandatory. Manual entry 92.

## 2. Open questions (this scope)

- Stretch distribution: full H/L dump never transcribed; only summary
  stats + gap2_1126 exist. Needs a re-run for the histogram.
- Merge distance: shortest silence producing two edges. Unmeasured.
- Min assert width: smallest burst the demod trips on. Unmeasured;
  matters only if short dits are possible.
- Custom PC6 decode floor = stretch + merge distance. Unmeasured until
  the two above are captured.

## 3. Loose ends

- Base34 dump alphabet (drop O/I, keep L; var-width, space-delimited;
  stats as checksum) is a PROPOSAL, not a decision. Revisit at spec time.
- Morse/Huffman variable-length custom encode is a Phase-3 idea, not a
  decision.
- BDS memory matcher: keys split on underscores, fire per token
  (FAQ §20). The precise substring-vs-token result was recorded only as
  "functional"; if known, record exact semantics.

## 4. Suggested next scope

- Base34 ENVSHAPE TXer mod (BASIC dump section only, ASM frozen
  byte-for-byte): one keypress, transcribe all 37 deltas, measure
  stretch and merge from real data before any decoder thresholds.
