/-
  RECOGNITION — BrokenMemory: KNOWN FAILURE (mutation control).

  Identical to Memory.lean except wellformedness is DROPPED (any
  combination admitted). The foundation theorem MUST FAIL: without the
  M₁–M₃ requirement, foundationless M₄ "exists". A memory theory that
  permits autonoetic recollection with no retention, continuity, or
  attribution is not a theory — the instrument must refuse it.
-/
namespace FormalRecognition

structure Mem5 where
  m1 : Bool
  m2 : Bool
  m3 : Bool
  m4 : Bool
  m5 : Bool
  deriving DecidableEq, Repr

/-- MUTATED: wellformedness dropped — everything admitted. -/
def wellformedMems : List Mem5 :=
  [true, false].flatMap fun a => [true, false].flatMap fun b =>
    [true, false].flatMap fun c => [true, false].flatMap fun d =>
      [true, false].map fun e => ⟨a, b, c, d, e⟩

/-- MUST FAIL: foundationless M₄ now occurs. -/
theorem m4_requires_foundation :
    (wellformedMems.filter fun m => m.m4 && !(m.m1 && m.m2 && m.m3)).length = 0 := by
  decide
