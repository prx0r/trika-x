# PROCESS NOTES — 2026-11-08 (cleanup, MCP hardening, corpus-wide traces)

*Targets: trika-x (writes) + openpatala (read/verify) + svread (read/verify).
Lanes respected: translation-work / ipvv / bookfactory / videofactory /
nibbanahelp read-only; no writes into their repos. Every number below was
measured this session.*

---

## 0. Verdicts up front

- **Clean tree + checkpoint.** The 2026-11-06 swarm dirt is committed in
  logical groups; tag `checkpoint-2026-11-08` set after 73 tests green and
  freshness SHARP. No history rewritten.
- **openpatala last session verified good, not complete.** `check.py` GREEN
  with two recorded BLOCKEDs; box DB 555 works / 909 passages / 102 editions /
  87 etexts / 1559 assertions / 121 translations / 20 people / 0 witnesses;
  API :8821 matches. Abhinavagupta seed idempotent (dry-run 0 re-inserts).
- **MCP surface is real and now documented from measurement.** 104 tools,
  8 families, all five children live. Docs had drifted (98 tools, `book__*`);
  fixed and gated with a machine catalog.
- **Trace coverage jumped 13 → 909.** 236 COMPLETE / 673 PARTIAL, 0 errors,
  every PARTIAL names its gaps.

---

## 1. Cleanup, versioning, checkpoint

Dirty state was the 11-06 swarm refresh: 14:xx expansion runs superseded by
15:49 reruns. Committed by concern (regenerating command named in each body):

| Commit | What |
|---|---|
| `9ee20e5` | `feat(tools)` freshness ledger (`freshness.py` + `data/freshness.json`) |
| `6484c64` | `data(swarm)` 11-06 late refresh; superseded 14:xx runs dropped |
| `c0f229c` | `feat(federation)` formal tool family + TAL binding tests |
| `85688e6` | `docs(plan)` MASTERPLAN2 + REVIEW + SYNERGY-CHAIN + MASTER-PLAN amendment |
| `b9724e7` | `imports` ochema + geometryofthinking mirrors + miner |

**Bug caught during commit:** `formal-trika/imports/ochema` had an embedded
`.git`, so it staged as a gitlink (mode 160000; clones would receive nothing).
Removed the embedded `.git` (frozen reading mirror, matching the ochema2
precedent), re-added as plain files, amended the unpushed commit. Verified
mode 100644 in the index.

Tag `checkpoint-2026-11-08`: 73 tests green, freshness SHARP. Branch
`box/peer-review-batch` is 25 ahead of `main` (main is an ancestor; clean
fast-forward possible). Nothing pushed.

---

## 2. Freshness ledger — numbers become a gate

`formal-trika/tools/freshness.py` records value + reproducing command + source
sha256 for: box DB counts, formal evidence/coverage, bridge, trika traces,
svread traces/source-map/surface, disk (context), git (context).
`--write` captures; `--check` fails on drift.

Design note learned this session: **disk is environment, not a claim.** A
10MB free-space change made `--check` fail; moving `disk` into the context
set (reported, never gating) fixed the false drift. Data claims remain gated.

Added `trika_traces` to the ledger after Q05:
`{"count": 909, "verdicts": {"COMPLETE": 236, "PARTIAL": 673}, "errors": 0}`.

---

## 3. MCP audit and hardening (M01–M05)

### M01 — inventory vs docs

Live gateway (`openpatala-federation`, initialize OK): **104 tools / 8
families**:

```
bookfactory 22 · federation 1 · formal 7 · openpatala 2
openpatala_mcp 5 · scholar 33 · translation 16 · video 18
```

Doc drift found:

