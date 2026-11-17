/- MUTANT C1: production appears.

  Formal Trika — A-IX: aperture inexternalism, the formalisable core.

  Tier H throughout: owner framework, not text, not scripture. Ground:
  research-library recognition/recognition-framework/aperture_inexternalism_position.md
  and RECOGNITION-FORMAL-FRAMEWORK.md §2 (the sigma-flip).

  WHAT THIS FILE IS: the structural core of the identity theory —
  (i) a finite field ⟨knower, world, relation, positioning⟩,
  (ii) recognition as a change of positioning only,
  (iii) proofs that content is preserved, positioning changes, and the
       operation is an involution of order two.

  WHAT THIS FILE IS NOT: a proof that a phenomenal field IS an aperture
  process. The identity D_i ≡_inext O_i* is a metaphysical identity across
  two modes of access. Lean can encode it as a definition and can prove its
  consequences; it cannot prove the identity. That limitation is load-bearing
  and is why this file carries no theorem named "identity".

  Tiers: positioning names and the flip are H (owner framework). The
  content/positioning separation is R (a reconstruction of IPVV V1E/V1D,
  not an entailment).
-/
namespace FormalTrika

/- LAYER C — exclusion constraints. What the theory forbids, as machine
   statements. Each is a stipulated invariant of our model, with a named
   twin that breaks exactly it. -/

/-- The two positionings of the self inside a finite field (IPVV V1E):
    the self as an instrument among things, or as the primary thing seen. -/
inductive Sigma where
  | instrument
  | primary
  deriving DecidableEq, Repr

/-- The positioning inventory: exactly two. -/
def sigmaValues : List Sigma := [.instrument, .primary]

theorem sigma_two : sigmaValues.length = 2 := by decide

theorem sigma_distinct : sigmaValues.Nodup := by decide

/-- A finite field: a knower, a world, their relation, and the positioning.
    One concrete process; the tuple is its content. -/
structure Field where
  knower : String
  world : String
  relation : String
  sigma : Sigma
  deriving DecidableEq, Repr

/-- Recognition: flip the positioning, leave the content untouched. -/
def recognise (f : Field) : Field :=
  { f with sigma := (match f.sigma with
                     | .instrument => .primary
                     | .primary => .instrument) }

/-- A-IX1: recognition changes no part of the content. -/
theorem recognise_preserves_content (f : Field) :
    (recognise f).knower = f.knower
    ∧ (recognise f).world = f.world
    ∧ (recognise f).relation = f.relation := by
  simp [recognise]

/-- A-IX2: recognition does change the positioning (it is not the identity). -/
theorem recognise_changes_positioning (f : Field) :
    (recognise f).sigma ≠ f.sigma := by
  obtain ⟨k, w, r, s⟩ := f
  cases s <;> simp [recognise]

/-- A-IX3: recognition is its own inverse — recognising twice returns the field. -/
theorem recognise_involution (f : Field) : recognise (recognise f) = f := by
  obtain ⟨k, w, r, s⟩ := f
  cases s <;> rfl

/-- A finite model: two knowers, two worlds, both positionings each. -/
def sampleFields : List Field :=
  [ ⟨"s1", "w1", "g1", .instrument⟩
  , ⟨"s1", "w1", "g1", .primary⟩
  , ⟨"s2", "w2", "g2", .instrument⟩
  , ⟨"s2", "w2", "g2", .primary⟩ ]

/-- A-IX4: over the sample, every recognisable field is closed under the flip
    (recognition never leaves the finite model). -/
theorem sample_closed :
    sampleFields.all (fun f => ¬ (sampleFields.all (fun g => g ≠ recognise f))) = true := by
  decide

/-- A-IX5: over the sample, no field is fixed by recognition. -/
theorem sample_no_fixed_point :
    sampleFields.all (fun f => recognise f ≠ f) = true := by
  decide

/-- Re-describe the same process in the other mode of access (extrinsic
    aperture <-> intrinsic field). The identity theory's claim is precisely
    that only the mode changes, so this operation is content-neutral. -/
def reDescribe (f : Field) : Field := f

/-- A-IX6 (decidable form, twin target): switching mode of access preserves
    knower, world, relation and positioning exactly. -/
theorem mode_switch_preserves_content :
    sampleFields.all (fun f =>
      ((reDescribe f).knower == f.knower) &&
      ((reDescribe f).world == f.world) &&
      ((reDescribe f).relation == f.relation) &&
      ((reDescribe f).sigma == f.sigma)) = true := by
  decide

/-- Exclusion C1: no transition in this model produces a state.
    Production is not among the operations; a function that is constantly
    false says so in a checkable way. -/
def producesSomething : Field → Bool := fun _ => true

/-- C1: over the sample, nothing is produced. -/
theorem sample_no_production :
    sampleFields.all (fun f => !producesSomething f) = true := by
  decide

/-- The extrinsic description of the same process (aperture mode of access).
    If the identity theory holds, re-describing preserves content. -/
def describeExtrinsic : Field → Field := fun f => f

/-- C2: over the sample, extrinsic redescription is the identity on every field. -/
theorem sample_one_process :
    sampleFields.all (fun f => decide (describeExtrinsic f = f)) = true := by
  decide

end FormalTrika
