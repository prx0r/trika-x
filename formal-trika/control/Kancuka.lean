/-
  Formal Trika — P-TK2: the 5 kañcukas (coverings).

  Each kañcuka pairs one infinite capacity of the Lord with its finite form
  in the limited experient. Tiers: the FIVE NAMES are T (tsa-a08 T1:
  kalā ×50, vidyā ×6, rāga ×3, kāla ×2, niyati ×1); the capacity-pairing
  gloss is R (reconstructive here until a reviewed argmap pins each pairing
  to a cited span). The proposed source references are not pinned in this file.
-/
namespace FormalTrika

/-- The five coverings. -/
inductive Kancuka where
  | kala    -- limited doership (kiñcitkartṛtva)
  | vidya   -- limited knowledge (kiñcijjñatva)
  | raga    -- desire for the unfinished (attachment)
  | kalaTime-- temporal sequence (past/present/future division)
  | niyati  -- restriction (place/form/destiny fixity)
  deriving DecidableEq, Repr

/-- The infinite capacities they contract (R-tier gloss). -/
inductive Capacity where
  | allDoership    -- sarvakartṛtva
  | allKnowledge   -- sarvajñatva
  | satisfaction   -- pūrṇatva / self-sufficiency
  | eternity       -- nityatva
  | pervasion      -- vyāpakatva
  deriving DecidableEq, Repr

open Kancuka Capacity

def kancukas : List Kancuka := [.kala, .vidya, .raga, .kalaTime, .niyati]

/-- Each covering restricts exactly one capacity. -/
def restricts : Kancuka → Capacity
  | .kala     => .allDoership
  | .vidya    => .allKnowledge
  | .raga     => .satisfaction
  | .kalaTime => .eternity
  | .niyati   => .pervasion

/-- The tradition's count: 5. -/
theorem count_5 : kancukas.length = 5 := by decide

/-- The pairing covers 5 distinct capacities (no two coverings limit the same). -/
theorem pairings_distinct : ((kancukas.map restricts).eraseDups).length = 5 := by decide

end FormalTrika
