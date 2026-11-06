/-
  Formal Trika — F3: grace as a free variable (F-GRACE).

  From the day-7 decode: grace-clauses (#26 "nothing can be done",
  #28 "levitating out", #33 "create the conditions for grace") state
  possible preconditions; the transition itself takes an unconditioned step
  in this reconstruction. Tantrasāra 8.35 and 8.39 mention power-descent
  and grace in specific contexts; they do not establish this model's
  universal readiness-and-grace biconditional.

  What this file IS: the report's structure. Flip requires BOTH readiness
  (surrender/resolve/readiness predicates — the diarist's "conditions")
  AND a grace flag. Treating it as exogenous to the model is a modeling
  choice, not a claim that grace is external to consciousness. Either flag
  alone is insufficient inside this finite model of 4 states by definition.
  What it is NOT: a proof that grace exists, or that any lived transition
  involved it. The empirical bite is T-C3 (clause audit), not this file.
-/
namespace FormalRecognition

/-- The minimal transition state: readiness (the conditions) + grace. -/
structure GraceState where
  ready : Bool  -- surrender/resolve/readiness present
  grace : Bool  -- the unconditioned step (śaktipāta-side, exogenous)
  deriving DecidableEq, Repr

/-- Flip iff BOTH hold. Neither alone suffices — that is the whole claim. -/
def gflip (m : GraceState) : Bool := m.ready && m.grace

def allGraceStates : List GraceState :=
  [true, false].flatMap fun r => [true, false].map fun g => ⟨r, g⟩

/-- Readiness alone never flips (the day-7 #26 structure). -/
theorem readiness_insufficient :
    (allGraceStates.filter fun m => m.ready && !m.grace && gflip m).length = 0 := by
  decide

/-- Grace alone never flips an unreadied state (no bypass). -/
theorem grace_insufficient_alone :
    (allGraceStates.filter fun m => !m.ready && m.grace && gflip m).length = 0 := by
  decide

/-- The biconditional, over all 4 states: flip ↔ ready ∧ grace. -/
theorem flip_iff_ready_and_grace :
    (allGraceStates.filter fun m => gflip m == (m.ready && m.grace)).length = 4 := by
  decide

/-- Both witnesses exist: a ready-but-unflipped state and a graced-but-unflipped one. -/
theorem both_gaps_exist :
    (allGraceStates.filter fun m => m.ready && !gflip m).length > 0 ∧
    (allGraceStates.filter fun m => m.grace && !gflip m).length > 0 := by
  decide

end FormalRecognition
