# Results — formal Trika

Results are appended below; an earlier result is never edited. Predictions are
scored against their preregistration files. Scoring stays **provisional** until
the scored conditions are fully met (independent raters, replication,
sufficient n).

**Correction for TK-R2:** the original 36 total masked two compensating
classification errors, and its eleven-faculty interpretation used the wrong
groups. The historical entries below describe the earlier model, not the
corrected one. See [the source review](SANSKRIT-FOUNDATION-REVIEW-2026-11-06.md).
Old runs do not verify a changed model; a fresh Lean run and independent
source-to-model review are required.

**Correction for T-C1:** the historical p-value below is a descriptive
one-sided Fisher calculation on machine-proposed, owner-unreviewed labels.
The arcs come from repeated observations of one person, so independence
cannot be assumed; p=0.0462 does not establish that the rāga correspondence
holds. The mapping remains an unvalidated interpretive hypothesis.

### Correction run — 2026-11-06

Against the amended files on base `f42a2ea`, the pinned Lean 4.34.1 release
compiled the control and recognition suites. The control suite rejected its
seven intended mutants, including a new test that incorrectly places māyā
among the five pure tattvas; the recognition suite reported 26/26 positive
and intended-negative checks. `#print axioms` reported none for
`FormalTrika.eleven_wombed`, `FormalTrika.thirty_six` and
`FormalTattvaInventory.pure_excludes_maya`, and `[propext]` for
`FormalTattvaInventory.named_tattvas_exhaustive`.

Exact source hashes: `Tattva.lean` SHA-256
`06c067d5ea4a0912391156cc359aefcd6fb0a83f89778df9d3eb74f143e7b1ea`;
`TattvaInventory.lean` SHA-256
`7845ffef27afdce6c60bb0a722e52ab04bfd7ca10d2bce09e5c24e75fca92535`;
`Avarana.lean` SHA-256
`3ae1d40958acccb78ccab135a20f2f2a6d94825fa6f989ba61261850826a7f33`.
The Lean archive hash is the one in README; these checks establish properties
of the amended models, not the accuracy of the Sanskrit interpretation.

### Combined-branch checks — 2026-11-06

After integrating main through `44e1a09`, Lean 4.34.1 compiled the combined
control suite and rejected all nine intended mutants, including the restored
`Pramatr.lean` negative control. The recognition suite reported 26/26
positive and intended-negative checks. These are model checks, not
independent verification of sources or interpretations.

---

## 2026-11-06 — Arm A: control (TK-C1/C2, P-TK1–4)

`control/run.sh` (Lean 4.34.1, no dependencies) → **PASS.**

### What was built

- **`Mala.lean`** — 3 malas inductive, `count_3`.
- **`Pramatr.lean`** — 3 binary axes → 8 combos; R1 (no free-floating kārma)
  → 7 well-formed rows; profile `[2,3,1,2,1,2,0]`; unverified name labels
  (positional, R-tier, flagged).
- **`Kancuka.lean`** — 5 kañcukas, `restricts` table (capacity pairings, R),
  `count_5`, `pairings_distinct`.
- **`Recognition.lean`** — AM0 σ-flip over 64 states: content preserved,
  always lands ¬Sv(O), adds nothing.
- **`Broken.lean` / `BrokenKancuka.lean`** — mutants; `must_fail.py` requires
  the named `by decide` theorem to be false (same statement, pinned Lean,
  warnings-as-errors).

### What checks

| Theorem | Statement |
|---|---|
| `count_3` | tradition counts 3 malas |
| `eight_combos` | 3 binary axes = 8 combinations |
| `seven` | R1 excludes exactly 1; 7 rows survive |
| `profile` | mala-count profile [2,3,1,2,1,2,0] in generation order |
| `count_5` | tradition counts 5 kañcukas |
| `pairings_distinct` | 5 distinct capacities (no overlap) |
| `recognition_preserves_content` | σ-flip changes no content bits (64 states) |
| `recognition_lands_recognized` | always lands ¬Sv(O) |
| `recognition_adds_nothing` | content before = after |

### Scoring (provisional)

- **TK-C1 (7+1 from general rules): PASS** — but P-TK1 (one-to-one textual
  class mapping) **UNESTABLISHED** (PREREGISTRATION-2026-11-06 §1: the
  mantra-triad split is adhvan-positional, not mala-compositional).
- **TK-C2 (known failure): PASS** — R1 deletion breaks the count; must_fail
  confirms the mutant refuses.
