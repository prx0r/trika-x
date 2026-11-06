# PROCESS NOTES — autonomous endgame build (2026-11-06)

 Companion to MASTER-PLAN.md. Appended same-session as work completes.
 Agent: box (opencode). Owner order: wire + test, 50 todos, realistic
 order, document everything.

## 09:15 UTC — start. Reconnaissance.

- CF token present (env + file), wrangler present — model-quota probe
  deferred to D2/F1 (needs account ID for Workers AI; test then).
- translation-work: 87 passage ledgers; `data/*.argmap.json` machine
  lists (93 units tsa-a08 with speaker/question/premises/…) — B3 is
  consume-don't-reparse. No decisions table — B2 is read-only checker.
- openpatala: full patala/ package (api/query/ingest/gold_dossiers/
  mcp_server). Postgres 15 installable (deb12u1 candidate). R2 dump
  (248 KB, SHA verified) + JSON seeds on hand.
- 50 todos written (A1–A8, B1–B6, C1–C10, D1–D6, E1–E10, F1–F6, G1–G4).
  MASTER-PLAN.md canonical. Blocked items marked, not skipped.
- Order: A → B → C → F(CPU) → D → E → G per plan §Logical order.

## A1 — postgres install + schema restore (running)

## A1–A6 — populated openpatala DB live on box.

- PG15 installed; R2 dump unusable on 15 (needs PG18 header 1.16) —
  built identical 34-table schema from repo migrations/*.sql instead
  (dump's 34 COPYs match 24+10 migration tables; schema-equivalent).
- Loader `tools/openpatala_seed.py` (idempotent, repo-read-only):
  fought 4 schema mismatches, all resolved honestly — ARRAY cols need
  lists not JSON; recorded_at NOT NULL (NOW() = box-load time);
  created_from_event NOT NULL ('seed:gold-dossier-load');
  ext-ids use `identifier` not `value` (all 121); dossier events are
  ID-only stubs → SKIPPED by design (fabrication refused).
- Seeded: 444 works / 442 assertions / 121 ext-ids. Rerun = all-skipped.
  IPVV works present (isvarapratyabhijnakarika et al.);
  tantrasara dossier carries GRETIL ext-id (confirms CANDIDATE-EDITION).
- A6 outcome: NO map change needed — dossier evidence confirms existing
  links; witnesses table 0 rows everywhere (triple-confirmed). Map stays
  honest as-is.
- A7 recipe in bridge/README.md. A8 (NGMPP eyes) recorded BLOCKED.

## B1 — source-record audit next.

## B1–B6 — graph track live.

- B1: 87/87 works carry source records (27 SOURCE.sha + 60 source/*.json
  — two-variant layout accepted, both carry origin; tool source_audit.py).
- B2: 1/87 scholar ledgers (paramarthasara only), 0/87 layer-accept
  decisions (tool decision_check.py; writes are owning lane's job).
- B3: argmap_nodes.py — 249 files → 2269 nodes, 701 uncertainties.
  Join debugging: bare ranges ("1-9") needed prefix-optional regex;
  single-verse ledgers needed single-number parse; stotra works needed
  stotra-aware join (song sNN); cross-work songs (sivasutra span-* =
  spanda chunks) flagged cross_work, never silently merged. Residual 103
  UNKNOWN (4.5%): 71 units in 5 works WITH argmaps but NO passages ledger
  (mpa/deha/rpa/pdva/gita — real pipeline gap for owning lane) + 30
  sivasutra span-p07/08 orphans (no locator anywhere) + 2 misc.
- B4: crux_queue.py — 888 candidates (811 uncertainties + 77 pushing
  probes), formal-adjacent first. Note: top ranks are philological notes,
  not doctrinal cruxes — triage separates them.
- B5/B6: treeka.py keyed work:locator (bare locators COLLIDE: 12 shared
  across works — anu-*/par-* recorded in ambiguous_locators; EVIDENCE
  bare-locator cites inherit the ambiguity, flagged). 909 passages;
  gaps unargued=659, cruxless=70, essayless=250, unformalized=864.
- Tests: test_graph.py 4/4 (range parsing, join rules incl. UNKNOWN +
  stotra, keying, audit smoke).

## C1/C2 — heaps rung (E-HEAP1–4 PASS, recognition 24/24).

- Prereg PD-HEAPS (thin-premise cap, parts-vs-causes parked) → Heaps.lean
  (4 theorems) + 2 surgical twins (dupes, not deletions — first twins
  were over-broad, must_fail rejected them correctly: 2 errors not 1).
- LIVE BUG CAUGHT: `++ [mind]` bound inside flatMap lambda (15 not 11);
  fixed with parens. Evidence for the method, recorded in RESULTS.
- Axioms: 3 zero + [propext]. EVIDENCE 93/91+2 clean. TABLE 89+4 rows.
- Coverage still 7/45 (heaps deepen tsa08-p04).

## C3 — blind-Upaya pilot next.

## C3 — blind-Upaya pilot (SAME ×5, VOCAB-GAP ×1).

- Wrote blind/UpayaBlind.lean from Vocab {ready,pure} only (Upaya.lean
  unread until after); checks clean. śāmbhava/śākta rules regenerate
  IDENTICALLY (same counts, independent writing) — compression-confirmed
  (single-family). āṇava repetition UNFORMULABLE: vocab has no
  counter/step type; Upaya.lean's Nat param predicted as gap, confirmed
  on read. Note: blind/UpayaBlind-NOTE-2026-11-06.md (verdict table +
  justification + lead-agent recommendation; vocab NOT edited to match).
- Flag: same model line as builders — pilot, not replication.

## D2 — CF Workers AI probe next (gates D1-live + F1).

