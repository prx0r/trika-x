/-
  Formal Trika — P-PRA: manifestation priority (twin-attack pilot).

  Ground (R, not T): ochema claim-01 (TĀ 1.54 via Dyczkowski), inherited
  one tier down (their T → my R; I have not verified verse/translation).
  See PREREGISTRATION-PRAKASA-RUNG.md. First twin-attack on imported
  claim files: the attack asks what single change breaks the claim.

  What this file IS: finite roster check (`decide` inside scope only).
  What it is NOT: proof of transcendental priority, unity, or anything
  metaphysical. Covers: the appearing-check only.
-/
namespace FormalTrika

/-- Account items with appearance flags. -/
def roster : List Bool := [true, true, true, true]

/-- P-PRA1: everything in the account appears. -/
theorem all_appear : roster.all id = true := by decide

end FormalTrika
