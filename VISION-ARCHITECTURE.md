# Visionary Architecture: the Lean Recognition Stack inside the Endgame

**Date:** 2026-11-05. **Status:** PROPOSED (this report asserts nothing built beyond what it cites).
**Rule (owner):** formalizations arise OUT OF the data. Nothing here defines anything;
every target lists only where the evidence lives. Machine proposes, human disposes.

## 0. The thesis in one page

The endgame is a machine for turning hard Trika questions into signed, replayable
answers: *question → witness → signed DOI'd essay*, with every link hash-pinned
(`svread/ENDGAME-BUILD-PLAN.md` definition of done). Three things were missing from
that machine, and all three now exist in first usable form under `/root/trika-x/`:

1. **Something that PROVES instead of scoring.** SanskritBench scores heuristics;
   `audit_draft` checks citations; both are advisory by design. Lean's `decide`
   is the first component in the estate that *proves*: `formal-trika/control/`
   checks 8 mala-axis combos → exactly 7 well-formed experients (TK-C1 PASS),
   and refuses the mutated file (TK-C2 PASS). No model, no judge, no proxy.
2. **A runtime that refuses ungated transitions.** qprivately (`ipvv/tools/qp_acom/`)
   already implements `S[t+1] = T(S[t],P)` iff ALL gates PASS, with FAIL receipts
   as first-class artifacts, content-addressed ids, independent `settle()` replay,
   and V0–V12 proof levels. Recognition modeled as a gated σ-transition inherits
   all of this for free: no pass, no flip; failed attempts are recorded, not hidden.
3. **An evolution lab with honest fitness.** cg (`/root/cg`, cogymkernel) already
   implements content-addressed run ids (blake3, volatile fields stripped),
   replayable worldpacks, lexicographic gates-over-objectives selection, and an
   `oracle_hash` that is *evaluator-side only, never in observations*. A
   recognition worldpack makes Lean the oracle: candidate rule-sets compete on
   whether `decide` regenerates the traditional counts. Fitness is ground truth,
   not a judge's mood.

The visionary claim of this report: **recognition — the tradition's own central
operation (pratyabhijñā as σ-flip, T_rec) — becomes the first machine-checked
doctrine in the estate, and its checking machinery (Lean proving, qp gating, cg
replaying) becomes the template every other doctrine (kañcukas, malas, tattvas,
upāyas) inherits.** The pushing corpus supplies the conjectures; the gold layers
supply the keys; chat/essays/packs/video supply the surfaces that consume only
gated outputs.

Tiers everywhere (frontier T/R/E/C/H/X): T = root text, R = reconstruction
(AM0, inexternalism, CSID — all R, never smuggled as T), E = empirical, C =
correspondence, H = hypothesis, X = rejected. A reconstruction may never promote
itself. The report marks every load-bearing claim with its tier.

---

## 1. The estate as it stands (surveyed 2026-11-05)

### 1.1 The seven systems

| # | System | Role | State |
|---|---|---|---|
| 1 | sanskritbench | VERIFY (gold, proof gate, tau meta-eval, run_recorder, lemma spine) | Foundation DONE; P1 tau table + calibration pending; metrics advisory-only |
| 2 | openpatala | IDENTITY (Work→Edition→Witness→Surrogate→EText, R0–R5, Merkle ledger, 1,099 works) | BUILT + verified; chunk bridge = next |
| 3 | translation-work + Scholar | EVIDENCE + AUTHORITY (T1→L4 + GATE/proofs, ARGMAP, drafts→review→signoff→bridge→release, MCP 30 tools, Qwen) | LIVE; `scholar/` on 1 work; source binding uneven; Zenodo token pending |
| 4 | satsang + tantrasara + deitybody | SURFACES (TV/distribution, video factory, text→practice→body) | LIVE catalogue/factory/backend; S1–S7 wiring pending |
| 5 | nibbanahelp | PERSONAL + ORGANISM (tensions open→loosening→resolved, relay canon/lineage/lived/trika, demand signal, journey-ledger spec owner-gated) | LIVE relay/tensions; N1 exporter + N3 ledger not built |
| 6 | sanskrithelp | STUDY + BODY-DATA + FRONTIER (grammar/drills, mātṛkā map = TĀ 15.117–120 v2, VBT 65/112, 5 phonemic targets) | LIVE; SH1–SH3 = wiring tasks |
| 7 | The estate | RAW MATERIAL (awesome-essays 1,195/90-curated, research-library ~900, philosophy archive 1,933, kits, 57-crux catalog, slang editions) | Indexed; starters mined |

