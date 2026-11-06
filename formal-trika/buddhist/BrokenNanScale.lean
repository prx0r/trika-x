/-
  BrokenNanScale — surgical twin: orders scale by three, not four.

  Only orders_scale refuses ([4,12,36] ≠ [4,16,64]); matchings and erasure
  intact. Models a ternary reflexion hierarchy (wrong base, right shape).
-/
namespace FormalTrika

def nanMembers : List Nat := [0, 1, 2, 3]

def allUnorderedPairs : List (Nat × Nat) :=
  nanMembers.flatMap fun i =>
    (nanMembers.filter fun j => decide (i < j)).map fun j => (i, j)

def pairLT : Nat × Nat → Nat × Nat → Bool
  | (a, b), (c, d) => decide (a < c ∨ (a = c ∧ b < d))

def allPairings : List (List (Nat × Nat)) :=
  (allUnorderedPairs.flatMap fun p =>
    (allUnorderedPairs.filter fun q => pairLT p q).map fun q => [p, q]).filter
    fun pr => match pr with
      | [(a, b), (c, d)] => decide ([a, b, c, d].Nodup ∧ ([a, b, c, d].all fun x => x < 4))
      | _ => false

def orderCount : Nat → Nat
  | n => 4 ^ n * 3

theorem matchings_three : allPairings.length = 3 := by decide

theorem orders_scale : (List.range 3).map orderCount = [4, 16, 64] := by decide

def eraseParasite (members : List Nat) (parasite : Nat) : List Nat :=
  (members ++ [parasite]).filter fun m => m != parasite

theorem parasite_erase : eraseParasite [0, 1, 2, 3] 99 = [0, 1, 2, 3] := by decide

end FormalTrika
