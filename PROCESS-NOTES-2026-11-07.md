# PROCESS NOTES — trika-x + openpatala joint session (2026-11-07)

 Targets this session: trika-x + openpatala. Lanes respected: translation-work /
 ipvv / bookfactory / videofactory read-only (their agents own their MCPs).
 Openpatala repo itself read-only for assessment (no writes; its AGENTS gate
 requires MANIFEST registration — notes live here, not there).

## 0. Verdicts up front

- trika-x: NOT finished. Green at small scope (153 theorems / 151 entries + 2
  exemptions, 0 bad chunk refs, bridge BYTES_MATCH, axiom CLEAN), but formal
  coverage 13/154 passage chunks (8%). Peer verdicts (LEAD-REVIEW + PEER-REVIEW
  2026-11-06) stand: useful finite-model experiments, not publication-ready.
  Branch `box/peer-review-batch` dirty. Disk 98% (2.0G free).
- openpatala: NOT finished. README claims Phase 0.6+1.0 complete (1099 works,
  6 proofs + 26 gates + 5/5 conformance + 4/4 red-team PASS), but its own
  peer reviews (PEER-REVIEW-2/3/4) say prototype/theatre: PANDiT char-split
  assertions, empty dossiers, UNKNOWN coverage, 27 P0s in P0-FIX-PLAN, latest
  fixes surface-only (uuid/rfc8785 adopted but not in requirements.txt, old
  impls remain as fallback, weak conformance fixtures). On this box:
  `check.py` path stale, conformance crashes on missing `rfc8785`,
  `data/runs/` absent, 2 commits total, witnesses 0 everywhere.

## 1. openpatala — what was run

```sh
# check gate (stale path per AGENTS.md)
python3 check.py --status            # -> no such file /root/openpatala/check.py
# conformance
PYTHONPATH=. python3 patala/tests/conformance.py
# -> ModuleNotFoundError: No module named 'rfc8785' (env gap; PEER-REVIEW-3
#    predicted exactly this: dep not in requirements.txt)
# evidence bundle (machine-produced, per anti-cheat rule)
python3 -c "import json; d=json.load(open('data/evidence/evidence-bundle.json')); ..."
# -> works 996 / assertions 79 / ext_ids 38 / events 990 / clean_install OK
#    (differs from README 1099/247/108/2181 — stale README or different run)
git log --oneline -15               # -> 51ef45a WITNESS-OCR skill (Nov 6, docs-only, 1 file)
                                    #    4147a19 BUILD-NOTES (Aug 17)
git status --short                  # -> clean
ls data/evidence/ data/runs/        # -> evidence-bundle.json only; runs/ missing
```

Box DBs (trika-x populated `openpatala`, NOT upstream corpus):

```
openpatala (live): works 544 / passages 909 / witnesses 0
openpatala_box:    DOES NOT EXIST (translation-work DB-BACKBONE references an
                   s3://patala/box dump + restore recipe; not restored here.
                   Its doc already warns: local live DB is another track's shape)
disk: /dev/sda1 75G, 73G used, 2.0G free (98%)
```

Peer-review record (their words, not mine):
- PEER-REVIEW-4: "Most of what I built is theatre." PANDiT titles split into
  chars ("Rangacarya..." -> 24 assertions), dossiers 95% empty, coverage UNKNOWN.
- PEER-REVIEW-2: "Architecturally promising prototype, not mass-ingest-safe
  infrastructure." Invariants claimed proven are false.
- PEER-REVIEW-3: fixes are surface (uuid/rfc8785 adopted but old impls remain,
  convenience IDs still truncate to 12 chars, replay test = 5 JSONL roundtrip,
  adapters check dict keys, API uses ambient DB, UUID test 10k not 10M).
- P0-FIX-PLAN: 27 P0s across core/ingestion/identity/schema correctness.
- DEV-PLAN phase map: 1.1 gold dossiers -> 1.2 cross-source identity ->
  1.3 query layer -> 1.4 coverage/frontier -> 1.5 providers -> 1.6 discovery
  -> 1.7 annotation interop -> 1.8 witness collation. All still open per above.

WITNESS-OCR skill (HEAD commit): free-agent OCR -> openpatala spans, docs-only.
Not wired to box DB; witnesses still 0. Treat as proposal, not pipeline.