Master sequence (owner order, `ENDGAME-BUILD-PLAN.md §0`): 1 openpatala-ize →
2 sanskritbench (tau pilot in parallel, smoke only) → 3 IPVV + Tantrāloka
translation track → 4 datastructures (decision trail, ARGMAP nodes, sidecar) →
5 pathways + content (Treeka, syllabus C1–C4, courses, vids). Invariant: no rung
ships without hash + decision/grounds + gate + signer-role.

### 1.2 What the pipelines already move

- **Pushing** (`ipvv/site/data/pushing/`): Logicvid sessions (question → text's
  answer → sharper question, ROUNDs) with per-question verdicts
  (`GEM/RESOLVED/PLAUSIBLE/PARTIAL/TEXT SPEAKS/RIVAL open/HONEST-LIMIT/CORRECTION`),
  each carrying `chain` + `session` + `verses[]`; `INDEX.json` registries;
  `PUSHING-*.md` aggregators; peer-review of the recognition essay library.
  Sessions are conjecture mines with honest-limit markings — ideal formalization fuel.
- **Essay kits** (per-essay `STRUCTURE/ACQUIRE/WEAVE/PUSHBACK`, e.g.
  `gochema/essays/*/`, mirrored in the philosophy archive): STRUCTURE (thesis +
  stops) → ACQUIRE (fetch list) → WEAVE (verbatim quote bank `[ID] SOURCE —
  QUOTE — cite — SLOT`) → PUSHBACK (claim → question → what sources actually say
  → Resolution + Honest remainder; owner verbatim immutable).
- **Scholar claim flow** (`svread/mcp/claims.py`, `audit.py`): `essay-claim/1`
  links exact essay-rev paragraphs to typed claims
  (quotation/translation/historical/interpretive/argument/open_question) with typed
  evidence links (supports/qualifies/opposes/context) + `UNASSESSED/DISPUTED/
  HUMAN_ASSESSED`; `audit_draft` enforces same-paragraph verbatim binding;
  PUSHBACK returns revision-bound candidate issues; edits stale sign-offs.
- **Packs → factory** (`svread/endgame/tantrasara/PIPELINE.md`, nibbanahelp
  `resolve.py`): essay + `tension:*`/`chunk:*` evidence refs (fail-closed
  `validate_evidence`, lingua-checked) → frozen storyboard + approval SHAs →
  audio → forced align (≥0.85) → holds/cards → deterministic video → golden
  verify → delivery. One essay per pack, one tension resolved max.
- **Chat/relay** (nibbanahelp relay never advises; tiers canon→lineage→lived→
  trika over ~1,895 vectors; every session logged with relayed ids; trika tier =
  104 chunks): the demand signal (N1 miner, unbuilt) and the explanation surface.
- **Syllabus compiler** (`SYLLABUS-COMPILER.md` + `/root/satsang-practice/`):
  unitize → type → **eligibility gate** (text-study / doable / requires-dīkṣā,
  default study-only, no model-granted initiation) → assemble paths with
  `path:trika/*` lingua IDs. C1 pilot = VBT (65 dhāraṇās mapped).

---

## 2. The Lean recognition stack as built (today, checked)

Location: `/root/trika-x/formal-trika/`. Lean 4.34.1 (installed `/root/.elan`),
zero dependencies for `control/`. Prereg before code
(`PREREGISTRATION.md`, P-TK1–P-TK4 + kill criteria, tiers declared).

