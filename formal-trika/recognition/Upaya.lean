/-
  Formal Trika — F2: the three means as distinct transition relations (F-UPAYA).

  From the day-7 decode: mantra-repetition (#23) and insight-cascade
  (#30–31) share thought-factors but are different MEANS. T-tier ground:
  tsa-a08 v17 (the five pure-course followers: śāmbhava/śākta/…/mantra)
  and VBT dhāraṇās (the means catalog; experience-language criteria live
  in UPAYA-CRITERIA.md, not here).

  What this file IS: three transition relations over a minimal means-state
  (readiness + purified-vikalpa flag + application count), with their
  distinctness checked: śāmbhava flips in one step wherever ready;
  śākta needs the purified-vikalpa flag; āṇava needs repeated application
  (n ≥ 2). Ordering recorded whichever way it falls.
  What it is NOT: a proof that any lived clause used any means. The
  empirical bite is T-C2 (rater agreement on criteria), not this file.
-/
namespace FormalRecognition

/-- The minimal means-state. -/
structure MeansState where
  ready : Bool  -- the practitioner is ripe for the flip
  pure  : Bool  -- vikalpa purified (śākta precondition)
  deriving DecidableEq, Repr

def allMeansStates : List MeansState :=
  [true, false].flatMap fun r => [true, false].map fun p => ⟨r, p⟩

/-- Śāmbhava: immediate — flips wherever ready, no flag, no repetition. -/
def sambhavaReach (s : MeansState) : Bool := s.ready

/-- Śākta: needs readiness AND the purified-vikalpa flag. -/
def saktaReach (s : MeansState) : Bool := s.ready && s.pure

/-- Āṇava: needs readiness AND repeated application (n ≥ 2). -/
def anavaReach (s : MeansState) (n : Nat) : Bool := s.ready && 2 ≤ n

/-- Śāmbhava reaches from every ready state. -/
theorem sambhava_immediate :
    (allMeansStates.filter fun s => s.ready && sambhavaReach s).length = 2 := by
  decide

/-- Śākta is strictly narrower: a ready-but-impure state it cannot reach. -/
theorem sakta_needs_purity :
    (allMeansStates.filter fun s =>
      s.ready && !s.pure && sambhavaReach s && !saktaReach s).length > 0 := by
  decide

/-- Āṇava is strictly slower: one application never suffices, even ready. -/
theorem anava_needs_repetition :
    (allMeansStates.filter fun s =>
      s.ready && sambhavaReach s && !anavaReach s 1).length = 2 := by
  decide

/-- Two applications suffice wherever readiness holds. -/
theorem anava_two_suffice :
    (allMeansStates.filter fun s =>
      s.ready && anavaReach s 2).length = 2 := by
  decide

/-- Ordering (recorded as found): whatever āṇava reaches in 2, śāmbhava reaches. -/
theorem anava_within_sambhava :
    (allMeansStates.filter fun s =>
      anavaReach s 2 && !sambhavaReach s).length = 0 := by
  decide

/-- And śākta likewise (purity implies nothing beyond readiness for the immediate). -/
theorem sakta_within_sambhava :
    (allMeansStates.filter fun s =>
      saktaReach s && !sambhavaReach s).length = 0 := by
  decide

end FormalRecognition
