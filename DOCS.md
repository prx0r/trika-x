# DOCS — trika-x entry point, map, and handover (2026-11-08)
*Status: CANONICAL. Entry point + map; gate block is the verified contract (2026-11-14).

*If you are a new agent (or the next lead reviewer), start here. Three
reads, then the gates. Everything else is reference.*

## 0. Start here (three reads, 15 minutes)

1. **This file** (§1 handover + §4 map) — where everything lives and what to
   trust.
2. **`MASTERPLAN2.md` §0–§2** — the objective, the laws, the measured
   baseline. Then §12 (the 20-item queue with owners/gates) and §16–§17
   (northstar + PR #7 delivery order).
3. **`SYNERGY-CHAIN-2026-11-08.md` §1–§2** — how the parts compose; what each
   hop creates, carries, and must pass.

**If you are picking up the SEO/GEO build**, skip to
`/root/svread/HANDOVER-SEO-2026-11-08.md` — it is a self-contained buildable
handover: state, reuse map, data contracts, 20 todos, page spec, JSON-LD,
10 traps with file:line, commands, and the domain-cutover runbook. Its
research basis is `docs/AI-DISCOVERABILITY-2026-11-08.md`; the execution
spec is `svread/SEO-GEO-PLAN-2026-11-08.md`.

**If you are an external reviewer**, read `docs/REVIEW-BRIEF-2026-11-08.md`
(what to check, what is not done, what is messy, what needs insight).

Then run the gates (§3). If any gate fails, the docs are stale — fix the
number, never the gate.

## 1. Handover to the next lead agent

**State of the tree:** `main` is the working head; every claim below was
measured on box (freshness ledger SHARP at handover time). Dirty work is
not hidden: open items name their blocker and owner; nothing here is
"almost done".

**What the last session built** (all committed, all pushed, all gated):
traces for all 909 chunks (236 COMPLETE / 673 PARTIAL, every PARTIAL naming
its gaps); two formal rungs (phr-p05, vbt-p01/p02 — 157 theorems at that
revision, 206 now per the gate block); twins refusing, receipts exit 0/0/0); essay-derivation audit (6 essays, 0 BROKEN);
forgery-closed essay gate + clean-checkout fixtures; MCP federation
documented to match the surface (115 tools, machine catalog, drift gate);
review packets queued; propose-loop pilot (2-family, proposal only);
peer-review debt answered in writing; +3.1G disk reclaimed; PR #7 fully
wired (search "PR #7" in `MASTERPLAN2.md`, `SYNERGY-CHAIN`, `STATUS.md`).

**What is explicitly NOT done** (do not let anyone reframe these as done):
formal coverage is 16/154 chunks (10%) · witnesses 0 corpus-wide · no
DERIVED essay exemplar yet (Q12 gate) · no second-encoder twin review
(blocks any promotion above R) · no DOI · no auto-anything, ever.

**Your review contract** (as the lead agent):
1. Re-run §3 gates yourself. A number that doesn't reproduce is the highest
   severity finding in this project.
2. Read `docs/log/LEAD-REVIEW-2026-11-08-FULL.md` (latest full review, with the
   five findings it raised and fixed) and `docs/log/LEAD-REVIEW-2026-11-08.md` (prior verdict) and
   `docs/log/REVIEW-REQUEST-2026-11-08.md` (what was asked), then rule on
   what changed since.
3. Pick one rung to re-derive blind (gap-list head: vbt-p03) — same-family
   replication is the cheapest check we have.
4. Publish your verdict as a new dated file under `docs/log/`; never edit
   an old verdict. History is append-only.

**Standing human-gated list** (only humans/lanes unblock these; the machine
keeps building around them): Zenodo token (+DERIVED exemplar first) ·
P-TK1 / rater-2 / ti-ca rulings · NGMPP witness path · KMT filename +
Dyczkowski collation · dīkṣā policy · Search Console + outreach · token
rotation (checklist: `ROTATION-CHECKLIST-2026-11-08.md`) · svread publish of
909 packs + chat links + Sanskrit slice · translation-work decision-trail
wiring + chunk↔verse remainder · video evidence_refs · nibbanahelp exporter.
Quota/GPU: propose-loop continuous run, tau scale-up, COMET baselines.

## 2. Canonical docs (read in this order)