Reconciliation (openpatala vs box vs R2 vs trika-x bridge):
- Upstream corpus (README/evidence-bundle) != box DB (544/909/0). Box DB is
  trika-x's `openpatala_seed + openpatala_ingest + work_inventory` population
  (availability 260 + dossiers 184 + workdir rows), rerun-idempotent, events
  SKIPPED by design (ID stubs, fabrication refused). Bytes stay on disk/R2.
- R2 `s3://patala/openpatala/` per trika-x bridge/README: schema backup,
  NOT populated DB (dump 0 rows). Row data lives with GitHub repos.
- trika-x bridge: 28 works / 154 passage IDs BYTES_MATCH_SNAPSHOT, witnesses
  UNPINNED (hard-enforced). `source-map.json` 87 works: 6 bridged, 81 todo.
- Meaning: openpatala is the identity *spec + promising code*, box DB is the
  trika-x *working identity store*, bridge is the *locator inventory* between
  translation-work ledgers and that store. None is witness-grade today.

## 2. trika-x — what was run

```sh
git log --oneline -8                # -> 8638008 VBT proposal ... 7c02210 Rung 22 ...
git branch --show-current           # -> box/peer-review-batch
git status --short | head           # -> M tracks/F-LOGs + D swarm drafts (dirty)
python3 formal-trika/tools/evidence_check.py   # -> theorems 153, entries 151,
  # exemptions 2, chunk refs resolve 53 bad 0; direct refs 13/154 (8%);
  # covered: param-p04, phr-p01..04, span-p01, tal-a34-p01, tal-a15-p12,
  # tsa07-p01, tsa08-p01..04; gaps = everything else (see full list in output)
python3 formal-trika/tools/table.py --check       # -> EXIT 0
python3 formal-trika/tools/bridge_resolve.py --check --tw /root/translation-work
  # -> 28 works, 154 passage IDs; ledger bytes match pinned snapshot;
  #    witnesses UNPINNED. EXIT 0
python3 formal-trika/tools/axiom_audit.py --check # -> 76 files, CLEAN
  # (static half; kernel verdict still needs pinned Lean)
```

Standing blockers (unchanged): P-TK1 scholar ruling, rater-2 human pass,
ti/ca + station review, Zenodo token, tau scale quota, Mutate remainder,
diksa policy, journey go, owner flips (ledger/trajectory/vis-mode, sit
player, catalog), TAL emit cadence, svread lingua PR, witness eyes (NGMPP).

Hygiene (must-act): disk 98% — candidates: /tmp/muktabodha (259MB, R2-pinned),
/tmp/vidyut-data (78MB), venvs rebuildable, .git gc/prune only after remote
verify; secrets /root/.env ONLY, rotate pasted R2/Go keys; cron
`/tmp/nightly-verify.sh` ready, NOT installed (owner call).

## 3. What this means for the federated MCP plan

Children own their MCPs (translation / book / video agents building). From
here, without touching their repos:
- Freeze parent contract: `openpatala_work_id + ledger_sha256 + edition label
  + witness:UNPINNED + draft-only if UNRESOLVED` (REGISTRY-FEDERATION shape).
- Spec `formal-mcp` read-only: bridge_resolve / evidence_check / table check /
  treeka gaps. No Lean writes via MCP.
- Prep federation tests: prefix collisions, down-child FailOpen, prove no
  ship/render/publish/send/ISBN/post_id tools exist anywhere.
- Unblocks we own: P-TK1 packet + rater-2 + Zenodo dry-run + next rung from
  gap list (phr mala rows -> VBT clusters, prereg-first).