1. `FEDERATION.md` and `MODULES.md` said **98 tools** (stale count).
2. `FORMAL-MCP-SPEC` still declared itself **v2 PARTIAL** ("items 1–6 remain
   specced") while all 7 formal tools are live and tested.
3. `PARENT-CONTRACT` naming used `book__quote` / `book-mcp`; the real prefix is
   `bookfactory__` (child ids are literal: `openpatala_mcp__`, `video__`, …).
4. The gateway's own `instructions` text said `book__*` — fixed in code.
5. `tools/federation_pretest.py` expected an invented surface
   (`openpatala__bundle`, `translation__works`, `book__inspect`,
   `video__plan`), so it was green against fiction. Updated to real
   representative names (28), with the full truth moved to the catalog.

### M02 — servers actually work

Every family answered a real call with correct args:
`openpatala__resolve`, `formal__bridge/gaps/evidence`, `scholar__list_works`,
`translation__status`, `bookfactory__factory_overview`, `video__vf_status`,
`openpatala_mcp__get_health` (returns 555/909/… counts). Clean-error behaviour
confirmed (video needs `project`; translation `gates` has a different schema).

### M03 — docs fixed

- `FORMAL-MCP-SPEC` → **v3, IMPLEMENTED** (seven tools; test + catalog
  pointers).
- `PARENT-CONTRACT` → real topology/prefixes/counts; 11 tests; catalog.
- `FEDERATION.md`, `MODULES.md` → 104 tools.
- `MCP-OPS.md` → new operating guide (quickstart, topology, catalog,
  behaviour contract, verification, troubleshooting, known gaps, change
  protocol).

### M04 — conformance hardened

`tools/mcp_catalog.py` probes the gateway and writes
`formal-trika/data/mcp-catalog.json` (`trika-mcp-catalog/1`); `--check` is a
drift gate. Banned-surface check uses **exact/prefix token matching**, never
substring — the first draft flagged `scholar__list_published_essays` and
`video__vf_publish` (both legitimate), repeating the old `relationships`/`ship`
false positive. Added three gateway tests: guide names real prefixes (no
`book__*`), local families present, catalog equals live when all children are
up. Suite: **76 tests OK** (gateway 11).

### M05 — operating guide

`MCP-OPS.md` documents: one stdio parent, FailOpen on children, fail-closed on
identity, `Unknown tool` semantics, `UNPINNED/CANDIDATE/BLOCKED/PARTIAL`,
stdio-only gap (no HTTP/auth yet), and the three verification commands.

---

## 4. Q05 — corpus-wide trace coverage (trika-x side)

New tool `formal-trika/tools/trace_all.py` iterates every `passages.jsonl`
locator and calls `trace_bundle.compile_bundle` (read-only sources: ledgers,
layers, proofs, box DB, EVIDENCE, svread projections). Writes
`formal-trika/data/traces/<work>-<target>.json` + `index.json`
(`trika-traces-index/1`).

Result (measured, 18.5s):

```
909 bundles / 87 works / 0 errors
verdicts: COMPLETE 236 · PARTIAL 673
size: 4.2MB
```

Verification: `trace_bundle.py --verify` re-checked one COMPLETE
(`phrdaya:phr-p01`) and one PARTIAL (`ipvv:chunkA-svatyandya`) — both VERIFIED,
verdicts unchanged. No PARTIAL was promoted; gaps stay named.

Scope note: this is the **trika-x side**. svread's public index still lists 13;
publishing the 909 verify packs via `svread/tools/emit_verify.py` is the svread
lane's next step (Q05 remains open for that half).

---

## 5. Open / blocked (unchanged where human)

- Owner: disk headroom (1.73G free / 96.8%), cron install, R2/Go rotation,
  Zenodo token, Search Console/outreach, dīkṣā policy.
- Scholar: P-TK1, rater-2, ti/ca, NGMPP witness eyes.
- Lanes: translation decision-trail wiring + chunk↔verse map; svread
  emit_verify publication; book/video evidence_refs; nibbanahelp N1.
- openpatala upstream: adapters discover nothing; witnesses 0.

---

## 6. Re-verify this session (copy-paste)

```sh
cd /root/trika-x
git log --oneline -8 ; git status --short ; git tag -l | tail -3

# freshness
python3 formal-trika/tools/freshness.py --check          # SHARP

# MCP
python3 -m unittest formal-trika.tests.test_federation_gateway -v   # 11 OK
python3 tools/federation_pretest.py                      # GREEN
python3 tools/mcp_catalog.py --check                     # SHARP (104 tools)

# full suite
python3 -m unittest discover -s formal-trika/tests       # 76 OK

# traces
python3 formal-trika/tools/trace_all.py --index-only
python3 formal-trika/tools/trace_bundle.py --verify \
  formal-trika/data/traces/phrdaya-phr-p01.json           # VERIFIED COMPLETE

# openpatala (identity root)
cd /root/openpatala && python3 check.py
```

---

## 7. Q14 — peer-review debt disposition (2026-11-08)

*I do not rule on method questions; I record each item's live state with the
command or file that proves it. Rulings stay with scholar/lead/owner.*

### Lead review PR #5 (7 findings)

| # | Finding | Live state 2026-11-08 | Disposition |
|---|---|---|---|
| L1 | Containment misattributed | EVIDENCE provenance labels `R-SOURCE (reconstruction doc, not a chunk)`; registry refs unreviewed by contract | ADDRESSED in mechanism; scholarly ruling on the passage still open |
| L2 | Essay compiler could invent proof status | `essay_compile.py` prints "candidate argmap units, R; bytes rechecked" + "(registry references; proof and textual entailment not checked)"; old expansion drafts remain historical, labels not evidence | ADDRESSED in mechanism |
| L3 | Review-status check not a gate; name promotes to Core | `review_status.py` prints `ERROR: Core promotion is disabled until authenticated, revision-bound review is implemented` | ADDRESSED; identity design OPEN (scholar lane) |
| L4 | Snapshot broke CI | CI installs pinned Lean 4.34.1 by sha256 (`formal-checks.yml`); snapshot pinned | ADDRESSED |
| L5 | Nightly masked failures | `nightly-verify.sh` accumulates per-check exit into `STATUS`, exits non-zero on any failure; skips explicit | ADDRESSED; install still owner call |
| L6 | Roboscholar sends text; receipts not reproducibility | `--allow-external-text` required before any external excerpt; model alias/prompt hash still do not pin build/seed/params | PARTIAL: gate exists; provenance OPEN (owner caps or receipt schema v2) |
| L7 | Reconciliation overstated agreement | `map_agreement.py` returns `POSSIBLE-MATCH` for overlaps, manual review required; composition rechecks ledger hashes | ADDRESSED |

Plus standing method rules (kept, no rulings made): tiers are claims
requiring reviewable evidence (P-PHR4/5 assigned R by inheritance only);
mutant sensitivity ≠ meaningful test (second qualified reviewer still owed);
`cut_arith` stays model-only in EVIDENCE; registry ≠ snapshot; witness/rights/
model-provenance/scholar assessment stay open; disk flagged, no deletions.

### Review request (16 questions) → recorder's answers

| # | Question | Answer with pointer |
|---|---|---|
| R1 | tier-gate or reviewer-eyes? | No tier gate on box today (`evidence_check` verifies existence, not semantics) — reviewer-eyes by design, recorded |
| R2 | second-encoder twin review? | **OPEN**: designer still judges; §6 R-phr twins reviewed by construction only |
| R3 | `cut_arith` in EVIDENCE? | Kept as `TattvaGen.lean :: cut_arith`, explicitly model-only; dropping it is a reviewer's call, not mine |
| R4 | `--promote` with a name? | Promotion refuses (`review_status.py:59`); 0 Core rows — nothing actually promoted |
| R5 | roboscholar nondeterminism? | `--allow-external-text` gate exists; temperature/seed pinning OPEN |
| R6 | agreement receipt-only? | Kept receipt-only (twin-separability); enforcing is a design ruling — OPEN |
| R7 | trinity serving two masters? | Splitting formal registry from bridge snapshot is a design ruling — OPEN; mechanically in sync (BYTES_MATCH) |
| R8 | E-EMB alternative parked | Scholar confirmation still owed (packet item) — OPEN |
| R9 | Nyasa follow-ups | varga second key + order twin outstanding — OPEN |
| R10 | MITRA share-alike scope | Bulk-derivation boundaries need rights ruling — OPEN (scholar/legal lane) |
| R11 | Vidyut sandhi direction | Sandhi-module follow-up is the real step — direction call is owner's/lead's, OPEN |
| R12 | nightly skips Lean | Battery covers evidence/table/bridge/tests; run.sh excluded on time grounds — extend or accept is owner's call, OPEN |
| R13 | disk | Q01 inventory done (§8); deletions need owner eyes, OPEN |
| R14 | swarm calibration owed | Embed re-derivation benchmark still owed — OPEN |
| R15 | formal-refs grammar | PROPOSED (non-binding, lanes dispose): `theorem:<repo>:<path>::<name>` with pinned commit + exact span carried alongside, never replacing the span itself. Current free-form `File :: name` stays candidate-only |
| R16 | independence gap | Second key, Dyczkowski collation, KMT filename all need scholar channel — OPEN |

### Recorded deltas since 2026-11-06

- TW PRs #9–12 merged by their agent (provenance, formal stage, submission
  identity, MITRA grounds). Svread lingua PR status NOT re-checked today.
