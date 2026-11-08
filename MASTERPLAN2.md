# MASTERPLAN2 — execution plan for the measured machine (2026-11-08)

*Status: canonical execution plan from 2026-11-08. Supersedes the ordering in
`NEXT-STEPS.md` (kept as reference). `MASTER-PLAN.md` remains the architecture
and phase order — see its AMENDMENT 2026-11-08 for the updated scoreboard.
This file turns that scoreboard + the 20-todo queue + `REVIEW-2026-11-08.md`
into one ordered, gated build plan. Every number below was measured on box
2026-11-08; every unmeasured item is marked as a claim, never a fact.*

---

## 0. The objective (one line)

An outsider, with no account and no code, can take any claim we publish, fetch
its trace and its bytes, recompute the hashes, and see the same numbers we do —
and where we could not verify something, we said so first.

**Definition of done (whole plan):** one question asked in chat → witness-pinned
(or honestly CANDIDATE) passages → layers → checked theorem → argued node →
crux → audited draft → PUSHBACK → human sign → release + DOI → optional video —
and every link replays from the DOI back to the manuscript witness using only
the three legitimacy logs (audit receipts, openpatala events, sanskritbench runs).

---

## 1. Laws inherited (non-negotiable, none re-opened here)

1. **Nothing is real because a file exists.** A claim needs a logged,
   reproducible gate. BLOCKED is never PASS.
2. **Machine proposes, human disposes.** No auto-sign, auto-publish,
   auto-practice-authorization, ever.
3. **Tiers on every claim** (T/R/E/C/H/X); R never promotes itself.
4. **Fail-closed.** Timeouts, blocks, empty responses are ERRORS, never passes.
5. **No rung ships without** hash + grounds/decision + gate + signer-role.
6. **Only `decide` proves** inside its finite scope. Heuristic PASS ≠ proof.
7. **Lanes respected.** translation-work ingest, ipvv worker, bookfactory,
   videofactory, svread worker are other lanes: read-only + specs + CLAIMS
   notes from trika-x. No writes into their repos.
8. **History is never edited.** Corrections are new dated files.
9. **One identity system.** openpatala is the root. No second DB, ledger, or
   ID scheme.
10. **Private stays private.** Diary material ships only with explicit,
    scoped, revocable consent. No auto-publish of personal material, ever.

---

## 2. Measured baseline (2026-11-08 — the only trusted numbers)

| Layer | Measured state | Source |
|---|---|---|
| openpatala gate | GREEN: api/mcp/evidence/db PASS; conformance + witnesses BLOCKED (recorded) | `python3 check.py` |
| openpatala DB | 555 works · 909 passages · 102 editions · 87 etexts · 1559 assertions · 121 ext-ids · 20 people · **0 witnesses** | live postgres |
| Upstream evidence bundle | 996 works · 79 assertions · 38 ext-ids · 990 events · 1 artifact | `data/evidence/evidence-bundle.json` |
| translation bridge | 28 works · 154 passage IDs · ledger bytes match · witnesses UNPINNED | `bridge_resolve.py --check` |
| source-map | 87 works · **6 bridged / 81 todo** | svread `source-map.json` |
| formal | 153 theorems · 151 entries + 2 exemptions · 0 bad chunk refs · axiom CLEAN (static) | `evidence_check.py` |
| formal coverage | **13/154 passage chunks (8%)** · gap list published | `data/formal.json` |
| traces | **13 bundles** (12 COMPLETE / 1 PARTIAL w/ caveat), external verify pack live | svread `data/traces/index.json` |
| svread surface | 50 readable works · 55 scholar projections · 504 manifest assets · 10 Sanskrit lessons | live site + manifest |
| tests | trika-x 73 · svread 49/0 · gateway 8 · Lean harnesses green | 2026-11-07 run |
| PUSHBACK | live (mock/go/cf, opt-in, verbatim shield, never edits) | `formal-trika/tools/pushback.py` |
| Hygiene | disk **98% (1.7G free)** · branch `box/peer-review-batch` dirty · nightly cron NOT installed · token rotation unconfirmed | box |

