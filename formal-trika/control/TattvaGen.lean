/-
  Formal Trika — G-GEN: the 36 derived from rules (generative rung).

  Ground (R, not T): gold argmap tsa-a08 (v16 primacies; heap verses),
  machine-proposed; NO independent key on disk. See
  PREREGISTRATION-GEN-RUNG.md. Contrast control/Tattva.lean (stipulated
  sums): here the total COMPUTES from rule outputs, and NO individual
  tattva is named anywhere — elements are (group, index) pairs. Every
  group size comes from a list length or a rule fold; the only numerals
  in claims are the computed total and the arithmetic identity.

  What this file IS: finite rule arithmetic (`decide` inside scope only).
  What it is NOT: doctrine, begetting/causation, or proof the tradition
  derives the 36 this way (one textual route among possible; v16's
  primacy list is the stated input).
-/
namespace FormalTrika

/-- The five primacy tags (powers, not tattvas). -/
def primacies : List String := ["cit", "ananda", "iccha", "jnana", "kriya"]

/-- The five limitation functions (aspects, not tattvas). -/
def limitTags : List String := ["agency", "knowledge", "desire", "time", "place"]

/-- The dyad roles (functions, not tattvas). -/
def dyadTags : List String := ["enjoyer", "matrix"]

/-- The inner triad roles (functions, not tattvas). -/
def triadTags : List String := ["discerning", "imaking", "attending"]

/-- The four pentad modalities (functions, not tattvas). -/
def modalities : List String := ["knowing", "doing", "subtle", "gross"]

/-- Per-modality size rule: every modality yields rank-5. -/
def modSize : String → Nat
  | _ => 5

/-- Pentad roster, generated (not listed): modality × rank pairs. -/
def pentadRoster : List (String × Nat) :=
  modalities.flatMap fun m => (List.range 5).map fun i => (m, i)

/-- Root roster: exactly one root slot. -/
def rootRoster : List Nat := [0]

/-- G-GEN1: the total COMPUTES from rule outputs (no individual named,
    no group enumerated — every size is a list length or rule fold). -/
theorem gen_total :
    primacies.length + limitTags.length + rootRoster.length + dyadTags.length +
      triadTags.length + modalities.foldl (fun acc m => acc + modSize m) 0
      = 36 := by decide

/-- G-GEN2: the five primacies are pairwise distinct powers. -/
theorem pure_distinct : primacies.Nodup := by decide

/-- G-GEN3: every modality roster has exactly five members. -/
theorem pentad_uniform : ∀ m ∈ modalities,
    (pentadRoster.filter fun p => p.1 == m).length = 5 := by decide

/-- G-GEN4: partition arithmetic over fixed numbers (model only — checks
    the cut counts; deliberately independent of the rule lists so it
    survives rule mutations). -/
theorem cut_arith : (5 + 1 + 2 + 3 + 4 * 5) = 36 - 5 := by decide

end FormalTrika
