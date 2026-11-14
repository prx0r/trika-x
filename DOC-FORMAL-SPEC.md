# DOC-FORMAL-SPEC — documentation as a formal system (2026-11-14)
*Status: CANONICAL. This spec (2026-11-14); self-describing, machine-checked here.

*Status: CANONICAL. This spec governs every trika-x root doc. It does not
describe aspirations; it describes the gate in `formal-trika/tools/doc_check.py`
and the registry in `formal-trika/data/docs.json`, both of which exist and run.*

## The problem (measured, then fixed)

2026-11-14 audit of trika-x root docs (32 files): **zero dead internal links**
(the repo-wide link audit works), but live numbers scattered and stale —
"104 tools" in three places (live: 115), "157 theorems" in five (live: 206),
"555 works" in two (live: 1034 with provenance), "93 green" in the gate block
(live: 109). Each number was true once; nothing re-checked them. A doc system
where every number is true exactly once is theater with timestamps.

## The rule (one sentence)

**Every doc carries a machine-readable status; every live number a doc asserts
is either verified by the gate or the doc is not CANONICAL.**

## Status tiers (mirrors the claim tiers T/R/E/C/H/X, adapted for docs)

| Tier | Meaning | Numbers rule | Example |
|---|---|---|---|
| CANONICAL | live truth, human-maintained | every load-bearing live number registered as a claim and gate-verified | DOCS.md, MCP-OPS.md, WHAT-TRIKA-X-DOES.md |
| REFERENCE | stable background, rarely changes | no live numbers required; links must resolve | LAYER-NAMES-SPEC, BACKBONE.md |
| PROPOSED | spec, unbuilt by design | must say what is NOT built; no live numbers allowed | ENDGAME-RECIPES.md (R9), VISION-ARCHITECTURE.md |
| HISTORICAL | dated snapshot, frozen | must carry its date; never edited; never cited as current | MASTERPLAN-TECHNICAL-SPEC.md |
| SUPERSEDED | do not build on; kept for provenance | must name what supersedes it | NEXT-STEPS.md |
| RECEIPT | dated log, append-only, never edited | numbers are the session's, not the estate's | docs/log/* |

A CANONICAL doc may contain dated scopes ("measured 2026-11-08 baseline"):
the date IS the qualifier, and the checker accepts a number inside an
explicit dated scope without verifying it — but the scope must name its date,
and nothing outside a dated scope may carry a stale live number.

## File format (headers)

First 10 lines of every registered doc carry, in plain text:

```
# TITLE — one-line what (dated or versioned where it matters)
*Status: <TIER>. <one line saying what this doc is and is not.>*
```

The checker parses the `Status:` line and rejects mismatch with the registry.
No frontmatter, no YAML — grep must work on a dead box.

## Registry (`formal-trika/data/docs.json`)

One entry per in-scope doc:

```json
"DOCS.md": {
  "status": "CANONICAL",
  "note": "entry point + map; gate block is the verified contract",
  "claims": [
    {"id": "suite-green", "pattern": "Ran (\\d+) tests",
     "source": {"argv": ["python3", "-m", "unittest", "discover", "-s", "formal-trika/tests"], "pattern": "Ran (\\d+) tests", "timeout": 300}}
  ]
}
```

Claim kinds:
- `{"argv": [...], "pattern": "<one capture group>", "timeout": N}` — run it,
  extract one number from stdout, compare with the doc's number.
- `{"ledger": "<dotted.path>"}` — read it from
  `formal-trika/data/freshness.json`; doc number must match (the freshness
  gate owns liveness, this gate owns the doc↔ledger match).
- `{"ci": "<path>"}` — the CI workflow file must reference the path (used
  for Lean run counts: the proof runs in CI, the doc states the number).
- `{"jsonfile": "<repo-rel path>", "key": "<dotted>"}` — compare one
  committed-JSON value.
- Modifiers: `"requires": ["db"]` skips loudly (listed, never silent) when
  the box DB is unreachable (CI has no DB, so db claims SKIP there by
  design). `"optional": true` turns a missing doc-pattern into SKIP instead
  of FAIL (use sparingly; the live value is still checked when the pattern
  is present).

Verdict rules: **FAIL** on (1) a root `*.md` with no registry entry,
(2) header status/date mismatch with the registry, (3) any registered claim
mismatch, (4) any dead internal link. **WARN** (never fail, listed separately)
on prose that looks like an unregistered live number — reviewers promote
warnings to claims; the gate never invents them.

## Geometry (`formal-trika/data/docs-geometry.json`)

Nodes: every repo in the estate + every registered doc + key data files.
Edges, each with a kind:
- `cites` — a markdown link (machine-scanned; checker fails on dangling ends).
- `consumes` — a runtime read across a boundary (gateway children, treeka
  reader, emit pipeline; curated, verified by reading the importing code).
- `verifies` — a tool that checks a doc's claims (the gate itself; curated).
- `generates` — a tool that writes a doc or data file (emitters; curated).

The checker verifies every node path exists and every edge endpoint resolves.
Meaning lives in the edge kinds, not in prose about the graph.

## Lifecycle (the process — same shape as a formal rung)

```
PROPOSED (issue or lane ask; no file yet, or a dated proposal)
  → DRAFT (branch; header carries status + date from the first commit)
  → VERIFY (doc_check.py green on the branch: registry, claims, links, geometry)
  → REVIEW (human reads; numbers re-measured if the branch is older than the
     ledger's measured_at — stale branches re-verify, never hand-wave)
  → MERGE (main; registry's last_verified stamps the merge date)
  → MAINTAIN (numbers drift → new dated correction, never a silent edit)
```

Corrections are new dated content or a new registry verified-date — never a
quiet number swap. A doc whose claims fail the gate is demoted in status
(CANONICAL → HISTORICAL + superseded-by pointer), not patched in place to
look current.

## Lane rules (cross-repo)

- trika-x verifies trika-x docs. Lanes own theirs; this gate never reaches
  into another repo's files.
- Cross-repo citations use stable paths (`repo/path`), never box paths in
  prose that outlives the box (`/root/...` appears only in runbooks with a
  "box layout" scope note — see OPERATIONS.md convention).
- svatantrya's culmination docs follow this spec by reference (their own
  lanes dispose); the trika-x registry tracks only trika-x files.

## What this spec does NOT do

No LLM judges prose quality. No readability scores. No auto-rewriting docs
to match numbers (the fix direction is always human). No coverage quotas —
a doc with zero claims is fine if its status says REFERENCE and means it.
