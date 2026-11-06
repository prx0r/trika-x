# Pre-registration — sharpness micro-rung (S-SHARP), control family

**Registered 2026-11-06** by the box agent, before any sharpness code.
Found by the first mechanical sweep (`jubnzv/Mutate.lean`, 2026-11-06):
`contentEq -> ||` and `-> true` mutants SURVIVE — the three P-TK3
theorems cannot tell exact content-equality from a weakened one. Same
sweep found `key_grace_term_attested` (AnswerKey.lean) with NO covering
theorem at all. Historical files never edited. Nothing built unless the
runs ledger says so.

## 0 · Tiers

- **R (reconstructed):** `contentEq` (5-field conjunction, R) and the
  sharpness predicate below. No new T claims. The grace-term fix pins an
  existing VERIFIED-QUOTE (tsa-a08 v35) to a checked theorem; the quote
  itself is unchanged.

## 1 · Predictions

| ID | Prediction | Confidence |
|---|---|---|
| S-SHARP1 | `contentEq_sharp`: a pair differing in exactly one content field (o) is NOT content-equal. | 0.95 |
| S-SHARP2 | `BrokenSharp.lean` (one conjunct dropped) PASSES the three old P-TK3 theorems and FAILS `contentEq_sharp` — proving the new theorem adds discriminating power the old suite lacked. | 0.9 |
| S-GRACEKEY | `key_grace_term`: the attestation flag checks (pins v35 VERIFIED-QUOTE to the machine surface; no new content). | 0.99 |

## 2 · Kill criteria

- BrokenSharp twin CHECKS (sharpness proves under weakened equality) →
  instrument blind; stop, fix, re-register.
- BrokenSharp FAILS an old theorem → the twin is not surgical; rewrite
  the mutant (drop exactly one conjunct), re-register the attempt.
- Scope: sharpness is a property of OUR equality predicate, not a
  textual claim. Vacuous-enumeration survivors (`allStates -> false`)
  are recorded as known mutation-testing noise (universal-over-
  enumeration goes vacuous on collapse), NOT as gaps.

## 3 · What this is not

Not a new doctrine rung. A hardening pass: the equality means what it
says, and the key file has no unchecked flags.
