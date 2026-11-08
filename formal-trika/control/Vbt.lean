/-
  Formal Trika — P-VBT: VBT opening-question roster (R-tier).

  Ground (R, inherited): translation-work `vbt/` ARGMAP vbt-p01 inference
  roster + L2-vbt-p01 v.2–v.4 spans + C1-vbt-p01 EXPLANATION; L2-vbt-p02
  v.14 span + C1-vbt-p02 SUMMARY. See PREREGISTRATION-VBT-RUNG.md
  (P-VBT1) and PREREGISTRATION-VBT2-RUNG.md (P-VBT2). Checks TWO finite
  facts: the eight candidate-form terms, and the three unpointability
  coordinates.

  What this file IS: finite roster arithmetic (`decide` inside scope).
  What it is NOT: any doctrine about Bhairava's form (the question's own
  answers dissolve their objects — C1 FUNCTION), any unpointability
  doctrine beyond the verse grammar, or any dhāraṇā claim (C1 BOUNDARY:
  "still no technique" — dhāraṇā counts parked, see prereg).
-/
namespace FormalTrika

/-- The eight candidate forms (ARGMAP vbt-p01 inference roster). -/
inductive VbtForm where
  | sabdarasi_kala
  | navatman
  | trisiras
  | saktitraya
  | nadabindu
  | candrardha
  | cakrarudha
  | anacka
  deriving DecidableEq, Repr

/-- Question roster. -/
def vbtForms : List VbtForm :=
  [VbtForm.sabdarasi_kala, VbtForm.navatman, VbtForm.trisiras,
   VbtForm.saktitraya, VbtForm.nadabindu, VbtForm.candrardha,
   VbtForm.cakrarudha, VbtForm.anacka]

/-- P-VBT1: eight terms, distinct. -/
theorem forms_eight : vbtForms.length = 8 ∧ vbtForms.Nodup := by decide

/-- The three unpointability coordinates (L2 vbt-p02 v.14; C1 SUMMARY). -/
inductive Unpointable where
  | dik
  | kala
  | kalana
  deriving DecidableEq, Repr

/-- Coordinate roster. -/
def unpointables : List Unpointable :=
  [Unpointable.dik, Unpointable.kala, Unpointable.kalana]

/-- P-VBT2: three coordinates, distinct. -/
theorem coords_three : unpointables.length = 3 ∧ unpointables.Nodup := by decide

end FormalTrika
