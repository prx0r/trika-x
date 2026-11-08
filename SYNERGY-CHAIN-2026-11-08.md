# SYNERGY CHAIN — how openpatala, trika-x, svread and the factories compose

*2026-11-08. Canonical chain-of-events doc. Companion to `MASTERPLAN2.md`
(what to build, in what order) and `formal-trika/data/freshness.json` (what the
numbers are, and how to reproduce them). This file answers a different
question: **how the parts feed each other, and what keeps the seam clean.***

---

## 0. Verdict on last session's openpatala work — yes, it was good work

Not "complete", but real and honest:

- `check.py` exists and reports PASS/FAIL/BLOCKED (BLOCKED ≠ PASS).
- Box DB is a working identity store: **555 works · 909 passages · 102
  editions · 87 etexts · 1559 assertions · 121 translations · 20 people ·
  0 witnesses**. API live on `:8821` with matching counts.
- Seeds are idempotent: `seed_abhinavagupta.py` dry-run reports
  `people 0; works 0; assertions 47; editions 1; translations 105` — i.e.
  already applied, no re-inserts.
- Two blockers are recorded, not hidden: adapters discover nothing
  (upstream), witnesses are 0 (needs manuscript eyes).

So openpatala moved from "spec + theatre" to **a gated working identity
root**. The remaining work is coverage and witnesses, not foundation.

---

## 1. The canonical chain (one event order, never mixed)

```
accession ──► artifact ──► observation ──► candidate ──► resolution
   openpatala (identity)                                   │
                                                           ▼
                                          Work / Edition / EText / Passage
                                                           │ chunk locator
                                                           ▼
                        translation-work (layers T1→L0→argmap→L2→C1→L3→L4)
                                                           │ sha256 per layer
                                                           ▼
                        trika-x (formal theorem + prereg + twin + EVIDENCE)
                                                           │ trace bundle
                                                           ▼
                        svread (emit_verify: exact bytes + manifest)
                                                           │ curl + sha256
                                                           ▼
                        essay (claims → audit → PUSHBACK → human sign)
                                                           │ signoff + bridge
                                                           ▼
                        release ──► Zenodo DOI ──► pack ──► video
                                                           │
                                                           ▼
                        lesson / practice / diary echo ──► new crux
```

At every hop the payload is the same shape: **bytes + hash + status + where to
re-fetch**. A hop that cannot name its input fails closed.

| Hop | Creates | Carries forward | Gate | Owner |
|---|---|---|---|---|
| accession | artifact (sha512), raw observation | exact response bytes | fixity (one byte changes → fail) | openpatala |
| identity | Work/Edition/EText/Passage | openpatala work id, edition label, `witness: UNPINNED\|VERIFIED` | resolver R0–R5; never invent a witness | openpatala |
| ledger | chunk + layer files | locator (`tsa08-p03`), layer sha256, `GATE.json` | deterministic gates, proofs | translation-work |
| formal | Lean theorem, EVIDENCE, TABLE row | chunk → named theorem + run receipt | prereg → model → must-fail twin → audit | trika-x |
| trace | trace bundle + verify pack | immutable id, layer hashes, verdict (COMPLETE/PARTIAL) | every hash reproduces; PARTIAL labelled | trika-x + svread |
| essay | draft → claims → audit → PUSHBACK | claim table, verbatim spans, honest remainder | audit PASS; PUSHBACK cross-family | scholar lane |
| publish | signoff → branch → release → DOI | signed snapshot, rights, provenance | 409 on post-sign edit; no auto-merge | owner/scholar |
| render | pack (`read\|comic\|parable\|diagram`) → sealed mp4 | `evidence_refs` (work/locator/ledger-sha) | refuse render without refs; GOLDEN gates | factories |
| teach/practice | lesson, unit, path | source refs + eligibility (study/doable/dīkṣā) | eligibility gate; STUDY-only until signed | trika-x + satsang |
| diary | private tension/entry | consent scope (explicit, revocable) | VOICE RULE; no auto-publish ever | nibbanahelp |

---

## 2. Synergy rules (why this composition and no other)

1. **openpatala is identity, never truth.** A work id plus a shared GRETIL
   string is a candidate mapping, not a proven edition. UNPINNED/UNKNOWN are
   valid states.
2. **translation-work is evidence.** trika-x reads its layer bytes and writes
   nothing back. Their lane owns the pipeline; we own verification of it.
