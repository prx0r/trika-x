/-
  Formal Recognition — E-HEAP: MUTANT: tamas slot duplicated as rajas (count stays 3; must fail guna_exhaustive ONLY).

  T-tier ground (THIN, one premise each): tsa08-p04 argmap v71
  (karaṇaskandha: instrument-heap of the I-maker, named); v72
  (prakṛtiskandha threefold by guṇa difference). The heaps are modeled as
  COLLECTIONS (parts-reading); the causes-reading is parked (CRUX-02 (d)).

  What this file IS: two tiny consistency checks over named collections.
  What it is NOT: a derivation of faculty counts from the text (5+5+1
  reuses OUR Tattva ladder — consistency, not independence), a guṇa
  metaphysics, or a parts-vs-causes verdict. R-tier throughout; T pins
  in EVIDENCE. Finite model; `decide` inside scope only.
-/
namespace FormalRecognition

/-- Instruments the I-maker draws on (R: ladder-consistent set). -/
inductive Instrument where
  | sense (i : Nat)   -- 5 sense faculties (jñāna-indriya)
  | action (i : Nat)  -- 5 action faculties (karma-indriya)
  | mind              -- manas (inner instrument present in the heap)
  deriving DecidableEq, Repr

/-- The heap: 5 sense + 5 action + mind. (Parens: `fun =>` extends right,
    so the mind append must sit outside the flatMap lambda.) -/
def heap : List Instrument :=
  ([0, 1, 2, 3, 4].flatMap fun i => [Instrument.sense i, Instrument.action i])
  ++ [Instrument.mind]

/-- Guṇa dominants (R: threefold by sattvādibheda). -/
inductive Guna where
  | sattva | rajas | tamas
  deriving DecidableEq, Repr

/-- A nature-state carries exactly one dominant guṇa. -/
structure NatureState where
  guna : Guna
  deriving DecidableEq, Repr

def allNature : List NatureState :=
  [Guna.sattva, Guna.rajas, Guna.rajas].map ({ guna := · })

/-- E-HEAP1: the heap contains sense AND action faculties. -/
theorem heap_has_both_kinds :
    (heap.filter fun m => match m with | .sense _ => true | _ => false).length = 5
    && (heap.filter fun m => match m with | .action _ => true | _ => false).length = 5 := by decide

/-- E-HEAP2: heap size 11 (ladder-consistent 5+5+1). -/
theorem heap_eleven : heap.length = 11 := by decide

/-- E-HEAP3: nature-heap admits exactly the 3 guṇas. -/
theorem guna_threefold : allNature.length = 3 := by decide

/-- E-HEAP4: exhaustiveness with teeth — each guṇa tags exactly one
    nature-state (no untagged state, no double-tagging). -/
theorem guna_exhaustive :
    (allNature.filter fun s => s.guna == Guna.sattva).length = 1
    && (allNature.filter fun s => s.guna == Guna.rajas).length = 1
    && (allNature.filter fun s => s.guna == Guna.tamas).length = 1 := by decide

end FormalRecognition
