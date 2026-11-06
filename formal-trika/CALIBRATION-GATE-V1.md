# F2/F4/F6 — gate-vs-gold calibration report (thresholds/1, CPU, no model)

**Run:** `tools/calibrate_gate.py --n 200 --seed 0` on Mitrasamgraha test
pairs (gold) + 4 corruption kinds. Full log:
`formal-trika/data/calibration-gate-v1.txt`. Gate code: sanskritbench
`pipeline/translation_proof.py` (imported read-only, unmodified).

## Numbers (thresholds/1 = current constants: binding 3.5×, coverage ~40%, glossary-gated consistency)

| set | gate-PASS | reads as |
|---|---|---|
| gold (faithful) | 142/200 = 0.710 | false-BLOCK 0.290 |
| +hallucinated padding | 47/200 = 0.235 | binding catches ~3/4 |
| truncated to 30% | 177/200 = 0.885 | **coverage blind to 70% drops** |
| term-drifted | 145/200 = 0.725 | **consistency never fires (1.00 everywhere)** |
| source-repeat | 18/200 = 0.090 | abstention works |

Per-dimension gold PASS: BINDING 0.91, COVERAGE 1.00, ABSTENTION 0.96,
TERM_CONSISTENCY 1.00, CITATION_GROUNDING 0.82.

## F4 stamp

`gate-thresholds/1` STAMPED WITH VERDICT **NEEDS TUNING** (not a pass):
a threshold version is a versioned measurement, and this one measures
badly. No signal auto-passes alone (ENDGAME rule); no threshold change
without re-running this calibration (same n, same seed, same corruptions).

## F6 signal trust (earned, not asserted)

- **ABSTENTION: trusted** vs source-repeat (0.09 false-PASS). Keep.
- **SOURCE_BINDING: partial** (0.235 hallucinated PASS; 0.09 gold BLOCKED
  by length alone — the 3.5× heuristic punishes legitimate expansion).
- **COVERAGE: untrusted** — 88.5% PASS on 70%-dropped text. The ~40%
  floor is far too low; needs clause/pāda-level alignment, not word
  ratios. Do not cite coverage PASS as evidence of completeness.
- **TERM_CONSISTENCY: vacuous off-glossary** — 1.00 on everything because
  the check only fires on 12 glossary terms absent from most Gita verses.
  Untrusted outside its glossary domain; needs per-text term extraction
  (the sanskritbench Phase 3 lemma→sense map is the real fix).
- **CITATION_GROUNDING: over-blocking** — 0.82 on gold (18% of faithful
  translations BLOCKED). Tune or split (citation present vs sufficient).
- **F3 sweep: BLOCKED on pair data, by design.** Whole-work L2/C1 prose
  is not translation pairs; running pair-gates over commentary would
  manufacture BLOCKEDs. Correct next step: pair-structured emission
  (T1↔L1 segments, cf. ipvv-r2-staging pilot apparatus) with explicit
  alignment, then sweep. Recorded, not faked.
