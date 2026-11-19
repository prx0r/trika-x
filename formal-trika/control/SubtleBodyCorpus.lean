/-
  Formal Trika — the subtle body from the corpus (puryaṣṭaka), version 2.

  This file extends SubtleBody.lean with what a full pass over the Trika
  corpus actually attests. It is deliberately separate so the earlier model
  stays stable.

  CORPUS BASIS (all verbatim in translation-work/passages.jsonl)

  1. PRĀṆA FORMULA (A)
     ĪPVV chunkV3-M: "prāṇādipañcakam indriyavargau dau niścayātmikā ca
     tṛtīyā svīkṛtāntaḥkaraṇāntarā dhīr vyajyate" — five prāṇas + two
     indriya groups + the inner organ = 8.
     Also MV-vārttika mv-k02: "prāṇaḥ puryaṣṭakaṃ dehaṃ vyāpya viśvaṃ
     prakarṣati"; Gītārthasaṅgraha gita-a15 (on BG 15.8): the jīva goes
     "puryaṣṭakena saha"; ĪPVV V2-M: "prāṇapuryaṣṭakasāhitya".

  2. TANMĀTRA FORMULA (B)
     TĀ 24.19; Spanda span-p06: "tanmātrodayarūpeṇa mano'haṃbuddhivartinā
     puryaṣṭakena saṃruddhaḥ ... saṃsarati"; ĪPVV V3-M: "kecana
     puryaṣṭakam āhuḥ".

  3. GUṆA FORMULA (C) — Śivasūtravimarśinī ssv-u3 (Kṣemarāja):
     "manasi rajoguṇodaye ahaṃkāre tamoguṇodaye buddhau ca
     sattvaguṇodayarūpāyāṃ ... puryāṃ sūkṣmaśarīre tanmātrapañcakaṃ
     guṇatrayam iti ... aṣṭakaṃ ... tanmukhyaṃ puryaṣṭakaṃ".
     So: five tanmātras + the three guṇas (rajas→manas, tamas→ahaṃkāra,
     sattva→buddhi) = 8. Same count as B, different vocabulary.

  4. THREE-LEVEL BODY (TĀ 29.261-270 + ŚSV):
     "piṇḍaḥ paraḥ kalātmā sūkṣmaḥ puryaṣṭako bahiḥ sthūlaḥ" — a graded
     schema: the piṇḍa (para/kalā), the subtle puryaṣṭaka, and the outer
     gross body. ŚSV calls the puryaṣṭaka the sūkṣmaśarīra and the kāraṇa
     of the gross.

  5. FUNCTION (T): transmigration rides on the subtle body; without the
     puryaṣṭaka there is no heaven/hell (TĀ 24.21); liberation is the
     dissolution of body-ness = ahaṃtā (TĀ 15.235-236; Tantrasāra 13.24;
     ŚSV: "puryaṣṭakapramātṛtābhimānavigalana").

  WHAT IS PROVED: counts, distinctness of the three formulas' partitions,
  the three body levels and which one is carried, and the guṇa/inner-organ
  equal-cardinality correspondence. WHAT IS NOT PROVED: that any formula is
  the only true one, that guṇas ARE the inner instruments, or that the
  three-level schema is exhaustive.
-/
namespace FormalTrika

/-- Component kinds across the corpus formulas. -/
inductive Kind where
  | prana | jnana | karma | antahkarana          -- formula A
  | tanmatra | manas | buddhi | ahankara         -- formula B
  | sattva | rajas | tamas                       -- formula C (guṇas)
  deriving DecidableEq, Repr

open Kind

structure Decomposition where
  label : String
  groups : List (Nat × Kind)
  deriving DecidableEq, Repr

def total (d : Decomposition) : Nat := (d.groups.map Prod.fst).sum

def kindsOf (d : Decomposition) : List Kind := d.groups.map Prod.snd

/-- A: prāṇa-based (ĪPVV, MV-vārttika, Gītā). -/
def trikaA : Decomposition :=
  { label := "A prāṇa-based"
    groups := [(5, prana), (1, jnana), (1, karma), (1, antahkarana)] }

