# HANDOVER — trika-x endgame build (2026-11-06 mega-session)

**For the next agent. Read this + AGENTS.md + MASTERPLAN-TECHNICAL-SPEC.md
first. Everything below verified at push time; rerun §2 to confirm.**

## 0. Owner vision — VERBATIM (do not paraphrase, do not shorten)

> rn im getting the translation-work agent to basically automate their pipeline so that openpatala becomes like control panel.. im thinking we can do this for the whole system right everything dervises from openpatala sansrkit all the way up the chain up to c2 style translations to scholar essays and peer review /bookfactory video/factory it all becomes simple like functions from agent working over openpatala then we can then essentially get a work offload transaltion to transalter-work tehn get some vidoes made, perhaps a condensed book ,formalise it all and then write essays on it drafted for scholar to review and then teh scholar basically eners into 'pushing' type workflow and this itself is what create the essay its more enquiry hooked up to the rest of trika

**What it means (interpretation, kept separate from the words):**
openpatala is the control panel. An agent picks a work off it and the
whole chain runs as functions over openpatala: ingest → translation-work
pipeline (automated through C2) → scholar essays + peer review →
bookfactory (condensed book) → videofactory (videos) → formalisation →
essay drafts → scholar review → scholar enters a pushing-type enquiry
workflow hooked into the rest of Trika — **and the enquiry itself is
what creates the essay**. Functions, not departments.

## 1. Session inventory (all pushed to prx0r/trika-x main)

| Commit | What |
|---|---|
| b069256 | E-EGO ego-origin rung + sharpness hardening + TK-R2 prereg |
| 77bcdf4 | SOTA gates (axiom audit, Mutate sweep wrapper, kappa, witness candidates, source-map generator, R2 audit, TABLE coverage) |
| de6cb8a | Heaps/Avarana/Application rungs + graph track + practice compiler + pushback/calibration live + openpatala seed + master plan |
| f42a2ea | 50-todo autonomous build (rungs, graph, practice, pushback, calibration, seed, geometry) |
| 80e9c82 → cce66a0 → b730c6d | Nibbanahelp / deitybody / sanskrithelp synergies |
| f935ab1 | Consolidated process notes (531 lines) + scoreboard |
| 9073a25 | **Merge PR #4** (Sanskrit corrections — see §4) |
| 975cf69 | PR #4 wired across tree (36 tests green) |
| 44e1a09 | OPERATIONS + NEXT-STEPS docs |
| 60331ff → 946ce3e → de6cb8a…c49096d | Backbone (DB, ingest, bridge --db, Nyasa rung, advice, R2 dump) |
| 1862bca | **Merge PR #4 follow-ups** (joins, study-only, T-C1) |
| 4a2d39b | Endgame spec §12 + wiring |
| 8b7d00e | E-EMB embedding rung (5×5 containment, surgical twin, 124 theorems) |
| + this push | Step-1 reconciliation (agreement + composition tables, source_audit v2, ADVICE §6) |
| + beam/MV/synergy commits | go_beam.py lives in /root/scripts (NOT a repo); R2/box work logged |

Plus: svread `source-map.json` (d5bfe9f); ipvv acom/0.2 (c2cb6b35, rebased).

## 2. Green state (rerun to confirm; all green at last push)

```sh
export PATH="$HOME/.elan/bin:$PATH"   # Lean 4.34.1 lives here
sh formal-trika/control/run.sh        # 20 PASS incl. 12 mutants
sh formal-trika/recognition/run.sh    # 26/26
python3 -m unittest discover -s formal-trika/tests   # 46 green
python3 formal-trika/tools/evidence_check.py         # 121/119+2, 0 problems
python3 formal-trika/tools/table.py --check \
  formal-trika/tools/vocab.py --check \
  formal-trika/tools/blind.py --check \
  formal-trika/tools/runs-index.py --check \
  formal-trika/tools/axiom_audit.py --check          # 107 CLEAN
python3 formal-trika/tools/bridge_resolve.py --check --tw /root/translation-work
python3 formal-trika/tools/map_agreement.py --tw /root/translation-work
python3 formal-trika/tools/compose_bridge.py --tw /root/translation-work
python3 formal-trika/tools/source_audit.py --tw /root/translation-work
su postgres -c "psql -d openpatala -t -c 'SELECT count(*) FROM passages;'"  # 909
```
Formal: **124 theorems** (80 zero-axiom), 20 refusing mutants, EVIDENCE
122 entries + 2 exemptions, 0 problems; TABLE all rows; axiom CLEAN.
Reconciliation: 102-work agreement (3 AGREE / 21 THEIRS-NEW / 63 proposals /
15 open, 0 conflicts); 7-work composition (3 COMPOSED / 3 PARTIAL / 1
DOUBLE-GAP = tal-a15); records 55 RECORDED / 47 NO-SOURCE / 0 invalid.
Box DB: works 544, passages 909, witnesses 0 (enforced). R2 mirror:
`s3://patala/openpatala/box-2026-11-06/` (restore-proven).

