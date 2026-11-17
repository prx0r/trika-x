/-
  Formal Trika — TESTBED: one carrier, dynamics + action, jointly checked.

  H-tier pilot. Implements the "common testbed" move from Yan et al. (2026):
  instead of comparing theories in prose, put the structures on one finite
  carrier and check them together. Here the carrier is the sample index set,
  the dynamics is recognition (nextIdx), the symmetry is Z/2 (act). The testbed
  theorem states both at once: dynamics never cross a block, and the action
  never changes content.

  A flag on this testbed (dynamics on/off, action on/off) is how another
  theory would dock: IIT needs a kernel, GWT a broadcast step, HOT a
  meta-relation, PCM a continuous group. Those layers are NOT built here;
  their absence is the honest state, not an oversight.
-/
import Cuttable
import PerspectivalAction

namespace FormalTrika

/-- Index to field: the testbed carrier. -/
def fieldOf : Nat → Field
  | 0 => ⟨"s1", "w1", "g1", .instrument⟩
  | 1 => ⟨"s1", "w1", "g1", .primary⟩
  | 2 => ⟨"s2", "w2", "g2", .instrument⟩
  | _ => ⟨"s2", "w2", "g2", .primary⟩

/-- The dynamics as installed in this testbed. Indirection on purpose:
    the twin corrupts the installation, not the shared definition. -/
def step : Nat → Nat := nextIdx

/-- JOINT: one term, both properties. Dynamics stay in-block AND the Z/2
    action preserves content, over every index and every group element. -/
theorem testbed_joint : sampleIdx.all (fun i =>
    z2elts.all (fun g =>
      decide (blockOf (step i) == blockOf i) &&
      decide ((act g (fieldOf i)).world == (fieldOf i).world) &&
      decide ((act g (fieldOf i)).knower == (fieldOf i).knower))) = true := by
  decide

end FormalTrika