- Family-2 replication closed (Mistral+Qwen). Blind vocab decision still lead's.
- New this session: P-PHR4/5 rung greens with twins;.trace coverage 909;
  treeka refs 5→14; calibration reproduced; MCP catalog gates.

---

## 8. Q01 — disk inventory (read-only; no deletions made)

```
/dev/sda1  75G  73G  1.6G free (98%)
/root/.cache            958M  (ms-playwright 924M — browser binaries for the svread test suites; pip 24M; rest small)
/tmp/ochema2            461M  (shallow clone; markdown already imported to trika-x; binaries NOT imported — re-clone restores)
/tmp/parab              100M  (live, untouched)
/tmp/vidyut-data         78M  (re-downloadable)
/tmp/svread-pr8          53M
/tmp/nib-pr1             73M  (from 11-07 inventory)
/tmp/essayseeds          31M  (from 11-07 inventory)
formal-trika/data/traces 4.2M (new today, 909 bundles)
```

Largest safe reclamation candidates (owner decision, in order): `/tmp/ochema2`
(461M; reading mirror already vendored + provenance recorded) →
`~/.cache/ms-playwright` (924M; breaks svread browser tests if removed — only
with explicit owner go) → shared-checkout review (`/root/projects` 6.3G,
`gcomedy` 2.1G, `damn` 2.0G — outside our targets, never touched).

