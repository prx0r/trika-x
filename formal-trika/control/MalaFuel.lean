/-
  Formal Trika — P-PUSH1: mala powers as fuel (phr-p04, pushing row 2).

  T-tier ground: phrdaya p04 argmap (sūtras 13–16): climb to knowing's
  seat (śaktipāta + grace); IT BURNS KNOWABLES FOR FUEL (the three
  malas); grown strong, the world owned; return by recognition, not
  effort. EXTENDS Recognition.lean's removal clause (content effect)
  with the strength effect (burning empowers); no contradiction.

  What this file IS: burn dynamics over 3 mala flags + knowing/grace
  ignition, with termination, monotonic strength, ignition necessity.
  What it is NOT: a claim that burning "really" strengthens anyone, or
  that grace/means disputes are settled. R-tier; T pins in EVIDENCE.
  Finite model; `decide` inside scope only.
-/
namespace FormalTrika

/-- Burn state per mala + ignition. -/
structure FuelState where
  anavaBurnt : Bool
  mayiyaBurnt : Bool
  karmaBurnt : Bool
  knowing : Bool  -- knowing's seat reached (śaktipāta + grace side)
  deriving DecidableEq, Repr

def allFuel : List FuelState :=
  [true, false].flatMap fun a => [true, false].flatMap fun m =>
    [true, false].flatMap fun k => [true, false].map fun n =>
      { anavaBurnt := a, mayiyaBurnt := m, karmaBurnt := k, knowing := n }

/-- Strength: count of burnt malas (grown strong, world owned). -/
def strength (s : FuelState) : Nat :=
  (if s.anavaBurnt then 1 else 0) + (if s.mayiyaBurnt then 1 else 0)
  + (if s.karmaBurnt then 1 else 0)

/-- One burn step: an unburnt mala ignites iff knowing holds. -/
def burnStep (s : FuelState) : FuelState :=
  if !s.knowing then s
  else if !s.anavaBurnt then { s with anavaBurnt := true }
  else if !s.mayiyaBurnt then { s with mayiyaBurnt := true }
  else if !s.karmaBurnt then { s with karmaBurnt := true }
  else s

/-- P-PUSH1a: burning terminates — 3 steps from all-unburned reach all-burnt. -/
theorem fuel_terminates :
    strength (burnStep (burnStep (burnStep
      { anavaBurnt := false, mayiyaBurnt := false, karmaBurnt := false, knowing := true }))) = 3 := by decide

/-- P-PUSH1b: strength never decreases along a burn step. -/
theorem strength_monotone :
    (allFuel.filter fun s => strength (burnStep s) < strength s).length = 0 := by decide

/-- P-PUSH1c: no ignition without knowing (grace necessary to start). -/
theorem grace_ignites :
    (allFuel.filter fun s => !s.knowing && strength (burnStep s) > strength s).length = 0 := by decide

end FormalTrika
