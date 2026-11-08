# PREREGISTRATION — Phrdaya closing-sequence rung (P-PHR4–5, R-tier)

*2026-11-08. Follows PREREGISTRATION-PHR-RUNG.md (P-PHR1–3 are theorems in
`control/Phrdaya.lean`). This rung covers the ledger's fifth locator,
phr-p05 (sūtras 17–20). Nothing here executes without the twin refusing.*

Ground: translation-work `phrdaya/` ledger row phr-p05 (immutable
`pt:pid:phrdaya:005`), L2-phr-p05.md (four v-headings: v.17 madhyavikāsāc /
v.18 iha upāyāḥ / v.19 cidaikyāmarśa / v.20 bhavati śivam), ARGMAP phr-p05
(token premises, `unresolved: none`). Tier R by inheritance. Held Sanskrit
spans (from ledger/L2): 17 `madhyavikāsāc cidānandalābhaḥ`, 18 `iha upāyāḥ`,
19 `cidaikyāmarśān nityoditasamādhilābhaḥ`, 20 `bhavatīti śivam`.

Finite claims:

- **P-PHR4 (four-closing sequence):** the passage spans sūtras 17, 18, 19, 20
  in that order — exactly four, strictly ascending. Model: roster
  `[17, 18, 19, 20]`, theorem `length = 4 ∧ Sorted (· < ·)`.
- **P-PHR5 (means named once):** of the four closing sūtras, a means-term
  (upāyāḥ) appears in exactly one — v.18. Model: roster `[18]`, theorem
  `length = 1 ∧ Nodup`.

Traps: sequence is a locator fact, not a doctrine about "the middle"; v.20's
identity (`bhavati śivam`) is NOT modeled (recognition doctrine beyond verse
grammar — same limit as P-PHR1–3); no other means-terms claimed (mirroring
C1/L2 only).

Twins: PhrThreeCloses (drop 18 → roster `[17, 19, 20]` fails four-length);
PhrTwoMeans (add 19 → roster `[18, 19]` fails exactly-one). Single-line diffs.

Kill criteria: if held L2 headings or the ledger order contradict either
count, that claim dies. Confidence: 0.85 / 0.8.
