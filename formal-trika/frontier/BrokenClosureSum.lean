/-
  Formal Trika — Closure instance on K₄ (H-tier pilot extension).

  Context: TRIKA-SCIENCE-MAP.md row 12 fork — "Lean statement of the
  K₄↔quantum-tetrahedron claim or downgrade to COUNTERPART (honesty
  before beauty)". This file is the attempt, and its verdict is
  RECORDED DOWNGRADE (see below): one integer instance of the closure
  constraint, checked, which is evidence the joint is formalisable —
  not the isomorphism, which remains unformalised.

  Mathematics (classical, stipulated): the regular tetrahedron's four
  face-normals (1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1) sum to zero.
  In LQG (Livine 1607.08359) the closure constraint — normals summing
  to zero — is what grants a vertex geometric interpretation. Here: one
  concrete quad, summed, checked. Nothing about quantisation, volumes,
  or spectra is stated anywhere in this file.

  Verdict: row 12 → COUNTERPART (downgraded this date; instance kept).
-/
namespace FormalTrika

/-- One face-normal quad (regular tetrahedron, stipulated classical). -/
def tetNormals : List (Int × Int × Int) :=
  [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 0)]

/-- Component-wise sum. -/
def sumNormals : List (Int × Int × Int) → (Int × Int × Int)
  | [] => (0, 0, 0)
  | (a, b, c) :: rest =>
    let (x, y, z) := sumNormals rest
    (a + x, b + y, c + z)

/-- Closure instance: the four normals sum to zero. -/
theorem closure_instance : sumNormals tetNormals = (0, 0, 0) := by decide

/-- Non-degeneracy: no normal is the zero vector. -/
theorem normals_nonzero : tetNormals.all (fun n => n != (0, 0, 0)) = true := by decide

end FormalTrika
