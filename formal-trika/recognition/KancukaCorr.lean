/-
  Formal Trika — F1: felt↔structural correspondence (F-CORR).

  From the day-7 lived decode: lobha-weather (pull) rides with thina
  (stall); the requirements doc (REQUIREMENTS-FROM-DECODE.md F1) proposes
  rāga-kañcuka presents as lobha, kalā-kañcuka as thina/stall.
  T-tier ground: tsa08-p03 argmap (kalā→partial agency; "rāga functions"
  in partial agency; "now knowing partially, clinging, I do").

  What this file IS: a partial map from decode-side felt markers to the
  five contraction coordinates, with unknowns FIRST-CLASS (`none`).
  KEY DATA, not rules: the firm rows below are stipulated mappings (R-tier),
  each pinned to lived-decode evidence; no theorem derives them. Their
  empirical bite is T-C1 (statistical, `tools/tc1_cooccurrence.py`).
  Firm rows and evidence pins (play/*.jsonl, days 1–7 decodes):
    pull→va   day-7 #6–8, #22, #35; day-2 #1–2, #6–7; day-4 #1; day-5 #13
    stall→ac  day-7 #18 (want+blocked); day-4 #0 (torpor)
    churn→ac  day-7 #2 (scrambling); day-4 #0 (hot-bothered) — R, thin
    doubt→kn  day-5 #9 (explicit); day-2 #26; day-7 #20 (have-it/feel-it)
  Explicit unknowns: push (dosa-side), urgency (kāla candidate),
  placedness (niyati candidate) — unestablished, recorded, never forced.
  What it is NOT: a proof that any clause IS any kañcuka.
  Scope: a theorem about this finite table, nothing more.
-/
namespace FormalRecognition

/-- The five contraction coordinates (Coords.lean order). -/
inductive CorrCoord where
  | kn | ac | va | ti | ca
  deriving DecidableEq, Repr

/-- Decode-side felt markers (experience language, from the decode table). -/
inductive Felt where
  | pull         -- lobha-side want ("craving for the state")
  | stall        -- thina-side blockage ("i feel blocked")
  | churn        -- uddhacca-side agitation ("scrambling")
  | doubtStammer -- vicikiccha-side (have-it vs feel-it)
  | push         -- dosa-side (unknown structural signature)
  | urgency      -- hurry-pressure (kāla candidate, unestablished)
  | placedness   -- here-agency (niyati candidate, unestablished)
  deriving DecidableEq, Repr

open CorrCoord Felt

/-- The correspondence: partial by design. `none` = unknown, not absent. -/
def corr : Felt → Option CorrCoord
  | .pull         => some .va   -- rāga presents as pull (day-7 §§1-2, 4)
  | .stall        => some .ac   -- kalā presents as stall (day-7 #18)
  | .churn        => some .ac   -- R: agitation rides agency-loss (thin — flagged)
  | .doubtStammer => some .kn   -- R: conflicted knowing (vidyā-side, day-7 #20)
  | .push         => none
  | .urgency      => none
  | .placedness   => none

def allFelt : List Felt :=
  [.pull, .stall, .churn, .doubtStammer, .push, .urgency, .placedness]

/-- Firm row 1: pull maps to the value coordinate (rāga). -/
theorem corr_pull_raga : corr .pull = some .va := by decide

/-- Firm row 2: stall maps to the action coordinate (kalā). -/
theorem corr_stall_kala : corr .stall = some .ac := by decide

/-- R-tier row: doubt-stammer maps to the epistemic coordinate (vidyā). -/
theorem corr_doubt_vidya : corr .doubtStammer = some .kn := by decide

/-- Unknowns are explicit: three markers map to nothing. -/
theorem unknowns_explicit :
    corr .push = none ∧ corr .urgency = none ∧ corr .placedness = none := by
  decide

/-- Coverage is PARTIAL: 3 of 5 coordinates hit (ti, ca unmapped).
    The full-coverage prediction (F-CORR) is therefore NOT established by
    this table — it lives or dies on T-C1 + future decodes. -/
theorem coverage_partial :
    ((allFelt.filterMap corr).eraseDups.length = 3) := by decide

end FormalRecognition
