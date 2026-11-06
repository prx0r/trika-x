/-
  Formal Recognition — kañcuka coordinates + agent finitude (R).

  From logicframework/logicframework2 (C+H): the five kañcukas as
  coordinates of contraction — vidyā→K (partial observability),
  kalā→A (policy space), rāga→V (valence), kāla→T (horizon),
  niyati→C (location). Agent theorem: A_i ⇒ K,A,V,T,C finite.
  "No restriction ⇒ no particular access ⇒ no particular perspective."

  Note (T, for validation): TĀ 9.183 (kalā as activating agency),
  9.203 (four other limitations as effects of kalā), 9.204 (Māyā + five
  as SIX coverings) — cited in logicframework2. The six-covering scheme
  (māyā as sixth) is NOT formalized here: follow-up rung. This file
  covers the five kañcukas only, matching Kancuka.lean's count_5.
-/
namespace FormalRecognition

set_option maxRecDepth 100000
set_option maxHeartbeats 2000000

/-- The five contraction coordinates: K epistemic, A action-space,
    V value-space, T temporal horizon, C causal position. -/
inductive Coord where
  | kn | ac | va | ti | ca
  deriving DecidableEq, Repr

/-- The five kañcukas, logicframework order. -/
inductive Kancuka5 where
  | vidya | kala | raga | kalaTime | niyati
  deriving DecidableEq, Repr

open Coord Kancuka5

/-- Each kañcuka restricts exactly one coordinate (doc table). -/
def restrictsTo : Kancuka5 → Coord
  | .vidya    => .kn
  | .kala     => .ac
  | .raga     => .va
  | .kalaTime => .ti
  | .niyati   => .ca

def allK5 : List Kancuka5 := [.vidya, .kala, .raga, .kalaTime, .niyati]

/-- The mapping covers all five coordinates exactly once (bijective:
    no overlap, no gap — contraction is total and non-redundant).
    eraseDups: a colliding map covers fewer. -/
theorem coords_covered_once :
    ((allK5.map restrictsTo).eraseDups).length = 5 := by decide

/-- Agent: perspective exists only with restriction. -/
structure Agent where
  persp : Bool  -- particular perspective exists
  restr : Bool  -- restriction (contraction) present
  deriving DecidableEq, Repr

def agentWellformed (a : Agent) : Bool := !(a.persp && !a.restr)

def allAgents : List Agent :=
  [true, false].flatMap fun p => [true, false].map fun r => ⟨p, r⟩

/-- Witness: restricted perspective exists (the finite knower). -/
theorem restricted_perspective_exists :
    (allAgents.filter fun a => a.persp && a.restr).length > 0 := by decide

/-- No restriction ⇒ no particular perspective (0 violations). -/
theorem no_unrestricted_perspective :
    (allAgents.filter fun a => !agentWellformed a).length = 0 := by decide

end FormalRecognition
