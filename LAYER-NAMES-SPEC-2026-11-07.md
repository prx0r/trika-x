# LAYER-NAMES SPEC — internal codes for us, human names for callers (v1, 2026-11-07)
*Status: CANONICAL. Internal/external name contract; resolver + tests enforce it. (2026-11-14.)

 Status: SPEC + reference implementation (trika-x only). No lane's code is
 changed by this file. Translation-work schemas + validators stay
 authoritative; nothing here renames a bare code.

## The problem (owner's words)

 Someone calling the API doesn't want to see `l0`. Our stack speaks in
 codes (T1/L0/ARGMAP/L2/C1/C2/L3/L4); callers think in names
 (draft, gloss, argument, translation, essence, render, final, song).

## The rule

 1. Internal codes NEVER change (validators, gates, ledgers, packs, lingua,
    treeka, essay compiler key on them — see `test_layer_names.py`
    `test_codes_stable`, which fails on rename/reorder).
 2. Public names are ADDITIVE. Surfaces present `{code, public}` together
    and accept either on input (`to_internal` passes codes through).
 3. A bare rename of codes requires a major schema version + migration.
    Never a quiet edit.

## The map (canonical: formal-trika/data/layer-names.json)

 | code | public | label |
 |---|---|---|
 | SOURCE | source | Source text |
 | T1 | draft-translation | Draft translation |
 | L0 | literal-gloss | Literal gloss |
 | ARGMAP | argument-map | Argument map |
 | L2 | reading-translation | Reading translation |
 | C1 | essence | Essence |
 | C2 | register-render | Register render |
 | L3 | final-translation | Final translation |
 | L4 | song | Song |

 Every entry carries `blurb` (caller-facing) + `comment` (our personal name
 for it, quoted from LAYERS.md/mistakes.md — e.g. L0 "forks live HERE and
 nowhere else", C1 "states the MATTERS, never the document", L4 "music,
 never doctrine"). Comments document our names; they never ship as doctrine.

## Adoption per lane (proposed, lane owners dispose)

 - scholar MCP `passage_evidence`: `layers` values gain `{code, public,
   ...}` alongside current code keys; `target`/`layer` params accept either
   via `to_internal`. No existing tool changes shape (additive fields only).
 - translation-work site data (`data/*.t1.json` …): filenames + JSON keys
   stay codes; reader UI shows labels; API docs show both.
 - bookfactory `inspect`/`quote`: `--ref`/`--layer` accept public names,
   resolve to codes before touching layers.
 - lingua `resolve_ref`: chunk/layer refs accept either; canonical output
   keeps codes.
 - packs/factory: evidence refs keep codes (fail-closed `validate_evidence`
   matches exact strings); storyboards may show labels.

## Reference implementation (this repo, tested)

 - `formal-trika/tools/layer_names.py`: `to_internal`, `to_public`,
   `describe`, `codes`, `publics` (fail-closed ValueError on unknown).
 - `formal-trika/tests/test_layer_names.py`: 6 tests (roundtrip, tolerance,
   fail-closed, codes-stable, comments-present, publics-unique). GREEN.

## Non-goals

 No new layer, no reordering (stack.json order stands), no L200 revival in
 this spec, no renaming files on disk, no cross-scholar style mixing.
