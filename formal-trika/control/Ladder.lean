/-
  Formal Trika — L-LAD: the a34 ladder law (resort by abandonment), checked.

  Ground (R, not T): gold argmap tal-a34-v01..v04 (GOLD #54, machine-proposed;
  v04 LIVE fork excluded; record NO-SOURCE-RECORD). See
  PREREGISTRATION-LADDER-RUNG.md. This file models the step-structure only:
  four ranked means, resort steps, stipulated reachability closure.

  What this file IS: finite step arithmetic (`decide` inside scope only).
  What it is NOT: doctrine, Sanskrit semantics, or proof that abandonment
  causes ascent (the text's generative claim is NOT formalized here).
-/
namespace FormalTrika

/-- The four means, lowest to highest (names only, no semantics). -/
def means : List String := ["anava", "sakta", "sambhava", "anupaya"]

/-- Ranks (bounded quantification domain; all resort ends lie inside). -/
def ranks : List Nat := [0, 1, 2, 3]

/-- Resort steps: each rung is resorted by abandoning it for the next. -/
def resort : List (Nat × Nat) := [(0, 1), (1, 2), (2, 3)]

/-- Reachability closure, stipulated as data (model only, like Tattva sums). -/
def ladderClosure : List (Nat × Nat) :=
  [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

/-- L-LAD1: chained resorts compose inside the closure (transitivity facet). -/
theorem chain_trans : ∀ a ∈ ranks, ∀ b ∈ ranks, ∀ c ∈ ranks,
    (a, b) ∈ resort → (b, c) ∈ resort → (a, c) ∈ ladderClosure := by decide

/-- L-LAD2: the terminal means (anupāya, rank 3) has no outgoing resort. -/
theorem terminal_no_successor : ∀ p ∈ resort, p.1 ≠ 3 := by decide

/-- L-LAD3: every resort step ascends exactly one rung (strict, no leaps). -/
theorem abandon_strict : ∀ p ∈ resort, p.2 = p.1 + 1 := by decide

end FormalTrika