**Staleness register** (fix the paper, not the machine; full list in
`REVIEW-2026-11-08.md`): openpatala README counts (1099/247/2181) are stale vs
evidence-bundle (996/79/990) vs box DB (555); "slang landed" unverifiable on
svread disk; "Treeka assembler = one tool" not built; WITNESS-OCR is a doc.

---

## 3. Workstreams (the 20 todos, grouped and ordered)

Each item: **gate that marks it done** · **owner/lane** · **blocker**.
Priority: P0 = unblocks everything; P1 = proof/verification; P2 = surface &
closure; P3 = scale & humans; P4 = personal recipes (consent-gated).

### W0 — Hygiene & autonomy (P0, do first, ~1 session)

| # | Item | Done when | Owner | Blocker |
|---|---|---|---|---|
| 10a | Disk recovery to safe headroom | `df -h /` ≥ 15% free; deletions only of R2-pinned/rebuildable temp, each logged | box ops | owner eyes on shared checkouts |
| 10b | Dirty branch resolved | `box/peer-review-batch` committed or stashed with dated rationale; `git status` clean | trika-x | none |
| 10c | Nightly verify cron | log shows 7 consecutive green days | owner (writes cron) | owner call |
| 10d | Token rotation | R2 + Go keys rotated, old revoked, `/root/.env` updated, repo scans clean | owner | owner action |
| 10e | Secrets + disk guard in CI | preflight fails on secret grep hit or disk <10% | trika-x | none |

*Why first:* every later gate (tau scale, Mutate remainder ~2.9G, COMET torch)
needs disk; a dirty branch makes every `evidence_check` unreproducible.

### W1 — Identity root / openpatala (P1)

| # | Item | Done when | Owner | Blocker |
|---|---|---|---|---|
| 1 | Honest gate stays green | `check.py` GREEN with only numbered BLOCKED; no new silent FAIL | openpatala lane | adapter fix upstream |
| 19 | Corpus/biblio feed routine | atlas seeds re-run on atlas rev change; people/translations/editions current; refs not forked | trika-x | atlas rev cadence |
| 13 | Chunk↔verse map + source_verses | bridge resolves chunk → verse → witness-status for every ledger work; remainder tracked | translation-work lane | their build |

*Correction to old plan:* A-track is not "get everything openpatala" — 102
workdirs already have rows. It is "keep the gate honest and close the 81
unbridged works one lane decision at a time."

### W2 — Verification & traces (P1, the moat)

| # | Item | Done when | Owner | Blocker |
|---|---|---|---|---|
| 2 | R1 trace every readable passage | `data/traces/index.json` covers ≥90% of passages in readable works; every pack reproduces its trace; PARTIAL is labelled, never hidden | trika-x + svread | none (autonomous) |
| 5 | R4 chat cites verifiably | every chat answer citing a trace-bearing chunk returns trace + pack link; untraced chunks say "unverified" | svread worker | worker lane |
| 11 | Bench calibration (CPU first) | tau 3×3 smoke logged; gate-vs-gold false-PASS/BLOCK rates measured; thresholds stamped | sanskritbench | quota only for scale |

*Why now:* this is the one thing no competitor has — checkability without our
code. Broadening it from 13 chunks to all readable passages multiplies the moat
with zero new infrastructure.

### W3 — Formal coverage (P1, gap-list order only)

| # | Item | Done when | Owner | Blocker |
|---|---|---|---|---|
| 4 | R3 formal >50% of gold chunks | each new theorem: prereg → model → must-fail twin → EVIDENCE → TABLE → run receipt; gap list still published | trika-x | scholar review for promotion (P-TK1) |

Order (never by taste): **phr mala rows (head phr-p05, prereg exists)** → VBT
clusters → tsa08 remainder → tsa01–22 gaps → tal-a15 remainder. P-TK1 / ti-ca /
rater-2 promote claims; they never initiate rungs.

### W4 — Witness column (P1, the only human-archive gate)