- **P-TK2 (5 kañcukas): PASS** — count_5 + pairings_distinct check.
- **P-TK3 (σ-flip): PASS** — content preserved, lands ¬Sv(O), adds nothing.
- **P-TK4 (compression < 1.0): PASS** — 1 rule clause ÷ 7 rows ≈ 0.14.

### Honest limits

The 7 Boolean rows have no proven one-to-one mapping to the traditional
seven experients (saptapramātṛ). The name labels are R-tier proposals,
unused by any count theorem. The capacity pairings in Kancuka.lean are
stipulated (R), not derived from the text.

---

## 2026-11-06 — Arm A: recognition rungs (R-REC1–8)

`recognition/run.sh` (Lean 4.34.1) → **PASS, 18/18** (9 positive + 9
must-fail mutants).

### What was built

- **`Transitions.lean`** — R-REC1 (σ-laws over 12-bit RecState, 4096 states:
  embodiment kept, bondage cleared, limitation retained, idempotent) +
  R-REC2 (mala pathologies: āṇava stuck, acquisition ≠ recognition, kārma
  self-loop — each distinct from T_rec).
- **`NonEntail.lean`** — R-REC3 (A–F chain: six one-step countermodels +
  A..E-without-F) + R-REC4 (V₁–V₇ independence 128 combos, U non-transitive,
  no-global-section triad).
- **`Conjuncts.lean`** — R-REC5 (recognition unique 1/16, 4 drop-one
  theorems, misidentification never recognizes) + R-REC6 (Part coherent,
  PI-independent, Śiva-requires-S) + R-REC8 (unus-ambo exhibit).
- **`Memory.lean`** — R-REC7 (M₄ requires M₁–M₃, M₄⇏M₅, sees-without-enacts,
  no enacts-without-sees).
- **`Tractatus.lean`** — support-set locality (no universal S), Rec₁/Rec₂/
  FullRec hierarchy, layers L1–L4, finite no-self-model shadow, path fork
  (suffering vs recognition reachable; reflexive edge load-bearing).
- **`Coords.lean`** — kañcuka→coordinate bijection (5 distinct), agent
  finitude (restricted perspective exists, no unrestricted among admitted).

### Scoring (provisional)

- **R-REC1–8: all PASS** (each with a must-fail mutant that refuses).
- Kill conditions not triggered (no Broken twin checks).
- Honest limits: finite models only (12-bit/64/128/4096 states); station
  tags applied to ~4 moments of 144 lived decodes; ti/ca coordinates have
  no felt signature (F-CORR partial, 3/5).

---

## 2026-11-06 — Arm B: decode rung (T-C1, T-C3, T-C4)

Prereg: PREREGISTRATION-DECODE-RUNG.md (committed before code).

### What was built

- **`KancukaCorr.lean`** — felt→coordinate map (pull→va, stall→ac, doubt→kn;
  push/urgency/placedness = explicit unknowns). KEY (stipulated + evidence-
  pinned), not derived. `coverage_partial` (3/5 coords).
- **`Grace.lean`** — flip ↔ ready ∧ grace over 4 states; readiness and grace
  each necessary, jointly sufficient; both gaps inhabited.
- **`Upaya.lean`** — śāmbhava (1-step), śākta (needs purity), āṇava (needs
  n≥2 repetition); distinctness checked; orderings recorded as found.
- **`tc1_cooccurrence.py`** — Fisher exact over vendored decodes (26 arcs).

### Scoring (provisional)

- **T-C1 (pull+stall co-occur): HOLDS** — p=0.0462 one-sided, 26 arcs.
  3/3 thin/churn arcs carry lobha; thin never without lobha. Pilot only:
  n small, single diarist, machine-proposed decodes, owner-unreviewed.
- **T-C3 (grace variable): KEPT** — 5/5 grace-clauses keep the variable
  (residual unconditioned step). Kill not triggered. Single rater.
- **T-C4 (conjunct audit): HOLDS** — claimed-recognition 3.0 vs state-
  craving 0.0 (n=4). S=0 throughout (no stabilization evidence yet).
- **T-C2 (upaya agreement): UNRESOLVED** — rater-2 sheet ready, awaiting
  independent mind.

### Honest limits

All decodes are machine-proposed, owner-unreviewed. n is tiny. The grace
audit may be circular (looking for residual steps finds them). ti/ca
coordinates silent. Station tags on 4/144 moments.

---

## 2026-11-06 — Arm C: methodology instruments

Prereg: PREREGISTRATION-ARMC.md (committed before verification).

### What was built