| # | Doc | What it is | Status |
|---|---|---|---|
| 1 | `DOCS.md` (this file) | entry point, map, handover | CANONICAL |
| 2 | `MASTERPLAN2.md` | execution plan: objective, laws, baseline, queue, phases, gates | CANONICAL (amended 2026-11-08) |
| 3 | `SYNERGY-CHAIN-2026-11-08.md` | composition contract: event order, synergy rules, versioning protocol, PR #7 boundaries | CANONICAL |
| 4 | `STATUS.md` | every artifact, one line, with status + verifying command | CANONICAL (refresh on change) |
| 5 | `ROADMAP.md` | five rungs with done-gates (R1 traces → R5 links) | CANONICAL |
| 6 | `MODULES.md` | every repo: role, measured state, gate | CANONICAL |
| 7 | `ENDGAME-RECIPES.md` | R1–R9 recipes (spec only; diary invariants) | CANONICAL SPEC |
| 8 | `FEDERATION.md` + `FORMAL-MCP-SPEC-2026-11-07.md` + `PARENT-CONTRACT-SPEC-2026-11-07.md` + `LAYER-NAMES-SPEC-2026-11-07.md` + `MCP-OPS.md` | federation topology, contracts, layer names, ops | CANONICAL |
| 8b | `CANONICAL-OPERATIONS.md` | how concurrent agents share the box: ownership map, trace pipeline, no-clobber rules, handoff protocol | CANONICAL |
| 8c | `WHAT-TRIKA-X-DOES.md` | what trika-x is and does, plainly: the 5 jobs, every component, downstream consumers, the exact ChatGPT path, the point of it all | CANONICAL |
| 9 | `MASTER-PLAN.md` (+2026-11-08 amendment) | architecture + order; old scoreboard superseded by amendment | CANONICAL (architecture), HISTORICAL (pre-amendment numbers) |
| 10 | `BACKBONE.md`, `PATALA-COVERAGE.md`, `OPERATIONS.md`, `VISION-ARCHITECTURE.md`, `INDEX.md` | spine thesis, coverage map, runbook, vision, literature index | REFERENCE (vision doc self-marks proposal) |
| 11 | `SYNERGIES-{DEITYBODY,NIBBANA,SANSKRITHELP}.md`, `SVREAD-SANSKRIT-SPEC-2026-11-07.md`, `ADVICE-TRANSLATION-OPENPATALA.md`, `REQUIREMENTS-FROM-DECODE.md`, `LANE-ASKS-2026-11-08.md`, `ROTATION-CHECKLIST-2026-11-08.md` | lane-facing proposals, asks, checklists | PROPOSED / OPEN (disposed by owning lane) |
| 12 | `MASTERPLAN-TECHNICAL-SPEC.md`, `MASTERPLAN-ALIGNMENT.md` (→docs/log) | older technical plan + 20-todo alignment ledger | HISTORICAL (superseded by MASTERPLAN2) |
| 13 | `NEXT-STEPS.md` | old ordering (bannered as superseded) | SUPERSEDED (kept for per-item gates) |
| 14 | `docs/log/` (20 files) | dated process notes, reviews, requests, handoffs, PR descriptions | HISTORICAL RECORD (append-only; never edit, never delete) |

## 3. Gates (run these; they outrank every doc)

```sh
cd /root/trika-x && git status --short          # must be clean to start work
python3 -m unittest discover -s formal-trika/tests   # 117 green (2026-11-14)
python3 formal-trika/tools/evidence_check.py     # 206 theorems / 155 entries (+1 generated cert), 16/154 chunks (10%)
python3 formal-trika/tools/table.py --check      # rc=0
python3 formal-trika/tools/freshness.py --check  # SHARP
python3 tools/federation_pretest.py              # GREEN (28 expected tools)
python3 tools/mcp_catalog.py --check             # SHARP (115 tools, 2026-11-14)
python3 formal-trika/tools/doc_check.py            # docs: SHARP (registry + claims + links + geometry)
python3 formal-trika/tools/formal_sketch_check.py formal-trika/pilot/dsp-a18  # ALL GATES PASS
python3 formal-trika/tools/essay_derive.py       # 6 essays, all PARTIAL
cd /root/openpatala && python3 check.py           # GREEN + 2 recorded BLOCKED roots
```

## 4. Conventions that keep this clean

- One concern per commit; code before docs in the same session's stack.
- History is append-only: corrections are new dated files under `docs/log/`.
- Counts carry bytes + hash + where-to-re-fetch, or they don't ship
  (`freshness.py --check` enforces it).
- BLOCKED is never PASS. PARTIAL is never COMPLETE. R never promotes itself.
- No writes into other lanes' repos from here (read + specs + CLAIMS notes).
- A new doc belongs at root only if it is canonical, a live spec, or an
  open ask. Everything dated goes to `docs/log/` the session it is written.