| File | Content | Verdict |
|---|---|---|
| `control/Mala.lean` | 3 malas inductive, `count_3` | PASS (`decide`) |
| `control/Pramatr.lean` | 3 binary axes → 8 combos; R1 (no free-floating karma) → 7 well-formed; profile `[2,3,1,2,1,2,0]`; R-tier name attachment | TK-C1 PASS |
| `control/Broken.lean` | R1 deleted → `seven` MUST fail | TK-C2 PASS (refuses, as required) |
| `control/Kancuka.lean` | 5 coverings, 5 distinct capacity-pairings | PASS (P-TK2) |
| `control/Recognition.lean` | AM0 σ-flip over 64 states: content preserved everywhere, always lands ¬Sv(O), adds nothing | PASS (P-TK3a/b/c) |
| `control/run.sh` | C1-must-check / C2-must-fail harness (mirrors Thon Ly) | green |
| `runs/INDEX.md` | Verdict ledger | 4 PASS recorded |

Compression at control: 1 rule clause ÷ 7 rows ≈ 0.14 (P-TK4 holds).
P-TK1b confirmed structurally: the mantra-triad split is adhvan-positional (R),
not mala-compositional — flagged, not derived. The machine corrected the author's
hand-written profile vector on first run (predicted order wrong → `decide` false →
observed order recorded). That is the instrument working.

**What Lean is and isn't here.** It verifies that stated definitions yield stated
counts. It does not prove Trika true, predict physics, or certify translations.
Heuristic scores (sanskritbench PASS, audit receipts) are never cited as semantic
proof — only `lean` checking a theorem counts, and only inside the model's stated
scope. (Tier discipline: the mala/kañcuka *names* are T via gold T1; the axis
reading, capacity glosses, and all of AM0 are R.)

---

## 3. qprivately + cg: the two kernels the stack plugs into

### 3.1 qprivately — gated transitions with receipts

- `transition()` is the only proposal→state path; ALL gates must PASS; FAIL
  receipts are first-class (evidence root preserved). New gates register with
  content-addressed `program_hash`; new logic = new id, never silent edits.
- `settle()` replays everything independently (id recompute + every gate
  re-executed); signatures ride outside the hashed body; proof levels V0–V12;
  `grants.py` authorizes capabilities fail-closed (UNSIGNED never authorizes).
- **Recognition mapping:** σ becomes qp state; T_rec becomes a `transition()`
  call under a new `sigma-flip-v1` gate: PASS iff `content_root` unchanged AND
  σ moved Sv→¬Sv (or stayed ¬Sv); content change → FAIL as *acquisition, not
  recognition* (first-class FAIL receipt, exactly the honest-limit pattern).
  The `grant` field carries the human `assert-recognition` capability, so
  machine-proposed flips stay MACHINE_PROPOSED until authority signs (ipvv Law 8,
  mechanical). Proof levels carry T/R tiers into the receipt.

### 3.2 cg — evolution with ground-truth fitness

- Frozen contracts, blake3 `content_id` (volatile stripped), replayable
  worldpacks, lexicographic gates-over-objectives, `oracle_hash`
  evaluator-side-only (the formal-abhidhamma collated-key pattern, natively).
- The `toy.py` signal game is the template: hidden bit → costly noisy evidence →
  COMMIT → gate on correctness, minimize cost.
- **Recognition worldpack** (`recognition_world.py`, sketched): hidden σ of the
  modeled subject; `OBSERVE_DETERMINATION` samples a δᵢ slice (noisy, costly);
  `COMMIT_RECOGNITION` asserts T_rec with a content-equality proof;
  `content_preserved == 1.0` is the gate (breaking it = learning, not
  recognition); Lean-verified keys live in `oracle_hash`. Evolution searches
  *rule-space* (mutants of R1-style rules); fitness = regenerate traditional
  counts with minimal clauses; `decide` is the oracle gate; `Broken.lean` is the
  automatic mutation control. Compression ratio becomes a selection objective.
- cg statistics (Wilson/bootstrap over runs) live *above* Lean: `decide` is
  proof, Wilson is uncertainty about behavior. Never the same receipt field.

### 3.3 The pin-together