| # | Item | Done when | Owner | Blocker |
|---|---|---|---|---|
| 3 | R2 one VERIFIED witness | one core work has `witness.status = VERIFIED` with a real shelfmark; its trace's source hop cites it; UNKNOWN stays UNKNOWN elsewhere | owner/scholar (NGMPP) | manuscript eyes |

Candidates file is ready (`bridge/witness-candidates.json`). WITNESS-OCR is a
proposal, not a pipeline — do not present it as one.

### W5 — Datastructures / Treeka (P1–P2)

| # | Item | Done when | Owner | Blocker |
|---|---|---|---|---|
| 12 | Decision trail at ingest | L0/L2/L4 acceptance writes decision rows; submission with unsigned load-bearing decision refused (409) | translation-work lane (checker ready) | lane wiring |
| 14 | Treeka view live | works → passages → argmaps → cruxes → essays + gap report (unargued / cruxless / essayless / unformalised) rendered and queryable | trika-x (`treeka.json` live) + svread view | none for read-only assembler |

### W6 — Scholar loop (P1–P2, Variety 1 + 2)

| # | Item | Done when | Owner | Blocker |
|---|---|---|---|---|
| 7 | Variety 1 close | PUSHBACK pass runs pre-review by default (opt-in quota); one signed essay gets a resolving Zenodo DOI; outsider replays DOI → witness | svread lane + owner token | **Zenodo token** |
| 15 | Crux queue + propose loop | gap report + pushing catalog → prioritized queue; Svatantrya drafts per crux (assisted flagged, quota-limited), audit + PUSHBACK, leaves proposal; never auto-sign | trika-x + scholar | quota for live runs |
| 20 | Peer-review debt | LEAD-REVIEW 16 flaws + REVIEW-REQUEST PR #5 answered in dated notes; each flaw marked fixed / accepted / rejected with evidence | trika-x | none |

### W7 — Surfaces (P2)

| # | Item | Done when | Owner | Blocker |
|---|---|---|---|---|
| 6 | Sanskrit `?view=sanskrit` slice | lesson l01 (mamātmā) shows verse, literal-gloss breakdown, rb-1/rb-2, chat from the same evidence spine with receipts, grammar tab labels every ML line with model+status; outsider replays lesson→locator→bytes→gate | svread lane (spec: `SVREAD-SANSKRIT-SPEC-2026-11-07.md`) | audio render = owner go |
| 9 | R5 discoverability | `site:` returns pages; Search Console impressions; ≥1 external referring domain | owner + trika-x content | owner Search Console / outreach |

*Honest note:* Google ignores llms.txt (documented). The lever is static
crawlable lesson pages + inbound links. Keep llms.txt for agents, never claim
it buys Google citations.

### W8 — Media / practice loop (P2–P3)

| # | Item | Done when | Owner | Blocker |
|---|---|---|---|---|
| 16 | Video carry-through | packs carry `evidence_refs` (work/locator/ledger-sha); sealed mp4 inherits GOLDEN gates; render refuses on missing refs | videofactory lane | their sealed path |
| 17 | Nibbanahelp N1 | sessions → tension/crux queue exporter, read-only, recurring unresolved questions feed the Treeka gap report | nibbanahelp + trika-x | VOICE RULE compliance |
| 18 | Syllabus compiler C1–C4 | C1 one practice unit rendered (study-only) → C2 37 āhṇikas classified → C3 path IDs + Series → C4 loop closure (day-gate, request→vid) | trika-x + satsang practice | dīkṣā policy (owner) |

### W9 — Endgame recipes (P4, consent-gated spec→build)

| # | Item | Done when | Owner | Blocker |
|---|---|---|---|---|
| 8a | R1 diary → personal essay (read) | consent-scoped diary → retrieve-first teacher → essay compile (verbatim diary voice + banked claims + tiers) → audit → pushback → human sign; no auto-publish | nibbanahelp + essay lane | running diary consent path |
| 8b | R7 diary year-review book | year boundary explicit; tension arcs human-flipped only; unresolved tensions stay unresolved in print; TEXT-GATE per entry | bookfactory lane | owner go |
| 8c | R8 poem book from your words | verbatim selection only (arrangement is the only craft); no generated or paraphrased lines; L3/L4 craft passes | bookfactory lane | owner go |