## 4b. Autonomous run (2026-11-07, continued) — federation-first, no child writes

 Disk (inventory only, zero deletions — pressure is outside our targets):
 - /tmp: ochema2 461M, parab 100M, vidyut-data 78M (re-downloadable, left
   untouched — may be live), nib-pr1 73M, svread-pr8 53M, essayseeds 31M.
 - /root top: projects 6.3G, gcomedy 2.1G, damn 2.0G, kashaudio 1.9G …
 - trika-x .git 15M, openpatala .git 616K (both tiny now). No deletions:
   LEAD-REVIEW forbids deleting shared checkouts / others' work; disk needs
   owner eyes, not agent cleanup.

 Green suite re-proved (this run, all EXIT 0):
 - evidence_check: 153 theorems / 151 entries + 2 exemptions, 53 chunk refs,
   0 bad; direct refs 13/154 (8%).
 - table/vocab/blind/runs-index --check: current/clean.
 - axiom_audit: CLEAN (static half; kernel needs pinned Lean).
 - bridge_resolve --check: 28 works / 154 passage IDs BYTES_MATCH, UNPINNED.
 - unittest: 52 tests OK. control/run.sh PASS. recognition/run.sh 26/0.
   (Note: run.sh needs `export PATH="$HOME/.elan/bin:$PATH"` — bare `sh`
   fails with "Lean 4.34.1 unavailable" despite toolchain present 4.34.1.)

 Specs frozen (new files, our lane only):
 - PARENT-CONTRACT-SPEC-2026-11-07.md — openpatala as federated parent:
   identity block, prefixMode prefixed, FailOpen, entitlements at parent,
   banned surface (ship/render/seal/publish/send/spend/post/isbn/grant/
   signoff/submit), draft-only on UNRESOLVED.
 - FORMAL-MCP-SPEC-2026-11-07.md — 6 read-only tools (bridge/evidence/
   table/gaps/runs/axioms), no Lean/EVIDENCE/ledger writes via MCP.
 - tools/federation_pretest.py — GREEN (26 expected tools; prefix + banned
   + routing + contract). Fixed own bug: substring scan flagged
   "relationships" for "ship" — now exact/prefix name matching only.
   Note: `list_published_essays` (read-only list) correctly NOT banned.

 MCP verification:
 - scholar MCP: `tools/list` → 33 tools, clean.
 - openpatala MCP: SDK not installed (`mcp` package missing) + needs live
   DB — recorded skip, no pip install on 98% disk. Static scan covers it.

 Queue (no code without prereg — none written this run):
 - Next rung: phr mala rows (gap head phr-p05) — PREREGISTRATION-PHR-RUNG.md
   EXISTS. Then VBT clusters per MASTERPLAN-ALIGNMENT backlog order.
 - P-TK1: PTK1-REVIEW-PACK.md prepared 2026-11-06, status UNESTABLISHED /
   NOT reviewed — awaiting scholar ruling.
 - Rater-2: T-C2-RATER2-SHEET.md ready — awaiting second human rater
   (kappa ≥ 0.6 path). 6 review packets MACHINE-COMPILED, awaiting review.

## 4c. Openpatala LIVE run (2026-11-07, continued) — API up, R2 checked

 DB (single live DB `openpatala`; `openpatala_box` does not exist here):
 works 544 / passages 909 / witnesses 0 / editions 101 / etexts 87 /
 assertions 1512 / ext_ids 121. (R2 manifest says assertions 1532 — the
 known −20 delta per translation-work DB-BACKBONE; NOT "fixed" by writing.)

 R2 (`patala` bucket, via boto3 + /root/.r2-env — aws-cli stays broken):
 - `openpatala/box-2026-11-06/manifest.json` — seed manifest: built 2026-11-06
   from trika-x 975cf69 + openpatala 4147a19 + translation-work e05e640,
   PG15-readable `pg_restore` dump (115,225 B), 544/1532/87/87/909/0.
 - `openpatala/SHA256SUMS.txt` — SHAs match trika-x bridge/README
   (dump `0d2d909c…`, repo tarball `9579e264…`). Restore story holds.
 - `openpatala/openpatala.dump` (248,312 B) = schema-only (needs PG18);
   box dump above is the PG15-readable one. No new uploads made.

 Port reality: 8801–8806 + 8799 squatted by 35-day-old `python3 -m http.server`
 fleet (pids 22143xx, ochemapp dirs — NOT ours, left alone). 8802 taken too.
 API started on **8821**: `PYTHONPATH=. nohup python3 -m uvicorn
 patala.api:app --port 8821 --host 127.0.0.1` (log /tmp/openpatala-api-8821.log).
 - `GET /health` → ok 1.0.0, counts match DB (witnesses 0, events 0→5 after
   our /works+/bundle reads — API appears to log query events; observed,
   not judged).
 - `GET /v1/works?limit=3` → real dossiers (translation availability incl.).
 - `GET /v1/bundle/tantrasara` → entity + dossier resolves.
 - `bridge_resolve.py chunk:tsa08-p03 --db` → tantrasara / CANDIDATE-EDITION
   / UNPINNED. Honest (no siglum invented).

 Deps: `rfc8785` installed via `pip --break-system-packages` (tiny pure-python;
 disk still 2.0G free). API imports fine. Conformance re-run: past hashing,
 now FAILS at `test_adapter_conformance: No items discovered` — honest failure,
 consistent with peer-review critique (adapters discover nothing). Upstream
 fix is their lane; recorded, not patched.

 Still open: witnesses 0 (NGMPP eyes), resolver R0–R5 against live data,
 8801 squatter cleanup (owner call — not ours to kill), pm2 `scholar-memos`
 crash-loop (217 restarts — scholar lane, flagged not fixed), data/runs/
 absent upstream, PR #9-style edition_id propagation into bundles.

