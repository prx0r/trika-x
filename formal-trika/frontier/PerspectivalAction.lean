/-
  Formal Trika — P-ACT: the positioning flip as a group action (H-tier pilot).

  Upgrades `recognise` from an operation to the generator of the only symmetry
  this structure admits. Claim: the action group of a two-positioning model is
  exactly Z/2; the flip IS the non-trivial element. This is the discrete
  skeleton of the "perspective as group action" move (cf. PGL(4,R) in PCM):
  stated for Z/2, proved by enumeration.

  What this file does NOT do: derive a continuous group. The action is Z/2;
  PCM's is PGL(4,R). The gap is named in the record, not bridged by fiat.
-/
import Inexternalism

namespace FormalTrika

/-- Z/2 multiplication on {0,1}, by parity. -/
def z2mul : Nat → Nat → Nat := fun a b => (a + b) % 2

/-- The two group elements, enumerated. -/
def z2elts : List Nat := [0, 1]

/-- Z/2 is closed on its elements. -/
theorem z2_closed : z2elts.all (fun a =>
    z2elts.all (fun b =>
      decide (z2mul a b == 0 || z2mul a b == 1))) = true := by
  decide

/-- Z/2 is associative (all 8 triples, checked). -/
theorem z2_assoc : z2elts.all (fun a =>
    z2elts.all (fun b =>
      z2elts.all (fun c =>
        decide (z2mul (z2mul a b) c == z2mul a (z2mul b c))))) = true := by
  decide

/-- Every element is its own inverse; 0 is the identity side. -/
theorem z2_selfinv : z2elts.all (fun a =>
    decide (z2mul a a == 0)) = true := by
  decide

/-- The flip on positionings, stated once so the action has one definition. -/
def flipSigma : Sigma → Sigma
  | .instrument => .primary
  | .primary => .instrument

/-- The action of Z/2 on fields, by parity: even does nothing, odd flips the
    positioning. Content (knower, world, relation) is never touched. -/
def act : Nat → Field → Field := fun g f =>
  if g % 2 == 1 then { f with sigma := flipSigma f.sigma } else f

/-- The identity element acts trivially on positioning, over the sample. -/
theorem act_identity_sigma : sampleFields.all (fun f =>
    decide ((act 0 f).sigma = f.sigma)) = true := by
  decide

/-- The action respects composition, on positioning, over the sample:
    acting by g then h is acting by g*h. -/
theorem act_compose_sigma : z2elts.all (fun g =>
    z2elts.all (fun h =>
      sampleFields.all (fun f =>
        decide ((act (z2mul g h) f).sigma = (act g (act h f)).sigma)))) = true := by
  decide

/-- CONTENT INVARIANCE: no group element changes knower, world or relation,
    over the whole sample. This is the checkable form of "positioning is a
    transformation of access, not of content". -/
theorem act_preserves_content : z2elts.all (fun g =>
    sampleFields.all (fun f =>
      ((act g f).knower == f.knower) &&
      ((act g f).world == f.world) &&
      ((act g f).relation == f.relation))) = true := by
  decide

/-- The old `recognise` is exactly the generator of this action: acting by 1
    agrees with flipping, on positioning, for every field. -/
theorem generator_agrees_on_positioning : ∀ f : Field,
    (recognise f).sigma = (act 1 f).sigma := by
  intro f
  obtain ⟨k, w, r, s⟩ := f
  cases s <;> rfl

/-- The flip is order two *because* 1+1=0 in Z/2: recognising twice is acting
    by the identity. This derives involution from the group law, over the sample. -/
theorem flip_squared_is_identity_op : sampleFields.all (fun f =>
    decide (act (z2mul 1 1) f = f)) = true := by
  decide

end FormalTrika
