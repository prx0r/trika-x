/-
  BrokenApertureDrop — surgical twin: "inter-stream-influence" removed.

  Only aperture_nine refuses (8 ≠ 9); the rest stay distinct. Models an
  8-operation aperture: every named op genuine, one missing from the whole.
-/
namespace FormalTrika

def apertureOps : List String :=
  ["manifestation", "retention", "determination", "stream-integration",
   "counterfactual-generation", "value-weighting", "finite-possibility-space",
   "cross-stream-boundary"]

theorem aperture_nine : apertureOps.length = 9 := by decide

theorem aperture_distinct : apertureOps.Nodup := by decide

end FormalTrika
