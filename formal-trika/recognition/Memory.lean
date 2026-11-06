/-
  Formal Recognition — R-REC7: memory gradation, sees vs enacts.

  From ESSAY-RECOGNITION-FELT-RE-COGNITION.md (R gloss on T Pāli/Ñāṇavīra
  material): five memories M₁ retention · M₂ continuity · M₃ attribution ·
  M₄ autonoetic · M₅ identity. Encoded rule: M₄ → M₁+M₂+M₃; M₄ ⇏ M₅.
  The converse is not assumed: the model admits M₁+M₂+M₃ without M₄.
  Gradation law: stream-enterer SEES deception (Layer 3); arahant has REMOVED
  asmimāna with structure intact (Layer 4). Formula: Knowₒ[p] ⟹̸ Enactₒ[p].
-/
namespace FormalRecognition

/-- The five memories. -/
structure Mem5 where
  m1 : Bool  -- retention
  m2 : Bool  -- continuity
  m3 : Bool  -- attribution
  m4 : Bool  -- autonoetic (first-personal recollection)
  m5 : Bool  -- identity (ownership as self)
  deriving DecidableEq, Repr

/-- Well-formed: M₄ requires its M₁–M₃ foundation (no foundationless
    autonoetic memory). M₅ floats free (the contested step). -/
def memWellformed (m : Mem5) : Bool :=
  !(m.m4 && !(m.m1 && m.m2 && m.m3))

def allMem5 : List Mem5 :=
  [true, false].flatMap fun a => [true, false].flatMap fun b =>
    [true, false].flatMap fun c => [true, false].flatMap fun d =>
      [true, false].map fun e => ⟨a, b, c, d, e⟩

def wellformedMems : List Mem5 := allMem5.filter memWellformed

/-- Foundation rule holds: no well-formed M₄ without M₁–M₃. -/
theorem m4_requires_foundation :
    (wellformedMems.filter fun m => m.m4 && !(m.m1 && m.m2 && m.m3)).length = 0 := by
  decide

/-- The converse of the encoded foundation rule does not follow. -/
theorem foundations_without_m4_exist :
    (wellformedMems.filter fun m => m.m1 && m.m2 && m.m3 && !m.m4).length > 0 := by
  decide

/-- R-REC7a: M₄ ⇏ M₅ — autonoetic memory without identity-ownership exists. -/
theorem m4_without_m5 :
    (wellformedMems.filter fun m => m.m4 && !m.m5).length > 0 := by
  decide

/-- Seeing vs enacting: Layer 3 (sees deception) and Layer 4 (enacts
    removal). Enacting requires seeing; seeing does not require enacting. -/
structure SeerDoer where
  sees   : Bool  -- Layer 3: deception seen through
  enacts : Bool  -- Layer 4: asmimāna removed, structure intact
  deriving DecidableEq, Repr

def seerWellformed (s : SeerDoer) : Bool := !(s.enacts && !s.sees)

def allSeerDoer : List SeerDoer :=
  [true, false].flatMap fun a => [true, false].map fun b => ⟨a, b⟩

def wellformedSeers : List SeerDoer := allSeerDoer.filter seerWellformed

/-- R-REC7b: Know ⟹̸ Enact — seeing without enacting exists (stream-enterer). -/
theorem sees_without_enacting :
    (wellformedSeers.filter fun s => s.sees && !s.enacts).length > 0 := by
  decide

/-- Enacting without seeing is ill-formed (no removal without seeing). -/
theorem no_enacting_without_seeing :
    (wellformedSeers.filter fun s => s.enacts && !s.sees).length = 0 := by
  decide

end FormalRecognition
