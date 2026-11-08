/-
  Formal Trika — P-VBT: VBT opening-question roster (R-tier).

  Ground (R, inherited): translation-work `vbt/` ARGMAP vbt-p01 inference
  roster + L2-vbt-p01 v.2–v.4 spans + C1-vbt-p01 EXPLANATION. See
  PREREGISTRATION-VBT-RUNG.md. Checks ONE finite fact: the eight
  candidate-form terms of the opening question.

  What this file IS: finite roster arithmetic (`decide` inside scope).
  What it is NOT: any doctrine about Bhairava's form (the question's own
  answers dissolve their objects — C1 FUNCTION), or any dhāraṇā claim
  (C1 BOUNDARY: "still no technique" — P-VBT2 parked, see prereg).
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
   VbtForm.cakrarudha]

/-- P-VBT1: eight terms, distinct. -/
theorem forms_eight : vbtForms.length = 8 ∧ vbtForms.Nodup := by decide

end FormalTrika
