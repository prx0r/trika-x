/-
  Formal Trika — P-TK2b: the puryaṣṭaka (city of eight), the subtle body.
  KIND: KEY TABLE (constituents) + MODEL (the body as ahaṃtā and its burning).
  Tiers:
   - The TERM puryaṣṭaka and its identification with deha, and dehatva as
     ahaṃtā, are T (attested): Tantrasāra 13.24 (tsa13-p02 / tsa-a13-v25) and
     Tantrāloka 15.234–236 (tal-a15-p24). The transmigration corollary
     (no puryaṣṭaka -> no heaven/hell) is T: Tantrāloka 24.20–21
     (tal-a24-p02, tal-a24-p03). The kañcuka contraction link is T:
     Tantrāloka 9.204–205 (tal-a09-p21).
   - The ENUMERATION of the eight as five tanmātras + manas + ahaṃkāra +
     buddhi is R (reconstructive): Tantrāloka 24.19's list is compressed and
     does not name all eight. This file models the classical set; it does not
     derive it from the verse.
   - `six_fewer_than_eight` is arithmetic over the stipulated counts only:
     it says nothing about how the kañcukas actually contract.
  What is NOT proved here: that the model is the tradition's only reading,
  that the enumeration is the verse's own, or any philological claim.
-/
namespace FormalTrika

/-- The eight constituents: five tanmātras and the three inner instruments. -/
inductive Constituent where
  | sound | touch | form | taste | smell
  | manas | ahankara | buddhi
  deriving DecidableEq, Repr

open Constituent

/-- The five subtle elements. -/
def tanmatras : List Constituent := [.sound, .touch, .form, .taste, .smell]

/-- The three inner instruments (manas, ahaṃkāra, buddhi). -/
def antahkarana : List Constituent := [.manas, .ahankara, .buddhi]

/-- The city of eight (R-tier enumeration). -/
def constituents : List Constituent := tanmatras ++ antahkarana

/-- The tradition's count: eight. -/
theorem constituents_eight : constituents.length = 8 := by decide

/-- The partition is non-redundant: five plus three, no overlap. -/
theorem partition_disjoint : constituents.eraseDups.length = 8 := by decide

theorem five_tanmatras : tanmatras.length = 5 := by decide

theorem three_inner : antahkarana.length = 3 := by decide

/-- The six coverings (TĀ 9.204 names them; cf. Kancuka.lean). -/
inductive Kancuka where
  | maya | kala | raga | vidya | kalaTime | niyati
  deriving DecidableEq, Repr

def kancukas : List Kancuka := [.maya, .kala, .raga, .vidya, .kalaTime, .niyati]

theorem kancukas_six : kancukas.length = 6 := by decide

/-- Six coverings, eight constituents: a count comparison, not a mechanism. -/
theorem six_fewer_than_eight : kancukas.length < constituents.length := by decide

/-- A body: its constituents plus the 'I'-sense that makes it a body. -/
structure Body where
  members : List Constituent
  ahamta : Bool
  deriving DecidableEq, Repr

/-- The city of eight as a body, with the I-sense present. -/
def cityOfEight : Body := { members := constituents, ahamta := true }

/-- Body-ness IS the I-sense (TĀ 15.235: ahantāyāṃ hi dehatvam). -/
def isBody (b : Body) : Bool := b.ahamta

/-- "Burning the body" removes the I-sense, not the constituents
    (Tantrasāra 13.24: ahambhāva-tyāgena dehatāṃ dahet). -/
def burn (b : Body) : Body := { b with ahamta := false }

theorem body_is_ahamta (b : Body) : isBody b = b.ahamta := rfl

theorem city_is_body : isBody cityOfEight = true := by decide

/-- Burning destroys body-ness. -/
theorem burn_removes_body (b : Body) : isBody (burn b) = false := by
  simp [burn, isBody]

/-- Burning is idempotent: once the I-sense is gone, burning again changes
    nothing. -/
theorem burn_idempotent (b : Body) : burn (burn b) = burn b := by
  cases b
  simp [burn]

/-- Transmigration rides on body-ness (TĀ 24.21: with the puryaṣṭaka gone,
    no heaven or hell). -/
def transmigrates (b : Body) : Bool := isBody b

theorem no_transmigration_without_body (b : Body) :
    transmigrates (burn b) = false := by
  simp [transmigrates, burn, isBody]

end FormalTrika
