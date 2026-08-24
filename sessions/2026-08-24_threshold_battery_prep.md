# Handoff — threshold battery prep + ground-truth convention (single scope)

Date: 2026-08-24
Scope: verify live pycjr run_test contract, emit threshold pinning
battery, restore AGCPROBE anchor, establish ground-truth handoff
convention.

## Verified this session

- Live pycjr.py contract verified via grep_repo read: `--run_test FILE`
  (`nargs='?'`), trial grammar `label,lead,on,off...`,
  `build_probe_wave` semantics, `run_battery` sequencing, `run_suite`
  batching.
- Repo drift: root pycjr.py (664 lines, harness) vs bin/pycjr.py
  (stale `store_true`/`testing_macro`). Live Pi file authoritative.
- AGCPROBE.BAS pasted by user; DATA 1000-1100 byte-identical to the
  ENVSHAPE block, matching CH0CAL.ASM 100-byte image.
- Threshold battery emitted: merge S=180/190/200/210; recovery
  S=260/300/340/380, W=62, lead=0, trailing=5000. 8 trials / 2 batches.
- Ground-truth convention adopted: anchors to `docs/anchors/`, handoff
  gains a Ground truth section.

## Open questions

- Whether merge-battery ed=2 trials will dump H: the BASIC gate requires
  ed>=3; ed count is the merge signal.
- W=250 H asymmetry still open (from agc_profile_probe).
- Whether the ingest path accepts `docs/anchors/` on unzip.

## Loose ends

- AGCPROBE ed>=2 dump variant for merged-high capture not yet
  implemented.
- W_c sweep 150/175/200/225 and N=12 train deferred.
- bin/pycjr.py stale copy needs sync or removal.
- refs/pcjr_repo_grep.py docstring still shows `--run-test` (hyphen)
  example.
- Session sidebar titles generic; needs system prompt final-line edit.

## Suggested next scope

- Run threshold battery on hardware with CH0CAL anchor first; record
  results and append test_log.
- Apply skill-file edits for ground-truth convention (payload_generation
  session rules, test_workflow anchor registry) and system prompt final
  line for scoped session titles.

## Ground truth

- CH0CAL.ASM -> docs/anchors/CH0CAL.ASM (design logic)
- ENVSHAPE.BAS -> docs/anchors/ENVSHAPE.BAS (frozen BASIC runner)
- AGCPROBE.BAS -> docs/anchors/AGCPROBE.BAS (probe capture variant)
- Agreement: ENVSHAPE.BAS and AGCPROBE.BAS DATA blocks byte-match
  CH0CAL.ASM; regenerate via debug_asm, never hand-roll.
# Handoff — threshold battery prep + ground-truth convention (single scope)

Date: 2026-08-24
Scope: verify live pycjr run_test contract, emit threshold pinning
battery, restore AGCPROBE anchor, establish ground-truth handoff
convention.

## Verified this session

- Live pycjr.py contract verified via grep_repo read: `--run_test FILE`
  (`nargs='?'`), trial grammar `label,lead,on,off...`,
  `build_probe_wave` semantics, `run_battery` sequencing, `run_suite`
  batching.
- Repo drift: root pycjr.py (664 lines, harness) vs bin/pycjr.py
  (stale `store_true`/`testing_macro`). Live Pi file authoritative.
- AGCPROBE.BAS pasted by user; DATA 1000-1100 byte-identical to the
  ENVSHAPE block, matching CH0CAL.ASM 100-byte image.
- Threshold battery emitted: merge S=180/190/200/210; recovery
  S=260/300/340/380, W=62, lead=0, trailing=5000. 8 trials / 2 batches.
- Ground-truth convention adopted: anchors to `docs/anchors/`, handoff
  gains a Ground truth section.

## Open questions

- Whether merge-battery ed=2 trials will dump H: the BASIC gate requires
  ed>=3; ed count is the merge signal.
- W=250 H asymmetry still open (from agc_profile_probe).
- Whether the ingest path accepts `docs/anchors/` on unzip.

## Loose ends

- AGCPROBE ed>=2 dump variant for merged-high capture not yet
  implemented.
- W_c sweep 150/175/200/225 and N=12 train deferred.
- bin/pycjr.py stale copy needs sync or removal.
- refs/pcjr_repo_grep.py docstring still shows `--run-test` (hyphen)
  example.
- Session sidebar titles generic; needs system prompt final-line edit.

## Suggested next scope

- Run threshold battery on hardware with CH0CAL anchor first; record
  results and append test_log.
- Apply skill-file edits for ground-truth convention (payload_generation
  session rules, test_workflow anchor registry) and system prompt final
  line for scoped session titles.

## Ground truth

- CH0CAL.ASM -> docs/anchors/CH0CAL.ASM (design logic)
- ENVSHAPE.BAS -> docs/anchors/ENVSHAPE.BAS (frozen BASIC runner)
- AGCPROBE.BAS -> docs/anchors/AGCPROBE.BAS (probe capture variant)
- Agreement: ENVSHAPE.BAS and AGCPROBE.BAS DATA blocks byte-match
  CH0CAL.ASM; regenerate via debug_asm, never hand-roll.
