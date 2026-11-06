/-
  RECOGNITION — BrokenCoords: KNOWN FAILURE (mutation control).

  Identical to Coords.lean except TWO kañcukas restrict the SAME
  coordinate (kalā and niyati both → causal position) while the
  temporal horizon is restricted by nothing. The coverage theorem
  MUST FAIL: contraction with a gap and an overlap is not total.
-/
namespace FormalRecognition

inductive Coord where
  | kn | ac | va | ti | ca
  deriving DecidableEq, Repr

inductive Kancuka5 where
  | vidya | kala | raga | kalaTime | niyati
  deriving DecidableEq, Repr

open Coord Kancuka5

/-- MUTATED: kala and niyati collide on .ca; .ti uncovered. -/
def restrictsTo : Kancuka5 → Coord
  | .vidya    => .kn
  | .kala     => .ca
  | .raga     => .va
  | .kalaTime => .ti
  | .niyati   => .ca

def allK5 : List Kancuka5 := [.vidya, .kala, .raga, .kalaTime, .niyati]

/-- MUST FAIL: only 4 distinct coordinates covered, not 5. -/
theorem coords_covered_once :
    ((allK5.map restrictsTo).eraseDups).length = 5 := by decide
