/-
  BrokenLadderBeyond — surgical twin: resort gains (3, 4), a fifth rung.

  Only terminal_no_successor refuses: the step is still +1 (strict holds)
  and starts no new chains (nothing leaves 4). Models ascent beyond the
  enumerated means — the law's terminality is exactly the claim that no
  fifth rung exists, and this twin denies precisely that.
-/
namespace FormalTrika

def means : List String := ["anava", "sakta", "sambhava", "anupaya"]

def ranks : List Nat := [0, 1, 2, 3]

def resort : List (Nat × Nat) := [(0, 1), (1, 2), (2, 3), (3, 4)]

def ladderClosure : List (Nat × Nat) :=
  [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

theorem chain_trans : ∀ a ∈ ranks, ∀ b ∈ ranks, ∀ c ∈ ranks,
    (a, b) ∈ resort → (b, c) ∈ resort → (a, c) ∈ ladderClosure := by decide

theorem terminal_no_successor : ∀ p ∈ resort, p.1 ≠ 3 := by decide

theorem abandon_strict : ∀ p ∈ resort, p.2 = p.1 + 1 := by decide

end FormalTrika