- **`AnswerKey.lean`** — 5 tradition figures (5 kañcukas / 36 tattvas /
  7 experients / 5 followers / 112 dhāraṇās) with per-figure status
  (VERIFIED-QUOTE / ARGMAP-PINNED / PREREGISTERED-ONLY). Excluded list
  names our non-traditional constructs.
- **`vocab.py` + `Vocab.lean`** — 26 types extracted, Lean-checking,
  `--check` green (blind protocol instrument).
- **`table.py` + `TABLE.md` + `TABLE-READINGS.md`** — 76 theorems with
  hand-written plain-English readings; staleness-checked.
- **`TRIKA-METHOD.md`** — tiers, layers-as-variable, kill rules, compression
  honesty, machine-proposes-human-disposes.
- **`BLIND.md`** — second-encoder protocol (never run yet).

### Scoring (provisional)

- M-KEY / M-BLIND / M-TABLE / M-LEDGER / M-GREEN: all HOLD (PREREGISTRATION-
  ARMC predictions). Blind re-derivation: instrument built, no run yet.

---

## 2026-11-06 — Arm D+E+F: evidence chain + bridge + cruxes

### What was built

- **`EVIDENCE.json`** — 74 theorem entries + 2 exemptions, each pinned to
  chunk locators / R-sources / lived decodes. `evidence_check.py`: 22/22
  chunk refs resolve.
- **`treeka_formal.py`** — formal column: 6/45 formalized, 16 armed,
  23 unarmed + gap list.
- **`bridge/`** — passage snapshot (SHA-256 ledger pins), openpatala-map
  (CANDIDATE-* status, witnesses UNPINNED), `bridge_resolve.py` with
  `--tw` byte-verification.
- **`CRUX-WALKTHROUGH-01`** — rāga↔lobha (tsa08-p03): chunk → formal →
  argument → essay draft with claim table + PUSHBACK. Chain runs.
- **`CRUX-WALKTHROUGH-02`** — ego-origin (tsa08-p04): derivative (Sāṅkhya)
  vs self-reflexive (Trika). Formal gap identified (no ego-origin model).
  Chain runs on a second crux.

### Scoring (provisional)

- Coverage 6/45 (13%) — the formal core exists but most gold is untouched.
- Witnesses all UNPINNED (needs openpatala resolver).
- Both cruxes prove the chain runs; neither proves its claim (open by design).

---

## 2026-11-06 — Rung 2: tattva ladder generation (TK-R2)

Prereg: PREREGISTRATION-DECODE-RUNG.md §F-UPAYA-adjacent (structural rules,
not trained). T-tier ground: tsa07-p01 argmap (36 natures, magnitude ladder,
"one-eleven-wombed ahaṃkāra" = aikādaśagarbha = 5 tanmātra + 5 mahābhūta +
1 manas).

### What was built

- **`Tattva.lean`** — general rules over the tattva ladder structure:
  10 group-size clauses (5 gross elements via 10× ladder, 5 subtle, 5 sense,
  5 action, 1 mind, 1 intellect, 1 ego [11-wombed], 1 nature, 5 coverings,
  7 pure principles). Generation from structural rules; count check.
- **`BrokenTattva.lean`** — mutant: purePrinciple size 7→6; `must_fail.py`
  confirms `thirty_six` refuses.

### What checks

| Theorem | Statement |
|---|---|
| `five_gross_elements` | 10× ladder yields exactly 5 gross elements |
| `eleven_wombed` | ahaṃkāra = 5 tanmātra + 5 mahābhūta + 1 manas = 11 |
| `thirty_six` | generated total = 36 (matches AnswerKey) |
| `all_groups_present` | every group accounted, no orphan/double-count |
| `compression_ratio` | 10 group-size clauses ÷ 36 rows ≈ 0.28 |

### Scoring (provisional)

- **TK-R2 (36 from structural rules): PASS** — `thirty_six` checks;
  BrokenTattva mutant refuses.
- **Compression: 0.28** (10 clauses ÷ 36 rows). Thon Ly's sangaha:
  0.22 over 121, 0.30 over 89. Comparable — the tattva structure is
  hierarchical (groups of different sizes), not combinatorial (independent
  axes), hence slightly worse than the citta count but same order.
- **Honest limits:** group sizes are structural data (derived from the
  ladder's own composition, not from the text's per-item enumeration).
  The "11-wombed" formula is T-tier (tsa07-p01 v09). The pure-principle
  count (7) is our reconstruction — the text's list may differ; flagged.

---

