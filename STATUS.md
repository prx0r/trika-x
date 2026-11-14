# STATUS — every artifact, one line (2026-11-08)

*PR #7 P2: one current entry point with explicit status per artifact.
Statuses: IMPLEMENTED@rev (tested at revision) · PROTOTYPE (works, not
gated for release) · PROPOSED (spec only) · BLOCKED (named blocker) ·
HISTORICAL (superseded reference, do not build on). A dashboard count says
what it counts; nothing here implies human acceptance or deployment.*

## Trika-x machine gates (all IMPLEMENTED, verified 2026-11-08)

| Artifact | Status | Owner | Verify |
|---|---|---|---|
| `formal-trika/control/` rungs (157 theorems) + twins | IMPLEMENTED@ab5dfcc/247d897 | trika-x | `control/run.sh` + receipts |
| `evidence_check.py` (157/155, 16/154) | IMPLEMENTED | trika-x | `evidence_check.py` |
| `table.py` + TABLE.md + readings | IMPLEMENTED | trika-x | `table.py --check` |
| `bridge_resolve.py` (28/154 BYTES_MATCH) | IMPLEMENTED | trika-x | `--check --tw` |
| `axiom_audit.py` (CLEAN static) | IMPLEMENTED | trika-x | `--check` |
| `trace_bundle.py` + verify (assurance-separated) | IMPLEMENTED | trika-x | `tests/test_trace_bundle.py` (10) |
| `trace_all.py` (909 bundles) + `data/traces/` | IMPLEMENTED | trika-x | `--index-only` reproduces |
| `treeka.py` + `treeka_report.py` + cross-check test | IMPLEMENTED | trika-x | `tests/test_treeka_report.py` (4) |
| `chunk_verse_map.py` (23 works, 105 chunks, CANDIDATE) | IMPLEMENTED | trika-x | `--check` SHARP |
| `essay_check.py` (forgery-closed) | IMPLEMENTED | trika-x | `tests/test_essay_check.py` (7) |
| `essay_derive.py` (6 PARTIAL, 0 BROKEN) | IMPLEMENTED | trika-x | `--json` |
| `review_status.py` (0 Core / 157 Frontier) | IMPLEMENTED | trika-x | `--check` |
| `decision_check.py`, `chunk_verse.py`, `crux_queue.py` | IMPLEMENTED | trika-x | direct run |
| `review_packet.py` (7 packets queued) | IMPLEMENTED | trika-x | `swarm/review-packets/` |
| `mcp_catalog.py` (112 tools) + gateway + pretest | IMPLEMENTED | trika-x | `--check`, 11 gateway tests |
| `MCP-OPS.md` (operating guide) + `DOCS.md` (entry point + map) | IMPLEMENTED | trika-x | read + run their commands |
| `docs/log/` (20 dated records, links verified) | IMPLEMENTED | trika-x | repo-wide md-link audit, 0 broken |
| `docs/AI-DISCOVERABILITY-2026-11-08.md` (GEO research notes) | IMPLEMENTED | trika-x | sources cited; plan in svread |
| `svread/SEO-GEO-PLAN-2026-11-08.md` (execution spec) | IMPLEMENTED (spec) | svread | 10 gates defined, none built yet |
| `svread/HANDOVER-SEO-2026-11-08.md` (build handover) | IMPLEMENTED | svread | traps verified against code |
| `freshness.py` ledger + SHARP gate | IMPLEMENTED | trika-x | `--check` |
| `pushback.py`, `roboscholar.py` (1 pilot, 2-family) | IMPLEMENTED | trika-x | pilot files in `swarm/` |
| `calibrate_gate.py` (NEEDS TUNING, reproduced) | IMPLEMENTED | trika-x | `--n 200` |
| Clean-checkout fixture suite | IMPLEMENTED | trika-x | `test_clean_checkout.py` |
| `check.py` (GREEN + 2 recorded BLOCKED roots) | IMPLEMENTED | openpatala | `check.py` |
| Box DB 555/909/102/87/1559/121/20/**0 witnesses** | IMPLEMENTED | openpatala | psql counts / API |
| `validate_benchmark.py` 3×3 smoke (null result, logged) | IMPLEMENTED | sanskritbench | run `54b08b41` |

## PROTOTYPE (works, not release-gated)

| Artifact | Owner | What's missing |
|---|---|---|
| Treeka reader view | svread | surface in reader; data side done |
| Propose loop | trika-x | 1 pilot done; continuous operation needs quota + human triage |
| `treeka.json`-driven crux queue | trika-x | queue live; scholar uptake pending |

## PROPOSED (spec only, no build)

**Claim pages / SEO-GEO build** (B02–B20 in `svread/HANDOVER-SEO-2026-11-08.md`)
· Second-encoder twin review · per-declaration run digests · DERIVED exemplar
(Q12 gate) · video `evidence_refs` carry-through · Nibbanahelp N1 exporter ·
C2/slang register renders · short movies R9 (explicitly NOT YET).

## BLOCKED (named blocker, owner/lane/scholar)

Witnesses 0 (NGMPP/manuscript channel) · Zenodo token (+DERIVED exemplar
first) · cron install + token rotation (owner) · disk Tier 2/3 (owner) ·
tau scale-up + COMET (quota/GPU) · chunk↔verse remainder + decision-trail
writes (translation-work lane) · svread publish/chat/Sanskrit slice
(svread lane) · evidence refs handoff (factories) · P-TK1/rater-2/ti-ca
(scholar) · dīkṣā policy + recipes + outreach (owner).

## HISTORICAL (reference only)

`docs/log/HANDOVER.md` (11-06 mega-session) · `NEXT-STEPS.md` ordering (superseded by
MASTERPLAN2) · `MASTER-PLAN.md` pre-amendment text · swarm superseded 14:xx
runs (removed, recorded) · `MASTERPLAN-TECHNICAL-SPEC.md` 11-06 claims
superseded by measured 11-08 baseline.