3. **trika-x is the verifier, not a second store.** `treeka.json`,
   `data/formal.json`, `source-map.json` are **derived indexes**: delete them
   and they regenerate from ledgers + traces. If an index cannot regenerate,
   it is a source of truth in disguise — refuse it.
4. **svread is the surface and the publication gate.** `emit_verify.py` is the
   hinge: it publishes the exact bytes the trace hashes, and refuses when any
   hash fails. Nothing reaches a reader without passing it.
5. **Factories render; they never source.** A pack may only cite locators that
   resolve; a render without `evidence_refs` is a failed render.
6. **sanskritbench calibrates; it never verdicts.** Thresholds are stamped;
   a metric that auto-passes alone is a bug.
7. **nibbanahelp is private by construction.** Consent per use, scoped,
   revocable; one-way into essays/recipes; never auto-published.
8. **One identity, one ledger, one truth per stage.** No second DB, ID scheme,
   or parallel truth. This is the rule that keeps the whole thing clean.

---

## 3. Six invariants that keep it clean

1. **Name your inputs.** Every derived artifact records the sha256 of what it
   was derived from.
2. **Numbers live in `freshness.json`.** A count without a reproducing command
   and a source hash is not evidence, and does not ship in llms.txt, README, or
   any doc. `freshness.py --check` is the gate.
3. **Status vocabulary is fixed.** MEASURED / BLOCKED / CANDIDATE /
   UNRESOLVED / PARTIAL. BLOCKED is never PASS; PARTIAL is never COMPLETE.
4. **History is append-only.** Corrections are new dated files. Never edit an
   old claim into looking right.
5. **Lanes are read-only.** No writes into translation-work, ipvv, bookfactory,
   videofactory, nibbanahelp. Specs + CLAIMS notes only.
6. **No auto-anything.** No auto-sign, auto-publish, auto-authorize,
   auto-promote. Machine proposes; human disposes.

---

## 4. Versioning protocol (clean tree = reproducible state)

### Branch + commit taxonomy

- Work branches: `box/*`, `feat/*`, `data/*`. `main` receives merges only.
- One concern per commit, in this order of preference:
  - `docs(scope):` — plans, reviews, specs (no data claims)
  - `feat(scope):` — code that changes behavior
  - `data(scope):` — regenerated indexes/logs; the **command that regenerated
    them goes in the body**
  - `imports(scope):` — frozen reading mirrors with PROVENANCE.md
  - `chore(scope):` — hygiene, no semantic change
- Never mix a code change and a data refresh in one commit — it destroys the
  ability to tell drift from intent.

### Checkpoints

- After tests green **and** `freshness.py --check` says SHARP, tag
  `checkpoint-YYYY-MM-DD`.
- A checkpoint means: clone at this tag, run the recorded commands, get these
  numbers. That is what "versioned" means here.

### Dirty-tree policy

- No work starts on a dirty tree. Either commit it (with the regenerating
  command) or stash it with a dated reason. The 2026-11-06 swarm refresh is
  committed under this rule.
- Before deleting regenerated duplicates, log sha256 of kept vs removed
  (one line in process notes). "Byte-identical, therefore deleted" is a
  claim — hash it first (lead review F12, 2026-11-08).

### Data-sharp ritual (run before every push)

```sh
python3 -m unittest discover -s formal-trika/tests        # 73 tests
python3 formal-trika/tools/evidence_check.py              # theorems + coverage
python3 formal-trika/tools/bridge_resolve.py --check --tw /root/translation-work
python3 formal-trika/tools/freshness.py --write           # capture
python3 formal-trika/tools/freshness.py --check           # must be SHARP
df -h / ; git status --short                              # headroom + clean
```

If any step fails, nothing is pushed. If a number moved, the commit message
says why it moved.

---

## 5. Chain of events — the next ten moves

Ordered by dependency, not taste. Each ends with a gate.

1. **Clean + checkpoint.** Commit the 11-06 swarm refresh, the 11-08 plan docs,
   the freshness ledger; tag `checkpoint-2026-11-08`. Gate: SHARP + 73 green.
2. **W0 owner asks.** Disk headroom, cron install, token rotation (all owner
   actions; the box cannot do them alone). Gate: `df` ≥15%, 7 green cron days,
   rotation confirmed.
3. **R1 traces everywhere.** Compile traces for every passage in every readable
   work; publish PARTIAL honestly; extend `data/traces/index.json` toward ≥90%.
   Gate: outsider verifies any readable passage with curl+sha256.
