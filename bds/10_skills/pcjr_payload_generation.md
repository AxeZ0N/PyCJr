# PCjr Payload Generation — Session-Close Record Emitter

## Activation

Use at the end of a PyCJr session when the user asks to emit the record
payload. Repo is source of truth; re-read the ingest contract from
`facts.md` heading `ingest_payload` and `docs/FAQ.md` §7/§21 before
emitting. Repo wins over this skill on drift.

## Payload contract (verified 2026-08-22, extended 2026-08-24)

- Payload = a zip of exactly these files, emitted through BDS LONG_WORK
with BDS:create_file per file:

- `COMMIT.txt` — one-line commit message.
- `facts.append.md` — facts to append to `facts.md`.
- `sessions/<date>_<scope>.md` — the new session handoff file.
- `docs/test_log.append.md` — ONLY if a hardware run happened.
- `docs/anchors/<PROG>.BAS` and `docs/anchors/<PROG>.ASM` — only when
  adding or restoring a ground-truth anchor; `unzip payload.zip` places
  them at the correct path.
- Repo files are never overwritten. Ingest appends facts (dedupe by
heading), appends session/doc content, one commit.
- User runs `bin/jr-ingest.sh <payload.zip>`.

## facts.append.md rules

- One `##` heading per fact, shape: `## YYYY-MM-DD · fact_name · status`
where status is one of `manual-verified`, `empirical`, `unverified`,
`conflict`, `policy`, `decision`, `open item`, `analysis`.
- Body is markdown text under the heading. Never edit old facts in the
payload; supersede with `supersedes: <old_heading>` on its own line.
- Never emit `facts.md` in the payload — only `facts.append.md`.

## sessions file rules

- Filename: `sessions/YYYY-MM-DD_<scope>.md`, unique per session.
- Single defined scope. If a scope is done, recommend a new session.
- Markdown handoff with five sections in this order: Verified this
  session; Open questions; Loose ends; Suggested next scope; Ground
  truth.
- Open items and proposals stay proposals. Never lock a future spec into
  session notes unless the user says "lock it".
- Reference anchors by name; full listing only for a new program.

### Ground truth section rules

- Every hardware-passed program must have `docs/anchors/<PROG>.BAS`
  (BASIC runner, full retypable listing) and
  `docs/anchors/<PROG>.ASM` (machine-code design logic).
- The Ground truth section lists anchor paths only, not listings.
- No anchor path present means the session cannot close.
- DATA blocks in `.BAS` must byte-match the corresponding `.ASM`;
  regenerate via `jr-build`, never hand-roll.

## test_log rules

- Emit `docs/test_log.append.md` only when a run produced a result
block. No run -> omit the file entirely, no empty append.
- Result entries use the test-workflow contract/result format; never
copy one routine's expectations into another routine's contract.

## COMMIT.txt rules

- Exactly one line. Verb-first summary of the session, low-noise:
`throughput rethink: retire 86ch/s as link figure, record stock two-floor bound, open envelope floor`.
- No markdown, no bullets.

## Emission rules

- Wrap all create_file calls in BDS:LONG_WORK; the zip is the deliverable.
- After LONG_WORK closes, one short plain sentence naming the files and
whether test_log was included. Never re-explain every file.
- If the payload was already emitted and got lost, re-emit the SAME
files; do not reformat into prose.
- Ask before inventing a new file type not in the ingest contract.

## Memory batch rules (separate from the payload, same close)

- Propose the full memory batch — every key and its complete value —
  and wait for approval. One batch per turn. Never write silently.
- Key naming: lowercase snake_case, no `pcjr_` prefix. The matcher
  splits on underscores and fires per token (FAQ §20).
- Optimize keyword hit rate. Pick tokens a user will actually type
  when recalling the decision (`base26`, `ch0cal`, `polling`). Never
  build a called key from generic tokens (`cpu`, `port`, `frame`,
  `direction`) — they fire on unrelated messages and poison context.
- Value budget: target ~200 chars, hard cap 300. A value is a route
  to the ledger, not the ledger itself. End with the pointer:
  `→ sessions/<file>.md` or `→ facts <heading>`.
- Do not duplicate facts.md. If a value is already a facts.md heading,
  the memory value references the heading and adds only the retrieval
  hook. Never restate the full fact.
- Prefer few called keys, one per decision cluster. Keep `always`
  keys near-empty.
- Example good value (called): `throughput_rethink: "86 retired
  (INT16h drain); 60=throttle; floors 4840us IBG + KBDNMI ~4.8ms/frame;
  → 2026-08-22_throughput_rethink.md"`.

## Anti-patterns (never)

- Emitting `facts.md` or any repo-overwrite file in the payload.
- Emitting `docs/test_log.append.md` with no run.
- Putting a markdown block inside COMMIT.txt.
- Handing the user prose when they asked for the payload zip.
- Inventing the payload format from memory; grep the repo contract first.
- Bundling future decoder/encode specs into session notes as decisions.
- Emitting a handoff without the Ground truth section.
- Shipping a `docs/anchors/` file that overwrites an existing anchor.
- A memory key that duplicates a facts.md heading body-for-body.
- A memory value over 300 chars.
- A `pcjr_`-prefixed memory key.
- Writing any memory tag before the full batch is approved.
- Mixing memory tags with prose in one message (emit each tag alone).
