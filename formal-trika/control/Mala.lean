/-
  Formal Trika — the 3 malas (impurities) and their classes.
  KIND: KEY DATA (datatype + tradition count; nothing derived).
  Tiers: the three NAMES are T (root/āgama vocabulary, cf. translation-work
  phrdaya mala argmap + tsa-a08 T1); the axis reading (presence/absence
  booleans composing experient classes) is R (reconstruction).
  What this is NOT: a derivation of the three — the count is tradition's.
-/
namespace FormalTrika

/-- The three malas: āṇava (atomicity/ignorance), māyīya (differentiation),
    kārma (karmic residue). -/
inductive Mala where
  | anava | mayiya | karma
  deriving DecidableEq, Repr

/-- All three. -/
def malas : List Mala := [.anava, .mayiya, .karma]

/-- The tradition's count: 3. -/
theorem count_3 : malas.length = 3 := by decide

end FormalTrika
