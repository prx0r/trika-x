# SYNERGIES — nibbanahelp × formal-trika (2026-11-06, read-only discipline)
*Status: PROPOSED. Lane-facing proposal; owning lane disposes.

All reads of nibbanahelp are read-only from here (their lane, VOICE RULE,
active agent today). Writes land in trika-x only. Nothing below edits
their content, worker, site, or schemas.

## S1. Mālinī order verified (N1, DONE)

deitybody `data/malini_order.json` (50, na→pha) == MV 3.36–41 order
(MIRI M00160 fetched live this session); TĀ-15 GRETIL text same skeleton
+ 5 reading variants logged. Extract: `data/mv3-malini-vv36-41.json`
(CC BY-NC noted). Method note: raw token scans can't verify sandhied
verse (11/50); anchors + parsed structures carry the check; Heritage
parse still open. Feeds: nyāsa rung (PHONEMIC-BODY-SPEC updated with
three-nyāsa character + ORDER key).

## S2. Tensions → crux queue (N3, DONE)

`tools/tensions_export.py`: public tensions only (headers+status, never
body text) → `data/tensions-export.jsonl` (3 tensions, 3 open). Treeka
merges next (crux queue currently argmap+pushing; lived-tension join is
the N-side input to essayless-crux prioritization).

## S3. Day-gate halves (N4, NOTED — no code change)

Journey truth = their tz-lock (Asia/Bangkok, git-committed) + repo-derived
day numbers + my posting-day counts (`day_gate.py`). Complementary, not
competing: tz answers "which day is it", repo answers "which days exist",
counts answer "how many posting days". Their journey-ledger spec (owner-
gated, NOT BUILT — respected) already designs ordering/existence/authorship
on transparency-log pattern (CT/Rekor/Go-checksum); my day_gate.py is a
compatible micro-implementation of the counting third. No action until
owner goes on the ledger.

## S4. R2 env mapping (N5, NOTED)

Theirs: `/root/.r2-env` (`R2_ACCESS_KEY_ID`, fixed today from
`R2_ACCESS_KEY` crash). Mine: `/root/.env` (`R2_PATALA_*` staging set).
Pattern for any shared client: accept both names (their fix's pattern),
never print values. No shared client built (no need yet).

## S5. Teacher-stage0 as review surface (N6, REVIEWED — their build)

Local decode-review (inspect/correct machine-proposed decodes; journal
private, never auto-committed; contradictory sets refused). Directly
unblocks OUR T-C2 (rater-2 surface exists!), station full pass, ti/ca
signatures — WHEN the owner corrects. Consumer plan (ours, read-only):
watch `~/.local/share/nibbanahelp/teacher-revisions.jsonl` (if shared)
or re-run kappa/station/ti-ca harnesses against corrected decodes on
owner signal. Teacher-endgame spec (today, their lane) already cites
STATION-TABLE/UPAYA-CRITERIA/TREC/GRACE-AUDIT as PILOT inputs and
names the teacher-as-assessor reading diary through the formalization
(station/means/conjuncts/grace) — convergence recorded, not duplicated:
their assessor READS our models; our models do NOT depend on their relay.

## S6. Outstanding (theirs; NOT mine to build)

journey-ledger (owner-gated), trajectory-endgame (NOT BUILT, prerequisite
for teacher Stage 1), jev-register-gate (LATER), vis Trika mode (lens,
not mapping — their doc already refuses the lobha-mala merger; concur),
hxrmxs-bulk Vectorize migration, nibbanahelp N1 sessions→queue (my N3
covers the tensions half; sessions half waits on their schema call).

## S7. What I did NOT do (lane respect log)

No edits to nibbanahelp content/worker/site/sessions/tensions/schemas;
no relay weight changes; no index rebuilds; no deploys. MV e-text lives
in /tmp (extract in trika-x data/ with license); full text stays at MIRI.
