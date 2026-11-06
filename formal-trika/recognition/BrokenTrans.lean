/-
  RECOGNITION — BrokenTrans: the KNOWN FAILURE (mutation control).

  Identical to Transitions.lean except T_rec ALSO flips a kept bit
  (limitation). The preservation theorem MUST FAIL: a "recognition" that
  rewrites embodiment is acquisition wearing recognition's clothes.
  If this file ever checks, the instrument is blind — stop, fix, re-register.
-/
namespace FormalRecognition

set_option maxRecDepth 100000
set_option maxHeartbeats 2000000

structure RecState where
  xdm  : Bool
  exh  : Bool
  grnd : Bool
  own  : Bool
  agy  : Bool
  pol  : Bool
  ext  : Bool
  body : Bool
  lim  : Bool
  fld  : Bool
  prv  : Bool
  wrld : Bool
  deriving DecidableEq, Repr

/-- MUTATED: flips lim along with the positioning bits. -/
def trec (m : RecState) : RecState :=
  { m with xdm := false, exh := false, grnd := false, own := false,
             agy := false, pol := false, ext := false, lim := !m.lim }

def kept (m : RecState) : Bool × Bool × Bool × Bool × Bool :=
  (m.body, m.lim, m.fld, m.prv, m.wrld)

def allRecStates : List RecState :=
  [true, false].flatMap fun x => [true, false].flatMap fun e =>
    [true, false].flatMap fun g => [true, false].flatMap fun o =>
      [true, false].flatMap fun a => [true, false].flatMap fun p =>
        [true, false].flatMap fun x2 => [true, false].flatMap fun b =>
          [true, false].flatMap fun l => [true, false].flatMap fun f =>
            [true, false].flatMap fun pv => [true, false].map fun w =>
              ⟨x, e, g, o, a, p, x2, b, l, f, pv, w⟩

/-- MUST FAIL: embodiment is rewritten, so preservation is false. -/
theorem trec_preserves_embodiment :
    (allRecStates.filter fun m => kept m == kept (trec m)).length = 4096 := by
  decide
