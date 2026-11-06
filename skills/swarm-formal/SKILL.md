# SKILL: swarm-formal — the swarm process for formal rungs

*Companion law to the rung discipline (prereg → model → twin → evidence),
never a replacement. Hand-modeled rungs remain the gold path; this skill
adds the swarm layer on top for volume. The assessor (smart agent, full
knowledge) owns every tier call, fidelity verdict, and EVIDENCE entry.
Nothing beam writes is canonical. Nothing beam writes is T-tier.*

*Why it exists: a 93-unit ahnika cannot be hand-formalized verse by verse
in one session without turning the smart agent into a batch worker. The
swarm drafts sketches; the assessor spends judgment only where judgment
lives. DUMB scales horizontally (free). SMART batches judgment (never
one-offs). Never trade one for the other.*

## 0. Scope boundary (read twice)

Swarm MAY produce: Lean sketches (finite models from gold argmaps), twin
sketches (broken copies), span-bind sweeps (token containment vs volume
manifests), blind re-derivations (same prompt, other families), count
cross-checks (argmap numbers vs model numbers), receipt assembly.
Swarm MUST NEVER produce: EVIDENCE entries, tier calls, T-tier claims,
fidelity signoff, practice inference, pushes, witness statements.
Every swarm artifact lands in `formal-trika/swarm/` labeled
machine-proposed with model + prompt sha. Promotion into `control/` is an
assessor act (gates green + fidelity read + prereg linked), never a worker
act. A draft that invents a tier is rejected, not fixed.

## 1. The cast

- **Drafters (N=3–5, beam-free/CF free-tier, $0).** Dumb, fast, obedient.
  They hold no doctrine; they follow packets. One task, one prompt sha.
- **The assessor (smart agent).** Holds the prereg, the argmaps, the gates.
  Writes transmission packets first, reviews every sketch, adjudicates
  fidelity, runs gates + proofs, owns every EVIDENCE entry and tier.
- **Deterministic gates.** Compile (pinned Lean 4.34.1), twin-refusal
  (`must_fail.py`, exactly-one-refusal rule), tier presence, count checks.
  Scripts assemble, never author. Pydantic-style shape checks where cheap;
  only the assessor validates MEANING (membership vs begetting has no
  mechanical proxy — CRUX-03 proved it twice).

## 2. Transmission (the step that makes it work)

Never send drafters a bare verse. Every packet carries a prereg the
assessor writes FIRST:

1. The claim in words (one para) → the formalizable skeleton (named
   theorems) → **the traps** (look-alikes, flattening risks, numerology
   temptations, unformalizable remainders) → kill conditions → tiers.
2. Rule: transmission tells drafters what the argument IS, what to look
   FOR, and how to approach it — never what conclusion to reach. A packet
   that dictates the model is fabrication outsourcing.

## 3. Task kinds + gates (mechanical first, meaning last)

| kind | drafter writes | shape gate | assessor gate |
|---|---|---|---|
| `rung-sketch` (one passage) | Lean model + named theorems | compiles; only finite defs; named theorems match packet | fidelity read vs argmap; tier check; twin order |
| `twin-sketch` | broken copy | compiles-or-fails deterministically | surgical review (one refusal each; unrelated breakage rejected — BrokenLadder lesson) |
| `bind-sweep` | token-containment rows vs spans | span shas re-verified; normalization stated | compound-tolerance review; tier stays R |
| `blind-rerun` | re-derivation from vocab | same prompt sha; receipted | SAME/DIFFERENT/GAP grading vs checked-in |

**Scope rule (proven):** one passage per task, never multi-chunk sketches;
rungs stay chunk-scoped like translations stay verse-scoped. Tasks over one
passage degenerate into flattened mush (Embed lesson: matrix first, verses never).
**Size routing:** XS passages (≤10 units) the assessor models directly —
reviewing costs more than drafting. Bigger: drafters sketch first, assessor
redacts. Never the reverse.
Bounce notes must be actionable (wrong bound, leaky quantifier, invented
tier, flattened relation). Max 3 attempts, then assessor hand-models. Failed
tasks keep their notes as history.

## 4. Calibration (prove the tool before scaling it)

Before scaling ANY new drafter path, benchmark against a gold rung:

1. Pick a finished rung (Embed containment, Ladder law).
2. Blind sketch (withhold the checked-in file), then score: compiles ·
   twins surgical (exactly-one-refusal each) · tiers R-only · no invented
   doctrine · relation fidelity (assessor reads).
3. Record verdict below. Scale only paths that pass; keep the rest manual.

Standing results: _none yet — first calibration is the Embed re-derivation
trial, owed before any swarm sketch enters `control/`._

## 5. Autonomy loop (how a batch runs while the assessor reviews)

```bash
python3 tools/arrivals.py --rebuild     # pins CURRENT, derived data fresh
# drafters, in parallel (stateless calls, prompt sha logged):
python3 tools/blind_family2.py --model @cf/mistralai/mistral-small-3.1-24b-instruct
# assessor, in parallel:
sh formal-trika/control/run.sh          # compile + twin gates
python3 formal-trika/tools/evidence_check.py
python3 formal-trika/tools/pushback.py --draft D --refs R --model mock  # live behind opt-in
```

Self-discipline built in: prompt shas in every receipt; fresh session per
call (no history); free-tier only (neurons logged, quota untouched);
fail-closed (null content = ERROR, never data). Workers are prompts, not
processes — relaunch per batch.

## 6. Gold-standard bar (unchanged — the swarm feeds it, never lowers it)

A rung is DONE only when, after assessor promotion: prereg linked ·
compiles on pinned Lean · every twin refuses surgically · EVIDENCE entry
with chunks + tier + note · TABLE reading · axiom audit CLEAN · runs
receipt · process notes same session. T-tier never machine-assigned.
Unformalizable chapters record that as the finding (no forced rungs).

## 7. Failure log (numbered — see mistakes pattern)

- F1: over-broad twin (BrokenLadder cycle broke 3 theorems; must_fail
  demands one) — rejected, split into 3 surgical twins.
- F2: bounded-quantifier escape ((3,4) ∉ ranks passed terminal) —
  caught pre-run, pair-quantified. New rule: bounds are claims too.
- F3: JSON comma surgery doubled a comma (assumed comma-less, didn't
  assert) — repaired + validated. New rule: assert line-end state first.
- F4: branch-artifact drift (arrivals read a feature branch as HEAD) —
  rebased + returned to master. New rule: canonical checkout before pins.

## 8. Porting (this skill's first customer)

translation-work formal stage (PR #10, `process/FORMAL-STAGE-PROPOSAL.md`)
is this skill run by their lane: same cast (their assessor judges), same
gates (their validate_all + our must_fail), same bar (machine-proposed,
never canonical). Lanes keep their gates; the skill travels, authority doesn't.
