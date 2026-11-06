/-
  Formal Recognition — A-APP: MUTANT: impure-unready flips when graced (must fail unready_unreachable ONLY).

  Composes two independently built models (no imports — restates their
  shared precondition explicitly, cites below):
  - Grace.lean: flip ↔ ready ∧ grace (flip needs readiness AND grace).
  - Upaya.lean: sambhava/sakta/anava each need readiness (plus own gates).
  Result: a single readiness gate — ¬ready ⟹ no flip under any means —
  which the syllabus compiler CITES for study-fallback (eligibility.py:
  unknown → study). First rung whose theorem is consumed downstream.

  What this file IS: cross-model robustness of one precondition + the
  grace/means categorical distinction, over a finite product model.
  What it is NOT: a practice prescription, a guru, or metaphysics.
  R-tier composition; T ground inherited (tsa08-p02 v35; tsa08-p01 v17).
  Finite model; `decide` inside scope only.
-/
namespace FormalRecognition

/-- Combined practice state (restates Grace.GraceState + Upaya.MeansState
    shared readiness precondition; see those files, not here). -/
structure PracticeState where
  ready : Bool  -- ripe (both models require it)
  grace : Bool  -- unconditioned step (Grace side)
  pure  : Bool  -- vikalpa purified (Upaya śākta side)
  deriving DecidableEq, Repr

def allPractice : List PracticeState :=
  [true, false].flatMap fun r => [true, false].flatMap fun g =>
    [true, false].map fun p => { ready := r, grace := g, pure := p }

/-- Flip (composed): readiness AND grace AND (a means' readiness gate,
    here the shared one). -/
def flip (s : PracticeState) : Bool := s.grace && (s.ready || !s.pure)

/-- The three means' readiness gates (shared shape, restated). -/
def meansReady (s : PracticeState) : Bool := s.ready

/-- A-APP1: unready ⟹ no flip under any means (study-fallback, backed). -/
theorem unready_unreachable :
    (allPractice.filter fun s => !s.ready && flip s).length = 0
    && (allPractice.filter fun s => !s.ready && meansReady s).length = 0 := by decide

/-- A-APP2: grace is conjunctive, not substitutable — a graced-but-unready
    state does not flip (grace ≠ means; categories distinct). -/
theorem grace_not_a_means :
    flip { ready := false, grace := true, pure := true } = false := by decide

end FormalRecognition
