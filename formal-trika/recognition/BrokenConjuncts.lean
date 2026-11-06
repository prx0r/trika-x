/-
  RECOGNITION — BrokenConjuncts: the KNOWN FAILURE (mutation control).

  Identical to Conjuncts.lean except veridicality is DROPPED from
  recogHolds (identification without truth). The misidentification
  theorem MUST FAIL: without veridicality, false identifications
  "recognize". Profound experience without truth is conversion,
  not recognition — this file proves the instrument knows it.
-/
namespace FormalRecognition

structure RecogInst where
  present    : Bool
  acquainted : Bool
  identify   : Bool
  a : Fin 2
  b : Fin 2
  deriving DecidableEq, Repr

/-- MUTATED: veridicality (a == b) removed. -/
def recogHolds (r : RecogInst) : Bool :=
  r.present && r.acquainted && r.identify

def allRecogInsts : List RecogInst :=
  [true, false].flatMap fun p => [true, false].flatMap fun q =>
    [true, false].flatMap fun i => ([0, 1] : List (Fin 2)).flatMap fun a =>
      ([0, 1] : List (Fin 2)).map fun b => ⟨p, q, i, a, b⟩

/-- MUST FAIL: misidentifications now "recognize". -/
theorem misidentification_never_recognizes :
    (allRecogInsts.filter fun r => (r.a != r.b) && recogHolds r).length = 0 := by
  decide
