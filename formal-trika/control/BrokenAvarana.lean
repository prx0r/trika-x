/-
  Formal Trika — E-AVAR: MUTANT: covering/purePrinciple swapped (must fail course_ascends ONLY).

  T-tier ground: tsa07-p01 argmap v23 (tattvas as mutual-coverings:
  the later pervades, the earlier is pervaded).
  Design history: the first draft derived `links` and `covers` from the
  SAME list (tautological — the BrokenAvarana twin exposed it; see
  PREREGISTRATION-AVARANA-RUNG-AMEND.md). This version derives cover
  from an INDEPENDENT rule: course-rank ascent over the v3–v22 magnitude
  ladder (gross < subtle < mind < impure < pure). Finding: the ladder is
  PARTIALLY ordered (six groups share course .mind); v23 does not rank
  within a course, and the model exhibits that honestly.

  What this file IS: cross-course ascent checks + exhibited
  underdetermination, over OUR Tattva groups (imports Tattva.lean).
  What it is NOT: a total order, a size constraint, or metaphysics.
  Finite model; `decide` inside scope only.
-/
import Tattva
namespace FormalTrika
open TGroup TCourse

/-- The ladder ascent (R): gross elements lowest … pure principles highest. -/
def ladder : List TGroup :=
  [.grossElement, .subtleElement, .senseFaculty, .actionFaculty,
   .mind, .intellect, .ego, .nature, .purePrinciple, .covering]

/-- Course rank (R, from the v3–v22 magnitude ladder, NOT from the list). -/
def courseRank : TCourse → Nat
  | .gross => 0 | .subtle => 1 | .mind => 2 | .impure => 3 | .pure => 4

/-- Cover principle (v23, T-side): later covers earlier iff its course
    outranks. General rule over courses, never per-group. -/
def covers (later earlier : TGroup) : Bool :=
  decide (courseRank (groupCourse later) > courseRank (groupCourse earlier))

/-- Adjacent pairs of the ladder (later, earlier). -/
def links : List (TGroup × TGroup) :=
  (List.range 9).flatMap fun i =>
    match ladder[i+1]?, ladder[i]? with
    | some a, some b => [(a, b)]
    | _, _ => []

/-- E-AVAR1r: every CROSS-course adjacent pair strictly ascends. -/
theorem course_ascends :
    ((links.filter fun p =>
      groupCourse p.1 != groupCourse p.2).filter fun p =>
      covers p.1 p.2).length
    = (links.filter fun p =>
      groupCourse p.1 != groupCourse p.2).length := by decide

/-- E-AVAR2r: underdetermination exhibited — an intra-course adjacent
    pair exists (v23 leaves within-course order open; the model does
    not force what the text does not give). -/
theorem partial_order_honest :
    (links.filter fun p =>
      groupCourse p.1 == groupCourse p.2).length > 0 := by decide

end FormalTrika
