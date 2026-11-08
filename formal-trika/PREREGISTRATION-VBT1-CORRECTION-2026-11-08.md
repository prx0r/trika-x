# CORRECTION — VBT rung readings overclaimed the verses (2026-11-08, lead review)

*Dated correction. The preregs and Lean files stay as written; this records
what they actually prove and fixes the readings that overstated it.*

## Finding

`PREREGISTRATION-VBT-RUNG.md` says "the opening question banks **exactly
eight** candidate-form terms". The first half is true of the ARGMAP roster
it cites. It is **not** true of the verses, which name more:

- v.3 — `navātmabheda`, `bhairava / bhairavākṛti`, `triśirobheda`,
  `śaktitraya`
- v.4 — `nādabindu`, `candrārdha`, `cakrārūḍha`, `anacka`, and
  **`śaktisvarūpa`** ("power-formed"), which is a distinct word from
  `śaktitraya` in v.3
- v.2 — `śabdarāśikalā`

So the verse names **at least nine** candidates; the ARGMAP roster and the
Lean `VbtForm` enum carry eight and omit `śaktisvarūpa`. Whether
`bhairavākṛti` is a tenth alternative or the locus of the ninefold division
is a scholarly judgement the held layers do not settle.

`PREREGISTRATION-VBT2-RUNG.md` says p02 frees "exactly three coordinates".
v.14 is `dikkālakalanonmuktā deśoddeśāviśeṣinī` — freed of direction, time
and counting, *and* having no particular place (`deśa`) or point
(`uddeśa`). C1's summary names three; the verse names **five**. The theorem
counts C1's three.

## What the theorems actually establish

- `forms_eight`: the eight-term ARGMAP roster is eight, distinct. True and
  load-bearing on that roster. It is a claim about the map, not the verse.
- `coords_three`: the three-term C1 summary is three, distinct. Same class.

Both stay R-tier, both keep their twins. Neither is a claim that the text
has exactly that many items.

## Fix applied

- `TABLE-READINGS.md`: `forms_eight` reading changed from "the opening
  question's whole inventory" to the roster it actually counts;
  `coords_three` names the verse's extra coordinates.
- `Vbt.lean` header states the omission explicitly.
- No theorem renamed, no theorem removed, no history edited.

## Standing rule for the next rung

A rung whose ground is an intermediate layer (ARGMAP / C1) may count that
layer — but its reading must say "as listed in X", never "the whole
inventory". PR #7 §3 P0 makes the same point about collapsing "checked"
meanings; this is that failure in miniature, caught in review.
