/-
  Formal Trika — TK-C2: the KNOWN FAILURE (mutation control).

  Identical to Pramatr.lean with general rule R1 DELETED (karma floats free).
  The `seven` theorem MUST FAIL to check: with R1 gone, (F,F,T) survives and
  the count is 8, not 7. If this file ever checks, the instrument is blind —
  stop, fix, re-register. (Mirrors formal-abhidhamma control/Broken.lean.)
-/
import Mala
namespace FormalTrika
open Mala

structure Pramatr where
  anava  : Bool
  mayiya : Bool
  karma  : Bool
  deriving DecidableEq, Repr

def combos : List Pramatr :=
  [true, false].flatMap fun a => [true, false].flatMap fun m =>
    [false, true].map fun k => ⟨a, m, k⟩

/-- R1 DELETED ON PURPOSE: every combination well-formed. -/
def wellformed (_ : Pramatr) : Bool := true

def generated : List Pramatr := combos.filter wellformed

/-- MUST FAIL: with R1 deleted the count is 8, not the traditional 7. -/
theorem seven : generated.length = 7 := by decide
