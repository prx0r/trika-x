/-
  Formal Recognition — R-REC1 + R-REC2: the σ-transition laws.

  From FORMALIZATION-OF-RECOGNITION.md (R-tier schema of T-tier doctrine):
  recognition changes Xᵢ,eᵢ,gᵢ,ωᵢ,αᵢ,Πᵢ (+externalization) and RETAINS
  Oᵢ,Lᵢ,Dᵢ,∂Dᵢ,Wᵢ. Bondage Bᵢ = Lᵢ ∧ identification ∧ externalization:
  recognition clears bondage WITHOUT destroying limitation.

  State: 7 flipped fields (exclusive positioning) + 5 kept fields (finite
  embodiment) = 12 bits, 4096 states, everything by decide.
  Scope: a theorem about this finite model, not about minds.
-/
namespace FormalRecognition

set_option maxRecDepth 100000
set_option maxHeartbeats 2000000

/-- The recognition state: 7 positioning bits + 5 embodiment bits. -/
structure RecState where
  xdm  : Bool  -- exclusive self-determination Xᵢ
  exh  : Bool  -- standpoint-as-exhaustive eᵢ
  grnd : Bool  -- ground attribution gᵢ
  own  : Bool  -- exclusive ownership ωᵢ
  agy  : Bool  -- independent authorship αᵢ
  pol  : Bool  -- exclusive metacontrol Πᵢ
  ext  : Bool  -- externalization of the world
  body : Bool  -- body-process Oᵢ
  lim  : Bool  -- finite limitation Lᵢ
  fld  : Bool  -- local phenomenal field Dᵢ
  prv  : Bool  -- field privacy ∂Dᵢ
  wrld : Bool  -- organism-relative world Wᵢ
  deriving DecidableEq, Repr

/-- T_rec: de-exclusivize the 7 positioning bits; embodiment untouched. -/
def trec (m : RecState) : RecState :=
  { m with xdm := false, exh := false, grnd := false, own := false,
             agy := false, pol := false, ext := false }

/-- Acquisition (learning): rewrites a content bit, moves no σ.
    The discriminator — what recognition is NOT. -/
def acquire (m : RecState) : RecState := { m with body := !m.body }

/-- Bondage: limitation + exhaustive-identification + externalization. -/
def bondage (m : RecState) : Bool := m.lim && m.exh && m.ext

/-- Embodiment profile (the 5 kept bits). -/
def kept (m : RecState) : Bool × Bool × Bool × Bool × Bool :=
  (m.body, m.lim, m.fld, m.prv, m.wrld)

/-- The whole space: 2^12 = 4096. -/
def allRecStates : List RecState :=
  [true, false].flatMap fun x => [true, false].flatMap fun e =>
    [true, false].flatMap fun g => [true, false].flatMap fun o =>
      [true, false].flatMap fun a => [true, false].flatMap fun p =>
        [true, false].flatMap fun x2 => [true, false].flatMap fun b =>
          [true, false].flatMap fun l => [true, false].flatMap fun f =>
            [true, false].flatMap fun pv => [true, false].map fun w =>
              ⟨x, e, g, o, a, p, x2, b, l, f, pv, w⟩

/-- R-REC1a: content preserved on every state (removal, nothing added). -/
theorem trec_preserves_embodiment :
    (allRecStates.filter fun m => kept m == kept (trec m)).length = 4096 := by
  decide

/-- R-REC1b: bondage cleared on every state. -/
theorem trec_clears_bondage :
    (allRecStates.filter fun m => !(bondage (trec m))).length = 4096 := by
  decide

/-- R-REC1c: limitation retained on every state (no destruction of δᵢ). -/
theorem trec_retains_limitation :
    (allRecStates.filter fun m => (trec m).lim == m.lim).length = 4096 := by
  decide

/-- R-REC1d: applying this function twice has the same result as once.
    This alone says nothing about backsliding under other transitions. -/
theorem trec_idempotent :
    (allRecStates.filter fun m => trec (trec m) == trec m).length = 4096 := by
  decide

/-- R-REC2a: a state with the selected flags exists. No transition relation
    is defined here, so this does not prove that a state stays stuck. -/
theorem anava_stuck_exists :
    (allRecStates.filter fun m => m.exh && bondage m).length > 0 := by
  decide

/-- R-REC2b (māyīya): acquisition rewrites content — provably NOT T_rec.
    There are states where acquire changes embodiment but trec does not. -/
theorem acquire_is_not_recognition :
    (allRecStates.filter fun m =>
      (kept m != kept (acquire m)) && (kept m == kept (trec m))).length = 4096 := by
  decide

/-- R-REC2c: states with the selected positioning flags exist. No transition
    or self-loop is proved by this Boolean existence check. -/
theorem karma_loop_exists :
    (allRecStates.filter fun m =>
      m.xdm && m.exh && m.own && m.agy).length > 0 := by
  decide

end FormalRecognition