---

## 10. Q08 receipt (2026-11-08)

`runs/runs.jsonl` @ 2026-11-08T06:29:49Z, rev `ab5dfcc`: control exit 0,
recognition exit 0, tc1 exit 0. Control tail includes both new twin refusals.
Full harness run detached via `setsid nohup … & disown` (plain `&` dies with
the tool call — see §9). Coverage: 155 theorems / 153 entries, 14/154 chunks.

---

## 11. Q01 — disk candidate ranking (2026-11-08, read-only)

Box: 75G disk, 73G used, 1.6G free (98%). Every repo below is a live git
checkout — nothing deleted, nothing `gc`'d. Ranked by reclaim vs risk.

### Tier 1 — rebuildable from lockfiles (~2.4G, owner go)

- `manuscriptAI/node_modules` (1023M): `package-lock.json` present, `npm ci`
  rebuilds. Live quill-app repo — rebuild before next deploy/test.
- `content/moneyprinterturbo/.venv` (754M): `requirements.txt` present. LOW.
- `engines/.venv` (631M): numpy/opencv/onnx stack, no requirements file —
  `pip freeze` first, then rebuild. MEDIUM (feeds sleepdraw comparisons).
- `freaktown/node_modules` (167M): lockfile present. LOW.

### Tier 2 — committed binaries / history (~1.6G, surgery not deletion)

- `kashaudio/.git` pack (1.11G): `verify-pack` shows committed renders
  (`shiva_render/shiva_ch01.mp4` 18M, `cards/trad/*_full.mp4` 12M,
  `shiva_render/audio/*.m4a` 10M). In sync with `origin/main`, so re-clone
  saves nothing — needs filter-repo or media-to-R2/LFS.
- `projects/.git` (530M): top blobs `generated-data.ts` 17M + seed JPEGs
  ~4M; accumulated history. Audit before surgery.

### Tier 3 — /tmp + caches (~1.6G, verify-then-remove)