## 4d. Abhinavagupta corpus completion (2026-11-07, continued) — DB now complete

 Q (user): is openpatala wired up so all translated works are in, with complete
 knowledge of translated works + Abhinavagupta sources incl. lost works?
 A: yes for translated works (100%); Abhinavagupta extant corpus wired;
 lost works seeded as reported-status records (no fabrication).

 1. WORKS: all 102 translation-work workdirs have works rows (112 dirs minus
    10 infra dirs). Nothing missing.
 2. PASSAGES: ledger total 909 = DB total 909. BUT 17 rows were keyed under
    dossier IDs, not tw ids (reconciliation script proved it):
    - paramarthasara 12 rows under PTCND_sa_abhinavagupta-paramArthasAra
    - tsa07-p01 + tsa08-p01..04 (5 rows) under PTCND_sa_abhinavagupta-tantrasAra
    Root cause: ingest maps tw workdir -> dossier key (openpatala-map.json
    CANDIDATE-EDITION links); DB-BACKBONE + REGISTRY-FEDERATION say tw workdir
    is canonical. Fix (recorded, bytes unchanged — ids/locators identical):
    12+1+4 UPDATEs re-keying work_id to paramarthasara/tantrasara-a07/
    tantrasara-a08. Same for 3 edition + 3 etext rows (ids already tw-keyed,
    work_id re-pointed). Total still 909; bridge --check green; API serves
    works/tantrasara-a08 + /paramarthasara with editions+passages. PTCND works
    rows + dossiers untouched (candidate side preserved). No auto-promotion:
    status stays CANDIDATE-EDITION, witnesses UNPINNED.
 3. EDITIONS/ETEXTS: only gap among ledger works was the same 3 (fixed).
    Works without ledgers (abhinavabharati, ipvv-vivrti-vimarsini: source-only;
    mystics: specs only) correctly have none — owning lanes, not gaps.
 4. TRANSLATIONS table: was 16 atlas seeds (external: Gnoli/Dyczkowski/Singh/
    Silburn/Vasudeva...). Patalacheckpoints check (user prompt): their
    texts.ts = separate 17-text Krama/Kula corpus; audited.ts = 11 entries;
    NO lost-works registry, NO ours-status wiring anywhere — so the seed
    below is new, not duplication. It references atlas IDs, never copies.
 5. New seed (trika-x, our lane; box DB only):
    - formal-trika/data/abhinavagupta-corpus.json (finding-aid provenance:
      Wikipedia/Abhinavagupta + verify-via-Rastogi/Torella/GRETIL gap notes)
    - formal-trika/tools/seed_abhinavagupta.py (dry-run default, --apply,
      ON CONFLICT DO NOTHING; mirrors seed_atlas_biblio.py)
    - 8 people (Abhinavagupta + Dupuche/Padoux/Marjanovic/Bansat-Boudon/
      Tripathi/BN-Pandit/Torella; Gnoli etc. already present)
    - 11 works: 7 LOST (Purvapancika, Kramakeli, Sivashaktyavinabhava-stotra,
      Sivadrishti-locana, Padarthapravesha-nirnaya-tika, Prakirnavivarana,
      Kavyakautukavivarana — each with source-quoted basis) + 4
      ATTESTED-UNVERIFIED (Tantroccaya, Tantravatadhanika, Kathamukha-tilaka,
      Bhedavada-vidarana). NO edition/witness/etext claims for these.
      Assertions: TITLE/AUTHOR/LANGUAGE observed + STATUS reported (the only
      non-observed rows in the table, clearly marked).
    - Tantraloka dossier-equivalent: TITLE/AUTHOR/LANGUAGE + KSTS-23 edition
      + 5 biblio translations (Gnoli/Silburn+Dupuche/Dyczkowski/Lakshmanjoo
      from live-verified Nov-6 biblio; rights UNKNOWN).
    - 101 ours translations (seed:ours:<work>:t0): OURS-GOLD-MACHINE-PROPOSED
      (71) vs OURS-PENDING (30); translator [translation-work]; provenance
      REGISTRY sha + GATE.json pointer; human review pending.
    Counts now: works 555 / assertions 1559 / translations 122 / people 20 /
    passages 909 / witnesses 0. Idempotent re-apply clean. API verified:
    /v1/works/lost-kramakeli (LOST + basis), /v1/bundle/tantraloka.
 6. Still open (not ours to invent): GRETIL/Muktabodha manuscript-level
    witnesses (0 box-wide; NGMPP eyes), KSTS-23 volume-level edition rows,
    translator persons for Bansat-Boudon-era scholars beyond names, full
    papers bibliography (biblio gaps list stands), human review of all 71
    golds, P-TK1/rater-2. Files left untracked on box/peer-review-batch
    (no commit without owner ask).