Recipes R2–R6, R9 stay spec-only. **R9 short movies explicitly NOT YET** —
gated on model quality set by the owner; no build, no tests, no placeholders.

---

## 4. Phased execution

### Phase 0 — Hygiene + honesty lock (this week, autonomous)
W0 complete; openpatala gate re-run and pinned; `REVIEW-2026-11-08.md` accepted
as the staleness register; canonical-counts rule enforced (counts carry
bytes+hash or they don't ship). **Exit:** disk ≥15% free, clean branch, cron
decision recorded, one honest gate run archived.

### Phase 1 — Broaden the moat (autonomous, 1–2 weeks)
W2 R1 traces to ≥90% of readable passages; W4 R4 chat verify links where traces
exist; W3 formal works the gap list from phr-p05; W5 treeka view (read-only)
plus decision-trail checker wired to the lane. **Exit:** an outsider can verify
any readable passage, not just 13; treeka gap report is queryable; formal
coverage climbing with receipts.

### Phase 2 — Close the loop (needs 2 human answers)
W6 Variety 1 to DOI (Zenodo token) + PUSHBACK default + crux propose loop;
W7 Sanskrit slice accepted and deployed; W1 bridge remainder decisions with
the translation lane. **Exit:** one DOI'd essay replays end-to-end; Sanskrit
lesson verifies; 81 unbridged works have explicit decisions (bridged or
UNRESOLVED-with-reason).

### Phase 3 — Scale + scarce reality (quota/GPU/humans)
W3 >50% coverage with promotion gates; W4 one VERIFIED witness; W8 video
carry-through + syllabus C1–C4; W9 recipes as owner approves consent paths;
bench tau scale (n≥30, Wilson CI) when quota allows. **Exit:** the
definition-of-done slice exists once, with every link green.

### Phase 4 — Replication & breadth (only after Phase 3)
Second model family on the same claims (REPLICATED status path); Greek/Pāli
breadth only if the same primitives hold unchanged; no non-Trika expansion
before the loop closes.

---

## 5. Dependency graph

```
W0 hygiene ──► everything (disk, clean tree)
W1 openpatala gate ──► W2 traces ──► W6 DOI replay
W1 bridge (28/154) ──► W5 treeka view ──► W6 crux queue
W3 formal ──► W5 treeka formal column ──► W6 essay grounds
W4 witness ──► W2 trace source hop ──► W6 citable primary source
W7 Sanskrit ──► W8 syllabus (lesson units) ──► W8 practice loop
W6 PUSHBACK ──► W9 recipe audit (reuse, don't rebuild)
W2 bench calibration ──► every metric claim (thresholds stamped)
```

Rules: no arrow may be skipped by claiming its upstream is "close enough";
BLOCKED upstream propagates as BLOCKED downstream, never as PASS.

---

## 6. Human-gate register (what we cannot unblock ourselves)

| Gate | Who | Unblocks | Status |
|---|---|---|---|
| Zenodo token | owner | first DOI (Variety 1) | dry-run builds ready |
| P-TK1 ruling | scholar | first scholar-signed formal claim | pack ready, unestablished |
| rater-2 pass | second human | T-C2 criteria bite (kappa ≥0.6) | sheet ready |
| ti/ca signatures + station | scholar | mapping beyond structural side | pilots exist |
| NGMPP / microfilm eyes | owner/scholar | VERIFIED witness | candidates ready |
| dīkṣā policy | owner | practice authorization boundary | compiler holds STUDY-only |
| Journey / ledger / trajectory / vis-mode go | owner | W8 loop closure | spec only |
| Audit voice render go | owner | Sanskrit recitation audio | audio-plan ready |
| Search Console + outreach | owner | R5 indexing | site shipped |
| Token rotation + cron install | owner | W0 closure | scripts ready |

**Rule:** rulings promote, never initiate. The machine keeps building.

---

## 7. Scoreboard (current → target, with honest denominators)

| Metric | Now | Phase 1 | Phase 2 | Phase 3 |
|---|---|---|---|---|
| openpatala gate | GREEN, 2 BLOCKED | same, numbered | same | ≤1 BLOCKED (witness) |
| Works in DB | 555 | 555 | 555+ | 600+ |
| Bridged works | 6/87 | 6/87 | 87/87 decided | 87/87 |
| Traces | 13 | ≥90% readable | all readable | all + packs |
| Formal coverage | 13/154 (8%) | ~30/154 | ~50/154 | >77/154 (50%) |
| Witnesses | 0 | 0 | 0 | ≥1 VERIFIED |
| Scholar projections | 55 | 55 | 56+ | all readable |
| Essays with DOI | 0 | 0 | 1 | several |
| Sanskrit lessons live | 10 (verbatim) | l01 slice | full slice | audio (go) |
| Discoverability | 0 indexed | submitted | indexed | ≥1 ref domain |
| Tests | 73 / 49 / 8 | +new | +new | CI gate |
| Disk free | 1.7G (98%) | ≥15% | ≥15% | ≥15% |

Never report a numerator without its denominator. Never report "complete"
without a replay path.

---

## 8. Risk register

| Risk | Impact | Mitigation |
|---|---|---|
| Disk 98% | blocks tau scale, Mutate, torch | W0a first; owner eyes before deleting shared checkouts |
| Dirty peer-review branch | unreproducible evidence | W0b: commit/stash with rationale before any rung |
| Three-number drift (1099/996/555) | credibility hole | canonical-counts rule; wiring test enforces llms.txt |
| Token exposure (R2/Go pasted) | security | W0d rotation; `/root/.env` only; secret grep in preflight |
| Lane collision | other agents' repos corrupted | read-only + specs + CLAIMS notes; never write their files |
| Scope creep (R9 movies, Greek) | dilution | explicitly parked; Phase 4 only after loop closes |
| Quota dependence (tau, PUSHBACK live) | stalls calibration | CPU-first calibration; live runs batched to funded sessions |
| Overclaiming formal/coverage | repeats 0.5.2 failure | tiers + `formalized: null` for unknown; gap list always published |

---

## 9. Change control

- **MASTERPLAN2** supersedes `NEXT-STEPS.md` ordering (NEXT-STEPS stays as
  reference). `MASTER-PLAN.md` keeps architecture + phase order; its
  2026-11-08 amendment carries the scoreboard.
- `DECISION-PACKET-2026-11-06.md` remains the live list of human asks; update
  statuses there, do not fork a second ask list.
- `REVIEW-2026-11-08.md` is the staleness register; corrections to it are new
  dated files, never edits.
- `SYNERGY-CHAIN-2026-11-08.md` is the composition + versioning protocol (how
  the parts feed each other, how numbers stay sharp). `freshness.py --check`
  is the drift gate it depends on.
- Each workstream item closes with: commit SHA, gate output pasted into a dated
  process note, and the artifact path. If it isn't in the trace, it didn't
  happen.

---

## 10. Non-goals (binding)

No second database, ledger, or ID scheme. No auto-sign / auto-publish /
auto-practice-authorization. No quota spend on grunt work. No GPU-blocked work
without a GPU box. No heuristic PASS, beautiful output, or big model treated as
proof. No invented witnesses, editions, or DOIs. No editing history. No
non-Trika expansion until the loop closes. No claiming the model is the mind.
No rendering short movies (R9) until the owner sets the bar and models qualify.

---

## 11. First three moves (this session, if nothing else)

1. **W0** — disk headroom + commit/stash the dirty branch (no destructive gc
   without owner go). Everything else depends on it.
2. **W2/R1** — run the trace compiler over all readable works; publish PARTIAL
   honestly; extend `data/traces/index.json` toward ≥90%.
3. **W5/treeka** — refresh the read-only treeka gap report so the next rung,
   the crux queue, and the Sanskrit lessons all read from one live index.

Everything after that is ordered by the phases above, and every claim is
reported with its denominator and its replay path.
