/-
  Formal Trika — E-EMB: MUTANT: sound rank lifted (ether holds nothing; must fail ether_sound_only ONLY).

  T-tier ground (THIN): tsa07-p01 argmap v9 (gross includes subtle
  substances). Gradient reading (ether 1 … earth 5) is STANDARD DOCTRINE
  flagged R — needs scholar confirmation; uniform alternative parked
  (see prereg). Order: ether finest … earth grossest (accumulation).

  What this file IS: 5×5 containment matrix + earth/ether witnesses +
  nesting, over finite Bools.
  What it is NOT: cosmology proof, size claim, or verdict on
  gradient-vs-uniform (scholar decides; remodel ready). R-tier; T pin
  thin. Finite model; `decide` inside scope only.
-/
namespace FormalTrika

/-- Gross elements, finest first (R order). -/
inductive Gross where
  | ether | wind | fire | water | earth
  deriving DecidableEq, Repr

/-- Subtle elements. -/
inductive Subtle where
  | sound | touch | form | taste | smell
  deriving DecidableEq, Repr

def allGross : List Gross := [.ether, .wind, .fire, .water, .earth]
def allSubtle : List Subtle :=
  [.sound, .touch, .form, .taste, .smell]

/-- Containment (R gradient): rank(gross) ≥ rank(subtle) in subtlety
    order ether<wind<fire<water<earth vs sound<touch<form<taste<smell.
    Ether holds sound alone; earth holds all five. -/
def rankG : Gross → Nat
  | .ether => 0 | .wind => 1 | .fire => 2 | .water => 3 | .earth => 4

def rankS : Subtle → Nat
  | .sound => 1 | .touch => 1 | .form => 2 | .taste => 3 | .smell => 4

def contains (g : Gross) (s : Subtle) : Bool :=
  decide (rankS s ≤ rankG g)

/-- E-EMB1: earth row holds all five tanmātras. -/
theorem earth_all5 :
    (allSubtle.filter fun s => contains .earth s).length = 5 := by decide

/-- E-EMB2: ether row holds sound alone. -/
theorem ether_sound_only :
    (allSubtle.filter fun s => contains .ether s) = [.sound] := by decide

/-- E-EMB3: nesting — each grosser row's set includes the next finer
    (pairs are (finer, grosser); finer's substances persist upward). -/
theorem nesting :
    (allGross.zip (allGross.drop 1)).all fun p =>
      (allSubtle.filter fun s => contains p.1 s).all fun s =>
        contains p.2 s := by decide

end FormalTrika
