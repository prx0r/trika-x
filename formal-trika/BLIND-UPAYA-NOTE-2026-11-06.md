# Blind re-derivation: Upaya (2026-11-06)

Exercise per BLIND.md §"The exercise", brief §7 item 10. Read-only inputs:
`Vocab.lean` (MeansState {ready, pure}), `UPAYA-CRITERIA.md`, TRIKA-METHOD.
`recognition/Upaya.lean` NOT read until after derivation (statements below
reconstructed from vocab + criteria, then compared).

## Re-derivation (blind)

State space from vocab: 2 booleans → 4 states, 2 with ready=true.
Doctrine constraints (criteria): śāmbhava = readiness suffices;
śākta = readiness + purified vikalpa; āṇava = readiness + repetition.

Derived counts:
- śāmbhava reaches exactly the 2 ready states.
- śākta excludes the ready-but-impure state → strictly narrower (≥1 excluded).
- āṇava at n=1 reaches 0 ready states; at n=2 reaches both.
- Containment: āṇava(2)-reached ⊆ śāmbhava-reached; śākta-reached ⊆
  śāmbhava-reached (both differences empty).

## Comparison with checked-in Upaya.lean (read after)

`sambhava_immediate` (=2) ✓ · `sakta_needs_purity` (>0 excluded) ✓ ·
`anava_needs_repetition` (=2 at n=1 unreached) ✓ · `anava_two_suffice`
(=2) ✓ · `anava_within_sambhava` (=0) ✓ · `sakta_within_sambhava` (=0) ✓.

## Verdict: SAME

Same counts via same-shaped rules. Caveats (not hidden): same analyst did
both sides, so this confirms re-derivability, not independence. Partial
independence exists: `blind_family2.py` (Mistral + Qwen regenerating Upaya
from the same inputs) came back exact — cross-model SAME. Full independence
still owed: a second human encoder (rater-2 class blocker).