## 2026-11-06 — Rung 3: ego-origin accounts (E-EGO, CRUX-02 gap)

Prereg: PREREGISTRATION-EGO-RUNG.md (committed before code; E-EGO1–5).
T-tier ground: tsa08-p04 argmap (v68 silver-in-shell, v69 rejection of
Sāṅkhya on I-feeling + makership, v70 pure I as non-rivalled vimarśa;
v71/v72 heaps parked).

### What was built

- **`EgoOrigin.lean`** — 16-state bit-model (D/F/M/R flags): Sāṅkhya
  admission = D ∧ ¬F ∧ ¬M; Trika admission = ¬D ∧ F ∧ M ∧ ¬R (pure-I
  witness). 6 theorems, all `by decide`, all **zero-axiom** (`#print
  axioms`: no axioms at all).
- **`BrokenEgoOrigin.lean`** — mutant: Sāṅkhya D-requirement dropped
  (single definition line + header); `must_fail.py` confirms
  `sankhya_requires_cause` refuses.
- **`BrokenEgoRival.lean`** — mutant: Trika N-requirement dropped;
  `nonrivalled_does_work` refuses.

### Scoring (provisional)

- **E-EGO1–5: all PASS** (each key theorem with a must-fail twin for the
  two load-bearing ones; E-EGO3a/b and E-EGO5 are exhibits, twin-covered
  by family).
- Recognition harness now **21/21** (10 positive + 11 must-fail).
  Evidence coverage **7/45 (15%)** — tsa08-p04 formalized.
- **Honest limits:** consistency of two axiom sets only; no verdict on
  which account is true about minds (prereg §2). Silver-in-shell read as
  origin-dependence (structure reading parked). F/M separability is
  model-level, not a textual claim on (c). Heaps unmodeled. Absence claim
  scoped to formal-trika (Thon Ly corpus unsurveyed).

---

## 2026-11-06 — Correction: TK-R2 compression claim downgraded
(Correction record; the 2026-11-06 Rung 2 section above is not edited.)

Legitimacy review against Thon Ly's bar found the 0.28 ratio unearned:
unlike sangaha (general constraints over axes + an INDEPENDENT per-factor
second key), our group sizes are table data (`groupSize` lookup) and the
cross-checks (`eleven_wombed`, `five_gross_elements`) reuse the same
sizes. **TK-R2 stands as a checked restatement with internal consistency
(`thirty_six` + refusing mutant), NOT as compression in Thon Ly's sense.**
EVIDENCE.json Tattva notes corrected the same session (restatement
language, no-independent-key flags). To earn a ratio: find independent
textual constraints on group sizes (second key), or drop the claim.
Status of `thirty_six` itself (36 generated, mutant refuses): unchanged.

---

## 2026-11-06 — Hardening pass: sharpness + grace-key (S-SHARP)

Prereg: PREREGISTRATION-SHARPNESS.md (S-SHARP1–2, S-GRACEKEY).
Found by the first mechanical sweep (`jubnzv/Mutate.lean`, built from
source this session, Lean 4.33.1 frontend): `contentEq -> ||` / `-> true`
mutants SURVIVED the P-TK3 suite, and `key_grace_term_attested` had NO
covering theorem. Full-sweep disposition: Mala/Kancuka/Tattva
survived=0; AnswerKey 3 survivors = the grace flag (fixed here);
Recognition 17 survivors = weakened-equality (fixed here) +
enumeration-collapse vacuous cases (recorded noise, prereg §2).

### What was built

- **`contentEq_sharp`** (Recognition.lean): single-field difference ⟹
  NOT content-equal. Zero-axiom. Twin `BrokenSharp.lean` (one conjunct
  dropped, single-line diff): old 3 theorems PASS on it, sharp FAILS —
  proving discriminating power the old suite lacked (S-SHARP2).
- **`key_grace_term`** (AnswerKey.lean): pins the v35 VERIFIED-QUOTE flag.
  Zero-axiom. EVIDENCE entry KEY/VERIFIED-QUOTE.
- TABLE source list fixed (predated Tattva; claimed 76, repo had 81):
  all 89 covered, count dynamic, 13 hand readings added.

### Scoring (provisional)

- **S-SHARP1–2, S-GRACEKEY: all PASS.** Control harness extended
  (BrokenSharp twin). Dynamic axiom audit: 89/89 CLEAN (75 zero-axiom).
- **Honest limits:** sharpness is OUR predicate's property, not textual.
  Vacuous-enumeration survivors are mutation-testing noise, not gaps.

