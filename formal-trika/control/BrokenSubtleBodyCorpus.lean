/- Mutation: the guṇa formula is given four guṇas (a fourth added), so its
   count is no longer eight. The same by-decide theorem as in
   SubtleBodyCorpus.lean must fail for exactly this reason. -/
namespace FormalTrika

inductive Kind where
  | prana | jnana | karma | antahkarana
  | tanmatra | manas | buddhi | ahankara
  | sattva | rajas | tamas
  deriving DecidableEq, Repr

open Kind

structure Decomposition where
  label : String
  groups : List (Nat × Kind)
  deriving DecidableEq, Repr

def total (d : Decomposition) : Nat := (d.groups.map Prod.fst).sum

def trikaC : Decomposition :=
  { label := "C tanmātra + guṇas"
    groups := [(5, tanmatra), (1, sattva), (1, rajas), (1, tamas), (1, sattva)] }  -- deliberate duplicate

theorem C_count : total trikaC = 8 := by decide

end FormalTrika
