/-
  Formal Trika — T-TET: tetrahedron selector-facts (H-tier pilot).

  Ground (H, not T/R): owner-line tetrahedron-as-selector proof +
  tantraloka-tetrahedron notes (rescue volume), classical roster
  stipulated. See PREREGISTRATION-TETRA-RUNG.md. Checks THREE facts
  the proof leans on. No selector, subject, or consciousness claim.

  What this file IS: finite roster arithmetic (`decide` inside scope).
  What it is NOT: proof of the selector, of uniqueness in nature, or
  of anything beyond the listed roster. The 9×4-vs-sharing tension is
  recorded open in the prereg, never modeled here.
  Covers: roster gap + uniqueness + Euler inventory (all of the rung).
-/
namespace FormalTrika

/-- Platonic vertex counts (stipulated classical roster, model data). -/
def platonicVerts : List Nat := [4, 6, 8, 12, 20]

/-- T-TET1: no uniform 5-vertex solid (the spectral gap). -/
theorem gap_five : 5 ∉ platonicVerts := by decide

/-- T-TET2: exactly one 4-vertex uniform solid. -/
theorem unique_four : platonicVerts.filter (· == 4) = [4] := by decide

/-- Tetrahedron inventory (vertices, edges, faces). -/
def tetV : Nat := 4
def tetE : Nat := 6
def tetF : Nat := 4

/-- T-TET3: Euler inventory (model check). -/
theorem euler_tet : (tetV - tetE + tetF : Int) = 2 := by decide

end FormalTrika