---

## 2026-11-06 — Rung 4: heaps (E-HEAP: v71 instrument, v72 nature)

Prereg: PREREGISTRATION-HEAPS-RUNG.md (E-HEAP1–4; thin-premise cap 0.65;
parts-reading exhibited, causes-reading parked). T-tier ground: tsa08-p04
argmap v71 (karaṇaskandha named) + v72 (threefold by guṇa difference).

### What was built

- **`Heaps.lean`** — instrument heap (5 sense + 5 action + mind = 11,
  ladder-consistent) + 3-guṇa nature-states. 4 theorems, all `by decide`
  (3 zero-axiom, `heap_has_both_kinds` on `[propext]` only).
- **`BrokenHeaps.lean`** — action slots as sense dupes (heap stays 11):
  `heap_has_both_kinds` refuses, siblings pass (surgical).
- **`BrokenHeapsGuna.lean`** — tamas slot as rajas dupe (count stays 3):
  `guna_exhaustive` refuses, `guna_threefold` passes (surgical).
- Caught live: `++ [mind]` parsed inside the flatMap lambda (heap came
  out 15, not 11) — found by running the check, fixed with parens,
  recorded here. The discipline works.

### Scoring (provisional)

- **E-HEAP1–4: all PASS** (each with a must-fail twin for the two
  load-bearing ones; E-HEAP2/3 are counts, twin-covered by family).
- Recognition harness now **24/24**. Evidence **93 theorems, 91+2,
  0 problems**. TABLE covers all 89+4. Coverage still 7/45 chunks —
  heaps deepen tsa08-p04, no new chunk.
- **Honest limits:** 5+5+1 reuses OUR ladder (consistency, not
  independence); parts-vs-causes NOT decided; thin T premises cap what
  the rung can ever claim.

---

## 2026-11-06 — Rung 5: āvaraṇa covering-chain (E-AVAR, first second key)
Prereg: PREREGISTRATION-AVARANA-RUNG.md + same-day AMEND (chain
tautology found by the twin BEFORE any recorded run — first draft
derived links and cover from the same list; must_fail rejected the
twin; redesigned to course-rank ascent). T-tier ground: tsa07-p01 v23.

### What was built

- **`Avarana.lean`** (imports Tattva.lean, like Pramatr imports Mala):
  ladder list (R) + `covers` from INDEPENDENT course-rank rule (gross 0
  < subtle 1 < mind 2 < impure 3 < pure 4, from v3–v22 magnitudes).
  2 theorems (`course_ascends`, `partial_order_honest`), both on
  `[propext]` only.
- **`BrokenAvarana.lean`** (covering↔purePrinciple swap, single-line
  diff): `course_ascends` refuses, sibling passes.
- Genuine finding: the ladder is PARTIALLY ordered — six groups share
  course .mind; v23 does not rank within a course. Exhibited, not forced.

### Scoring (provisional)

- **E-AVAR1r–3r: all PASS.** Control harness extended. First INDEPENDENT
  structural constraint (order, disjoint from sizes) — one step toward
  re-earning a compression claim (v9 embedding designed next).
- **Honest limits:** order only; sizes untouched; ratio stays downgraded.

---

## 2026-11-06 — Rung 6: applications (A-APP, first consumed theorem)

Prereg: PREREGISTRATION-APPLICATION-RUNG.md (A-APP1–2). Composes Grace
(flip needs ready∧grace) + Upaya (every means needs ready) with NO
imports — restates the shared precondition explicitly, cites both.

### What was built

- **`Application.lean`** — product PracticeState {ready, grace, pure}:
  `unready_unreachable` (¬ready ⟹ no flip under any means),
  `grace_not_a_means` (graced-but-unready does not flip). Both
  zero-axiom.
- **`BrokenApplication.lean`** (flip := grace ∧ (ready ∨ ¬pure):
  impure-unready flips when graced; A-APP2 witness stays unflipped):
  `unready_unreachable` refuses, sibling passes. (First twin draft was
  over-broad — harness rejected it; surgical redraft passed. Twice in
  one session the negative controls caught design errors, not code bugs.)
- Consumer wired by citation: syllabus compiler's study-fallback
  (eligibility.py unknown → study) now cites A-APP1 as its formal
  backing. First rung whose theorem is USED downstream.

### Scoring (provisional)

- **A-APP1–2: PASS.** See runs ledger for harness totals.
  EVIDENCE 97/95+2 clean. Dynamic audit: both zero-axiom.
