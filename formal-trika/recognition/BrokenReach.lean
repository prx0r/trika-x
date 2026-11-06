/-
  RECOGNITION — BrokenReach: KNOWN FAILURE (mutation control).

  Identical to Tractatus.lean's fork except a DIRECT edge 0→5 is added
  (recognition without the chain, without the reflexive edge). The
  needs-reflexive theorem MUST FAIL: a recognition that bypasses
  difference, boundedness, and self-model is not recognition but fiat.
-/
namespace FormalRecognition

set_option maxRecDepth 100000
set_option maxHeartbeats 2000000

/-- MUTATED: direct edge manifestation→recognition added. -/
def edgeNoRefl : Fin 6 → Fin 6 → Bool
  | 0, 1 => true  | 1, 2 => true  | 2, 3 => true
  | 3, 4 => true  | 0, 5 => true
  | _, _ => false

def reachNR : Nat → Fin 6 → Fin 6 → Bool
  | 0, a, b => (a == b)
  | n+1, a, b =>
    (a == b) || edgeNoRefl a b ||
    ([0, 1, 2, 3, 4, 5] : List (Fin 6)).any fun m =>
      edgeNoRefl a m && reachNR n m b

/-- MUST FAIL: recognition is now "reachable" by fiat. -/
theorem recognition_needs_reflexive_edge : reachNR 5 0 5 = false := by decide
