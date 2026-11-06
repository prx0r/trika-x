/-
  BrokenTetDrop — surgical twin: the tetrahedron removed from the roster.

  Only unique_four refuses ([] ≠ [4]); gap and Euler intact. Models a
  roster without the minimum system (gap widens downward).
-/
namespace FormalTrika

def platonicVerts : List Nat := [6, 8, 12, 20]

theorem gap_five : 5 ∉ platonicVerts := by decide

theorem unique_four : platonicVerts.filter (· == 4) = [4] := by decide

/-- Tetrahedron inventory (vertices, edges, faces). -/
def tetV : Nat := 4
def tetE : Nat := 6
def tetF : Nat := 4

/-- T-TET3: Euler inventory (model check). -/
theorem euler_tet : (tetV - tetE + tetF : Int) = 2 := by decide

end FormalTrika
