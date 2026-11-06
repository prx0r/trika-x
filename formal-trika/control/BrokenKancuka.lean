/- Mutation: two coverings map to the same capacity. The same distinctness
   theorem as in Kancuka.lean must fail for this specific reason. -/
namespace FormalTrika
inductive Kancuka where
  | kala | vidya | raga | kalaTime | niyati
  deriving DecidableEq, Repr
inductive Capacity where
  | allDoership | allKnowledge | satisfaction | eternity | pervasion
  deriving DecidableEq, Repr
open Kancuka Capacity
def kancukas : List Kancuka := [.kala, .vidya, .raga, .kalaTime, .niyati]
def restricts : Kancuka → Capacity
  | .kala     => .allDoership
  | .vidya    => .allDoership -- deliberate collision
  | .raga     => .satisfaction
  | .kalaTime => .eternity
  | .niyati   => .pervasion
theorem pairings_distinct : ((kancukas.map restricts).eraseDups).length = 5 := by decide
end FormalTrika
