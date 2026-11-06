/-
  Formal Recognition — E-EGO: two accounts of ego-origin (CRUX-02).

  T-tier ground: tsa08-p04 argmap (v68 silver-in-shell: ego from
  mind-mirrored object-contact, Sāṅkhya account; v69 rejection: Sāṅkhya
  denies I-feeling AND makership; v70 Trika correction: pure I =
  non-rivalled wonder-formed deliberation, vimarśa). v71/v72 heaps named,
  NOT modeled (parked). Silver-in-shell read as ORIGIN-dependence; the
  structure reading is parked.

  What this file IS: internal-consistency checks of two axiom sets over a
  finite 16-state bit-model + a recorded structural difference.
  What it is NOT: a verdict on which account is true about minds (finite
  models ≠ metaphysical verdicts). R-tier throughout; T pins in EVIDENCE.
-/
namespace FormalRecognition

/-- Ego flags (R: CRUX-02 reconstruction). D = derivative cause present
    (guṇa-mixture / mirror-contact); F = I-feeling; M = makership;
    R = a rival I-origin present. -/
structure EgoState where
  deriv : Bool
  feel  : Bool
  make  : Bool
  rival : Bool
  deriving DecidableEq, Repr

/-- Non-rivalled (v70): no rival origin present. -/
def nonrivalled (s : EgoState) : Bool := !s.rival

/-- Sāṅkhya admission (v68+v69 R reading): derivative cause required;
    I-feeling and makership denied. -/
def sankhyaAdmits (s : EgoState) : Bool :=
  s.deriv && !s.feel && !s.make

/-- Trika admission (v70 R reading): self-grounding pure I — no
    derivative cause, with I-feeling and makership, non-rivalled. -/
def trikaAdmits (s : EgoState) : Bool :=
  !s.deriv && s.feel && s.make && nonrivalled s

/-- All 16 ego-flag combinations. -/
def allEgo : List EgoState :=
  [true, false].flatMap fun d => [true, false].flatMap fun f =>
    [true, false].flatMap fun m => [false, true].map fun r =>
      { deriv := d, feel := f, make := m, rival := r }

/-- E-EGO1: every Sāṅkhya-admitted ego-state carries a derivative cause. -/
theorem sankhya_requires_cause :
    (allEgo.filter sankhyaAdmits).all (fun s => s.deriv) = true := by decide

/-- E-EGO2: the pure-I state (no cause, feeling, makership, non-rivalled)
    is admitted — self-reflexive ego is consistent in the model. -/
theorem trika_self_grounding_exists :
    trikaAdmits { deriv := false, feel := true, make := true, rival := false } = true := by decide

/-- E-EGO3a: the pure-I state is Trika-admitted but NOT Sāṅkhya-admitted. -/
theorem accounts_differ_pureI :
    sankhyaAdmits { deriv := false, feel := true, make := true, rival := false } = false := by decide

/-- E-EGO3b: a derivative state is Sāṅkhya-admitted but NOT Trika-admitted.
    Together with E-EGO3a: neither admission contains the other. -/
theorem accounts_differ_derivative :
    trikaAdmits { deriv := true, feel := false, make := false, rival := false } = false := by decide

/-- E-EGO4: "non-rivalled" does formal work — every Trika-admitted state
    is rival-free (answers CRUX-02 unresolved (a) inside this model). -/
theorem nonrivalled_does_work :
    (allEgo.filter trikaAdmits).all (fun s => !s.rival) = true := by decide

/-- E-EGO5: I-feeling without makership is satisfiable — F and M are
    separable bits IN THE MODEL (not a textual claim about (c)). -/
theorem feeling_makership_independent :
    (allEgo.filter (fun s => s.feel && !s.make)).length != 0 := by decide

end FormalRecognition
