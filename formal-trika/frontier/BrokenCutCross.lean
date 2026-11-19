/- MUTANT: see changed definition.

  Formal Trika — CUT: recognition dynamics decouple across field-instances.

  H-tier pilot. Recognition flips positioning within one (knower, world) pair;
  it never couples distinct pairs. Formalised on the sample index set: a
  transition with explicit blocks, and a theorem that no transition crosses a
  block boundary.

  IIT reading (explicit, not claimed as IIT): this is the Φ = 0 case. A system
  whose dynamics factor through disconnected components has no cross-cut
  causation for any integrated-information measure to find. We do NOT compute
  Φ — there is no Φ definition here. We prove the factorisation that would make
  Φ vanish. If a dynamics layer is ever built, this theorem is its base case.
-/
namespace FormalTrika

/-- Recognition dynamics on the sample index set: next maps 0↔1 and 2↔3. -/
def nextIdx : Nat → Nat
  | 0 => 1
  | 1 => 3
  | 2 => 3
  | 3 => 2
  | n => n

/-- Block membership: the two knower-world pairs. -/
def blockOf : Nat → Nat
  | 0 => 0
  | 1 => 0
  | 2 => 1
  | 3 => 1
  | _ => 2

/-- The sample index set. -/
def sampleIdx : List Nat := [0, 1, 2, 3]

/-- CUT: no transition crosses a block boundary. -/
theorem no_cross_cut_flow : sampleIdx.all (fun i =>
    decide (blockOf (nextIdx i) == blockOf i)) = true := by
  decide

end FormalTrika
