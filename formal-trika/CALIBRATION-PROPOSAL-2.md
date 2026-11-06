# CALIBRATION PROPOSAL — thresholds/2 candidate (for the gate owners to dispose)

Derived from `CALIBRATION-GATE-V1.md` (n=200, seed 0, same corruptions).
This file proposes constants only; no gate code touched (translation_proof
is read-only imported). Adopt = edit gate + rerun `calibrate_gate.py`
(same n/seed/corruptions) and restamp.

| Dimension | /1 constant | Measured fault | /2 candidate | Rationale |
|---|---|---|---|---|
| COVERAGE floor | ~0.40 word ratio | 0.885 PASS on 70%-dropped text | 0.70 interim + clause/pāda alignment as the real fix | floor alone can't catch drops; alignment is structural |
| SOURCE_BINDING length | 3.5× expansion cap | 0.09 gold BLOCKED (legit expansion punished) | length-normalized binding (cap scales with source length) or 4.5× | stop punishing faithful long renders |
| CITATION_GROUNDING | single check, 0.82 gold | 18% faithful BLOCKED | split present vs sufficient (two checks) | presence ≠ sufficiency; tune separately |
| TERM_CONSISTENCY | 12-term glossary | 1.00 everywhere (vacuous) | per-text term extraction (their Phase 3 lemma→sense map) | glossary-domain check must not pass outside its domain |
| ABSTENTION | current | trusted (0.09 false-PASS) | unchanged | keep |

Non-goals: F3 sweep stays blocked on pair data (unchanged); no threshold
auto-adopts (rerun + restamp required); pilot statistics stay descriptive.
