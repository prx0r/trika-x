/-
  RECOGNITION — BrokenNonEntail: the KNOWN FAILURE (mutation control).

  Identical to NonEntail.lean except the entailment is SMUGGLED IN as a
  well-formedness rule: chains where A..E hold but F fails are EXCLUDED.
  The abcde_without_f witness MUST FAIL: begging the question destroys
  the investigation. This is what a rigged catechism looks like —
  the file that must never check.
-/
namespace FormalRecognition

structure Chain where
  a : Bool
  b : Bool
  c : Bool
  d : Bool
  e : Bool
  f : Bool
  deriving DecidableEq, Repr

def allChains : List Chain :=
  [true, false].flatMap fun a => [true, false].flatMap fun b =>
    [true, false].flatMap fun c => [true, false].flatMap fun d =>
      [true, false].flatMap fun e => [true, false].map fun f =>
        ⟨a, b, c, d, e, f⟩

/-- MUTATED: the conclusion is built into the admission rule. -/
def wellformed (m : Chain) : Bool :=
  !((m.a && m.b && m.c && m.d && m.e) && !m.f)

def admitted : List Chain := allChains.filter wellformed

/-- MUST FAIL: the witness was excluded by fiat, so the set is empty. -/
theorem abcde_without_f :
    (admitted.filter fun m =>
      m.a && m.b && m.c && m.d && m.e && !m.f).length > 0 := by
  decide
