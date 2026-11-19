/- Mutation: formula A is given six vital breaths instead of five, so the
   "eight" is no longer eight. The same by-decide theorem as in
   SubtleBody.lean must fail for exactly this reason. -/
namespace FormalTrika

inductive Kind where
  | prana | jnana | karma | antahkarana
  | tanmatra | manas | buddhi | ahankara
  | citta
  deriving DecidableEq, Repr

open Kind

structure Decomposition where
  label : String
  groups : List (Nat × Kind)
  deriving DecidableEq, Repr

def total (d : Decomposition) : Nat := (d.groups.map Prod.fst).sum

def trikaA : Decomposition :=
  { label := "trika/puryaṣṭaka (prāṇa-based)"
    groups := [(6, prana), (1, jnana), (1, karma), (1, antahkarana)] }  -- deliberate error

theorem trikaA_count : total trikaA = 8 := by decide

end FormalTrika
