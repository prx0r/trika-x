# Pre-registration — tattva rung (TK-R2), structural generation

**Registered 2026-11-06** by the box agent, before any change to
`control/Tattva.lean` beyond the committed `93dbf7a` state. This file gives
TK-R2 the dedicated registration it lacked (previously only
`PREREGISTRATION-DECODE-RUNG.md §F-UPAYA-adjacent`: "structural rules, not
trained"). Historical files are never edited; corrections go in new dated
files (see `PREREGISTRATION-2026-11-06.md` for the pattern). Nothing here is
built unless the runs ledger says so.

## 0 · Source tiers (frontier T/R/E/C/H/X)

- **T (textual):** `translation-work/tantrasara-a07` tsa07-p01 argmap
  (36 natures, magnitude ladder: earth 100-crore → water 10× → …
  → ahaṃkāra "one-eleven-wombed" = aikādaśagarbha = 5 tanmātra +
  5 mahābhūta + 1 manas (v09) → buddhi 100× → prakṛti → Māyā →
  Kāla → Niyati → Rāga → Vidyā → pure course). AnswerKey
  `key_thirtysix_tattvas` = 36 (T, ARGMAP-PINNED).
- **R (reconstructed):** group-size clauses (5/5/5/5/1/1/1/1/5/7),
  course assignments (gross/subtle/mind/impure/pure), pure-principle
  count 7 (our reconstruction — the text's list may differ; flagged R).
- A reconstruction never promotes itself. Any T-tier contradiction means
  the mapping is wrong — fix the formalization, never the text (ipvv Law #1).

## 1 · Predictions (made before code changes)

| ID | Prediction | Confidence |
|---|---|---|
| TK-R2a | `five_gross_elements`: 10× ladder yields exactly 5 gross elements. | 0.9 |
| TK-R2b | `eleven_wombed`: 5 + 5 + 1 = 11 (N-wombed formula). | 0.85 |
| TK-R2c | `thirty_six`: 10 group-size clauses generate total 36, matching AnswerKey. | 0.7 |
| TK-R2d | `all_groups_present`: 10/10 groups accounted, no orphan/double-count. | 0.9 |
| TK-R2e | Compression 10/36 ≈ 0.28, same order as Thon Ly sangaha (0.22 over 121, 0.30 over 89). Hierarchical (uneven groups) compresses worse than combinatorial (independent axes). | 0.65 |

## 2 · Kill and reopen criteria

- **TK-R2c null** (generated ≠ 36) → group sizes are per-item data, not
  structural rules; rung parked, no ratio claimed.
- **BrokenTattva CHECKS** (7→6 mutant still proves `thirty_six`) →
  instrument blind; stop, fix `must_fail.py`, re-register.
- **Pure-7 contradicted by T** (text lists different pure principles) →
  mapping wrong; fix `groupSize .purePrinciple`, never the text.
- **T-tier contradiction anywhere** → mapping wrong; T1 immutable.
- **Scope discipline:** every theorem carries finite-model size;
  `decide` proves inside scope only, never metaphysical truth.

## 3 · What this is not

Not a proof that 36 tattvas are the structure of reality, that the ladder
is metaphysically true, or that any translation is certified. A Lean
`decide` verifies stated definitions yield stated counts. Compression ratio
is an arithmetic statistic for this encoding, not demonstrated compression
of a traditional classification (cf. PREREGISTRATION-2026-11-06 §1).
