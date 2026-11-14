# What trika-x does

*The plain-language, complete account. If you read one trika-x doc, read this
one. Every number was produced by running the command beside it on main,
2026-11-14. Where a claim cannot be machine-checked, it says so.*

## In one paragraph

**trika-x is the estate's proof layer.** Translation-work produces Sanskrit
scholarship; openpatala says which work is which; svread shows it to readers.
trika-x sits between the scholarship and the reader and answers one question:
*does this check out, and can you prove it?* It proves finite structural
claims in Lean (with hand-written mutants the checker must refuse), binds
every theorem to the passage chunks it talks about, compiles the whole chain
into per-chunk trace bundles an outsider can re-verify with `curl` and
`sha256sum`, and serves all of it over one MCP gateway that ChatGPT and any
other agent can call. Nothing here advises, translates, or publishes. It
checks, and it shows its work.

## The five jobs

### 1. PROVE — Lean formalizations with must-fail twins

Finite models of traditional doctrine, no semantics, no doctrine claims:
counts regenerate, orderings hold, gatings biconditional. Each rung ships with
twin files — single-definition mutations the checker is *required* to refuse
at the exact `by decide` line. If the checker were vacuous, the twin would
compile; it does not. That is the anti-vacuity check, and it is the whole
reason the proofs mean anything.

| Harness | Result | Command |
|---|---|---|
| Control (`control/`, 56 files) | **53 PASS / 0 FAIL** | `sh formal-trika/control/run.sh` |
| Recognition (`recognition/`, 26 files) | **26 passed / 0 failed** | `sh formal-trika/recognition/run.sh` |
| Axioms | **CLEAN (static)** — no `sorry`, no smuggled axioms | `python3 formal-trika/tools/axiom_audit.py --check` |

Lean 4.34.1, pinned. Adding a file: compile line in `run.sh`, twin with
must-fail check, EVIDENCE entry, TABLE row, run receipt. Prereg before code,
always.

### 2. VERIFY — every claim resolves or says why not

The verification battery, each fail-closed (BLOCKED/ERROR, never silent pass):

| Gate | What it proves | Status |
|---|---|---|
| `evidence_check.py` | every theorem ↔ chunks or named reason | **206 theorems · 155 entries · 2 exemptions · 1 generated · 0 problems; coverage 16/154 (10%)** |
| `table.py --check` | hand readings joined to sources | **rc=0** |
| `review_status.py --check` | every theorem has a tier row (0 Core / 206 Frontier — promotion disabled until authenticated review) | **passes** |
| `essay_check.py` + tests | essay claims bind to ledger passages (span+digest+edition); duplicates/unsafe names refused | **14/14 tests; 6 essays, 0 BROKEN** |
| `essay_derive.py` | is every essay derivable to Sanskrit? | **6 PARTIAL, 0 BROKEN** (honest: none fully derivable yet) |
| `freshness.py --check` | every canonical number reproduces from its recorded command | **SHARP** |
| `mcp_catalog.py --check` | live gateway matches the frozen catalog | **SHARP, 115 tools / 8 families** |
| `federation_pretest.py` | contract, prefixes, banned names | **GREEN (28)** |
| Full suite | everything above plus unit coverage | **107 tests OK** |

### 3. TRACE — the Sanskrit-to-essay chain, compiled per chunk

`trace_bundle.py` compiles one `trika-trace/1` bundle per chunk: source bytes
→ layer hashes → proof/gate records → formal theorems (REGISTERED
associations, `run_bound: false` — associations, not entailments) → citing
essays → verdict COMPLETE/PARTIAL with named gaps. `trace_all.py` compiles all
**909 bundles (236 COMPLETE / 673 PARTIAL), 0 errors**; `emit_verify --check`
is GREEN and svread publishes the bundles with verify packs. An outsider
re-verifies with `curl` + `sha256sum` — no account, no code, no trust.

### 4. ARGUE — the treeka graph and the crux queue

`treeka.py` assembles works → passages → argmap nodes → cruxes → essays, all
read-only, all keyed `work:locator`; `treeka_report.py` renders the queryable
gap report (unargued / cruxless / essayless / unformalised; queue worked in
gap-list order, never by taste). Supporting track: `crux_queue.py`,
`argmap_nodes.py`, `review_packet.py` (scholar-bound review packets),
`pushback.py` (cross-model destroy pass — a report, never a verdict, never an
edit), `review_status.py` (tiers on every theorem).

