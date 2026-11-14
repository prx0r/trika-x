# FULL AUDIT — open threads, endgame docs, visions (2026-11-14)

*A reconciliation of every plan/vision doc against measured live state. Where
they disagree, the live probe wins and the doc is marked STALE. Every status
below was checked this session.*

---

## A. The three visions — status

| Vision | Doc | State |
|---|---|---|
| **ChatGPT as MCP/plugins** | `svread/CHATGPT-PLUGIN.md` | **DONE + LIVE** — 13 hosts, console 210 tools, formal/Lean publicly callable (proven: `formal__trace` → COMPLETE). Only OAuth + directory submission remain (owner). |
| **Diary → teachings → media** (endgame recipes) | `trika-x/ENDGAME-RECIPES.md` | **PIPELINE EXISTS, NOT WIRED END-TO-END** — essay compile/check/pushback live; audio/video/book renderers exist but no consent path wired; R1 partial, R2–R8 spec, R9 intentionally NOT YET. |
| **Lean recognition stack** | `trika-x/VISION-ARCHITECTURE.md` | **HALF REAL** — the Lean proving half is real, live, tested (53+26 harnesses). The qprivately gating + cg evolution integration is PROPOSED, not built (and the doc's own 2026-11-06 review says so). |

---

## B. The 20-item execution queue (MASTERPLAN2 §12) — reconciled

| ID | Item | Status now | Owner |
|---|---|---|---|
| Q01 | Disk headroom | **OPEN** — 98% (2.0G). /tmp scraps only safe. Needs owner eyes on 6G+ trees | owner+box |
| Q02 | Nightly verify cron | cron logs exist; 7-day green not yet confirmed | owner |
| Q03 | Rotate R2/Go tokens | **OPEN** (owner) | owner |
| Q04 | Regression gate GREEN | **DONE** — all gates green (see FINAL-GREEN-RECEIPT) | trika-x |
| Q05 | Traces every chunk | **DONE** — 909 bundles (236 COMPLETE / 673 PARTIAL) | trika-x |
| Q06 | Chat answers carry trace+pack links | **PARTIAL** — traces published; chat link wiring is svread lane | svread |
| Q07 | Bench CPU calibration | **DONE** (det. reproduce; gate NEEDS TUNING recorded) | sanskritbench |
| Q08 | Formal rung phr-p05 | **DONE** (and VBT rungs) | trika-x |
| Q09 | One VERIFIED witness | **BLOCKED** — witnesses 0, needs manuscript eyes | owner/scholar |
| Q10 | Layer-accept decisions at ingest | **OPEN** — translation-work lane wiring | translation-work |
| Q11 | Treeka view live | **DONE** — `treeka__chain`/`treeka__frontier` live on formal host; report queryable | trika-x |
| Q12 | Variety-1 DOI | **BLOCKED** — needs DERIVED exemplar + Zenodo token | owner |
| Q13 | Crux queue + propose loop | **PILOT DONE** — queue live; continuous run needs quota | trika-x |
| Q14 | Peer-review debt | **DONE** — dispositions recorded | trika-x |
| Q15 | Sanskrit l01 slice | **LIVE** — sanskrit host serves passage_evidence + wheels | svread |
| Q16 | Discoverability R5 | **OPEN** — needs Search Console/outreach | owner |
| Q17 | Video evidence_refs | **OPEN** — videofactory lane | videofactory |
| Q18 | Nibbanahelp N1 exporter | **OPEN** — nibbanahelp lane | nibbanahelp |
| Q19 | Syllabus C1–C4 | **PARTIAL** — study-only units; dīkṣā policy owner-gated | trika-x+satsang |
| Q20 | Recipes R1/R7/R8 consent | **BLOCKED** — owner go | owner |

Tally: **8 done · 1 partial-done · 3 partial · 6 blocked/open (mostly non-trika-x) · 2 pilot**.

---

## C. Endgame recipes R1–R9 — honest state

| Recipe | State | Gate that would finish it |
|---|---|---|
| R1 diary→personal essay (read) | pipeline exists (essay_compile→check→pushback); **consent path not wired** | owner consent scope + nibbanahelp exporter (Q18) |
| R2 essay→audio (listen) | renderers exist (svread-audio); not bound to signed essays | TTS receipt matching signed essay text |
| R3 essay→video (own/publish) | videofactory gated; **no `evidence_refs` carry-through** (Q17) | render refuses without refs |
| R4 journey-linked publishing | **NOT BUILT** (owner-gated) | journey ledger go |
| R5 parables/C2 registers | C2 layer exists; register renders are spec | lane review of first render |
| R6 kids books | **SPEC ONLY**, highest bar, by design | human reads every line |
| R7 diary year-review book | **SPEC ONLY**, owner go | consent + TEXT-GATE per entry |
| R8 poem book from your words | **SPEC ONLY**, owner go | consent + verbatim selection |
| R9 short movies | **NOT YET**, by design (models don't qualify) | owner sets bar |

---

## D. Stale docs found (report, don't silently edit other lanes)

| Doc | Says | Reality |
|---|---|---|
| `svread/PRODUCTION.md` §0 | "Still not built: MCP bridge/tunnel + OAuth"; "BLOCKED: DB has 555 works" | bridge/tunnel **live**; DB **1034** (provenance: Muktabodha ingest, 479 shells) |
| `svread/data/mcp-registry.json` | federation 109, scholar 38 | **fixed this session** → 210 total, scholar 41, federation 112 |
| `trika-x/MCP-OPS.md` | "stdio only" | fixed → bridge §9 added |
| `openpatala/DEV-PLAN.md` | 08-17 phases 1099 works | bannered superseded; live 1034 (479 shells) |

---

## E. What is genuinely left to "finish" (short, honest)

**Agent-doable next (no human):**
1. `svread` q-path: nothing left (merged). `svread` chat-answer trace links (Q06) — svread lane.
2. Translation-work chunk↔verse remainder (Q10) — their lane.
3. Coverage climb 16/154: each rung is a prereg→Lean→twin→EVIDENCE cycle (slow, scholarly).
4. Treeka frontier polish; video `evidence_refs` spec PR to videofactory lane.

**Human-only (the actual finish):**
1. **OAuth** (per-user) → unlocks public writes + directory submission.
2. **Practice session** token → unlocks `progress__*`.
3. **Directory submission** → public discovery on ChatGPT.
4. **Zenodo token** → first DOI.
5. **Witness verification** → first primary-source citation.
6. **Rotate shared bearer** → safety.
7. **Disk reclaim** (owner eyes) → unblocks tau/Mutate.

---

## F. The one-line verdict

The **ChatGPT/MCP endgame is shipped and live**. The **diary→media recipe family
is specced and half-built** (pipeline exists, consent + render binding missing).
The **Lean verification spine is real, public and tested**. What remains is:
consent wiring (owner), OAuth (owner), and scholarly coverage climb — not new
engineering. Nothing fundamental is broken.

*Machine proposes, human disposes. STALE marked, not silently fixed across lanes.*
