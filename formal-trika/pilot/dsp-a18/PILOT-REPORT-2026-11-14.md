# PILOT REPORT — D-DSP tal-a18 concise-rite sketch (2026-11-14, machine-proposed)

*First customer of the translation-work FORMAL-STAGE proposal
(`process/FORMAL-STAGE-PROPOSAL.md`): swarm-equivalent drafts the sketch +
twins from the filed prereg, mechanical gates run, assessor judges only
fidelity. Nothing here is canonical: not wired into `control/run.sh`, not an
EVIDENCE row, assessor has not ruled. R-tier throughout, cited downstream only
as R with the prereg linked.*

## Inputs (read-only, other lanes' files untouched)

- Prereg: `formal-trika/PREREGISTRATION-DSP-RUNG.md` (D-DSP1–4, kill
  conditions, R-tier; PAUSED, kept as pilot input).
- ARGMAP: translation-work `tantraloka-a18/` — 11 gold units
  (tal-a18-v01..v11), passages tal-a18-p01 (18.1–18.10) / tal-a18-p02 (18.11).
- L0: `working-l0-tal-a18.json` — 104 rows, all PARSED, **0 flagged forks**,
  single-option throughout (matches prereg "0 forks").
- MITRA grounds spot-check: `dīkṣā`→initiation (68 attestations),
  `śiva` (3609) resolve with grounds; uncovered headwords return `[]`
  (never invented). Grounds shape matches what L0 options require.

## What was built (this branch)

- `formal-trika/pilot/dsp-a18/DspA18.lean` — 4 theorems, finite
  rite-configuration arithmetic (`decide`), pinned Lean 4.34.1.
- 4 Broken twins, single-definition diffs (drop-a-shed / flip-gating /
  analytic-invalid / end-varies).
- `sketch.json` manifest: theorem→{chunks, tier, status, twin, ground} +
  kill conditions + prereg pointer.
- `formal-trika/tools/formal_sketch_check.py` — the reusable consumer: the
  four mechanical gates for ANY sketch dir (compile / twins / tiers+kills /
  manifest+chunks). Tested: `tests/test_formal_sketch.py` (pass + fail-closed).

## Gate results (measured, this session)

| Gate | Result |
|---|---|
| Lean compile, warnings-as-errors | **PASS** |
| 4/4 twins refuse at expected proposition | **PASS** (`must_fail.py`, exactly-one-error rule) |
| R-tier declared, no T-tier | **PASS** |
| Manifest↔file, 1 chunk locator resolves | **PASS** (`tal-a18-p01` in ledger) |

## Evidence-shaped entries (R-tier, PILOT status — for the assessor, not EVIDENCE.json)

| Theorem | Chunks | Ground | Twin |
|---|---|---|---|
| `shed_three` | tal-a18-p01 | v01 enumeration [mandala, eve-rite, site] | BrokenDspDropShed |
| `concise_gated` | tal-a18-p01 | v08 biconditional read, scoped to concise measure | BrokenDspFlipGate |
| `routes_both_valid` | tal-a18-p01 | v07 universal rule in all mantras | BrokenDspAnalyticInvalid |
| `end_kept` | tal-a18-p01 | v01 charter + v09 pervasion warrant | BrokenDspEndVaries |

## One deviation from the prereg (recorded, assessor to rule)

The prereg states D-DSP2 "over all 8 configs". As filed, the biconditional
`conciseValid ⟺ ripe` is **false** over all 8 (full+ripe configs break it:
concise-invalid but ripe). The pilot scopes the theorem to the 4 concise
configs, because full-form validity is explicitly unmodeled in the prereg's
own NOT-claimed list — running the biconditional over all 8 would smuggle
full-form validity claims. If the gold revises gating to one-directional,
remodel per kill conditions. **Assessor question 1: is this scoping faithful
to v08, or does "in that measure … not otherwise" demand the 8-config form
with a different validity predicate?**

## Assessor questions (judgment only, never automatable)

1. Scoping above: faithful or forced?
2. Model fidelity: does the sketch shadow the text's relation or flatten it?
   (Particular worry: D-DSP3's `routeValid` is a constant-true function with
   teeth only from its twin — is that a shadow or a flattening?)
3. Tier calls: R throughout — confirm, or does any claim overreach toward
   doctrine?
4. Kill-condition adequacy: anything missing that would remodel on gold revision?

## Kill conditions (from prereg, wired into sketch.json)

Gold revises gating direction, route universality, or the shed-list →
remodel. Volumes land → tier notes upgrade per claim. v10 stays
unformalized (no forced rungs).

*Machine proposes. Assessor disposes. No rung ships without the sign-off.*
