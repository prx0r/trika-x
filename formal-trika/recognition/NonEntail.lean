/-
  Formal Recognition — R-REC3 + R-REC4: non-entailment countermodels.

  From pushing/research/truthanother.md (T: the chain shape, quoted verbatim):
    A ⇏ B ⇏ C ⇏ D ⇏ E ⇏ F
  "No source is permitted to inherit a later conclusion merely by
  establishing an earlier one."
  A=self-manifest · B=first-personality/ownership · C=ownership persists ·
  D=one enduring subject · E=genuine freedom · F=one universal consciousness.

  Method: each contention is a flag; a countermodel is an assignment where
  the earlier flags hold and the later fails. A non-empty witness set PROVES
  the arrow is missing inside this model. The model is R; the chain is T.
  Also: V₁–V₇ independence, U non-transitivity, no-global-section triad
  (home-checkpointcharlie, R).
-/
namespace FormalRecognition

set_option maxRecDepth 100000
set_option maxHeartbeats 2000000

/-- The six contentions as flags. No constraints: any combination is a
    candidate position; entailments must be EARNED, never built in. -/
structure Chain where
  a : Bool  -- self-manifest
  b : Bool  -- first-personality / ownership
  c : Bool  -- ownership persists across time
  d : Bool  -- one enduring subject
  e : Bool  -- genuine freedom (svātantrya, not flexibility)
  f : Bool  -- one universal consciousness
  deriving DecidableEq, Repr

def allChains : List Chain :=
  [true, false].flatMap fun a => [true, false].flatMap fun b =>
    [true, false].flatMap fun c => [true, false].flatMap fun d =>
      [true, false].flatMap fun e => [true, false].map fun f =>
        ⟨a, b, c, d, e, f⟩

/-- R-REC3: the six one-step witnesses + the full A..E-without-F. -/
theorem aby_not_b : (allChains.filter fun m => m.a && !m.b).length > 0 := by
  decide
theorem b_not_c : (allChains.filter fun m => m.b && !m.c).length > 0 := by
  decide
theorem c_not_d : (allChains.filter fun m => m.c && !m.d).length > 0 := by
  decide
theorem d_not_e : (allChains.filter fun m => m.d && !m.e).length > 0 := by
  decide
theorem e_not_f : (allChains.filter fun m => m.e && !m.f).length > 0 := by
  decide
theorem abcde_without_f :
    (allChains.filter fun m =>
      m.a && m.b && m.c && m.d && m.e && !m.f).length > 0 := by
  decide

/-- The seven vimarśas as independent flags (V₁ manifestness … V₇
    unrestricted freedom). Independence: all 128 combos occur — unity
    of the seven is NOT given. -/
structure Vim7 where
  v1 : Bool
  v2 : Bool
  v3 : Bool
  v4 : Bool
  v5 : Bool
  v6 : Bool
  v7 : Bool
  deriving DecidableEq, Repr

def allVim7 : List Vim7 :=
  [true, false].flatMap fun a => [true, false].flatMap fun b =>
    [true, false].flatMap fun c => [true, false].flatMap fun d =>
      [true, false].flatMap fun e => [true, false].flatMap fun f =>
        [true, false].map fun g => ⟨a, b, c, d, e, f, g⟩

/-- R-REC4a: V₁–V₇ dissociable — all 128 combinations well-formed. -/
theorem vim7_independent : allVim7.length = 128 := by decide

/-- Co-presence on three points: U(x,y) = x,y co-present.
    Witness: U(0,1), U(1,2) hold; U(0,2) fails. Non-transitive. -/
def coPresent : Fin 3 → Fin 3 → Bool
  | 0, 0 => true  | 1, 1 => true  | 2, 2 => true
  | 0, 1 => true  | 1, 0 => true
  | 1, 2 => true  | 2, 1 => true
  | _, _ => false

/-- R-REC4b: co-presence is NOT transitive. -/
theorem copresence_nontransitive :
    (coPresent 0 1 && coPresent 1 2 && !coPresent 0 2) = true := by decide

/-- R-REC4c (no global section): x=y, y=z, x≠z are pairwise satisfiable
    but jointly unsatisfiable — local coherence ⇏ global section. -/
theorem no_global_section :
    ¬∃ (x y z : Bool), x = y ∧ y = z ∧ x ≠ z := by decide

theorem pairwise_satisfiable_xy :
    (∃ (x y : Bool), x = y) := by decide

end FormalRecognition
