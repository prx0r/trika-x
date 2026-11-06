# Blind re-derivation note — Upaya (pilot, single-family)

**Date:** 2026-11-06. **Encoder:** box agent, fresh session (built E-EGO +
heaps this session; never touched Upaya; Upaya.lean body first read AFTER
writing `blind/UpayaBlind.lean`, which checks clean on pinned Lean).
**Flag (not hidden):** same model line as the original builders — this
pilots the vocab's sufficiency, NOT cross-family replication. A second
family re-derivation is still owed for REPLICATED-grade confidence.

## Read-before-writing set (only)

`Vocab.lean` (V.MeansState {ready, pure} only) + UPAYA-CRITERIA.md
criteria half + PREREGISTRATION-DECODE-RUNG.md F-UPAYA + TRIKA-METHOD.md
+ tsa-a08 v17 T-pins. Rater-1 table seen (irrelevant to encoding).

## Verdicts (one rung, per BLIND.md)

| Claim | Blind form | Checked-in form | Verdict |
|---|---|---|---|
| śāmbhava = readiness | `sambhavaReaches s := s.ready` | `sambhavaReach s := s.ready` | **SAME** (identical rule, independently written) |
| śākta = ready ∧ pure | `saktaReaches s := s.ready && s.pure` | `saktaReach s := s.ready && s.pure` | **SAME** |
| purity load-bearing | witness ready∧¬pure exhibited | filtered-length > 0 existence | **SAME** (content; shape differs: witness vs count) |
| śākta ⊆ śāmbhava | `all` over filtered | empty-difference count | **SAME** |
| śāmbhava = readiness only | `all` over filtered | length = 2 | **SAME** |
| āṇava repetition | UNFORMULABLE in {ready, pure} | `anavaReach s (n : Nat)` — extra Nat param | **VOCAB-GAP** (predicted before reading) |

## The gap (the best kind of result)

V.MeansState cannot express "repeated application": no counter, no step
index, no temporal structure anywhere in the vocab. Upaya.lean carries
the repetition as a def-level `Nat` parameter — structure the vocab
extraction (types only) never sees. Per BLIND.md this is NOT resolved by
editing the vocab to match: the note justifies instead. Justification:
state-types vs transition-structure are different families; āṇava lives
in the second. Recommendation (lead-agent decision, not taken here):
extend the vocab instrument to cover transition indices (Nat params on
reach-defs), re-run `vocab.py --check`, then re-derive āṇava blind
against the extended vocab. Until then, āṇava's encoding is
single-encoder work (checked + mutant-twinned, but not blind-confirmed).

## What this confirms

The śāmbhava/śākta distinction regenerates identically from the vocab
alone: same counts via independently written rules. That half of F-UPAYA
is compression-confirmed (single-family). The āṇava half rests on one
encoder's modeling choice (n≥2 minimal) + mutant twins. T-C2 (human
agreement on the criteria) remains the empirical bite for the whole rung.