## 3. Control-panel architecture (the vision, formalized)

```
openpatala (works/editions/etexts/passages/witnesses)
  │  ingest: openpatala_ingest.py (87 works) + Mode B (new files)
  │  resolve: bridge_resolve chunk:X [--db]
  ▼
translation-work.run(work_id)      # THEIR lane; automated pipeline to C2
  │  T1→L0→argmap→L2→C1→C2 per chunk; decision trails; pair emission
  ▼  (passages.jsonl locators == DB citation_value — verified)
formalize(chunk) -> Lean theorems  # prereg → model → twin → evidence
  │  treeka.formal column; gap report drives queue
  ▼
argue(chunk) -> nodes → crux queue → pushing probes
  ▼
essay(chunk|tension) -> draft → claims → audit → PUSHBACK → review → sign → DOI
  ├─► book(work): frozen layers → TEXT-GATE → paperback/postcard/social
  ├─► video(crux): pack (+evidence_refs) → sealed mp4 (GOLDEN gates)
  ├─► teach(unit): syllabus → score → path → slang register (consent)
  └─► practice → diary → teacher read → NEW QUESTIONS re-enter as cruxes
        ▲                                                        │
        └────────── scholar pushing-enquiry hooks here ──────────┘
              (enquiry hooked to Trika IS the essay engine)
```

Each arrow is a working function today EXCEPT: witness verification,
chunk↔verse map, pair emission, Zenodo token, rater/scholar rulings,
factory evidence_refs, owner-gated builds (ledger/trajectory/vis-mode).
Specs for each live in BACKBONE.md §5 / CHAIN-GAP doc / NEXT-STEPS.md.

## 4. PR #4 record (reviewed twice, both merged)

- 9073a25: Sanskrit corrections (kalā-in, pure-5, faculties 11-wombed,
  inventory list, māyā-control; Grace/Upaya/Application scope; study-only;
  opt-in). Key compound verified in T1 pre-merge. My overclaims corrected
  via dated records (TK-R2 ratio downgraded, A-APP consumed withdrawn).
- 1862bca: join rewrite (chapter-aware, reason codes, rev pinning),
  study-only exports, descriptive T-C1, synthetic tests. One run.sh
  conflict (mine kept). PR open as review record; head commits commented.

## 5. Blocked / resume paths (nothing vague)

- Witnesses: `bridge/witness-candidates.json` (NGMPP records) → manuscript eyes.
- Chunk↔verse + source_verses: CHAIN-GAP doc → translation-work/scholar lane.
- P-TK1/ti-ca/rater-2/station-full: packs + harnesses ready → scholar/owner.
- Zenodo live: dry-run builds → owner token. Tau scale: pilot logged → quota.
- Frontier: KMT-17 READY (GRETIL) → ṢaṭSS (fetch M00249) → KuRatnUdd (acquire).
- Nyasa follow-ups: varga rules need second key; v9 embedding designed.
- Tokens: R2 + Go keys pasted in chat — ROTATE. Secrets: `/root/.env` ONLY.
- Disk 3.5G: venv 631M + .git 2.3G + content dirs need owner eyes (full table
  in chat 2026-11-06; rail-db/telegraph/humor/deitydb removed already).
- Cron: `/tmp/nightly-verify.sh` ready, NOT installed (owner call).

## 6. Rules for the next agent

Tiers on everything; prereg before code; corrections = new dated files;
fail-closed (errors ≠ passes); single-line JSON surgery (never whole-file
dumps); def-line edits include the following line (3 syntax breaks this
session); lanes read-only (translation-work/ipvv/others' repos: specs +
notes only, rebase never force); secrets grep before every push; disk
check before big installs; process notes appended same session.
Box model rails: beam-free ($0, go_beam.py) + CF REST (neurons logged);
ox-alpha quota for planning/codegen ONLY.
