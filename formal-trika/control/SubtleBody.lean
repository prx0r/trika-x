/-
  Formal Trika — comparative anatomy of the subtle body (puryaṣṭaka).

  WHAT THIS FILE DOES
  It encodes, as typed data, the *two* eightfold formulas for the subtle body
  that Abhinavagupta himself distinguishes, plus the Vedāntic 17- and 19-part
  inventories, and machine-checks the arithmetic and the non-identity of the
  partitions. It does NOT prove any doctrine true, and it does not derive the
  lists from scripture: the lists are stipulated from the cited sources.

  THE TWO TRIKA FORMULAS (both are called puryaṣṭaka, "city of eight")
  A. PRĀṆA-BASED (ĪPVV, the formula Medhananda reports):
     five vital breaths + the two sense-organ groups (buddhīndriya and
     karmendriya) + the inner organ taken as one capacity = 8.
     Expanded into individual faculties: 5 + 5 + 5 + 3 = 18.
  B. TANMĀTRA-BASED (TĀ 24.19; Yogarāja on Paramārthasāra):
     five tanmātras + manas + buddhi + ahaṃkāra = 8.
  Abhinavagupta's own comment on the difference (ĪPVV, V3-M):
     "kecana puryaṣṭakam āhuḥ ... tata eva atra pakṣavaicitrye vastuno na
      vaicitryam" — some state it thus; the variety is in the formulation
      (pakṣa), not in the thing (vastu). That is an interpretive claim we
      quote and bind, never a theorem.

  VEDĀNTIC INVENTORIES (external sources; see EVIDENCE r_sources)
     17 = 5 prāṇas + 5 jñānendriyas + 5 karmendriyas + manas + buddhi
     19 = the same + ahaṃkāra + citta

  TIERS: the group/count structure is checked formally (model). The member
  lists are R (reconstructive/stipulated) except where a verse is quoted (T).
  Same-word-different-role for prāṇa is R: it records how the sources use the
  term, and the model does not adjudicate which use is "real".
-/
namespace FormalTrika

/-- Component kinds across the systems. One type so partitions can be
    compared without pretending the terms are the same. -/
inductive Kind where
  | prana | jnana | karma | antahkarana          -- Trika A
  | tanmatra | manas | buddhi | ahankara         -- Trika B
  | citta                                        -- Vedānta 19 only
  deriving DecidableEq, Repr

open Kind

/-- A decomposition counts groups: (how many units, which kind). -/
structure Decomposition where
  label : String
  groups : List (Nat × Kind)
  deriving DecidableEq, Repr

def total (d : Decomposition) : Nat := (d.groups.map Prod.fst).sum

def kindsOf (d : Decomposition) : List Kind := d.groups.map Prod.snd

/-- Trika formula A: 5 breaths + buddhīndriya + karmendriya + antaḥkaraṇa
    (the inner organ lumped as one capacity; Medhananda, Panentheism 2023). -/
def trikaA : Decomposition :=
  { label := "trika/puryaṣṭaka (prāṇa-based)"
    groups := [(5, prana), (1, jnana), (1, karma), (1, antahkarana)] }

/-- Trika formula B: 5 tanmātras + manas + buddhi + ahaṃkāra (TĀ 24.19). -/
def trikaB : Decomposition :=
  { label := "trika/puryaṣṭaka (tanmātra-based)"
    groups := [(5, tanmatra), (1, manas), (1, buddhi), (1, ahankara)] }

/-- Vedānta 17-part subtle body (Tattvabodha / Vedāntasāra). -/
def vedanta17 : Decomposition :=
  { label := "vedānta/sūkṣmaśarīra (17)"
    groups := [(5, prana), (5, jnana), (5, karma), (1, manas), (1, buddhi)] }

/-- Vedānta 19-part subtle body (adds ahaṃkāra and citta). -/
def vedanta19 : Decomposition :=
  { label := "vedānta/sūkṣmaśarīra (19)"
    groups := [(5, prana), (5, jnana), (5, karma),
               (1, manas), (1, buddhi), (1, ahankara), (1, citta)] }

