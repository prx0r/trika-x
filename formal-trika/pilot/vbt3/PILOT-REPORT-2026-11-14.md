# PILOT REPORT — P-VBT3 verse-level rosters (2026-11-14, machine-proposed)

*Second customer of the formal-stage pattern (after P-DSP). R-tier throughout,
assessor-gated, never canonical until signed. Turns the 2026-11-08 VBT
correction (`formal-trika/PREREGISTRATION-VBT1-CORRECTION-2026-11-08.md`)
into a formal roster rung: the earlier rungs count the ARGMAP/C1 layers; this
one counts the verse-level inventory those layers under-list.*

## Ground (R, inherited)

- Correction doc (2026-11-08): verses name more items than the ARGMAP/C1
  rosters. vv.2–4 name nine candidate forms (8 ARGMAP + `śaktisvarūpa`,
  distinct from v.3's `śaktitraya`). v.14 names five coordinates
  (`dikkālakalanonmuktā deśoddeśāviśeṣiṇī`) — C1 names three.
- translation-work `vbt/` L2/ARGMAP spans (vbt chunk).

## What was built

- `formal-trika/pilot/vbt3/Vbt3.lean` — 2 theorems, finite roster arithmetic.
- 2 twins (single-definition diffs): `BrokenVbt3Eight` (drop śaktisvarūpa),
  `BrokenVbt3FourCoords` (drop uddeśa).
- `sketch.json` manifest: theorem→{chunks, tier, status, twin, ground} + kill
  conditions + prereg pointer (the correction doc).

## Gate results (measured, this session)

| Gate | Result |
|---|---|
| Lean compile, warnings-as-errors | PASS |
| 2/2 twins refuse at expected proposition | PASS (must_fail exactly-one-error) |
| R-tier declared, no T-tier | PASS |
| Manifest↔file, chunk `vbt` resolves | PASS |

## The theorems (R-tier, PILOT status — for the assessor)

| Theorem | Chunks | Ground |
|---|---|---|
| `verse_forms_nine` | vbt | vv.2–4 as named: 8 ARGMAP forms + śaktisvarūpa |
| `verse_coords_five` | vbt | v.14: dik/kala/kalana/deśa/uddeśa |

## The one thing this rung refuses to claim

The correction's standing rule: a rung grounded in an intermediate layer may
count that layer, but its reading must say "as named in vv.2–4 / v.14", never
"the text names exactly nine / exactly five". `bhairavākṛti`'s status (tenth
alternative vs locus of the ninefold division) is a scholarly judgement the
held layers do not settle, so it is **not modeled**. Both theorems are roster
facts, not inventory-exhaustion claims.

## Assessor questions (judgment only)

1. Is the verse roster correctly nine (8 ARGMAP + śaktisvarūpa), or is
   `bhairavākṛti` a distinct tenth that must be added? (If yes: new rung, not
   a silent re-count — kill condition names this.)
2. Is v.14 correctly read as five coordinates, or are deśa/uddeśa modifiers of
   the same loka that C1's three already cover?
3. Kill conditions adequate?

*Machine proposes. Assessor disposes. No rung ships without the sign-off.*