/-- B: tanmātra-based (TĀ 24.19, Spanda). -/
def trikaB : Decomposition :=
  { label := "B tanmātra-based"
    groups := [(5, tanmatra), (1, manas), (1, buddhi), (1, ahankara)] }

/-- C: tanmātra + three guṇas (Śivasūtravimarśinī). -/
def trikaC : Decomposition :=
  { label := "C tanmātra + guṇas"
    groups := [(5, tanmatra), (1, sattva), (1, rajas), (1, tamas)] }

/-! ### The three formulas all count eight, and are not the same partition -/

theorem A_count : total trikaA = 8 := by decide
theorem B_count : total trikaB = 8 := by decide
theorem C_count : total trikaC = 8 := by decide

theorem three_formulas_eight :
    total trikaA = 8 ∧ total trikaB = 8 ∧ total trikaC = 8 := by decide

/-- B and C agree in count ... -/
theorem B_C_same_count : total trikaB = total trikaC := by decide

/-- ... and differ in the three inner terms (manas/buddhi/ahaṃkāra vs guṇas). -/
theorem B_C_different_vocabulary : kindsOf trikaB ≠ kindsOf trikaC := by decide

/-- A shares no group kind with either tanmātra formula. -/
theorem A_disjoint_B :
    (kindsOf trikaA).filter (fun k => k ∈ kindsOf trikaB) = [] := by decide

theorem A_disjoint_C :
    (kindsOf trikaA).filter (fun k => k ∈ kindsOf trikaC) = [] := by decide

/-! ### The guṇa ↔ inner-organ correspondence (ŚSV): equal and distinct -/

def gunas : List Kind := [sattva, rajas, tamas]
def innerOrgan : List Kind := [manas, buddhi, ahankara]

theorem guna_inner_same_count : gunas.length = innerOrgan.length := by decide

theorem gunas_distinct : gunas.eraseDups.length = 3 := by decide

theorem inner_distinct : innerOrgan.eraseDups.length = 3 := by decide

/-- The correspondence is cardinal, not identity: no guṇa IS an inner organ
    in this model. Naming them equal would be an R-tier doctrinal step the
    corpus text makes in its own words, not something proved here. -/
theorem guna_inner_not_identical :
    (gunas.filter (fun k => k ∈ innerOrgan)) = [] := by decide

/-! ### Three body levels (TĀ 29 + ŚSV) and what transmigration carries -/

inductive Level where
  | pinda   -- paraḥ kalātmā (causal/compact)
  | subtle  -- sūkṣmaḥ puryaṣṭakaḥ
  | gross   -- bahiḥ sthūla
  deriving DecidableEq, Repr

open Level

def levels : List Level := [pinda, subtle, gross]

theorem three_levels : levels.length = 3 := by decide

theorem levels_distinct : levels.eraseDups.length = 3 := by decide

/-- Only the subtle body is carried (Gītā 15.8 via Gītārthasaṅgraha;
    ŚSV: the gross is dropped, the puryaṣṭaka migrates). -/
def carried (l : Level) : Bool :=
  match l with
  | subtle => true
  | pinda  => false
  | gross  => false

theorem migration_at_subtle : carried subtle = true := by decide
theorem gross_not_carried : carried gross = false := by decide
theorem pinda_not_carried : carried pinda = false := by decide
theorem exactly_one_carried : (levels.filter carried).length = 1 := by decide

/-! ### Prāṇa pervades the city (MV-vārttika) -/

structure City where
  units : Nat
  pranaWithin : Bool
  ahamta : Bool
  deriving DecidableEq, Repr

def puryastaka : City := { units := 8, pranaWithin := true, ahamta := true }

theorem city_units : puryastaka.units = 8 := rfl

theorem prana_pervades_city : puryastaka.pranaWithin = true := rfl

/-- Body-ness is ahaṃtā (TĀ 15.235-236): dropping it is liberation. -/
def dropAhamta (c : City) : City := { c with ahamta := false }

theorem liberation_drops_bodyness (c : City) :
    (dropAhamta c).ahamta = false := rfl

theorem liberation_keeps_units (c : City) :
    (dropAhamta c).units = c.units := rfl

end FormalTrika
