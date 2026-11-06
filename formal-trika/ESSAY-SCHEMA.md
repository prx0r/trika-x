# ESSAY-SCHEMA.md — frozen schemas (2026-11-06, v1)

Everything the essay factory emits, field by field, read off the emitters
(`tools/essay_compile.py`, `tools/review_packet.py`). No essay may carry a
field outside these schemas; `essay_check.py` is the enforcer. Changes
require a dated amendment here + a schema-version bump, never silent drift.

## essay.json (`swarm/expansion-*.essay.json`, format `expansion-essay/1`)

| Field | Type | Rule |
|---|---|---|
| format | `"expansion-essay/1"` | exact |
| id | `essay:<slug>` | matches filename stem |
| title | string | from seed/compile args |
| date | YYYY-MM-DD | compile day |
| chunk | `work:locator` | must resolve in translation-work (fail-closed) |
| verses | [{id, text, tier}] | frozen at compile; prose may not add verses |
| voice | [units] | verbatim owner lines only, never paraphrased |
| claims | [{id, text, verse_id, tier, kind}] | **frozen first**; ids CLM-NNN; every claim needs a verse_id (orphans fail-closed); tier ∈ T/R/E/C/H/X |
| theorems | [{name, tier}] | Lean names; tier UNVERIFIED until registry-checked |
| open_questions | [strings] | PUSHBACK remainder, carried not hidden |
| tracks | [F-codes] | ≥1 required (check refuses untracked drafts) |
| tension | {id, relation} | SINGULAR, optional; relation ∈ {resolves, loosens}; id must resolve via lingua `tension:<id>`; private tensions refused (`tension-private`) |
| openpatala | {openpatala_work_id, mapping_status, record_status, record_sha256, edition_label, note} | mapping UNMAPPED until bridged; never invented |
| status | `MACHINE-COMPILED` | human dispositions live elsewhere |
| receipt | filename | pointer to the matching receipt |

## receipt.json (`swarm/expansion-*.receipt.json`, format `expansion-receipt/1`)

| Field | Type | Rule |
|---|---|---|
| format | `"expansion-receipt/1"` | exact |
| essay | slug | matches draft + essay.json |
| date | YYYY-MM-DD | |
| tracks | [F-codes] | mirrors essay.json |
| owner_quotes | [units] | verbatim bank lines used |
| banked_units | count | pushback bank debits |
| theorems | [names] | cited Lean theorems |
| openpatala | object | identity block, mirrored |
| frozen_claims | count | == len(claims); mismatch = corrupt |
| coverage | {claims, bound, orphans} | orphans must be 0 to ship |
| claims | [CLM ids] | the frozen set |
| audit | {drift verdicts} | L3/L4 tracing results |
| l3 / l4 | objects | justification edits, justified-only |
| graph | {nodes, edges added} | monotonicity receipt |
| note | string | compiler remarks |

## review packet (`swarm/review-packets/<slug>.md`)

Handoff file a human reviewer opens: draft pointer, claim summary, audit
summary, openpatala identity, reviewer checklist, honesty notes. Packets
decide nothing; decisions land outside the factory (scholar lane).

## Gate summary (essay_check.py)

SHIPPABLE iff: schema-valid + chunk resolves + zero orphans + ≥1 track +
theorems registry-checked (or UNVERIFIED-flagged) + tension (if present)
resolves + prose adds no verses/claims. Anything else prints named
failures and refuses.
