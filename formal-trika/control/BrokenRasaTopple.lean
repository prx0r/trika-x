/-
  Formal Trika — R-NAV: navarasa roster-facts (H-tier).

  Ground (H, stipulated): classical nine-rasa roster (INPUT, like T-TET's
  Platonic roster); pinned to held R2 aesthetics text (rasa vocabulary
  verified) + spandasandoha L2 (adbhuta/śānta). See
  PREREGISTRATION-NAV-RUNG.md. No layered rasa passages exist in
  translation-work — hence H. Checks THREE finite facts the rasa
  doctrine leans on: nine names, śānta on top, five-bliss order.

  What this file IS: finite roster arithmetic (`decide` inside scope).
  What it is NOT: a proof of supremacy, any valence mathematics (QRI /
  Tymoczko are held mathematics, cited elsewhere), or camatkāra modeled.
  Covers: nine + supremacy + gradient (all of the rung).
-/
namespace FormalTrika

/-- The nine rasas (stipulated classical roster, model data). -/
inductive Rasa where
  | sringara
  | hasya
  | karuna
  | raudra
  | vira
  | bhayanaka
  | bibhatsa
  | adbhuta
  | santa
  deriving DecidableEq, Repr

/-- Rasa roster. -/
def rasas : List Rasa :=
  [Rasa.sringara, Rasa.hasya, Rasa.karuna, Rasa.raudra, Rasa.vira,
   Rasa.bhayanaka, Rasa.bibhatsa, Rasa.adbhuta, Rasa.santa]

/-- R-NAV1: exactly nine, pairwise distinct (nodup). -/
theorem nine_only : rasas.length = 9 ∧ rasas.Nodup := by decide

/-- Rank: śānta sits above the other eight (stipulated doctrine, INPUT). -/
def rank : Rasa → Nat
  | .santa => 0
  | .sringara => 7
  | .vira => 6
  | .adbhuta => 5
  | .karuna => 4
  | .hasya => 3
  | .raudra => 2
  | .bhayanaka => 1
  | .bibhatsa => 0

/-- R-NAV2: śānta outranks every other roster member. -/
theorem santa_supreme : rasas.all (fun r => decide (rank r ≤ rank Rasa.santa)) = true ∧
    rasas.filter (fun r => decide (rank Rasa.santa ≤ rank r)) = [Rasa.santa] := by decide

/-- The five blisses, implicit → explicit (stipulated order, INPUT). -/
inductive Bliss where
  | innate
  | stillness
  | supreme
  | great
  | consciousness
  deriving DecidableEq, Repr

/-- Bliss gradient. -/
def blisses : List Bliss :=
  [Bliss.innate, Bliss.stillness, Bliss.supreme, Bliss.great, Bliss.consciousness]

/-- Bliss rank (strict ascent). -/
def blissRank : Bliss → Nat
  | .innate => 0
  | .stillness => 1
  | .supreme => 2
  | .great => 3
  | .consciousness => 4

/-- R-NAV3: the gradient is exactly this list, in strict rank ascent. -/
theorem bliss_gradient : blisses =
    [Bliss.innate, Bliss.stillness, Bliss.supreme, Bliss.great, Bliss.consciousness] ∧
    blissRank Bliss.innate < blissRank Bliss.stillness ∧
    blissRank Bliss.stillness < blissRank Bliss.supreme ∧
    blissRank Bliss.supreme < blissRank Bliss.great ∧
    blissRank Bliss.great < blissRank Bliss.consciousness := by decide

end FormalTrika
