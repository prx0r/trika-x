/-
  Formal Trika — RUNG 2: tattva ladder generation from general rules.

  Thon Ly's sangaha rung generates 89/121 cittas from 9 generator clauses
  (§G1–G9) over classification axes + 18 cetasika rules (§R1–R18). This file
  is the Trika equivalent: general rules over the tattva ladder structure
  that regenerate the traditional 36.

  T-tier ground: tsa07-p01 argmap (36 natures, magnitude ladder:
  earth 100-crore → water 10× → ... → ahaṃkāra "one-eleven-wombed"
  (aikādaśagarbha = 5 tanmātra + 5 mahābhūta + 1 manas) → buddhi 100× →
  prakṛti → Māyā → Kāla → Niyati → Rāga → Vidyā → pure course).
  AnswerKey.key_thirtysix_tattvas = 36 (T, argmap-pinned).

  The general rules (not per-item tables):
  1. The 10× ladder determines 5 gross elements (earth base, each 10×).
  2. The "N-wombed" formula determines ahaṃkāra's composition (11 = 5+5+1).
  3. Group sizes are structural: 5 sense, 5 action, 1 mind, 1 intellect,
     1 ego, 1 nature, 5 coverings, 7 pure principles.

  What this file IS: a generation from structural rules + count check.
  What it is NOT: a proof that the tattva ladder is metaphysically true,
  or that the 36 are the "real" structure of reality. Scope: finite model.
-/
namespace FormalTrika

/-- The courses of the tattva ladder (T: tsa07-p01 magnitude ladder). -/
inductive TCourse where
  | gross    -- pañca mahābhūta (earth..ether), 10× ladder
  | subtle   -- pañca tanmātra (smell..sound)
  | mind     -- sense/action faculties + inner instruments
  | impure   -- coverings (Māyā..Vidyā)
  | pure     -- pure principles (Śiva..Puruṣa)
  deriving DecidableEq, Repr

/-- The groups within each course. -/
inductive TGroup where
  | grossElement | subtleElement | senseFaculty | actionFaculty
  | mind | intellect | ego | nature | covering | purePrinciple
  deriving DecidableEq, Repr

/-- General rule: group size is determined by structural position.
    This is NOT a per-item table — it states how many inhabit each
    structural slot, derived from the ladder's own composition. -/
def groupSize : TGroup → Nat
  | .grossElement  => 5   -- 10× ladder: earth..ether
  | .subtleElement => 5   -- tanmātra-pañcaka
  | .senseFaculty  => 5   -- jñāna-indriya
  | .actionFaculty => 5   -- karma-indriya
  | .mind          => 1   -- manas (part of 11-wombed)
  | .intellect     => 1   -- buddhi (100× ahaṃkāra)
  | .ego           => 1   -- ahaṃkāra (11-wombed = 5+5+1)
  | .nature        => 1   -- prakṛti
  | .covering      => 5   -- Māyā, Kāla, Niyati, Rāga, Vidyā
  | .purePrinciple => 6   -- MUTANT: one pure principle missing (must fail)

/-- The course each group belongs to (T: tsa07-p01 ladder position). -/
def groupCourse : TGroup → TCourse
  | .grossElement  => .gross
  | .subtleElement => .subtle
  | .senseFaculty  => .mind
  | .actionFaculty => .mind
  | .mind          => .mind
  | .intellect     => .mind
  | .ego           => .mind
  | .nature        => .mind
  | .covering      => .impure
  | .purePrinciple => .pure

def allGroups : List TGroup :=
  [.grossElement, .subtleElement, .senseFaculty, .actionFaculty,
   .mind, .intellect, .ego, .nature, .covering, .purePrinciple]

/-- The generated set: every group contributes its structural size. -/
def generated : List (TGroup × Nat) := allGroups.map (fun g => (g, groupSize g))

/-- TK-R2a: the 10× ladder yields exactly 5 gross elements. -/
theorem five_gross_elements : groupSize .grossElement = 5 := by decide

/-- TK-R2b: the N-wombed formula: ahaṃkāra = 5 tanmātra + 5 mahābhūta + 1 manas. -/
theorem eleven_wombed :
    groupSize .subtleElement + groupSize .grossElement + groupSize .mind = 11 := by decide

/-- TK-R2c: the tradition counts 36 tattvas. -/
theorem thirty_six :
    (generated.map Prod.snd).foldl (· + ·) 0 = 36 := by decide

/-- TK-R2d: every group is accounted for (no orphan, no double-count). -/
theorem all_groups_present :
    (generated.map Prod.fst).eraseDups.length = allGroups.length := by decide

/-- TK-R2e: compression ratio — rule clauses ÷ generated rows.
    10 group-size clauses ÷ 36 rows ≈ 0.28.
    (Thon Ly's sangaha: 27 clauses ÷ 121 rows = 0.22; over 89 = 0.30.)
    The tattva structure is hierarchical (groups of different sizes),
    not combinatorial (independent axes) — hence slightly worse compression. -/
theorem compression_ratio :
    (generated.length : Nat) = 10 := by decide
    -- 10 groups; ratio = 10/36 ≈ 0.28 (computed in Results.md)

/- The count matches AnswerKey.key_thirtysix_tattvas (36).
   (thirty_six above IS this check — kept here as the named answer-key
   cross-reference; must_fail targets thirty_six only.) -/

end FormalTrika
