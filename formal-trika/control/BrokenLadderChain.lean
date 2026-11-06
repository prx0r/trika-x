/-
  BrokenLadderChain — surgical twin: the closure drops (0, 2).

  Only chain_trans refuses (0→1→2 no longer composes); terminal and strict
  still hold. Models a mis-stipulated reachability table.
-/
namespace FormalTrika

def means : List String := ["anava", "sakta", "sambhava", "anupaya"]

def ranks : List Nat := [0, 1, 2, 3]

def resort : List (Nat × Nat) := [(0, 1), (1, 2), (2, 3)]

def ladderClosure : List (Nat × Nat) :=
  [(0, 1), (0, 3), (1, 2), (1, 3), (2, 3)]

theorem chain_trans : ∀ a ∈ ranks, ∀ b ∈ ranks, ∀ c ∈ ranks,
    (a, b) ∈ resort → (b, c) ∈ resort → (a, c) ∈ ladderClosure := by decide

theorem terminal_no_successor : ∀ p ∈ resort, p.1 ≠ 3 := by decide

theorem abandon_strict : ∀ p ∈ resort, p.2 = p.1 + 1 := by decide

end FormalTrika