/-- Formula A expanded as individual faculties: 5 + 5 + 5 + 3. -/
def trikaAExpanded : Decomposition :=
  { label := "trika/puryaṣṭaka expanded (18)"
    groups := [(5, prana), (5, jnana), (5, karma),
               (1, manas), (1, buddhi), (1, ahankara)] }

/-! ### Counts (the arithmetic of the identification) -/

theorem trikaA_count : total trikaA = 8 := by decide
theorem trikaB_count : total trikaB = 8 := by decide
theorem trikaA_expanded_count : total trikaAExpanded = 18 := by decide
theorem vedanta17_count : total vedanta17 = 17 := by decide
theorem vedanta19_count : total vedanta19 = 19 := by decide

/-- Eight equals eight: the two Trika formulas have the same cardinality. -/
theorem same_cardinality : total trikaA = total trikaB := by decide

/-- But they are not the same partition: the group-kind lists differ. -/
theorem not_same_partition : kindsOf trikaA ≠ kindsOf trikaB := by decide

/-- And the group kinds are disjoint: no kind appears in both formulas. -/
theorem partitions_disjoint :
    (kindsOf trikaA).filter (fun k => k ∈ kindsOf trikaB) = [] := by decide

/-- "Eight does not mean the same eight": same count, disjoint content. -/
theorem eight_is_not_one_eight :
    total trikaA = total trikaB ∧
    kindsOf trikaA ≠ kindsOf trikaB ∧
    (kindsOf trikaA).filter (fun k => k ∈ kindsOf trikaB) = [] := by decide

/-- Formula A, expanded, is not formula B: 18 ≠ 8. -/
theorem expanded_differs : total trikaAExpanded ≠ total trikaB := by decide

/-- Vedānta 19 exceeds the expanded Trika A by exactly one (citta). -/
theorem vedanta19_adds_citta : total vedanta19 = total trikaAExpanded + 1 := by decide

/-- Vedānta 17 and 19 differ exactly by ahaṃkāra + citta (2). -/
theorem vedanta_17_19_gap : total vedanta19 = total vedanta17 + 2 := by decide

/-- Trika A and Vedānta 19 share the three fivefold groups but differ by citta. -/
theorem trikaA_vs_vedanta19 :
    total vedanta19 = total trikaAExpanded + 1 := by decide

/-! ### "Prāṇa": the same word, different theoretical role (R-tier) -/

inductive PranaRole where
  | vitalBreath            -- a specific vital wind (apāna … vyāna)
  | physiologicalFunction  -- "physiological functions" as a class
  | cosmicForce            -- Vivekananda's wider use (prāṇa as universal force)
  deriving DecidableEq, Repr

structure PranaUse where
  role : PranaRole
  count : Nat
  deriving DecidableEq, Repr

/-- Trika (formula A): five vital breaths. -/
def trikaPrana : PranaUse := { role := .vitalBreath, count := 5 }

/-- Advaita inventory: prāṇas as physiological functions. -/
def vedantaPrana : PranaUse := { role := .physiologicalFunction, count := 5 }

/-- Vivekananda also uses prāṇa for cosmic force (Raja-Yoga). -/
def vivekanandaPrana : PranaUse := { role := .cosmicForce, count := 5 }

/-- The count is the same everywhere ... -/
theorem prana_count_same :
    trikaPrana.count = vedantaPrana.count ∧
    vedantaPrana.count = vivekanandaPrana.count := by decide

/-- ... but the role is not: the term's sense is system-relative. -/
theorem prana_role_differs :
    trikaPrana.role ≠ vedantaPrana.role ∧
    vedantaPrana.role ≠ vivekanandaPrana.role := by decide

/-- Defining prāṇa rigidly = (role, count). Two systems can share the count
    and not the definition; that is exactly the comparative point. -/
theorem prana_same_count_not_same_definition :
    trikaPrana.count = vedantaPrana.count ∧ trikaPrana ≠ vedantaPrana := by decide

end FormalTrika
