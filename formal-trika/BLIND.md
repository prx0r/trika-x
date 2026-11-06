# BLIND.md — the second-encoder protocol

Borrowed from formal-abhidhamma (`model/blind/`, `BLIND.md`): one encoder's
reading must survive re-derivation by hands that never saw the encoding.

## The instrument

`tools/vocab.py` generates `Vocab.lean`: every `inductive`/`structure` in
formal-trika with field meanings, and NOTHING else — no combination rules,
no transition defs, no theorems, no row tables. It is current iff
`tools/vocab.py --check` passes (CI enforces).

## The exercise (for the lead agent or a fresh session)

1. Read ONLY: `Vocab.lean` + the preregistrations + `TRIKA-METHOD.md` +
   the cited T-tier passages (argmap ids, not our files).
2. Re-derive ONE rung blind (suggested order: Upaya — smallest relation
   set; then Pramatr): write the combination/transition rules as general
   constraints over the vocab types and count what they generate.
3. Record divergences against the checked-in models in a dated note:
   same counts via different rules (good — compression confirmed);
   different counts (better — one side is wrong, find which);
   unformulable-in-vocab (best — the vocab is missing a distinction, add it).

## Rules

- The blind encoder never reads `control/*.lean` / `recognition/*.lean`
  bodies before writing. Skimming file NAMES is allowed (know which rungs
  exist, not how they work).
- A divergence is never resolved by editing the vocab to match the model.
  Fix the model, or justify the vocab gap in the note.
- One rung per note. Verdicts plain: SAME / DIFFERENT-found-bug-here /
  VOCAB-GAP.

## Status

Instrument built 2026-11-06 (26 types extracted, generated file
Lean-checks). No blind run yet — first run is lead-agent work.