```
Lean .lean --decide--> counts/keys (JSON, content-hashed)
    |                            |
    | oracle_hash (cg, unseen)   | evidence item (qp, merkle-rooted)
    v                            v
cg worldpack runs ---------> qp transition() receipts
(blake3 run_ids, replay)     (receipt:<sha16>, signed, settled)
```

One σ-flip, three attestations: Lean (rules yield counts), cg (run replayed to
same id), qp (this flip passed its gates on this evidence). This is the REVIEW
spec's "three legitimacy logs" shape with recognition as its first completed slice.

---

## 4. Where the Lean setup plugs into every pipeline

### 4.1 Source identity (openpatala, master step 1)
Formalization consumes only pinned sources: every Lean key file records
`source_id` (SHA of the volume/edition) + `layer` + `content hash` of the T1/L0
rows used. The `source-record/1` sidecar contract (REVIEW §3) gains one optional
field: `formal_key` (hash of the Lean-verified count table derived from that
source version). A corrected transcription = new source version = new selectors =
stale formal keys, never silent overwrite. IPVV chunks stay BLOCKED/PROOF_NOT_RUN
until the migration contract completes; Lean files that touch IPVV material carry
`tier: R, source: frozen-T1-only` until then.

### 4.2 Verification (sanskritbench, master step 2)
- The tau table calibrates *signals*; Lean *is* a signal of a different kind
  (proof, not correlation) and must be labeled as such in every ensemble: no
  signal auto-passes, including ours (BUILD-PLAN §1.4). Proposed label:
  `LEAN_DECIDED` vs `MODEL_PROXY` — never mixed in one column.
- Gate-vs-gold calibration (1.2) gains adversarial fixtures from `Broken.lean`-style
  mutants: rule-deleted variants MUST fail. Our TK-C2 is the reference specimen.
- `run_recorder` discipline applies to cg runs: dataset digest, candidate IDs,
  code hash, config, failures, raw judgments, unique exec id, immutable artifacts.

