# Pre-registration — arm C (sharpness): methodology + instruments

**Registered 2026-11-06, BEFORE the arm-C verification runs.** Honest
sequencing note: an exploratory audit of the Lean files (rule/key/model
classification) preceded this prereg; no empirical claims were scored off
that audit. This prereg covers the arm-C BUILD (AnswerKey, blind
instrument, TABLE, runs ledger, method essay, header discipline). The
empirical rungs (T-C1..T-C4) remain governed by PREREGISTRATION-DECODE-RUNG.md.

## Predictions (checkable properties of the work itself, not the world)

| ID | Prediction | Confidence |
|---|---|---|
| M-KEY | AnswerKey collates 5 tradition figures with per-figure status (VERIFIED-QUOTE / ARGMAP-PINNED / PREREGISTERED-ONLY / UNPINNED); zero tradition-figures depend on our models; the excluded list names our non-traditional constructs. | 0.9 |
| M-BLIND | `vocab.py` extracts every inductive/structure (mutants excluded) into a Lean-checking Vocab.lean; `--check` passes; a blind reader can state what each type is FOR from docstrings alone. | 0.85 |
| M-TABLE | TABLE.md covers every `^theorem` in positive files (76 incl. 2 scaffolds marked); `table.py --check` passes; no reading asserts what its theorem does not state. | 0.8 |
| M-LEDGER | `record_run.py` appends one JSONL line per verification with rev+Lean+harness exits; runs/INDEX.md gains an arm-C section citing it. | 0.9 |
| M-GREEN | All harnesses + tests + tc1 stay green after every arm-C edit (control, recognition 18+/18+, test_tools, vocab/table checks, tc1 holds). Any red stops the line. | 0.85 |

## Kill / correction rules

- A M-* failure blocks the arm-C PR (fix or descope, recorded in ledger).
- Audit finding stands even if inconvenient: KancukaCorr.corr rows stay KEY
  (stipulated + evidence-pinned, never derived); `unverifiedProposedLabel`
  stays provisional; thina/middha rule gap (no root restriction vs the books)
  is documented, not silently kept — fix or flag in METHOD.
- No empirical claim may be scored off arm-C work products alone;
  T-C* verdicts cite only preregistered pilots.

## What this is not

Not a new empirical rung. No new claims about texts, minds, or the diary.
Instrument-building with acceptance criteria, nothing more.
