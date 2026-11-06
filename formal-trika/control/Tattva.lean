/-
  Formal Trika — RUNG 2: a grouped count, not a derivation of a tradition.

  Tantrasāra 7.9 lists five tanmātras and eleven akṣas within ahaṃkāra;
  8.73–77 identifies mind, five cognitive and five action faculties.
  7.13–21 and 8.16–17 distinguish puruṣa, the five kalā-led factors,
  māyā, and five pure tattvas. Ananta is a tattveśvara, not an extra tattva.
  GRETIL's prose segment numbers are digital locators; review the edition
  and mapping before treating this as authoritative textual interpretation.

  This model adds stipulated group sizes. The resulting sum is 36; it does
  not generate 36 named entities or prove a bijection with a Sanskrit list.
  The earlier model reached 36 through offsetting classification errors;
  see SANSKRIT-FOUNDATION-REVIEW-2026-11-06.md.
-/
namespace FormalTrika

/-- The courses of the tattva ladder (T: tsa07-p01 magnitude ladder). -/
inductive TCourse where
  | gross    -- pañca mahābhūta (earth..ether), 10× ladder
  | subtle   -- pañca tanmātra (smell..sound)
  | mind     -- sense/action faculties + inner instruments
  | impure   -- subject, five kañcukas, and māyā (coarse grouping)
  | pure     -- five pure principles (Śiva through śuddhavidyā)
  deriving DecidableEq, Repr

/-- The groups within each course. -/
inductive TGroup where
  | grossElement | subtleElement | senseFaculty | actionFaculty
  | mind | intellect | ego | nature | subject | covering | maya | purePrinciple
  deriving DecidableEq, Repr

/-- Stipulated group sizes. These are data, not independently derived rules. -/
def groupSize : TGroup → Nat
  | .grossElement  => 5   -- 10× ladder: earth..ether
  | .subtleElement => 5   -- tanmātra-pañcaka
  | .senseFaculty  => 5   -- jñāna-indriya
  | .actionFaculty => 5   -- karma-indriya
  | .mind          => 1   -- manas (part of 11-wombed)
  | .intellect     => 1   -- buddhi (100× ahaṃkāra)
  | .ego           => 1   -- ahaṃkāra
  | .nature        => 1   -- prakṛti
  | .subject       => 1   -- puruṣa
  | .covering      => 5   -- kalā, vidyā, rāga, kāla, niyati
  | .maya          => 1   -- māyā; with the five, a six-cover reckoning
  | .purePrinciple => 5   -- śiva, śakti, sadāśiva, īśvara, śuddhavidyā

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
  | .subject       => .impure
  | .covering      => .impure
  | .maya          => .impure
  | .purePrinciple => .pure

def allGroups : List TGroup :=
  [.grossElement, .subtleElement, .senseFaculty, .actionFaculty,
   .mind, .intellect, .ego, .nature, .subject, .covering, .maya, .purePrinciple]

/-- The group-size table. It does not enumerate the individual tattvas. -/
def generated : List (TGroup × Nat) := allGroups.map (fun g => (g, groupSize g))

/-- TK-R2a: the 10× ladder yields exactly 5 gross elements. -/
theorem five_gross_elements : groupSize .grossElement = 5 := by decide

/-- TK-R2b: eleven faculties = five cognitive + five action + mind. -/
theorem eleven_wombed :
    groupSize .senseFaculty + groupSize .actionFaculty + groupSize .mind = 11 := by decide

/-- TK-R2c: the stipulated group sizes sum to 36. -/
theorem thirty_six :
    (generated.map Prod.snd).foldl (· + ·) 0 = 36 := by decide

/-- TK-R2d: the listed group tags have no duplicates. This does not show
    that every possible tag or every Sanskrit tattva is present. -/
theorem all_groups_present :
    (generated.map Prod.fst).eraseDups.length = allGroups.length := by decide

/-- Historical name retained: this checks the number of groups, not a
    compression ratio or an independently generated inventory. -/
theorem compression_ratio :
    (generated.length : Nat) = 12 := by decide

/- Both totals are stipulated as 36. Equality alone is not independent
   textual corroboration. must_fail targets thirty_six. -/

end FormalTrika
