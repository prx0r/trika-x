/-
  Formal Trika — A-AP: aperture operation inventory (H-tier pilot).

  Ground (H, not T/R): owner aperture_spec_v0.7 (9-operation finite
  aperture). See PREREGISTRATION-APERTURE-RUNG.md. Models the INVENTORY
  ONLY: nine named operations, pairwise distinct. No phenomenal claim,
  no selector claim, no MEPIT thesis, no textual grounding.

  What this file IS: finite list arithmetic (`decide` inside scope only).
  What it is NOT: consciousness theory verified, experience explained,
  or any claim no finite list can carry.
  Covers: the op roster of aperture_spec_v0.7 §Core Architecture (all of it).
-/
namespace FormalTrika

/-- The nine aperture operations (owner-named functional tags). -/
def apertureOps : List String :=
  ["manifestation", "retention", "determination", "stream-integration",
   "counterfactual-generation", "value-weighting", "finite-possibility-space",
   "cross-stream-boundary", "inter-stream-influence"]

/-- A-AP1: the roster has exactly nine entries. -/
theorem aperture_nine : apertureOps.length = 9 := by decide

/-- A-AP2: the entries are pairwise distinct operations. -/
theorem aperture_distinct : apertureOps.Nodup := by decide

end FormalTrika
