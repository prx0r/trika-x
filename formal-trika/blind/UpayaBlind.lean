/-
  BLIND re-derivation: the three means (Upaya), from Vocab alone.

  Read before writing: Vocab.lean (V.MeansState {ready, pure} ONLY),
  UPAYA-CRITERIA.md top half (criteria, not the rater-1 table below it),
  PREREGISTRATION-DECODE-RUNG.md F-UPAYA, TRIKA-METHOD.md.
  NOT read: recognition/Upaya.lean or any Broken twin (per BLIND.md).
  Encoder: box agent, fresh session 2026-11-06 (built E-EGO/heaps, never
  touched Upaya). Single-family pilot (same model line as builders) —
  flagged, not hidden: this tests the vocab's sufficiency, not
  cross-family replication.

  Derivation (general constraints over V.MeansState, no per-state tables):
  - śāmbhava (no means, immediacy): reaches iff ready.
  - śākta (vikalpa purified): reaches iff ready AND pure.
  - āṇava (repeated embodied act): UNFORMULABLE — V.MeansState has no
    repetition counter or step index. Predicted VOCAB-GAP (see note).
-/
namespace BlindUpaya

structure MeansState where
  ready : Bool  -- ripe for the flip (V.MeansState.ready)
  pure  : Bool  -- vikalpa purified (V.MeansState.pure)
  deriving DecidableEq, Repr

def allMeans : List MeansState :=
  [true, false].flatMap fun r => [true, false].map fun p =>
    { ready := r, pure := p }

/-- śāmbhava reaches from readiness alone (no technique). -/
def sambhavaReaches (s : MeansState) : Bool := s.ready

/-- śākta reaches from readiness with purified vikalpa. -/
def saktaReaches (s : MeansState) : Bool := s.ready && s.pure

/-- Distinctness: a ready-but-impure state is śāmbhava-reached and NOT
    śākta-reached (purity is load-bearing). -/
theorem blind_sakta_needs_purity :
    sambhavaReaches { ready := true, pure := false } = true
    && saktaReaches { ready := true, pure := false } = false := by decide

/-- Ordering (recorded as found): śākta reach-set ⊆ śāmbhava reach-set. -/
theorem blind_sakta_within_sambhava :
    (allMeans.filter saktaReaches).all sambhavaReaches = true := by decide

/-- śāmbhava immediacy: every reached state is ready (no other gate). -/
theorem blind_sambhava_is_readiness :
    (allMeans.filter sambhavaReaches).all (fun s => s.ready) = true := by decide

end BlindUpaya