## 4e. Attached-volume deep dive + duplication audit (2026-11-07)

 Attached volume: /dev/sdb 60G @ /mnt/HC_Volume_106959365 (54G used).
 Looks like a full old system image (bin/boot/home/root/workspace, rescue
 tag bitt-rescue-20261021, root mtime 2026-08-13, .bash_history 2026-06-27).
 Port 8801–8806 squatters live on THIS box, not the volume.

 Found: /mnt/.../root/projects/patala — full monorepo @ b2512de (2026-08-14),
 remote prx0r/patala. Live /root/patalacheckpoints (566 commits, HEAD
 31c376f 2026-10-07, remote prx0r/patalacheckpoints) CONTAINS the volume's
 commits (0498769, 03da10a verified in live log) → live is the descendant;
 spun-out repos (wiggly/openpatala, translation-work, …) carry the build
 forward. Volume is superseded — nothing to port blindly.

 Duplication audit (user: "sure we did the bibliography"):
 - patalacheckpoints texts.ts = separate 17-text Krama/Kula corpus (NOT an
   Abhinavagupta corpus). audited.ts = 11 Trika entries (Tantraloka,
   Paratrimsika-vivarana, Vijnanabhairava…).
 - bibliographySeed.ts (volume AND live): IPVV Vimarshini + Vivriti-vimarshini
   (with KSTS/Archive.org scan URLs) + Paramarthasara. My seed does NOT touch
   these works — referenced only. No duplication.
 - "Lost" in volume/live atlas = Utpaladeva's fragmentary Vivrti (33-folio
   Torella), NOT Abhinavagupta's lost works. My 7 LOST + 4 ATTESTED-
   UNVERIFIED registry is new anywhere on disk. No duplication.
 - Ours-translations (101 works status): nowhere on disk. New. No duplication.
 - Tantraloka translations: atlas had Dyczkowski + Singh (seed:atlas:t0/t1).
   My Gnoli/Silburn/Dupuche/Lakshmanjoo rows are additions from the Nov-6
   live-verified biblio. My 5th row (Dyczkowski, seed:trika:t3) DUPLICATED
   seed:atlas:t0 → DELETED from DB + marked skip:true in corpus JSON +
   loader skips it (ids stable, re-run verified at 121, no re-insert).
 - Volume downloads/ (586M old-factory T1/L0/siva-corpus): superseded by the
   translation-work gold pipeline (101 works / 71 gold). DO NOT PORT.
 - Volume openpatala/reference/ (imported OpenAlex docs): absent from live
   wiggly repo; strategy reference only, no data. Left for the openpatala
   lane to adopt or ignore — not copied.
 - Re-key (§4d) is box-DB hygiene under trika-x loaders' purview; bridge map
   (CANDIDATE links) untouched; dossiers untouched.

