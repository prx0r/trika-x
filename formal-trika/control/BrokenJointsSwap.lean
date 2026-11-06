/-
  Formal Trika — C-JNT: correction-joint enumeration (R-tier).

  Ground (R, inherited): CRUX-WALKTHROUGH-05 over tsa08-p04
  (ARGMAP premises + L2). See PREREGISTRATION-JOINTS-RUNG.md.
  Closes the CRUX-05 formal gap at the enumeration level: the two
  joints are now counted and ordered. Their derivation is NOT modeled
  (stated limit — why the grants work remains outside scope).

  What this file IS: finite roster arithmetic (`decide` inside scope).
  What it is NOT: a proof of the correction, an endorsement of the
  anti-Sāṅkhya moves, or anything past the passage cut.
-/
namespace FormalTrika

/-- The two grants (stipulated from the chunk's two joints). -/
inductive Joint where
  | grasp
  | agency
  deriving DecidableEq, Repr

/-- Joint roster, in-chunk order. -/
def joints : List Joint := [Joint.agency, Joint.grasp]

/-- C-JNT1: exactly two joints, distinct. -/
theorem joints_two : joints.length = 2 ∧ joints.Nodup := by decide

/-- C-JNT2: grasp comes first (stipulated in-chunk order). -/
theorem grasp_first : joints.head? = some Joint.grasp := by decide

end FormalTrika
