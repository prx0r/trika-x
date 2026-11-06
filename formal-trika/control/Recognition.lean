/-
  Formal Trika — P-TK3: recognition as σ-flip (AM0, R-tier).

  From the owner's FORMALIZATION-OF-RECOGNITION (gochema, R-tier, NOT a root
  verse): the mental-state tuple m = (e,p,h,b,o,σ). Re-cognition T_rec changes
  NOTHING in content (e,p,h,b,o identical) and flips ONLY the self-grounding
  parameter σ: Sv(O) (object taken as independently real, observer exempted)
  → ¬Sv(O) (same object experienced as i-within-S).

  The three malas as formal failure modes (same source, R-tier):
  āṇava = σ stuck at Sv(O); māyīya = object o without dependence marker;
  kārma = attractor-lock re-instantiating Sv(O)-consistent patterns.
-/
namespace FormalTrika

/-- Minimal AM0 state: five content bits + the σ parameter.
    (Content fields are Bool here so the whole space is checkable by decide;
    this is a structural model of the flip, not a phenomenology.) -/
structure Am0State where
  e : Bool  -- event-type marker
  p : Bool  -- accessibility profile
  h : Bool  -- history marker
  b : Bool  -- buffer marker
  o : Bool  -- intentional object marker
  s : Bool  -- σ: true = Sv(O) (exempted), false = ¬Sv(O) (recognized)
  deriving DecidableEq, Repr

/-- T_rec: recognition. Content untouched, σ flipped to recognized. -/
def recognize (m : Am0State) : Am0State := { m with s := false }

/-- Content equality (σ excluded). -/
def contentEq (a b : Am0State) : Bool :=
  a.e == b.e && a.p == b.p && a.h == b.h && a.b == b.b && a.o == b.o

/-- The whole state space: 2^6 = 64. -/
def allStates : List Am0State :=
  [true, false].flatMap fun e => [true, false].flatMap fun p =>
    [true, false].flatMap fun h => [true, false].flatMap fun b =>
      [true, false].flatMap fun o => [true, false].map fun s =>
        ⟨e, p, h, b, o, s⟩

/-- P-TK3a: recognition preserves content on every state. -/
theorem recognition_preserves_content :
    (allStates.filter fun m => contentEq m (recognize m)).length = 64 := by decide

/-- P-TK3b: recognition always lands in ¬Sv(O). -/
theorem recognition_lands_recognized :
    (allStates.filter fun m => !(recognize m).s).length = 64 := by decide

/-- P-TK3c: recognition is NOT information gain — content before and after is
    identical for every state (the tuple content is unchanged; only the
    operator's relation to its dependence flips). -/
theorem recognition_adds_nothing :
    allStates.all (fun m => contentEq m (recognize m)) = true := by decide

end FormalTrika