- **Honest limits:** a compiler rule, not a prescription, not a guru.
  Composition is ours (R); T ground inherited.

---

## 2026-11-06 — Correction: PR #4 textual scope (merged 9073a25)

Merged peer-built corrections (reviewed line-by-line; key compound
`tanmātrapañcakākṣaikādaśa` verified in T1 line 39 pre-merge):
- TK-R2's eleven reading was substantive-wrong (subtle+gross+mind);
  corrected to faculties (5+5+1) with the grouped model repaired (kalā
  in, māyā separate, pure 5, puruṣa subject) + TattvaInventory candidate
  list + māyā-among-pure negative control. Old runs do not verify the
  amended model (fresh runs recorded post-merge).
- A-APP1 "consumed by compiler" claim WITHDRAWN as stated: the theorem
  is a property of a stipulated product model; it does not validate
  eligibility, readiness, or practice authorization (eligibility.py and
  path_assemble.py now render STUDY-only; keyword/doable labels are
  provisional, never authorizing).
- Grace/Upaya T-pins downgraded to CONTEXT_ONLY / MODEL (v35, v17, v69
  do not entail the Boolean rules; T-C2 agreement cannot authorize
  advice). EVIDENCE carries the corrected notes; TABLE readings fixed
  (eleven_wombed).
- Practice assembler + pushback external-text rules tightened (opt-in,
  no-DIY). My pre-merge artifacts re-rendered to the new law
  (unit-vbt-d001 STUDY; path tests assert STUDY).
- Standing corrected-record pattern: history kept, never edited.

---

## 2026-11-06 — Rung 7: mala fuel (P-PUSH1, pushing row 2)

Prereg: PREREGISTRATION-PUSHING-QUEUE.md (P-PUSH1a–c; row 1 deliberately
NOT re-registered — postdiction refused; P-PUSH2 krama-time registered
as question+method+kills with T-pins TBD). T-tier ground: phr-p04 argmap
(sūtras 13–16: climb, burn knowables for fuel, grown strong, return by
recognition not effort).

### What was built

- **`MalaFuel.lean`** — burn state (3 mala flags + knowing) + burnStep
  (ignites iff knowing) + strength counter: `fuel_terminates` (3 steps
  → all burnt), `strength_monotone` (never decreases), `grace_ignites`
  (no knowing, no burning). All zero-axiom. EXTENDS Recognition.lean's
  removal clause with the strength effect (no contradiction).
- **`BrokenFuel.lean`** (burns without knowing, single-line diff):
  `grace_ignites` refuses, siblings pass.

### Scoring (provisional)

- **P-PUSH1a–c: PASS.** Control harness extended. EVIDENCE 100/98+2.
- **Honest limits:** fuel dynamics only; strength effect is model-level.

---

## 2026-11-06 — Rung 10: nyāsa mapping (N-NYASA, geometry first)

Prereg: PREREGISTRATION-NYASA-RUNG.md + same-day AMEND (varga-rules-vs-
single-table circularity found pre-run; redesigned to independent keys).
T-tier: tal-a15-p12 (TĀ-15 nyāsa complex; work source NO-SOURCE-RECORD —
claims conditional) + MV 3.36–41 extract (CC BY-NC) + frozen body keys.

### What was built

- **`Nyasa.lean`** — 50-locus mātṛkā + Mālinī tables; `ka_uniform`
  (observed shape), `matrika_total` + `malini_total` (50 each),
  `maps_diverge` (50/50 differ — duality quantified), `order_chief` +
  `multiset_kept` (permutation pair). All zero-axiom. Varga→limb rules
  KEPT, labeled unchecked (need second key).
- **`BrokenNyasa.lean`** (pha unplaced): `malini_total` refuses.
- **`BrokenNyasaOrder.lean`** (order replaced): `order_chief` refuses.
- Bridge extended to 7th work (tal15: snapshot + map + EVIDENCE-works;
  edition explicitly UNRESOLVED per work record — bridged, not laundered).

### Scoring (provisional)

- **N-NYASA (amended IDs): PASS.** Control harness extended. EVIDENCE
  121/119+2 (tal-a15-p12 cited with source condition). Coverage 8/107.
- **Honest limits:** mapping inventories + orders; no efficacy/siddhi/
  medical claims; T-tier conditional on source resolution.

---

## 2026-11-06 — Rung 8: pratyāhāra intervals (P-SUT1–4, grammar pilot)

