# MODULES — every repo, what it is, what state it is in, who owns it

*2026-11-07. State verified by running each repo's gate on this box. Where a
number is given it was measured, not remembered.*

Read this before assuming any part is "done". Several repos call themselves
complete in old docs; the honest state is in the Status column.

## The spine

| Repo | Role | Status | Gate |
|---|---|---|---|
| **openpatala** | IDENTITY: work/edition/passage/witness root | DB 555 works / 909 passages / 0 witnesses; API live; MCP 5 tools | `python3 check.py` |
| **translation-work** | EVIDENCE: draft-translation→literal-gloss→argument-map→reading-translation→essence→final-translation→song (keys T1/L0/ARGMAP/L2/C1/L3/L4), proofs per song | 101 works in pipeline, 87 with ledgers, 72 gold, 55 projected | `python3 check.py` (their lane) |
| **trika-x** | FORMAL + verification: Lean theorems, traces, federation | 157 theorems, 909 trace bundles (236 C / 673 P), 104-tool MCP gateway | `python3 -m unittest discover -s formal-trika/tests` |
| **svread** | SURFACE: reader, Sanskrit lessons, bibliography, verify view, chat | 50 readable works, 10 lessons, 13 published traces + packs | `node --test tests/*.test.cjs` |

## Supporting

| Repo | Role | Status |
|---|---|---|
| **ipvv** | IPVV chunks, pushing lab data, qp receipts kernel | 49 chunks BLOCKED/PROOF_NOT_RUN; pushing INDEX 57 records |
| **bookfactory** | PRINT: gated paperbacks, quote cards | gate fail-closed: all 5 lanes BLOCKED (no ship path by design) |
| **videofactory** | VIDEO: parity rig, gated renders | build-only; unit-tests 2 failures; no production render |
| **sanskritbench** | VERIFY: gold sets, proof gate, tau meta-eval | foundation done; tau table PENDING; metrics advisory only |
| **sanskrithelp** | STUDY: grammar, drills, mātṛkā body map | live site; integration tasks SH1–SH3 open |
| **nibbanahelp** | PERSONAL: tensions, diary, relay | live; journey ledger owner-gated |
| **patalacheckpoints** | ATLAS + prior art: 254-record bibliography, source-resolver design | canonical bibliography source; its Lean claims are NONE |
| **aoc / aionboard** | Social content factory / business | separate track, not part of the Trika chain |

## How they join

```
openpatala (identity)
   ↓ chunk locator + immutable_id
translation-work (layers + proofs)
   ↓ sha256 per layer
trika-x (formal theorems + trace bundles)
   ↓ published traces + verify packs
svread (reader, lessons, bibliography, verify view, chat)
```

Every hop carries `bytes + hash + status + where to re-fetch`. The joins are
checked by `trika-x formal-trika/tools/trace_bundle.py` (compile) and
`svread tools/emit_verify.py` (publish exact bytes).

## Federation (one agent entry point)

`trika-x/formal-trika/tools/federation_gateway.py` multiplexes every child MCP:

```
openpatala__resolve / openpatala__coverage
formal__trace / formal__bridge / formal__evidence / formal__table
formal__gaps / formal__runs / formal__axioms
scholar__*        (41 tools, svread evidence + account + layers/forks/wheel)
translation__*    (16 tools, translation-work shastra)
bookfactory__*    (22 tools, draft-only)
video__*          (18 tools, gated renders)
```

112 tools total, all live (5 children + local families). FailOpen: a dead child
is excluded, never fatal. Catalog: `formal-trika/data/mcp-catalog.json`.
No tool anywhere can sign, publish, or ship.

## Cross-cutting rules (all repos)

1. Tiers on every claim (T/R/E/C/H/X). A reconstruction never promotes itself.
2. Machine proposes, human disposes. No auto-sign, no auto-publish.
3. Fail-closed: timeouts, blocks and empties are ERROR, never PASS.
4. Missing data is UNKNOWN/UNPINNED, never filled by analogy.
5. Lanes are read-only to each other: specs and CLAIMS notes, not edits.
6. Only `decide` proves, and only inside its stated finite model. A heuristic
   PASS is not semantic proof.
