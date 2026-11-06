/-
  Formal Trika — S-SPAND: spanda pulse-facts (R-tier).

  Ground (R, inherited): translation-work `spanda/` span-p01 L2 READ + C1
  (full pipeline, R2-verified). See PREREGISTRATION-SPAND-RUNG.md.
  Sanskrit quoted from held L2 only. Checks THREE finite facts the
  pulse doctrine leans on: two phases, three-state glide, three acts.

  What this file IS: finite roster arithmetic (`decide` inside scope).
  What it is NOT: a physics of vibration, a frequency claim, or anything
  about śakti-cakra beyond the verse's own grammar. Rosters are INPUT
  from held readings (stipulated model data), exactly the T-TET way.
  Covers: alternation + glide + triple act (all of the rung).
-/
namespace FormalTrika

/-- The two phases: opening and closing (SK 1.1, span-p01 v.1). -/
inductive Phase where
  | open
  | close
  deriving DecidableEq, Repr

/-- Phase roster (stipulated from v.1). -/
def phases : List Phase := [Phase.open, Phase.close]

/-- S-SPAND1: exactly two phases, and they differ. -/
theorem phases_two : phases.length = 2 ∧ (Phase.open ≠ Phase.close) := by decide

/-- The three states the perceiver glides through (span-p01 v.3). -/
inductive State where
  | waking
  | dreaming
  | deep
  deriving DecidableEq, Repr

/-- State roster (stipulated from v.3 jāgradādi). -/
def states : List State := [State.waking, State.dreaming, State.deep]

/-- Persistence as read in-span (model data: v.3 asserts it for all). -/
def persists : State → Bool
  | .waking => true
  | .dreaming => true
  | .deep => true

/-- S-SPAND2: the roster is three and persistence holds for each. -/
theorem glide_all : states.length = 3 ∧ (states.all persists = true) := by decide

/-- The triple act by the inner wheel (span-p01 v.6). -/
inductive Act where
  | forthgoing
  | standing
  | dissolving
  deriving DecidableEq, Repr

/-- Act roster (stipulated from v.6). -/
def acts : List Act := [Act.forthgoing, Act.standing, Act.dissolving]

/-- S-SPAND3: three acts, pairwise distinct. -/
theorem acts_three : acts.length = 3 ∧
    (Act.forthgoing ≠ Act.standing) ∧ (Act.standing ≠ Act.dissolving) ∧
    (Act.forthgoing ≠ Act.dissolving) := by decide

end FormalTrika