### 5. SERVE — one MCP gateway for every agent

`federation_gateway.py` multiplexes the child MCPs behind one stdio endpoint:
local identity (`openpatala__resolve/coverage`), guide
(`federation__guide`), scholar (41 tools), bookfactory (22), translation-work
(16), video (18), plus read-only `formal__*` (7) and treeka. FailOpen: a dead
child is excluded, never fatal. Banned action names rejected by exact/prefix
match. `tools/mcp_bridge.py` wraps it in Streamable HTTP (read sheaf of 26,
writes refuse `-32001` until OAuth exists); `tools/bridge_e2e.py` proves it
end-to-end (8/8).

## Tool reference (grouped; run `python3 formal-trika/tools/<name>.py --help`)

**Prove:** `control/run.sh`, `recognition/run.sh`, `axiom_audit.py`,
`must_fail.py`, `mutate_sweep.py`, `blind.py`, `blind_family2.py`,
`gen_prakriya_slice.py`, `formal_sketch_check.py`, `vocab.py`,
`tc1_cooccurrence.py`, `station_pass.py`, `kappa.py`, `calibrate_gate.py`,
`tau_pilot.py`, `roundtrip.py`, `vidyut_pilot.py`, `matrika_study.py`.

**Verify:** `evidence_check.py`, `table.py`, `review_status.py`,
`essay_check.py`, `essay_derive.py`, `essay_compile.py`, `essay_query.py`,
`essay_seeds.py`, `freshness.py`, `mcp_catalog.py`, `federation_pretest.py`,
`calibrate_gate.py`, `decision_check.py`, `source_audit.py`,
`map_agreement.py`, `bridge_resolve.py`, `chunk_verse.py`,
`chunk_verse_map.py`, `build_passage_snapshot.py`, `build_source_map.py`,
`compose_bridge.py`, `incidence_matrix.py`, `claim.py`,
`formalization_manifest.py`, `emit_keys.py`, `record_run.py`,
`runs-index.py`, `review_packet.py`, `pushback.py`, `roboscholar.py`,
`twin_to_session.py`.

**Trace:** `trace_bundle.py`, `trace_all.py`.

**Argue:** `treeka.py`, `treeka_formal.py`, `treeka_report.py`,
`treeka_gaps.py` (see file), `crux_queue.py`, `argmap_nodes.py`,
`essay_check.py` (gates), `review_packet.py`, `pushback.py`.

**Serve:** `federation_gateway.py`, `formal-trika/data/federation-children.json`,
`tools/mcp_bridge.py`, `tools/mcp_catalog.py`, `tools/federation_pretest.py`,
`tools/bridge_e2e.py`.

**Seed/ingest (box DB bootstrap, idempotent):** `openpatala_seed.py`,
`openpatala_ingest.py`, `seed_atlas_biblio.py`, `seed_abhinavagupta.py`,
`work_inventory.py`, `biblio_sweep.py`, `import_paper.py`,
`ingest_research_library.py`, `mine_got.py`.

**Practice compiler (study-only until dīkṣā policy lands):** `eligibility.py`,
`syllabus_unit.py`, `unit_to_score.py`, `path_assemble.py`, `day_gate.py`,
`bodymap_check.py`, `slang_pack.py`, `tensions_export.py`,
`CRUX-WALKTHROUGH-*.md`, `ENDGAME-ESSAYS.md`, practice tests.

**Bench:** `calibrate_gate.py`, `tau_pilot.py`, `roundtrip.py`,
`sanskritbench` lane (gold sets, proof gate, tau meta-eval — advisory only).

## What consumes trika-x (verified downstream effects)

