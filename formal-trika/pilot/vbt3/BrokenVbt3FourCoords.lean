/-
  Formal Trika — PILOT P-VBT3 TWIN (verse_coords_five must refuse): verse-level VBT rosters (R-tier, machine-proposed).

  Ground (R, inherited): translation-work vbt/ L2/ARGMAP spans v.2–v.4 and
  v.14 + C1 summaries; see PREREGISTRATION-VBT1-CORRECTION-2026-11-08.md,
  which established that the *verses* name more items than the ARGMAP/C1
  rosters the earlier rungs count.

  PILOT ONLY: not wired into control/run.sh, not an EVIDENCE row, assessor
  has not ruled. Cite the correction + this file, never as established.

  What this file IS: finite roster arithmetic (`decide` inside scope) over the
  VERSE-level inventory, stated "as named in vv.2–4 / v.14", never "the whole
  inventory of X".
  What it is NOT: any claim that the text names EXACTLY nine / EXACTLY five
  (bhairavākṛti's status is a scholarly judgement the held layers do not
  settle — see correction), nor any doctrine, nor any dhāraṇā claim.
-/
namespace FormalTrikaPilotVbt3

/-- The nine candidate forms the verses name: the eight ARGMAP forms plus
    śaktisvarūpa (a distinct word from v.3's śaktitraya). -/
inductive VerseForm where
  | sabdarasi_kala
  | navatman
  | trisiras
  | saktitraya
  | nadabindu
  | candrardha
  | cakrarudha
  | anacka
  | saktisvarupa
  deriving DecidableEq, Repr

/-- Verse-level form roster, as named in vv.2–4. -/
def verseForms : List VerseForm :=
  [VerseForm.sabdarasi_kala, VerseForm.navatman, VerseForm.trisiras,
   VerseForm.saktitraya, VerseForm.nadabindu, VerseForm.candrardha,
   VerseForm.cakrarudha, VerseForm.anacka, VerseForm.saktisvarupa]

/-- P-VBT3a: the verse roster lists nine forms, distinct. Roster fact, not a
    claim the text names exactly nine. -/
theorem verse_forms_nine : verseForms.length = 9 ∧ verseForms.Nodup := by decide

/-- śaktisvarūpa is distinct from śaktitraya (the correction's key point:
    v.4's word is not v.3's). -/
theorem saktisvarupa_distinct : VerseForm.saktisvarupa ≠ VerseForm.saktitraya := by
  decide

/-- The five unpointability coordinates the verse names in v.14
    (`dikkālakalanonmuktā deśoddeśāviśeṣiṇī`): the three C1 names plus deśa
    and uddeśa. -/
inductive VerseCoord where
  | dik
  | kala
  | kalana
  | desa
  | uddesa
  deriving DecidableEq, Repr

/-- Verse-level coordinate roster, as named in v.14. -/
def verseCoords : List VerseCoord :=
  [VerseCoord.dik, VerseCoord.kala, VerseCoord.kalana,
   VerseCoord.desa]

/-- P-VBT3b: the verse roster lists five coordinates, distinct. Roster fact. -/
theorem verse_coords_five : verseCoords.length = 5 ∧ verseCoords.Nodup := by
  decide

end FormalTrikaPilotVbt3