### 4.3 Translation track (master step 3) + gate sweep
Lean keys become regression fixtures for gates: the Paramārthasāra-1 omission
(REVIEW P0) is the model — a deliberately incomplete citation must FAIL the
corresponding Lean-checked coverage shape. As TĀ/Tantrasara gold lands, each
ahnika's tattva/kañcuka/mala vocabulary extends the key tables; the Lean files
grow rung by rung (control → sangaha-equivalent → canon-equivalent, mirroring
Thon Ly's L1/L2/L3 + two editions).

### 4.4 Treeka + crux queue (P2 2.1, P3 3.1)
The gap report gains a formal column per passage: `formalized / armed (armed =
key exists, theorem pending) / unarmed`. Unargued passages stay unargued; Lean
never fills a gap by itself — it *prioritizes* the crux queue (PUSHING verdicts
`GEM/RIVAL open/HONEST-LIMIT` rank by formalizability: a `RIVAL open` with two
competing formal readings is a high-value crux). N1 demand mining (sessions →
queue) and formalization meet here: recurring unanswered questions that *also*
resist formalization are the deepest cruxes.

### 4.5 Essay copilot (essayguide A–F + vision-07)
- **A thesis selection:** formal gaps are thesis generators (P-TK1b's mantra-triad
  exception *is* a ContributionClaim: RECONSTRUCTION with a flagged positional rule).
- **B argument architecture:** `EssayArgumentGraph` nodes gain `formal_status`
  (which premises are Lean-checked); objections that break a `decide` are closed
  objections; ones that don't are honest remainder — PUSHBACK output, structured.
- **C literature positioning:** Barendregt (AM₀, implicit-spec axioms) and Thon Ly
  (composition-rules-as-constraints) are the cited formal neighbours (already in
  `trika-x/INDEX.md`); the comparative paper (Abhidhamma 89/121×52×24 vs Trika
  36×5×3) is the D-contribution (COMPARISON + RECONSTRUCTION).
- **D contribution detection:** a new detection class — `FORMALIZATION` (with
  `decide`-hash + scope) alongside NEW_TRANSLATION/RECONSTRUCTION/CRUX/etc.
- **E rhetorical compression:** profiles stay (SCHOLARLY_ARTICLE … VIDEO_SCRIPT);
  formal content renders as *stated result + scope + tier*, never as proofiness.
  Slang register (tantrasara1–22) is explainer-tier, never evidence (S2/N2 guardrail).
- **F whole-document evaluation:** support/traceability checks gain `formal_scope`
  (which spans the theorem actually covers); warrant review asks the frontier
  question per claim (T/R/E/C/H/X status required before publish).

### 4.6 PUSHBACK + audit (review-as-compiler, vision-06)
PUSHBACK's destroy pass gains formal issues: *claim span exceeds theorem scope;
paragraph borrows a quote across the content boundary (`contentEq` false);
R-tier rule cited as T*. These are candidate issues (author disposes), not
auto-verdicts. `audit.py`'s same-paragraph verbatim binding is the runtime cousin
of `contentEq` — the essay equivalent of "recognition adds nothing": the claim
must not smuggle content the cited span doesn't contain.

### 4.7 Packs → factory → satsang (Varieties 3, S4/S5 loop)
Packs already carry `chunk:*` + `tension:*` evidence refs fail-closed. Add
`formal:*` refs (Lean theorem id + content hash + scope + tier), checked by
`resolve.py`-style validation: a pack claiming a formal result must resolve its
`formal:` ref to a checking theorem at the pinned hash. Generated-vs-catalogue
labels extend to proved-vs-illustrated: a diagram *illustrating* the σ-flip is
not a proof of it; the pack says which. The journal→essay→video→For-You loop
(S5) then distributes only gated packs — the content loop with teeth.

### 4.8 Chat + relay (Variety 4, N-system)
Relay tiers (canon→lineage→lived→trika) gain a response-side rule: **chat never
asserts recognition; it cites receipts.** A user asking "is this recognition?"
gets: the T_rec definition (R-tier, stated), the qp receipt if a gated flip
occurred on their logged session (with proof level), and the honest remainder.
Tension state changes (`open → loosening → resolved`) stay human-flipped;
a Lean/qp result may *support* a loosening (evidence link) but never flips it —
same law as packs (machine writes sidecars only). The trika tier's 104 chunks
grow a `formal_status` field as rungs land.

### 4.9 Syllabus compiler + practice (S3, C1–C4, deitybody)
The eligibility gate is where formalism earns its keep without overreach:
`text-study / doable / requires-dīkṣā` stays a *human-review* classification
(REVIEW P1: UNKNOWN stays study-only; no model grants initiation). Lean's role is
narrow and honest — verify *structural* prerequisites (e.g., "this dhāraṇā's
technique span cites the loci it claims," checked against the mātṛkā map v2
truth source SH1), never ritual eligibility. Practice proposals keep
`status: review`; VBT C1 pilot is the first consumer (65 mapped dhāraṇās; one
dhāraṇā end-to-end before C2's 37 āhṇikas).

### 4.10 Journey ledger + day truth (N3/S6/S1) + DOI (2.3)
- One shared legitimacy design (Merkle + checkpoints + witnesses) for nibbanahelp
  blocks + satsang Day-N records; qp receipt ids are natural ledger entries
  (content-addressed, signed, settleable). Owner-gated; until built, no ledger
  claims anywhere.
- Zenodo DOI bundles gain the formal artifacts (Lean sources + toolchain pin +
  theorem hashes) as part of the release manifest — the DOI resolves to bytes
  that re-check, not just prose that reads.

---

## 5. Worked example: one question through the whole machine

Question (chat): *"I saw the bottle clearly, then saw it as mine — did anything
in experience change?"*

1. **Relay** retrieves trika-tier spans (pratyabhijñā recognition passages,
   T-tier) + the AM0 gloss (R-tier, labeled) and logs the session with relayed ids.
2. **Pushing-style sharpening** restates: is T_rec content-preserving? (conjecture)
3. **Lean answers structurally**: `recognition_preserves_content` + `adds_nothing`
   over all 64 states — within the model, no: content identical, only σ flips.
   Scope stated (Bool abstraction, R-tier AM0). Not a metaphysical verdict.
4. **qp records** (if the user's logged tension resolves): `transition()` under
   `sigma-flip-v1` — content_root equality checked, σ Sv→¬Sv, FAIL-first-class if
   content moved. Receipt signed on human approval; tension flip stays human-only.
5. **Essay** drafts with `essay-claim/1` links (interpretive claim + supports-link
   to the Lean theorem hash + qualifies-link to the model's scope limits);
   PUSHBACK hounds scope overreach; audit enforces verbatim binding.
6. **cg** (offline): the conjecture's rule-shape joins the evolution population;
   mutants compete on regenerating the counts; results feed the crux queue.
7. **Pack + video**: essay → pack with `formal:` ref (theorem id + hash + scope) →
   factory → satsang Watch with proved-vs-illustrated label.
8. **DOI**: bundle (essay rev + receipts + Lean sources + toolchain pin + run ids)
   → Zenodo. An outsider replays DOI → receipt → gates → Lean `decide`.

Every hop preserves the tier and the honest remainder. Nothing launders.

---

## 6. The pushing corpus as fuel (concreteDescriptor)

Priority conjecture sources ( формализация queue, first pass):

| # | Source | Formal target | Why now |
|---|---|---|---|
| 1 | `pushing/tantraloka/LOGICVID-session-*-kancukas-*.md` + tsa-a08 T1 (kalā ×50…) | Kañcuka rung: 5 restrictions × capacity-pairings + textual span pins | Gold adjacent, counts small |
| 2 | `pushing/tantraloka/LOGICVID-session-impurities-powers.md` + phrdaya mala argmap | Mala composition: 3 axes → experient classes (TK-C1 already the seed) | Control exists; extend rows |
| 3 | `pushing/tantraloka/Q5-krama-time-extracted.txt` + sciencetime (t_phys/τᵢ) | Kāla-as-kañcuka axiom: finite temporal access, passage/lineage-dependent | SH1 body-map adjacent |
| 4 | `pushing/ipvv/IPVV-MEMORY-vs-whattheheckismemory.md` + IPVV kriya/jñāna chunks (frozen T1) | Memory/pramātṛ persistence across moments (continuity theorems) | Needs migration contract first — BLOCKED until then, flagged not built |
| 5 | `research/truth*.md` verdict chains (manifest→reflexive→one→universal→freedom) | The A→B→C→D→E→F non-entailment chain as Lean implications that FAIL to compose (prove the gaps!) | Negative results are findings |
| 6 | `PEER-REVIEW-RECOGNITION-ESSAYS.md` (7 magnum-opus + core essays) | Scope audit: which essay claims already fall inside checked theorems vs exceed them | Review-as-compiler input |

Rule: sessions → conjectures → Lean → verdicts flow *back* into `INDEX.json`
as a `formal` annotation per question (checked / refuted / out-of-scope), never
editing session bodies. The corpus learns what it proved.

---

## 7. Visionary horizon (what this unlocks, staged)

- **Near (rungs 2–3):** recognition transition relation + mala pathologies in
  Lean; `sigma-flip-v1` gate in qp (scratch copy first); Trika `FORMALIZATION`
  contribution class in the essay pipeline; `formal:` refs in packs. The
  comparative paper outline (two Buddhist systems, one method, Trika third).
- **Mid (crux queue with teeth):** Treeka's formal column drives P3.1; evolution
  (cg) proposes minimal rule-sets for tattva-descent + kañcuka + mala
  (36/5/3 regeneration attempt — the program's headline experiment, preregistered
  with kill criteria: *no layer generates the counts → transmitted rules
  incomplete, reported as the result*); syllabus C2–C4 consume only gated units.
- **Far (the book):** *Tantra as formal system* — alphabet (L0, done) → WFFs
  (argmaps) → axioms (Barendregt-style implicit spec) → inference rules (paṭṭhāna
  template × Trika move-catalog) → checker (Lean discipline) → models (CIMC/
  aperture/POMDP readings as interpretations) → comparative volume. The vision
  docs' "one historically-grounded tradition fully computable" (CORE-BIBLE),
  but with the one word the visions lacked: *checked*.

## 8. Safeguards and non-goals (load-bearing)

1. Tiers ride everywhere (T/R/E/C/H/X); an R-rule never ships as T; qp proof
   levels encode this. 2. Machine proposes, human disposes (grants, sign-offs,
   tension flips, publish — all human). 3. No heuristic PASS is semantic proof
   (sanskritbench/audit stay advisory; only `decide` proves, inside its scope).
   4. IPVV stays BLOCKED until the migration contract completes; no intake-shaped
   imports, no verse-ID forcing. 5. Privacy: sessions enter formalization only via
   N1 opt-in mining (questions, never diaries); revocation invalidates derived
   indices. 6. Non-goals: no auto-signing, no E2E practice authorization by
   model, no cross-scholar style mixing, no second ledger, no organism mining
   without grant, no claiming the model is the mind.

---

## 9. Build order (next 10, concrete)

1. `formal-trika/`: Recognition transition relation + no-backslide/idempotence +
   3 mala-pathology theorems (rung 2; zero-dep; ~60 lines). 2. Key export:
   Lean counts → JSON keys (`keys/*.json` + hashes) for qp evidence + cg oracle.
   3. qp scratch: `sigma-flip-v1` gate + one T_rec receipt walkthrough (copy of
   `qp_acom/`, never the lane). 4. cg sketch: `recognition_world.py` vs `toy.py`
   interface (hidden σ, OBSERVE/COMMIT, content gate). 5. Pushing queue §6 rows
   1–2 as preregistered predictions. 6. Treeka formal column (spec-before-code).
   7. Essay pipeline `FORMALIZATION` class + PUSHBACK formal-issue shapes.
   8. Pack `formal:` ref validation (resolve.py-style). 9. Relay response rule
   (cite receipts, never assert). 10. Comparative paper outline (trika-x).

## Appendix: file map (where everything cited lives)

- Lean program: `/root/trika-x/formal-trika/{PREREGISTRATION.md,control/{Mala,Pramatr,Kancuka,Recognition,Broken}.lean,control/run.sh,runs/INDEX.md}`; toolchain `/root/.elan` (4.34.1); corpora `/root/trika-x/{INDEX.md,papers/barendregt/,repos/{formal-abhidhamma,thonly-publications/}}`.
- Kernels: qprivately `/root/ipvv/tools/qp_acom/{gates,receipts,runs,versions,grants,synthesize}.py`; cg `/root/cg/cogymkernel/{kernel/{contracts,ids,runner},worlds/toy.py,eval/gates.py,evo/loop.py}`.
- Endgame: `/root/svread/{ENDGAME.md,ENDGAME-BUILD-PLAN.md,SCHOLAR-ENDGAME-{SPEC,VISION}.md,TENSIONS-ENDGAME.md,RESOURCES.md,endgame/{README,REVIEW-AND-IMPLEMENTATION-SPEC-2026-11-05.md,NIBBANAHELP-,SATSANG-,SYLLABUS-COMPILER,SANSKRITHELP-}-INTEGRATION.md,{vision,sanskritbench,openpatala,satsang,tantrasara,deitybody,sanskrithelp}/}`.
- Pipelines: pushing `/root/ipvv/site/data/pushing/`; kits `gochema/essays/*/{STRUCTURE,ACQUIRE,WEAVE,PUSHBACK}.md` + `/root/translation-work/ESSAY-STARTERS-P0.md`; factory `endgame/tantrasara/PIPELINE.md`; lingua `/root/svread/tools/lingua.py`; scholar MCP `/root/svread/mcp/{claims,audit,scholar_server,search}.py`; practice `/root/satsang-practice/`.
- Sources: translation-work gold (`tantrasara-a07/a08`, `paramarthasara`, `phrdaya`); drafts `awesome-essays/{inexternalism,sciencetime,ocheeema,frontier*,truth*}` + `Aperture inexternalism`; gochema `FORMALIZATION-OF-RECOGNITION.md`; seeds `/root/TRIKA-X-SEEDS.md`.
