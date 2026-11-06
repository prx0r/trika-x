/-
  Formal Trika — CONTROL TK-C1: the seven experients (saptapramātṛ).

  Three binary mala axes (āṇava × māyīya × kārma) give 8 combinations; ONE is
  ill-formed by general rule R1, leaving exactly the traditional 7.

  Source key (T): paramarthasara saptadha-pramātṛ scheme (GOLD) +
  tantrasara-a08 p03 (māyāgarbhādhikāriṇaḥ … vijñānākala … kalāpuṃviveka …).
  Name-to-row mapping is R (reconstruction): the mantra-triad split
  (mantra/mantreśvara/mantramaheśvara) is adhvan-positional, not
  mala-compositional — see P-TK1b. The COUNT theorem does not depend on names.
-/
import Mala
namespace FormalTrika
open Mala

/-- An experient station: which malas are present. -/
structure Pramatr where
  anava  : Bool   -- āṇavamala present
  mayiya : Bool   -- māyīyamala present
  karma  : Bool   -- kārmamala present
  deriving DecidableEq, Repr

/-- All 8 combinations of the three axes. -/
def combos : List Pramatr :=
  [true, false].flatMap fun a => [true, false].flatMap fun m =>
    [false, true].map fun k => ⟨a, m, k⟩

/-- GENERAL RULE (the only rule clause; R-tier justification):
    karma never floats free — it binds only where there is atomic ignorance
    (āṇava) or differentiation (māyīya) to bind through. Excludes exactly
    (F,F,T): karma with neither ignorance nor world to act in. -/
def wellformed (p : Pramatr) : Bool :=
  !(p.karma && !p.mayiya && !p.anava)   -- R1: no free-floating karma

/-- The generated set: rows satisfying all general rules. -/
def generated : List Pramatr := combos.filter wellformed

/-- How many malas each generated row carries (profile, order as generated). -/
def malaCount (p : Pramatr) : Nat :=
  (if p.anava then 1 else 0) + (if p.mayiya then 1 else 0) + (if p.karma then 1 else 0)

/-- TK-C1a: eight axis combinations. -/
theorem eight_combos : combos.length = 8 := by decide

/-- TK-C1b: the tradition's seven (saptapramātṛ). -/
theorem seven : generated.length = 7 := by decide

/-- TK-C1c: mala-count profile of the seven rows, in generation order.
    Observed (not hand-set): the count theorem is `seven`; this records the
    shape. Generation order: (T,T,F)=2, (T,T,T)=3, (T,F,F)=1, (T,F,T)=2,
    (F,T,F)=1, (F,T,T)=2, (F,F,F)=0. -/
theorem profile : generated.map malaCount = [2, 3, 1, 2, 1, 2, 0] := by decide

/-- R-tier name attachment (documentation only — counts do not depend on it).
    sakala (3) · pralayākala (A+K) · vijñānākala (A) · mantra stations (pure
    adhvan, positional split — P-TK1b exception, flagged R) · śiva (0). -/
def traditionalName : Pramatr → String
  | ⟨true, true, true⟩   => "sakala"
  | ⟨true, false, true⟩  => "pralayakala"
  | ⟨true, false, false⟩ => "vijnanakala"
  | ⟨false, true, true⟩  => "mantra (R: positional)"
  | ⟨false, true, false⟩ => "mantresvara (R: positional)"
  | ⟨false, false, false⟩=> "siva"
  | ⟨true, true, false⟩  => "sakala-pure-karma-free (R: transitional)"
  | ⟨false, false, true⟩ => "ILL-FORMED (excluded by R1)"

end FormalTrika
