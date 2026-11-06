/-
  BrokenGenRoot — surgical twin: the root roster emptied (no māyā slot).

  Only gen_total refuses (35 ≠ 36); primacies, uniformity, and the fixed
  arithmetic identity all hold. Models a rootless derivation: every group
  internally sound, one slot missing from the whole.
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
  modalities.flatMap fun m => (List.range 5).map fun i => (m, i)

def rootRoster : List Nat := []

theorem gen_total :
    primacies.length + limitTags.length + rootRoster.length + dyadTags.length +
      triadTags.length + modalities.foldl (fun acc m => acc + modSize m) 0
      = 36 := by decide

theorem pure_distinct : primacies.Nodup := by decide

theorem pentad_uniform : ∀ m ∈ modalities,
    (pentadRoster.filter fun p => p.1 == m).length = 5 := by decide

theorem cut_arith : (5 + 1 + 2 + 3 + 4 * 5) = 36 - 5 := by decide

end FormalTrika
