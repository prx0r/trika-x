# TRIKA-METHOD — how to formalize a tantra without smuggling in readings

Borrowed discipline (Thon Ly's formal-abhidhamma: prereg → controls →
mutation tests → verdicts plain; `letting-the-texts-lose` as nearest
method essay), adapted to Trika materials. This file is the standing
method; preregistrations instantiate it per rung.

## 1 · Tiers ride every claim (frontier T/R/E/C/H/X)

- **T** = what the Sanskrit explicitly states in a pinned gold layer
  (T1/L0/argmap, CANONICAL green; cite work + passage, e.g. tsa08-p03).
- **R** = the strongest argument recoverable (AM0, inexternalism, our
  glosses, capacity pairings, correspondence rows). An R-rule never
  promotes itself to T. Any T-tier contradiction means the mapping is
  wrong: fix the formalization, never the text (ipvv Law #1 applied).
- Tiers live in file headers AND theorem docstrings, not just in prose.

## 2 · General rules only; tables are key, never proof

A **general rule** constrains axes or classes (e.g. "kārma presupposes
māyīya/āṇava"). A **generated set** is what satisfies all rules of the
layer. **Compression ratio** = rule clauses ÷ generated rows. A per-item
table (name→value rows, e.g. correspondence mappings, capacity pairings,
unverified labels) is **KEY DATA**: collate it separately (AnswerKey
pattern), pin each row to evidence, and never let a rule restate it.
`unverifiedProposedLabel` (Pramatr.lean) is the reference specimen:
provisional, unused by any count theorem, flagged R.

## 3 · Textual layers as a variable (not yet run — instrument ready)

Which layer makes a count derivable? Candidate Trika layers, finest first:
root-verse wording → Abhinavagupta's vimarśinī reasoning → Tantrasāra
presentation → our reconstruction. Record per theorem which layer its
bridges need. Multi-edition work (Khmer/CST analogue: variant readings
across witnesses) is parked until openpatala chunk-bridge lands; until
then, edition + passage locators ride every T claim.

## 4 · Controls before trust, mutants always

No rung is trusted until: (a) a known-answer control checks, (b) a known
failure refuses (`must_fail.py`: same `by decide` statement, expected false
proposition, Lean pinned, warnings as errors — arbitrary compiler errors
never count), (c) every new file lands in its `run.sh` + CI the same commit.
Broken twins are hand-written models; matching statements don't prove the
mutant differs only as intended — review the semantic difference too.

## 5 · Prereg before code, verdicts plain, kills written in advance

Each rung: predictions + confidence + kill criteria, committed before the
Lean. Corrections are new dated files; historical preregs are never edited
(see PREREGISTRATION-2026-11-06 for the correction pattern). Runs ledger:
PASS / REFUTED / UNRESOLVED / PENDING-*; confounded flags where due
(small n, single rater, pilot scope). A null result is a result:
report it, keep the program.

## 6 · Blind re-derivation (instrument: Vocab.lean + BLIND.md)

Types without combination logic, given to a second encoder. Same counts via
different rules = compression confirmed. Different counts = find the bug.
Unformulable-in-vocab = the vocab is missing a distinction. Never resolve
by editing vocab to match the model.

## 7 · What a Lean `decide` is and isn't here

It verifies that stated definitions yield stated counts/shapes over finite
models. It does not prove Trika true, predict physics, certify a
translation, or bless a diary assignment. Heuristic scores (benchmark PASS,
audit receipts, embedding proximity, kappa) are never cited as semantic
proof — only `decide` proves, inside its model's stated scope (size on
every theorem family). Statistics over lived decodes are pilot signals
until preregistered n, independent raters, and replication.

## 8 · Machine proposes, human disposes

Formalization consumes pinned sources as evidence only and never writes
into source repos. A needed source fix is a CLAIM, not a patch. Publish
policy (gates, sign-off, DOI) is a separate lane with human signatures;
no inventory emitted here is a publication gate (see the evidence-boundary
tests, `tests/test_tools.py`).