| Consumer | What it takes | Verified how |
|---|---|---|
| svread MCP gateway | spawns `federation_gateway.py` as the `federation` child (see `svread/mcp/gateway/servers.json`) | live: federation tools answer through it |
| svread treeka surface | reads `formal-trika/data/treeka.json` directly (`treeka_server.py`: "joins, never invents") | file exists, tests green |
| svread verify view | publishes trika-x-compiled trace bundles + verify packs; refuses on any verify failure (fail-closed) | `emit_verify.py --check` GREEN |
| Scholar essays | every essay claim must resolve to a ledger passage (span+digest+edition); trika-x's EVIDENCE rows are the registry those claims cite | `essay_check` 14/14 |
| ChatGPT / any MCP agent | public bundle → federation → `formal__*` (see next section) | live calls, below |
| Local HTTP consumers | `tools/mcp_bridge.py` read sheaf (26 of 115) | `bridge_e2e.py` 8/8 |

What trika-x does **not** feed and never will: translations (translation-work's
lane), publications (no auto-anything), practice authorization (owner's
dīkṣā call), witnesses (archives' job — 0 corpus-wide, stated not hidden).

## How ChatGPT uses it (exact path, reproduced live)

1. **Handshake**: `POST https://mcp.svatantrya.net/mcp`
   `{"method":"initialize"}` → `protocolVersion: 2025-06-18` + read-sheaf
   instructions.
2. **Discovery**: `tools/list` → **51 tools** (openpatala 8, scholar 17,
   federation 1, formal 7, treeka 2, translate 6, compose 10).
3. **Proof**: `tools/call formal__trace {work: tantrasara-a08, target:
   tsa08-p03}` → verdict **COMPLETE**, **9 REGISTERED Lean theorem rows**.
4. **Evidence**: `tools/call scholar__passage_evidence {work:
   bodhapancadasika, target: bod-p01-v01}` → 9,474 bytes, Sanskrit + layers +
   `projection_sha256`.
5. **Refusal**: write calls without a bearer → `-32001` (OAuth unissued; the
   bridge says so instead of faking acceptance).

Any MCP-compatible agent (ChatGPT connectors, Claude, Google ADK
`MCPToolset`, open harnesses) consumes the identical surface: independently
verified with a FastMCP SDK client against a second host
(`formal.svatantrya.net`: 10 tools listed, `formal__gaps` answered). No
Google-specific endpoint exists or is needed — the protocol *is* the
integration.

## Why this exists (the point, plainly)

AI generation is cheap; provenance is scarce. Anyone can generate a confident
paragraph about Abhinavagupta. Almost nothing can tell you which bytes it came
from, whether the structure checks out, or who signed it. trika-x is the
machine that manufactures the scarce half: every claim hash-pinned to source,
every structural claim machine-checked (with the checker itself tested by
mutants), every draft human-gated, every gap published instead of papered
over. It does not make the estate smart. It makes the estate **checkable** —
by outsiders, by other agents, years later, without trusting us. That is the
whole point, and everything above is machinery in service of it.

## How to verify everything on this page (copy-paste)

```sh
cd /root/trika-x  # DOCS.md §3 is the canonical gate list
python3 -m unittest discover -s formal-trika/tests   # 107 green
python3 formal-trika/tools/evidence_check.py          # 206/155+1, 16/154
sh formal-trika/control/run.sh                        # 53 PASS (Lean 4.34.1)
sh formal-trika/recognition/run.sh                    # 26 passed
python3 tools/mcp_catalog.py --check                  # SHARP (115 tools)
python3 tools/bridge_e2e.py                           # 8/8 over HTTP
```

## What's next (build-out, with owners)

- **Coverage climb, gap-list order** (phr mala → VBT → tsa08 …): machine drafts
  per the pilot pattern (`formal-trika/pilot/`, PR #19 needs **assessor**
  ruling first); promotion needs **scholar** review. Nothing auto-promotes.
- **PR #15 trace refresh** (other agent): re-verify at merge time; the loop
  moves under refreshes — freeze, refresh, merge, in that order.
- **DERIVED exemplar + Zenodo DOI** (needs **owner** token): first essay whose
  chain goes DERIVED end-to-end.
- **Per-layer sha + review state in passage evidence** (svread lane): the one
  named V1 gap in the connected surface.
- **Second-encoder twin review, per-declaration run digests, video
  `evidence_refs`, N1 exporter, C2 renders, R9 movies**: spec'd, gated on
  humans/quota/models respectively — see STATUS.md PROPOSED/BLOCKED.