Prereg: PREREGISTRATION-SUTRA-RUNG.md (CANDIDATE-EDITION flagged; T-pin
open — no translation-work/MIRI/GRETIL source on hand; INTAKE-REQUEST-
sivasutras.md filed for a 14-line micro-intake). 43 sounds + 14 marker
tokens; pratyāhāra = sounds from first phoneme up to (excluding) marker.
Bugs caught live: first phoneme dropped (takeWhile skipped marks instead
of terminating); `set_option-in` invalid after docstring (moved above).

### What was built

- **`Pratyahara.lean`** — `ac_vowels` (a..C = 9 vowels), `hal_consonants`
  (ha..L = 34), `markers_excluded` (all 43×13 intervals marker-free;
  needs maxRecDepth, still `decide`), `inventory_43`, `markers_13`
  (Ṅ twice). All zero-axiom.
- **`BrokenSutra.lean`** (ai/au swapped — first twin over-broad,
  harness rejected; surgical redraft passed): `ac_vowels` refuses.

### Scoring (provisional)

- **P-SUT1–4: PASS.** Study backbone: pratyāhāra classes are study sets.

---

## 2026-11-06 — Rung 9: reversal comparison (P-REV1–2, external pilot)

Prereg: PREREGISTRATION-REVERSAL-RUNG.md (rights flagged: © practitioner
source, link-first, comparison control). Python pre-verified both EXACT.

### What was built

- **`Reversal.lean`** — `semi_reversed` ([va,la,ra,ya] = reverse
  [ya,ra,la,va]), `span_reversed` (25-letter ma..ka = reverse alphabet
  ka..ma). Both zero-axiom.
- **`BrokenReversal.lean`** (one pair swapped): `semi_reversed` refuses.

### Scoring (provisional)

- **P-REV1–2: PASS.** Methodological value: external tables checkable
  the same way, rights/register flagged. NOT doctrine, NOT a second key.

---

## 2026-11-06 — Rung 11: containment matrix (E-EMB1–3, gradient-flagged)

Prereg: PREREGISTRATION-EMBED-RUNG.md (E-EMB1–3; gradient reading
flagged R with scholar-confirmation owed; UNIFORM alternative parked
with remodel-ready kill). T-tier ground: tsa07-p01 v9 (thin, one
premise: gross includes subtle substances).

### What was built

- **`Embed.lean`** — 5×5 containment over rank orders: `earth_all5`
  (5/5), `ether_sound_only` (sound alone), `nesting` (finer persists
  upward). All zero-axiom.
- **`BrokenEmbed.lean`** (sound rank lifted; first draft swapped
  water/earth and broke two theorems — harness rejected, surgical
  redraft passed): `ether_sound_only` refuses, siblings pass.

### Scoring (provisional)

- **E-EMB1–3: PASS.** Control harness extended. EVIDENCE 122 entries
  (v9 T-side flagged R/conditional).
- **Honest limits:** shape only; gradient-vs-uniform undecided here;
  size composition with group sizes explicitly future.

---

## 2026-11-06 — Rung 12: ladder law (L-LAD1–3, first Tantraloka formal)

Prereg: PREREGISTRATION-LADDER-RUNG.md (R-ground ONLY: gold argmap
tal-a34-v01..v04, machine-proposed, NO-SOURCE-RECORD; v04 LIVE fork
excluded; v00 frame unit excluded). T-tier ground: none.

### What was built

- **`Ladder.lean`** — 4 ranked means, resort steps, stipulated closure;
  `chain_trans` (chained resorts compose), `terminal_no_successor`
  (no outgoing resort at rank 3, pair-quantified), `abandon_strict`
  (every step +1). All zero-axiom, `decide`.
- **Three surgical twins** (the firewall rejected a law-twin: must_fail
  demands exactly one refusal per file): `BrokenLadderChain` (closure
  drops (0,2) → chain only), `BrokenLadderLeap` (leap (0,2) → strict
  only), `BrokenLadderBeyond` (fifth rung (3,4) → terminal only).
  Finding: terminality has no in-rank mutant — the (3,4) formulation is
  the discovery; bounded quantification would have let it escape
  (caught pre-run, pair-quantified instead).

### Scoring (provisional)

- **L-LAD1–3: PASS.** EVIDENCE 125 entries (tal-a34-p01 chunks, tier R,
  ARGMAP-PINNED). Snapshot trinity 28 works / 154 passages.
- **Honest limits:** membership model, not begetting; closure stipulated
  (model-only, like Tattva sums); translation unreviewed; no witness.

---

## 2026-11-06 — Rung 13: generative 36 (G-GEN1–4, Thon Ly gap closed)

