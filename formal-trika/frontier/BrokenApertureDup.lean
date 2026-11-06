/-
  BrokenApertureDup — surgical twin: "retention" listed twice.

  Only aperture_distinct refuses; the count still computes to nine.
  Models a collapsed inventory (two names, one operation).
-/
namespace FormalTrika

def apertureOps : List String :=
  ["manifestation", "retention", "retention", "stream-integration",
   "counterfactual-generation", "value-weighting", "finite-possibility-space",
   "cross-stream-boundary", "inter-stream-influence"]

theorem aperture_nine : apertureOps.length = 9 := by decide

theorem aperture_distinct : apertureOps.Nodup := by decide

end FormalTrika
