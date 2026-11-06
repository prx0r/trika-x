/-
  BrokenTetEdges — surgical twin: tetrahedron given 5 restraints, not 6.

  Only euler_tet refuses (4−5+4 = 3 ≠ 2); gap and uniqueness intact.
  Models Fuller's own failure mode (five restraints change the shape).
-/
namespace FormalTrika

def platonicVerts : List Nat := [4, 6, 8, 12, 20]

theorem gap_five : 5 ∉ platonicVerts := by decide

theorem unique_four : platonicVerts.filter (· == 4) = [4] := by decide

/-- Tetrahedron inventory (vertices, edges, faces). -/
def tetV : Nat := 4
def tetE : Nat := 5
def tetF : Nat := 4

/-- T-TET3: Euler inventory (model check). -/
theorem euler_tet : (tetV - tetE + tetF : Int) = 2 := by decide

end FormalTrika
