# PUSHING SESSION SKELETON — BrokenTattvaInventory (machine-rendered, assessor fleshes)

- date: 2026-11-06 | positive: `TattvaInventory` | status: SKELETON (no derivations; assessor writes ROUNDs)
- twin says: ['MUTANT: māyā is incorrectly counted as a pure tattva.']

## ROUND 0 — the checked claim (assessor: root quotes here)

- `named_tattvas_36`: `inventory.length = 36`
  - ground: tsa07-p01 [T] — 7.1 mentions 36; this theorem counts a curated candidate list, not a verified source-derived enumeration.
- `named_tattvas_unique`: `inventory.eraseDups.length = inventory.length`
- `named_tattvas_exhaustive`: `∀ t : Tattva, t ∈ inventory := by intro t cases t <;> decide theorem pure_count : pureTattvas.length = 5`
- `kancuka_count`: `kancukas.length = 5`
  - ground: tsa07-p01 [T] — 7.16 lists the five kalā-led factors; this checks the candidate list.
- `maya_six_count`: `mayaSix.length = 6`
  - ground: tsa08-p03 [T] — 8.55 describes six coverings starting with māyā; this checks the candidate list.
- `pure_excludes_maya`: `pureTattvas.contains .maya = false`
  - ground: tsa08-p01 [T] — 8.16 identifies five pure tattvas; this checks how the candidate list classifies māyā.
- `pure_and_kancukas_disjoint`: `pureTattvas.all (fun t => !kancukas.contains t) = true`

## ROUND 1 — the twin's denied claim as objection (assessor: derivation here)

> The twin denies exactly this. If the text cannot answer why not, that is the finding.

## ROUND 2 — deeper (assessor only)

## Honest limit (assessor: what the text refuses)

_Skeleton rendered by twin_to_session.py. No derivation generated. Assessor fleshes or deletes._