- `~/.cache/ms-playwright` (924M): removal breaks svread browser tests;
  reinstall via `npx playwright install`. Owner go only.
- `/tmp/ochema2` (461M): markdown already vendored to trika-x with
  provenance; binaries never imported. Verify no live user, then remove.
- `/tmp/vidyut-data` (78M): re-downloadable.
- `/tmp/nib-pr1` + `/tmp/svread-pr8` + `/tmp/essayseeds` (73M + 53M + 31M):
  stale workdirs by shape — verify, then remove.
- `/tmp/parab` (100M): 11-07 notes say possibly live — DO NOT TOUCH.

### Do not touch

Chain repos (`translation-work`, `trika-x`, `svread`, `openpatala`,
`sanskritbench`, `nibbanahelp`). Any `.git` of an active repo. Shared
checkouts outside our targets (`/root/projects` 6.3G, `gcomedy`, `damn`,
`content-sources`, `blueteam`) — owner eyes only.

### Arithmetic

Tier 1 + safe Tier 3 ≈ 3.1G freed → ~94%. Plus playwright ≈ 4G → ~92%.
Tier 2 surgery ≈ +1.6G but is a project, not a deletion.

---

## 12. Q01 execution — Tier 1 reclaim (2026-11-08, owner-approved)

Safety checks before removal: no live process rooted in the three targets
(`vite preview` IS running from `freaktown/node_modules` → freaktown
SKIPPED, owner to stop that server first); all three targets gitignored;
`manuscriptAI` and `content` trees clean. Engines venv frozen first:
20 pins saved to `/tmp/opencode/engines-venv-freeze-2026-11-08.txt`
(numpy 2.4.6, opencv-headless 5.0.0.93, onnxruntime 1.31.0, …).

Removed:

- `/root/manuscriptAI/node_modules` (1023M) — rebuild: `npm ci`
- `/root/content/moneyprinterturbo/.venv` (754M) — rebuild:
  `pip install -r requirements.txt`
- `/root/engines/.venv` (631M) — rebuild: `pip install -r <freeze file>`

Skipped: `freaktown/node_modules` (167M) — live `vite preview` server.

Result: 1.3G free (99%) → **3.7G free (96%)**, +2.4G. Source files,
manifests and lockfiles verified intact after removal.

---

## 13. Q13 pilot — propose loop, one crux (2026-11-08)

`crux_queue.py` refreshed: 882 candidates, priority 0 = works with registry
references (param-p02 head: v15/v16/v18 uncertainties, EXACT_LOCATOR).
`roboscholar.py` (qwen3-30b-a3b-fp8, `--allow-external-text` explicit) drafted
one paragraph + 5 claim bullets from banked premises only; claim table 2/2
CITED; audit 12 checks; receipt `robo-param-p02-2026-11-08-071651.receipt.json`.
`pushback.py` (mistral-small-3.1-24b, different family, same opt-in) filed
2 objections with honest remainder: claims are R reconstructions, no formal
entries for these locators — correctly refused as authority.
Files: draft + receipt + `.pushback.md`, all MACHINE-PROPOSED, owner +
scholar dispose. No signoff, no publish. Quota spent: none (CF free neurons).

---

## 14. N05/N06 — VBT rungs (2026-11-08)

P-VBT1 (prereg `PREREGISTRATION-VBT-RUNG.md`): opening question banks
exactly 8 candidate-form terms (ARGMAP roster + L2 v.2–v.4 + C1).
`control/Vbt.lean`, twin `BrokenVbtSeven` (drop anacka) refuses.
P-VBT2 (`PREREGISTRATION-VBT2-RUNG.md`): p02 frees exactly 3 coordinates
(dik/kāla/kalanā; L2 v.14 + C1 SUMMARY enumeration). Twin
`BrokenVbtTwoCoords` refuses. Rejected this session: "p02 negates the 8
p01 terms" — false on held spans (v.11 also negates bhairava; kalā not
explicitly negated); recorded in the prereg so it stays dead.
Coverage now 157 theorems / 155 entries, 16/154 chunks (10%);
unformalised 893; queue head vbt-p03. Full harness receipt running
detached; commit lands with the receipt.
