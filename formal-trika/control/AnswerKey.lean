/-
  Formal Trika — ANSWER KEY: tradition-stated figures as data.

  This file is KEY, not rules: nothing here generates anything. It collates
  the counts the tradition states (with refs), SEPARATELY from any model,
  so no model can restate it. Status per figure: VERIFIED-QUOTE (read in
  the gold this session) · ARGMAP-PINNED (argmap passage id) ·
  PREREGISTERED-ONLY (claimed in PREREGISTRATION.md; machine recount pending)
  · UNPINNED (work cited, exact passage not yet pinned).

  Reckonings the texts mix are recorded as mixed (cf. tsa08-p03 six-cover
  scheme vs the five-kañcuka count) — never smoothed.
-/
namespace FormalTrika

/-- The five kañcuka names (T). ARGMAP-PINNED: tsa08-p03 (vivekas; kañcukas).
    T1 frequency per PREREGISTRATION.md (kalā ×50, vidyā ×6, rāga ×3,
    kāla ×2, niyati ×1): PREREGISTERED-ONLY — full-lemma recount pending;
    spot counts this session (L0 citation field) are partial, not the figure. -/
inductive KancukaName where
  | kala | vidya | raga | kalaTime | niyati
  deriving DecidableEq, Repr

def kancukaNames : List KancukaName :=
  [.kala, .vidya, .kalaTime, .raga, .niyati]

/-- KEY-1: the tradition counts five coverings. -/
theorem key_five_kancukas : kancukaNames.length = 5 := by decide

/-- KEY-1b (mixed reckoning, recorded not smoothed): tsa08-p03 states the
    Māyā-SIX as six covers (five kañcukas + Māyā). Both reckonings are T;
    models must declare which they use. -/
inductive CoverScheme where
  | five   -- five kañcukas
  | six    -- five kañcukas + Māyā (tsa08-p03: "Māyā-six = six covers")
  deriving DecidableEq, Repr

/-- The 36 tattvas (T). ARGMAP-PINNED: tsa07-p01 (place-course + 36
    principles with magnitude ladder, dissolution reverses into
    beyond-consciousness). -/
def key_tattva_count : Nat := 36

/-- KEY-2: thirty-six. -/
theorem key_thirtysix_tattvas : key_tattva_count = 36 := by decide

/-- The seven experients (T-count, not our rows). Refs: paramarthasara
    saptadhā-pramātṛ scheme (work cited; exact argmap passage UNPINNED) and
    tsa08-p03 Māyā-person discrimination ladder (vijñānākala above Māyā;
    kalā-person; mala-person→Śiva-equality; fullness-view→Śiva-hood).
    Our Pramatr.lean generates 7 Boolean rows; whether they ARE these seven
    is UNESTABLISHED (see PREREGISTRATION-2026-11-06 correction §1). -/
def key_experient_count : Nat := 7

/-- KEY-3: seven. -/
theorem key_seven_experients : key_experient_count = 7 := by decide

/-- The five pure-course followers (T). VERIFIED-QUOTE this session:
    tsa-a08 v35-context v17 T1: "Śāmbhavas, Śāktas, Mantramāheśvaras,
    Mantreśvaras, Mantras — thus the pure path." -/
inductive PureFollower where
  | sambhava | sakta | mantraMaheshvara | mantreshvara | mantra
  deriving DecidableEq, Repr

def pureFollowers : List PureFollower :=
  [.sambhava, .sakta, .mantraMaheshvara, .mantreshvara, .mantra]

/-- KEY-4: five. -/
theorem key_five_followers : pureFollowers.length = 5 := by decide

/-- śaktipāta as operative force (T). VERIFIED-QUOTE this session:
    tsa-a08 v35 T1 "by the Supreme Lord's power-descent sway"
    (parameśvaraśaktipātavaśāt, L0 citation). -/
def key_grace_term_attested : Bool := true

/-- The 112 dhāraṇās (T-count). Refs: translation-work/vbt (GRETIL
    sa_vijñānabhairava vv1-162; vv24-135 = 112 dhāraṇās per
    vbt/lore-2026-11-04.md; legacy verse-count confusion documented there).
    ARGMAP-PINNED: vbt-p01 argmap. -/
def key_dharana_count : Nat := 112

/-- KEY-5: one hundred twelve. -/
theorem key_hundred_twelve_dharanas : key_dharana_count = 112 := by decide

/- EXCLUDED ON PURPOSE (our definitions, not tradition counts):
    the 4 recognition conjuncts (Conjuncts.lean), the 12-bit RecState,
    the 3-value felt-to-coordinate firm rows (CorrKey), the 5-factor
    kancuka-to-coordinate pairing gloss (Coords.lean), mala-count profile
    [2,3,1,2,1,2,0] (observed shape of OUR model). None of these may ever
    be cited as traditional figures.
-/

end FormalTrika
