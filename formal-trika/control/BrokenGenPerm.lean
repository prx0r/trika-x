/-
  BrokenGenPerm — surgical twin: one roster member moved between modalities
  ("knowing" holds 6, "doing" holds 4; same 20 total).

  Only pentad_uniform refuses; the total, the primacies, and the cut all
  hold. Models non-uniform derivation: same count, wrong distribution.
-/
namespace FormalTrika

def primacies : List String := ["cit", "ananda", "iccha", "jnana", "kriya"]

def limitTags : List String := ["agency", "knowledge", "desire", "time", "place"]

def dyadTags : List String := ["enjoyer", "matrix"]

def triadTags : List String := ["discerning", "imaking", "attending"]

def modalities : List String := ["knowing", "doing", "subtle", "gross"]

def modSize : String → Nat
  | _ => 5

def pentadRoster : List (String × Nat) :=
  ([("knowing", 0), ("knowing", 1), ("knowing", 2), ("knowing", 3), ("knowing", 4),
    ("knowing", 0)] : List (String × Nat)) ++
  ([("doing", 1), ("doing", 2), ("doing", 3), ("doing", 4)] : List (String × Nat)) ++
  (["subtle", "gross"].flatMap fun m => (List.range 5).map fun i => (m, i))

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
