/-
  Formal Trika — N-NAN: Ñāṇavīra fundamental structure (finite core).

  Ground (R, not T): NANAVIRA-FUNDAMENTAL-STRUCTURE-SYNTHESIS.md quoting
  the primary text (nanavira.org Static/Dynamic Aspects), machine-
  unreviewed. See PREREGISTRATION-NANAVIRA-RUNG.md. Models ONLY: the
  base matchings (generated, not listed), the order scaling (computed vs
  stated rows, bounded), and parasite erasure as list surgery. No
  phenomenology, no soteriology, no debate position.

  What this file IS: finite combinatorics (`decide` inside scope only).
  What it is NOT: proof of the reflexivity guarantee (needs higher-order
  apparatus — open), stream-entry, nibbāna, or any claim about experience.
  Covers: Static Aspect base + orders 0–2 + Dynamic footnote j erasure.
-/
namespace FormalTrika

/-- The four base members (positional tags, not entities). -/
def nanMembers : List Nat := [0, 1, 2, 3]

/-- All unordered member pairs, generated. -/
def allUnorderedPairs : List (Nat × Nat) :=
  nanMembers.flatMap fun i =>
    (nanMembers.filter fun j => decide (i < j)).map fun j => (i, j)

/-- Canonical order on pairs (kills double-counted (p,q)/(q,p)). -/
def pairLT : Nat × Nat → Nat × Nat → Bool
  | (a, b), (c, d) => decide (a < c ∨ (a = c ∧ b < d))

/-- Disjoint covering pairs = perfect matchings, generated. -/
def allPairings : List (List (Nat × Nat)) :=
  (allUnorderedPairs.flatMap fun p =>
    (allUnorderedPairs.filter fun q => pairLT p q).map fun q => [p, q]).filter
    fun pr => match pr with
      | [(a, b), (c, d)] => decide ([a, b, c, d].Nodup ∧ ([a, b, c, d].all fun x => x < 4))
      | _ => false

/-- N-NAN1: exactly three perfect matchings — computed, then checked
    against the textual three (columns/rows/both). -/
theorem matchings_three : allPairings.length = 3 := by decide

/-- Order-n member count rule: ×4 per order (textual sequence). -/
def orderCount : Nat → Nat
  | n => 4 ^ (n + 1)

/-- N-NAN2: computed orders against stated rows [4, 16, 64] (bounded). -/
theorem orders_scale : (List.range 3).map orderCount = [4, 16, 64] := by decide

/-- Parasite erasure: removing the distinguished non-member recovers members. -/
def eraseParasite (members : List Nat) (parasite : Nat) : List Nat :=
  (members ++ [parasite]).filter fun m => m != parasite

/-- N-NAN3: erasure without change (structural half of removal). -/
theorem parasite_erase : eraseParasite [0, 1, 2, 3] 99 = [0, 1, 2, 3] := by decide

end FormalTrika
