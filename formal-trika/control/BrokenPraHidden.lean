/-
  BrokenPraHidden — surgical twin: one non-appearing item in the roster.

  Only all_appear refuses. Models an account containing what never
  appeared — the priority claim's exact denial.
-/
namespace FormalTrika

def roster : List Bool := [true, true, false, true]

theorem all_appear : roster.all id = true := by decide

end FormalTrika