4. **Treeka view.** Read-only assembler over works → passages → argmaps →
   cruxes → essays + gap report, fed by traces and `treeka.json`. Gate: gap
   report queryable; it drives the next rung and the crux queue.
5. **R4 chat verify-links.** Every answer citing a traced chunk returns trace +
   pack; untraced says "unverified". Gate: wiring test.
6. **Next formal rung.** phr-p05 head of the gap list, prereg exists. Gate:
   twin refuses; EVIDENCE + TABLE + run receipt.
7. **Sanskrit l01 slice.** `?view=sanskrit` with verse, gloss, rule boxes, chat
   from the same evidence spine; ML lines labelled. Gate: lesson → locator →
   bytes → gate replay.
8. **Decision trail in the lane.** Layer-accept rows at ingest; unsigned
   load-bearing decision refused (409). Gate: refusal test.
9. **Variety 1 closes.** PUSHBACK default before review; one signed essay gets
   a resolving Zenodo DOI. Gate: DOI → witness replay by an outsider.
10. **Witness + bench scale.** NGMPP eyes for one VERIFIED shelfmark; tau at
    n≥30 with Wilson CI when quota allows. Gate: one VERIFIED witness; one
    calibrated metric with a stamped threshold.

After move 10 the loop exists once, end to end. Only then: breadth (Greek/Pāli),
recipes (R1/R7/R8 diary books under consent), and R9 movies when the owner says
the models qualify.

---

## 6. Stale vs live (single source of truth)

- **Live numbers:** `formal-trika/data/freshness.json` (regenerate with
  `freshness.py --write`; gate with `--check`).
- **Stale-history register:** `docs/log/REVIEW-2026-11-08.md` (12 specific claims vs
  measured reality).
- **What to build:** `MASTERPLAN2.md`.
- **Architecture + phase order:** `MASTER-PLAN.md` (+ its 2026-11-08
  amendment).
- **Human asks:** `docs/log/DECISION-PACKET-2026-11-06.md` (update statuses there; do
  not fork a second ask list).

Rule of thumb: if a doc quotes a count and is older than 2026-11-07, treat the
count as reference, not evidence. Re-measure before quoting.

---

## 7. Stop rules (fail-closed at the seam)

- No hash → no link in the chain.
- No witness (or explicit UNPINNED) → never call it "primary source".
- No signature → no release, no DOI.
- No `evidence_refs` → no render.
- No consent → no personal material anywhere.
- No reproducing command → the number does not exist.
- A derived index that cannot regenerate → it is a second truth; delete it.

---

## 8. Adopted boundaries (PR #7 §4, 2026-11-08)

Ownership of each boundary, and what its owner is authoritative for. Adopted
verbatim in structure; trika-x's row restated as a constraint on everything
in this repo.

| Boundary | Owner | Authoritative for |
|---|---|---|
| Work / edition / witness / passage identity | OpenPāṭala | Stable identities, provenance, candidate mappings, reviewed decisions. An identity is not a verified reading. |
| Text and editorial layers | translation-work | The actual edition-specific source bytes, verse/span alignment, translations, annotations, argument maps, revision history. |
| People, private drafts, decisions | ipvv Scholar | Account-scoped access, selected sharing, revision-bound review and author sign-off. A self-attested name is not an independently verified identity. |
| Formal model | trika-x | Formal definitions, assumptions, theorem statements, toolchain and per-run results. **Not the text, not its interpretation, not a proof of entailment.** |
| Diagnostics | SanskritBench | Versioned benchmark outputs and limitations; advisory until independently validated for a named use. |
| Public reading | svread | A reproducible projection of explicitly pinned approved artifacts, with uncertainty and source links visible. |
| Teacher | nibbanahelp / Scholar integration | Private, consented personal workflow and source-grounded educational assistance. |
| Outputs | bookfactory, videofactory, visuals, deitybody | Rendered artifacts and delivery-specific metadata from a frozen source revision, separate preview and release decisions. |

Rules that come with the table: use a small versioned release manifest per
passage/artifact (work, edition, witness if verified, source bytes + SHA-256,
translation/claim revisions, editorial decisions + scope, formal declaration +
run digest if any, rights evidence, recipe + output digests). `UNKNOWN` is a
legitimate state. A release pins compatible versions; newer is not better.
Stale or missing inputs must be visible.
