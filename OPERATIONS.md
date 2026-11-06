# OPERATIONS — running the whole machine (canonical manual)

**Covers:** box postgres (openpatala) + formal-trika + graph track +
practice compiler + bench + model rails. Read-only where lanes require.
Every command below was run green 2026-11-06; re-run to verify.

## 0. One-command health check

```sh
export PATH="$HOME/.elan/bin:$PATH"
python3 formal-trika/tools/evidence_check.py --root /root/translation-work
python3 formal-trika/tools/table.py --check
python3 formal-trika/tools/vocab.py --check
python3 formal-trika/tools/blind.py --check
python3 formal-trika/tools/runs-index.py --check
python3 formal-trika/tools/bridge_resolve.py --check --tw /root/translation-work
python3 formal-trika/tools/axiom_audit.py --check
python3 -m unittest discover -s formal-trika/tests          # 33 green
sh formal-trika/control/run.sh                              # needs Lean 4.34.1
sh formal-trika/recognition/run.sh
python3 -m unittest discover -s /root/ipvv/tools/qp_acom -p "test_*.py"  # 11
su postgres -c "psql -d openpatala -t -c 'SELECT count(*) FROM passages;'"  # 909
```

Nightly read-only cron (proposed, NOT installed — owner call):
`0 3 * * * /tmp/nightly-verify.sh` (script ready; logs only, zero writes).

## 1. Box database (openpatala, postgres 15, survives reboot)

- Service: `postgresql` (enabled). DB `openpatala`, role `patala`/`patala`.
  DSN: `postgresql://patala:patala@localhost:5432/openpatala`.
- Schema: repo migrations (NOT the R2 dump — needs PG18; schema-equivalent,
  34 tables). Restore: `bridge/README.md` §Local populated DB.
- Seeds (idempotent, rerun = +0): `tools/openpatala_seed.py` (444 works,
  442 assertions, 121 ext-ids) then `tools/openpatala_ingest.py`
  (87 editions/etexts, 909 passages) then `tools/work_inventory.py --db`
  (107 works + 1070 HAS_LAYER assertions + activity row).
- Contents: works 544, assertions ~1530, editions 87, etexts 87,
  passages 909, witnesses 0 (enforced empty — R2 audit).
- Rules: bytes stay on disk/R2 (DB holds hashes+URIs); dossier events
  SKIPPED (ID stubs — fabrication refused); new tables need openpatala
  lane review (never ALTER from here); R2 dump re-check on any restore.

## 2. Formal track (Lean 4.34.1 via ~/.elan; commit 5045d005)

- `control/run.sh` — positives + must_fail twins (12 checks). Adding a
  file: compile line (+ `-o X.olean` if imported, + LEAN_PATH=. line if
  it imports), `check` line, `mustfail` line. Twins: single-definition
  diff, same statement, exactly-one-error (harness enforces).
- `recognition/run.sh` — same pattern (26 checks).
- New theorems: EVIDENCE.json entry (single-line format! never
  `json.dump` whole file) + TABLE-READINGS.md `## File :: thm` +
  `tools/table.py` SOURCES list + RESULTS.md append-only section +
  `record_run.py` + `runs-index.py` regen. Axiom audit: 107 CLEAN
  (73 zero-axiom); static gate in CI.
- Prereg BEFORE code (new dated file; historical never edited).
  Corrections = new dated files (TK-R2 + AVAR precedents).
- Mutate sweep: needs 4.33.1 (`elan toolchain install leanprover/lean4:
  v4.33.1`, ~2.9G — check `df` first!); `lake env lean --run
  /tmp/Mutate.lean/Mutate.lean FILE`; uninstall after; triage rule:
  vacuous-enumeration survivors = noise, sharpness-class = real.

## 3. Graph track (pure python, no Lean)

`source_audit.py` (87/87) → `decision_check.py` (1/87 ledgers — owning
lane) → `argmap_nodes.py` (2269 nodes; join rules: bare ranges, singles,
stotra-aware, song→chunk, cross_work flags; UNKNOWN = real gaps) →
`crux_queue.py` (888) → `treeka.py` (909 keyed work:locator; 13 ambiguous
recorded) → `tensions_export.py` (public headers only — VOICE RULE in
test). Regenerate in that order; all deterministic.

## 4. Practice compiler (syllabus C-series)

`eligibility.py` (study/doable/requires-diksha, fail-closed unknown→study,
A-APP1-cited) → `syllabus_unit.py` (C1: source refs, no seconds, R-gloss
provenance, review status, sha) → `unit_to_score.py` (syllabus steps, NO
timings, diksha emits zero steps — asserted) → THEIR compile_syllabus.py
(reviewer fills TODOs) → `path_assemble.py` (spines, no-DIY assert) →
`day_gate.py` (posting-day counts) → `bodymap_check.py` (one truth) →
`slang_pack.py` (pointers + consent gate). VBT/audio gaps in GAPS doc.

## 5. Bench + model rails (free first, quota never for grunt)

- CF REST (neurons logged) + beam-free via `/root/scripts/go_beam.py`
  (key ONLY in `/root/.env` 0600; session header + UA required).
- `tau_pilot.py` (cross-family judge), `calibrate_gate.py` (thresholds/1
  NEEDS TUNING — do not lower gates without re-running), `roundtrip.py`
  (uncalibrated prototype), `pushback.py` (mock/go:/cf:, verbatim shield,
  never edits).
- ox-alpha quota: planning/codegen ONLY (owner policy). Grunt = CF/beam.

## 6. Hygiene rules (learned this session, keep)

- EVIDENCE.json: single-line entries, python line-surgery (never whole-file
  dump); evidence_check catches slips (fail-closed proved itself).
- TABLE: SOURCES list + readings must grow with every new Lean file
  (`--check` is vacuous otherwise — caught once).
- test_*.py edits: never bare-def-line oldStrings (3 syntax breaks);
  prefer heredoc appends; always run suite after editing tests.
- /tmp is symlinks-aware (`/tmp/ipvv` → repo — never delete blindly);
  disk checks before big installs (4.33.1 = 2.9G); clean /tmp fetches
  same session (R2/GRETIL/MIRI downloads).
- Secrets: `/root/.env` ONLY; repo-wide grep before every push;
  rotate anything pasted in chat.
- Lanes: translation-work ingest + ipvv worker/deploys + other agents'
  repos = read-only + specs + notes. No force-push (rebase only).

## 7. Known quirks (don't "fix" blindly)

- spanda passages '20-3' (reversed range — parser swaps; flag, don't edit).
- sivasutra/data/span-p*.argmap.json = spanda chunks (cross-work, flagged).
- 5 works with argmaps but no ledgers (mpa/deha/rpa/pdva/gita).
- anu-/par- locator collisions across works (13 ambiguous, keyed apart).
- top-level mystic stubs vs mystics/* bytes live apart (record vs bytes).
- Pratyahara maxRecDepth bump (documented, still decide).
- Blind vocab lacks transition indices (VOCAB-GAP recorded).

## 8. Arrivals ritual (session-start canon — the swarm outruns sessions)

1. `python3 formal-trika/tools/arrivals.py` — HEAD vs snapshot/nodes pins.
2. If DRIFT: `--rebuild` (nodes/queue/treeka), then re-pin snapshot ONLY via
   `build_passage_snapshot.py` after any EVIDENCE edits (trinity lockstep).
3. Canonical checkout is master before pins (F4: branch reads lie).
4. Other lanes' trees are read-only + never rebased through dirty work.