Prereg: PREREGISTRATION-GEN-RUNG.md (R-ground ONLY: v16 primacies +
heap verses, machine-proposed; NO independent key on disk — owed second
projection recorded, not faked). Targets his generativity bar: rules over
axes, no individual tattva named (elements are (group,index) pairs).

### What was built

- **`TattvaGen.lean`** — axes (5 primacy tags, 5 limit functions, root
  roster, dyad/triad roles, 4 modalities × rank-5 rule) + `gen_total`
  COMPUTED (5+5+1+2+3+ΣmodSize = 36 — the numeral appears only in claim
  statements, never as input) + `pure_distinct` + `pentad_uniform` +
  `cut_arith` (deliberately rule-independent so it survives mutations).
  Self-review caught bare literals mid-build (regenerated from tag lists).
- **Three surgical twins**: BrokenGenDup (dup primacy → GEN2 only),
  BrokenGenPerm (6/4 roster split, same total → GEN3 only),
  BrokenGenRoot (emptied root → GEN1 only).
- Dual-projection mirror: per-group counts AND total from one rule set
  (his dual-projection check, structurally).

### Scoring (provisional)

- **G-GEN1–4: PASS.** EVIDENCE 129 entries (R, ARGMAP-PINNED; cut_arith
  model-only). Agreement with Tattva.thirty_six verified in receipt
  (both say 36; kept out of must_fail to preserve twin-separability).
- **Honest limits:** one textual route (v16); begetting unformalized;
  translation unreviewed; no witness; no independent key — generativity
  closed, independence + review still owed.

---

## 2026-11-06 — Rung 14: aperture inventory (A-AP1–2, first H-tier)

Prereg: PREREGISTRATION-APERTURE-RUNG.md (H-ground ONLY: owner
aperture_spec_v0.7; no text, no chunks — r_sources carry the spec).
Answers whether the endgame includes consciousness-theory formalisation:
yes, as H-tier inventory first (phenomenal/selector claims explicitly out).

### What was built

- **`Aperture.lean`** — 9 owner-named ops, `aperture_nine` (count) +
  `aperture_distinct` (Nodup). Zero-axiom, `decide`.
- **Two surgical twins**: BrokenApertureDup (dup → distinct only),
  BrokenApertureDrop (drop → count only).

### Scoring (provisional)

- **A-AP1–2: PASS.** EVIDENCE 131 entries (H, r_sources spec).
- **Honest limits:** inventory, not theory; MEPIT theses untouched;
  owner revision remodels (kill armed); human review owed like all.

---

## 2026-11-06 — Rung 15: Ñāṇavīra structure (N-NAN1–3, R)

Prereg: PREREGISTRATION-NANAVIRA-RUNG.md (R: synthesis-mediated primary
quotes; fixed-point + soteriology explicitly OUT). Self-review rewrote
circular lists into generated-vs-stated form (their profile pattern).

- **`Nanavira.lean`** — generated pairings (pair-product + filter) with
  `matchings_three` computed; `orders_scale` computed-vs-stated
  [4,16,64]; `parasite_erase` functional. Zero-axiom.
- **Three surgical twins** (drop-a-matching, ternary scale, lossy
  erasure — the anti-T_rec). All green.
- EVIDENCE 131+3 entries pending table (this battery).

## 2026-11-06 — Rung 16: tetrahedron selector-facts (T-TET1–3, H)

Prereg: PREREGISTRATION-TETRA-RUNG.md (H: owner-line Fuller proof +
TAL-tetra notes; roster stipulated classical). Nat-truncation caught
pre-run (Euler in Int); twin-statement rule forced def-based twins.

- **`Tetrahedron.lean`** — Platonic roster; `gap_five`, `unique_four`,
  `euler_tet` (Int). Zero-axiom.
- **Three surgical twins** (added solid, dropped tet, 5-restraint Euler).
- Open tension filed, not modeled: 9 chained tetras = 28 distinct ≠ 36
  (pushing material).

---

## What "done" would look like (honest checklist)
- [ ] Every unarmed chunk with an argmap formalized or explicitly parked
- [ ] Witnesses pinned (needs openpatala resolver)
- [ ] Blind re-derivation run at least once (Upaya first)
- [ ] T-C2 scored (rater-2)
- [ ] Week-2+ decodes re-running frozen tests
- [ ] ti/ca signatures found or coordinates dropped from claims
- [ ] Station pass over all 144 moments
- [ ] P-TK1 established or explicitly abandoned
