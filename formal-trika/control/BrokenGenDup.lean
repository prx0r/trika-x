/-
  BrokenGenDup — surgical twin: primacy list with a duplicate ("cit" twice).

  Only pure_distinct refuses; the total still computes to 36 and every
  other facet holds. Models a collapsed primacy (two powers, one name).
-/
namespace FormalTrika

def primacies : List String := ["cit", "cit", "iccha", "jnana", "kriya"]

def limitTags : List String := ["agency", "knowledge", "desire", "time", "place"]

def dyadTags : List String := ["enjoyer", "matrix"]

def triadTags : List String := ["discerning", "imaking", "attending"]

def modalities : List String := ["knowing", "doing", "subtle", "gross"]

def modSize : String → Nat
  | _ => 5

def pentadRoster : List (String × Nat) :=
  modalities.flatMap fun m => (List.range 5).map fun i => (m, i)

def rootRoster : List Nat := [0]

theorem gen_total :
    primacies.length + limitTags.length + rootRoster.length + dyadTags.length +
      triadTags.length + modalities.foldl (fun acc m => acc + modSize m) 0
      = 36 := by decide

theorem pure_distinct : primacies.Nodup := by decide

theorem pentad_uniform : ∀ m ∈ modalities,
    (pentadRoster.filter fun p => p.1 == m).length = 5 := by decide

theorem cut_arith : (5 + 1 + 2 + 3 + 4 * 5) = 36 - 5 := by decide

end FormalTrika