## 4f. Layer-names: internal codes for us, human names for callers (2026-11-07)

 Owner direction: callers shouldn't see `l0`; keep our personal names as
 comments. Built in trika-x lane (translation-work schemas untouched):
 - formal-trika/data/layer-names.json — 9 entries: code + public slug +
   label + caller blurb + comment (our words, quoted from LAYERS.md/
   mistakes.md: L0 'forks live HERE and nowhere else', C1 'states the
   MATTERS, never the document', L4 'music, never doctrine', …).
   Publics: source, draft-translation, literal-gloss, argument-map,
   reading-translation, essence, register-render, final-translation, song.
 - formal-trika/tools/layer_names.py — to_internal/to_public/describe/
   codes/publics; case/separator-tolerant, fail-closed ValueError.
 - formal-trika/tests/test_layer_names.py — 6 tests GREEN (roundtrip,
   tolerance, fail-closed, codes-stable, comments-present, publics-unique).
 - LAYER-NAMES-SPEC-2026-11-07.md — adoption per lane (additive {code,
   public}, accept-either on input; bare code rename = major version).
   Scholar MCP / site / packs / lingua changes are PROPOSED (lane owners
   dispose); nothing renamed anywhere today.

## 4g. Git-versioned (2026-11-07) — commit 65e0a5c on box/peer-review-batch

 All 10 session files committed + pushed (origin/box/peer-review-batch):
 PARENT-CONTRACT-SPEC, FORMAL-MCP-SPEC, LAYER-NAMES-SPEC, layer-names.json,
 layer_names.py + tests, abhinavagupta-corpus.json, seed_abhinavagupta.py,
 federation_pretest.py, PROCESS-NOTES. Secrets grepped pre-commit (clean;
 local box DSN matches repo-documented convention). Other process's dirty
 files untouched (staged exactly 10, verified via diff --cached --name-only).
 Anyone can now: clone the branch, edit, run the suites
 (evidence/table/vocab/blind/runs-index/axiom/bridge/unittest/Lean harnesses/
 federation_pretest), commit, push — versions accumulate as history. DB state
 itself isn't in git by design; it replays from versioned seeds
 (openpatala_seed + ingest + seed_atlas_biblio + seed_abhinavagupta) per the
 restore recipes. Rules for editors ride along: prereg before code, tiers on
 everything, fail-closed, machine proposes/human disposes, lanes read-only.

## 4h. Children MCPs reviewed + parent gateway built (2026-11-07)

 Children all pushed MCPs (fetched, read-only via origin/master — no tree
 touches except one disposable /tmp worktree, removed + pruned after):
 - translation-work `shastra` (FastMCP stdio, 14 tools) + MCP.md (expansive
   manual) + HANDOVER-2026-11-07-MCP.md. Verdict CLEAN: "No pushes, no
   signoffs, no PASS minting. Ever." promote refuses on gate failure.
 - videofactory `vf_*` (18 tools) + docs/MCP.md (full ref) + tests/test_mcp.
   Gated BUT: vf_launch/vf_queue ship=True default, vf_pack/vf_publish
   publish=True default. Gates hold (approval+green+one-video-law), seal/ears
   owner-only — filed as videofactory#1 (flip defaults to False, opt-in).
 - bookfactory `bf_mcp` (custom NDJSON stdio, 22 tools) + README + tools.py.
   Verdict CLEAN: draft-only previews, gated builds, no ship tool. Note:
   their paths are /home/box (another machine) — re-register with /root
   paths here; owner ruling respected (no Hermes registration).
 Naming: shastra/bf unprefixed, vf_ prefixed — gateway prefixes structurally,
 no renames needed. Wire: shastra FastMCP + vf/openpatala SDK imports missing
 here (pip mcp installed, legacy paths absent) — lanes' problem, FailOpen
 covers it. bf_mcp stdlib-only, runs anywhere (verified live).
 Parent gateway BUILT (trika-x, our lane): formal-trika/tools/
 federation_gateway.py — stdio NDJSON parent, prefixed tools/list, route by
 first segment, FailOpen (dead child excluded, Unknown tool on miss),
 local openpatala__resolve/coverage (source-map backed) + federation__guide.
 Config data/federation-children.json (FEDERATION_CONFIG override).
 Tests: 6 GREEN (live scholar 33 tools + live bookfactory 22 tools
 multiplexed, dead child excluded, routing + unknown-tool verified).
 Videofactory#1 filed: https://github.com/prx0r/videofactory/issues/1.

## 4i. Sanskrit view BUILT + preview-deployed (2026-11-07)

 User: build the Sanskrit tab. Done in svread on branch box/sanskrit-view
 (their repo, owner-directed): header item + ?view=sanskrit (lesson index by
 stage, 10 vendored lessons with Learn/Decode/Recognise tabs, rule boxes,
 witness, recitation guide, practice, provenance). Payload vendored from
 bookfactory 118b227 via svread/tools/emit_sanskrit.py (deterministic,
 fail-closed, no Google fonts, no scripts; 13 data/sanskrit/*.json in release
 manifest). Chat rail built on the Sanskrit path (same rail, ?work= scoped,
 ask-about-this-verse prefill); recitation reuses the reader; mpa + l10
 honestly reader-less (no ledger/projection — owning lanes).
 Tests: new view-contract + real-Chromium render/tab/chat-prefill (zero page
 errors); full suite 38 pass/0 fail. Deployed to branch preview
 https://box-sanskrit-view.svread.pages.dev (verified live: view, lessons,
 rule boxes). Production svread.pages.dev untouched (serves main) — merge =
 lane/owner call.

## 4. Commands to re-verify (copy-paste)

 Review of bookfactory 118b227 (fetched origin/master, read-only): GREEN —
 10 lessons Vol I (sounds→language→instructions, real source_refs), Panini-
 citing rule boxes (curated, stay curated), audio plan 20 clips awaiting
 owner go, gate canonical with exactly 2 DUE-LATER (ship handoff, PDF proof).
 Notes: Google Fonts CDN in lesson HTML (self-host the vendored OFL fonts at
 deploy); :8600 serves on the lane's box only (nothing here).
 Spec SVREAD-SANSKRIT-SPEC-2026-11-07.md (proposal, trika-x lane): header
 item + ?view=sanskrit route (same gated loaders), subdomain reality-check
 (nested sub of pages.dev not provisionable — view now, separate project +
 custom domain later), lesson payload vendored at release (emit step, hash-
 pinned), feature parity table (reader/chat/recitation/scholar/pushing),
 grammar-breakdown ML mapping (deterministic L0 spine first; Vidyut+ByT5
 candidates labelled; Mitra 5,552 + chrF baselines; COMET thresholded-only;
 proof gate over everything; Panini-ML = gap needing its own gold).

## 4j. Qwen realtime voice: reuse, don't rebuild (2026-11-07)

 Q: can the Sanskrit view reuse the Qwen realtime voice stuff? A: yes —
 both voice paths already exist and split the jobs correctly. (1) Recitation
 = Fish Audio POST /api/read → R2 read-v2 cache (s2.1-pro-free); the Learn
 Sanskrit audio-plan plugs in here after owner go. (2) Spoken conversation =
 scholar-voice.js (push-to-talk PCM client) + worker WS proxy
 (scholar-workspace.js:252-307, DashScope allowlist, omni-flash-realtime,
 key server-side, consent + quota + private transcripts). Sanskrit view
 instantiates the same client with lesson context. Switch-on is owner-gated
 (three env flags/keys) + one browser e2e (wire proven, session unverified).
 Gaps recorded in spec §7: pronunciation scoring, Panini-ML gold. Spec +
 notes committed (see push below).

## 4k. Sanskrit rail locked: fish recitation + voice chat, lesson/lore aware (2026-11-07)

 User decision: recitation = fish (pre-rendered R2), right-rail chat = voice
 (same as home). Spec updated (§3 rail row + new §3b context contract): same
 `/api/chat/:work` RAG spine (bge-m3 → gate-weighted → probes/hounds →
 diverse → reranker → arg-packets → lexical fallback → Qwen), scoped to the
 lesson's works, with pinned lesson+lore context prepended like chainCtx
 (verse + L2 + essence + L0 glosses + rule boxes + lore concepts; deterministic
 first, ML labelled). Voice = same ScholarVoice client on the rail (talk →
 transcript-as-message → reply text + audio). Committed below.

## 4. Commands to re-verify (copy-paste)

```sh
# openpatala
cd /root/openpatala && git log --oneline -5 && git status --short
python3 -c "import json;d=json.load(open('data/evidence/evidence-bundle.json'));print({k:d.get(k) for k in ['works_count','assertions_count','external_identifiers_count','events_count']})"
PYTHONPATH=. python3 patala/tests/conformance.py  # expect rfc8785 ImportError until env fixed
# box DB
su postgres -c "psql -d openpatala -t -c 'SELECT count(*) FROM works;'"
su postgres -c "psql -d openpatala -t -c 'SELECT count(*) FROM passages;'"
su postgres -c "psql -d openpatala -t -c 'SELECT count(*) FROM witnesses;'"
df -h / | tail -n 1
# trika-x
cd /root/trika-x && git branch --show-current && git status --short | head
python3 formal-trika/tools/evidence_check.py | head -n 5
python3 formal-trika/tools/bridge_resolve.py --check --tw /root/translation-work | tail -n 2
python3 formal-trika/tools/axiom_audit.py --check | tail -n 2
```
