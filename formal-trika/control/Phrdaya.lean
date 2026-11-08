/-
  Formal Trika — P-PHR: phrdaya count-facts (R-tier).

  Ground (R, inherited): translation-work `phrdaya/` L2 + C1 key terms +
  ARGMAP token premises (sūtras 1–20, 5 passages). See
  PREREGISTRATION-PHR-RUNG.md (P-PHR1–3) and
  PREREGISTRATION-PHR-CLOSE-RUNG.md (P-PHR4–5: phr-p05 closing sequence).
  Checks FIVE finite facts: seven pentads, five acts, triple epithet,
  four-closing sequence, once-named means.

  What this file IS: finite roster arithmetic (`decide` inside scope).
  What it is NOT: the 35 names (unlisted), the 5 act-names (unmodeled —
  absent from held layers, stated limit), v.20's identity claim
  (recognition doctrine beyond verse grammar — not modeled), or anything
  beyond held L2 headings and ledger order. Covers: pentads + acts +
  epithet + closing sequence (all of both rungs).
-/
namespace FormalTrika

/-- Seven pentads (saptapañcaka, C1 phr-p02 key terms; ×5 definitional). -/
def pentads : List Nat := [5, 5, 5, 5, 5, 5, 5]

/-- P-PHR1: seven groups summing to thirty-five. -/
theorem pentads_thirtyfive : pentads.length = 7 ∧ pentads.sum = 35 := by decide

/-- Five acts (pañcakṛtya, L2-phr-p03; names unmodeled, count only). -/
inductive Act5 where
  | a1
  | a2
  | a3
  | a4
  | a5
  deriving DecidableEq, Repr

/-- Act roster (count shape only). -/
def acts5 : List Act5 := [Act5.a1, Act5.a2, Act5.a3, Act5.a4, Act5.a5]

/-- P-PHR2: exactly five, distinct. -/
theorem five_acts : acts5.length = 5 ∧ acts5.Nodup := by decide

/-- The v1 triple epithet (argmap phr-p01 + L2 + C1). -/
inductive Epithet where
  | citih
  | svatantra
  | visvasiddhihetuh
  deriving DecidableEq, Repr

/-- Epithet roster. -/
def epithets : List Epithet :=
  [Epithet.citih, Epithet.svatantra, Epithet.visvasiddhihetuh]

/-- P-PHR3: three terms, distinct. -/
theorem epithet_three : epithets.length = 3 ∧ epithets.Nodup := by decide

/-- The closing sequence: sūtras 17–20 in order (ledger phr-p05, L2). -/
def closes : List Nat := [17, 18, 19, 20]

/-- P-PHR4: exactly the four closing sūtras, in order. -/
theorem closes_four : closes.length = 4 ∧ closes = [17, 18, 19, 20] := by decide

/-- Sūtra numbers naming a means-term (upāyāḥ in v.18 only). -/
def meansAt : List Nat := [18]

/-- P-PHR5: named exactly once. -/
theorem means_once : meansAt.length = 1 ∧ meansAt.Nodup := by decide

end FormalTrika
