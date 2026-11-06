/-
  Formal Recognition — R-REC5 + R-REC6 + R-REC8: conjuncts, targets, unus-ambo.

  From recognitionandsiva.md (R-tier constructor-theoretic schema of T-tier
  doctrine): Recognition_X = Transformation ∧ Reidentification ∧ Veridicality
  ∧ Stabilization. Generic: Recog(a,b) := Present(a) ∧ Acquainted(b) ∧
  Identify(a,b) ∧ a=b; if a≠b, misidentification regardless of certainty.
  S1–S5 + full Pratyabhijñāᵢ; three targets PI / Part / Śiva.
  From DAIMON-CONTACT-AS-RECOGNITION.md (R): unus-ambo 1×1 vs 1=1.
-/
namespace FormalRecognition

set_option maxRecDepth 100000
set_option maxHeartbeats 2000000

/-- The four conjuncts. -/
structure Conjuncts where
  trans : Bool  -- transformation of positioning
  reid  : Bool  -- reidentification (this is that)
  ver   : Bool  -- veridicality (it is so)
  stab  : Bool  -- stabilization (does not collapse)
  deriving DecidableEq, Repr

def recognitionHolds (k : Conjuncts) : Bool :=
  k.trans && k.reid && k.ver && k.stab

def allConjuncts : List Conjuncts :=
  [true, false].flatMap fun a => [true, false].flatMap fun b =>
    [true, false].flatMap fun c => [true, false].map fun d =>
      ⟨a, b, c, d⟩

/-- R-REC5a: exactly ONE of 16 combinations is recognition. -/
theorem recognition_unique :
    (allConjuncts.filter recognitionHolds).length = 1 := by decide

/-- R-REC5b–e: dropping any ONE conjunct loses recognition. -/
theorem drop_transformation_loses :
    (allConjuncts.filter fun k =>
      (!k.trans && k.reid && k.ver && k.stab) && recognitionHolds k).length = 0 := by
  decide
theorem drop_reidentification_loses :
    (allConjuncts.filter fun k =>
      (k.trans && !k.reid && k.ver && k.stab) && recognitionHolds k).length = 0 := by
  decide
theorem drop_veridicality_loses :
    (allConjuncts.filter fun k =>
      (k.trans && k.reid && !k.ver && k.stab) && recognitionHolds k).length = 0 := by
  decide
theorem drop_stabilization_loses :
    (allConjuncts.filter fun k =>
      (k.trans && k.reid && k.ver && !k.stab) && recognitionHolds k).length = 0 := by
  decide

/-- Generic Recog(a,b) over two presented items (Fin 2 keeps it finite). -/
structure RecogInst where
  present    : Bool  -- a is present
  acquainted : Bool  -- prior acquaintance with b
  identify   : Bool  -- a identified as b
  a : Fin 2
  b : Fin 2
  deriving DecidableEq, Repr

def recogHolds (r : RecogInst) : Bool :=
  r.present && r.acquainted && r.identify && (r.a == r.b)

def allRecogInsts : List RecogInst :=
  [true, false].flatMap fun p => [true, false].flatMap fun q =>
    [true, false].flatMap fun i => ([0, 1] : List (Fin 2)).flatMap fun a =>
      ([0, 1] : List (Fin 2)).map fun b => ⟨p, q, i, a, b⟩

/-- R-REC5f: misidentification — a≠b never recognizes, however certain. -/
theorem misidentification_never_recognizes :
    (allRecogInsts.filter fun r => (r.a != r.b) && recogHolds r).length = 0 := by
  decide

/-- The five Śaiva axioms as flags; Full = Part-ground + all five.
    Part = shared ground with distinct tokens (ground : Bool equal,
    subjects : Fin 2 distinct — coherent, exhibited). -/
structure TargetState where
  pi_pi   : Bool  -- process-inexternal identity holds (D≡O)
  g1      : Bool  -- ground of subject 1
  g2      : Bool  -- ground of subject 2
  s1      : Fin 2 -- subject-token 1
  s2      : Fin 2 -- subject-token 2
  s1axiom : Bool
  s2axiom : Bool
  s3axiom : Bool
  s4axiom : Bool
  s5axiom : Bool
  deriving DecidableEq, Repr

def partHolds (t : TargetState) : Bool := (t.g1 == t.g2) && (t.s1 != t.s2)

def fullSiva (t : TargetState) : Bool :=
  partHolds t && t.s1axiom && t.s2axiom && t.s3axiom && t.s4axiom && t.s5axiom

def allTargets : List TargetState :=
  [true, false].flatMap fun p => [true, false].flatMap fun g1 =>
    [true, false].flatMap fun g2 =>
      ([0, 1] : List (Fin 2)).flatMap fun s1 =>
        ([0, 1] : List (Fin 2)).flatMap fun s2 =>
          [true, false].flatMap fun q1 => [true, false].flatMap fun q2 =>
            [true, false].flatMap fun q3 => [true, false].flatMap fun q4 =>
              [true, false].map fun q5 =>
                ⟨p, g1, g2, s1, s2, q1, q2, q3, q4, q5⟩

/-- R-REC6a: the participatory reading is coherent — shared ground with
    genuinely distinct tokens exists in the model. -/
theorem part_coherent_distinct_tokens :
    (allTargets.filter partHolds).length > 0 := by decide

/-- R-REC6b: one modeled state has PI true and unequal ground flags. A single
    witness does not establish full independence over all assignments. -/
theorem pi_independent_of_grounds :
    (allTargets.filter fun t => t.pi_pi && (t.g1 != t.g2)).length > 0 := by
  decide

/-- R-REC6c: Śiva requires S — Part without S₁ is NOT the full recognition. -/
theorem siva_requires_axioms :
    (allTargets.filter fun t => partHolds t && !t.s1axiom && fullSiva t).length = 0 := by
  decide

/-- Unus-ambo (R): a symmetric non-identity bond exists — 1×1 is not 1=1.
    Exhibit: mutual relatedness without numerical identity. -/
def bonded : Fin 2 → Fin 2 → Bool
  | _, _ => true  -- all mutually bonded (one relation, two relata)

theorem unus_ambu_not_identity :
    ((bonded 0 1 && bonded 1 0) && ((0 : Fin 2) != 1)) = true := by decide

end FormalRecognition