## C3 — blind-Upaya pilot: SAME x5, VOCAB-GAP x1 (COMPLETE).

## D1/D2 — PUSHBACK CLI live (COMPLETE).

- Tool tools/pushback.py: draft + refs → claims.link table → per-claim
  objections (mock deterministic / cf:Workers-AI) → report with
  OBJECTION/Resolution/Honest-remainder; verbatim shielding; NEVER edits.
- CF probe: token works (account 954612af…); llama-3.1-8b "ok" 20 tokens
  0.3 neurons. Live CRUX-01 run on mistral-small-3.1-24b (cross-family):
  3 claims → 2 grounded objections (n=26 pilot, single diarist,
  structure-vs-vocabularies) citing banked entries.
- Live run caught a REAL tool bug: locator lookup keyed file::theorem,
  markers cite locators → "no formal entry". Fixed with locator index;
  re-ran, objections now cite Pramatr-seven etc. Receipt:
  data/pushback-crux01-2026-11-06.md (+ draft). Test: mock + shielding.
- Cost: one draft × 2 objections on 24b — neurons logged per call.

## F2/F3 — CPU calibration next.

## D1/D2 + F2/F4/F6 — PUSHBACK live, calibration logged.

- pushback.py (claim table → grounded objections, mock/cf, verbatim
  shield, never edits). CF token live; llama-8b probe ok. CRUX-01 live
  run (mistral-small-3.1, cross-family): 2 objections with real hits.
  Live run caught locator-lookup bug (fixed, re-ran). Receipt + draft in
  data/. Tests: mock + shielding (23 total green).
- calibrate_gate.py (F2, CPU, imports gate read-only): n=200 gold
  0.710 PASS (false-BLOCK 0.29); truncated 0.885 PASS (coverage blind);
  term-drift 0.725 PASS (consistency vacuous 1.00 everywhere);
  source-repeat 0.090 (abstention works); hallucinated 0.235 (binding
  partial). F4 stamp thresholds/1 = NEEDS TUNING (report
  CALIBRATION-GATE-V1.md + raw log data/calibration-gate-v1.txt).
- F3: BLOCKED on pair data by design (L2/C1 aren't pairs; apparatus
  pilots need explicit alignment first). F1/F5: quota/prototype queued
  behind probe (probe green — F1 runnable next session).

## E-track next (C1 unit + eligibility gate).

## E2/E3 — C1 unit rendered + eligibility gate (COMPLETE).

- tools/eligibility.py: diksha markers → requires-diksha (steps withheld);
  breath/attention/posture → doable + cautions; else study. Fail-closed:
  unknown → study, never doable. Caught live: "Stop breath" word order
  slipped the retention pattern → pattern widened, C1 re-rendered WITH
  retention caution.
- tools/syllabus_unit.py: dhāraṇā 1 → data/unit-vbt-d001.json
  (locator vbt-p03 ✓, no seconds, R-gloss provenance, review status,
  content sha). Tests: test_practice.py (tiers + invariants + sha +
  second-unit render).

## E4/E5/E6/E7/E8 — paths, day-gate, body truth, gaps (COMPLETE).

- path_assemble.py: path:trika/<slug>, spine stations (ts-six/ta-37/
  body-8), diksha units render STUDY-with-conditions (asserted no-DIY in
  code, tested). day_gate.py: Day N = distinct posting dates (tested:
  same-day re-post keeps N, empty days never advance).
- bodymap_check.py: truth + 2 mirrors byte-identical (7992c0db…), rc=0
  tested. One source confirmed (SH1 satisfied as-verified).
- GAPS-VBT-AUDIO.md: 61 unique mapped (doc's 65 = rows incl. dupes),
  51 missing listed; clips 50/50 by filename (SH2 "47/50" stale as file
  count) — open item is human-vs-synth PROVENANCE (their lane's log).
- Practice tests 5/5 (incl. bodymap).

## Remaining queue: C4/C5/C10, D3–D6, E1/E9/E10, F1/F5, G1–G4.

## E4/E5/E6/E7/E8/E1 — paths, day-gate, body truth, gaps, slang (COMPLETE).

- path_assemble.py (path:trika/<slug>, 3 spines, diksha→STUDY asserted).
- day_gate.py (posting-day counts; same-day keeps N; empties never advance).
- bodymap_check.py rc=0 (one truth 7992c0db). GAPS-VBT-AUDIO.md (61 unique,
  51 missing; clips 50/50 filenames, provenance open).
- slang_pack.py: 9 slang files pointer-manifested + consent gate
  (per-session grant, slang never replaces sources, diksha stays gated
  in every register).
- Practice tests 5/5 (test_practice.py repaired twice — edit-hygiene
  note: always include the following line in oldString).

## C5 — āvaraṇa rung (E-AVAR1r–3r PASS; first independent key).

- Second-key hunt (v3/v9/v10/v23): v23 covering-hierarchy immediately
  checkable; v9 embedding parked as designed next size-key.
- LIVE DESIGN BUG CAUGHT: first draft derived links+cover from the SAME
  list (tautological — twin exposed it, must_fail rejected). Amended
  same-day (PREREGISTRATION-AVARANA-RUNG-AMEND.md, no recorded runs
  affected); redesigned to course-rank ascent → genuine finding: ladder
  PARTIALLY ordered (six groups share .mind). Avarana.lean (+twin,
  single-line diff) green; axioms [propext]; EVIDENCE 95/93+2; TABLE all
  rows; control harness extended.
- Score: 95 theorems, 7 receipts, 28 unit tests green.

## Next: C10 applications design, D5/D6 chain+audit, C6/C7 prep, F1/F5, G-track.
