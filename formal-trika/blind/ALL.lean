-- blind/Mala.lean (from control/Mala.lean)

namespace FormalTrika

/-- The three malas: āṇava (atomicity/ignorance), māyīya (differentiation),
    kārma (karmic residue). -/
inductive Mala where
  | anava | mayiya | karma
  deriving DecidableEq, Repr

/-- All three. -/
def malas : List Mala := [.anava, .mayiya, .karma]

/-- The tradition's count: 3. -/
theorem count_3 : malas.length = 3 := by decide

end FormalTrika

-- blind/Pramatr.lean (from control/Pramatr.lean)

import Mala
namespace FormalTrika
open Mala

/-- An experient station: which malas are present. -/
structure Pramatr where
  anava  : Bool   -- āṇavamala present
  mayiya : Bool   -- māyīyamala present
  karma  : Bool   -- kārmamala present
  deriving DecidableEq, Repr

/-- All 8 combinations of the three axes. -/
def combos : List Pramatr :=
  [true, false].flatMap fun a => [true, false].flatMap fun m =>
    [false, true].map fun k => ⟨a, m, k⟩

/-- GENERAL RULE (the only rule clause; R-tier justification):
    karma never floats free — it binds only where there is atomic ignorance
    (āṇava) or differentiation (māyīya) to bind through. Excludes exactly
    (F,F,T): karma with neither ignorance nor world to act in. -/
def wellformed (p : Pramatr) : Bool :=
  !(p.karma && !p.mayiya && !p.anava)   -- R1: no free-floating karma

/-- The generated set: rows satisfying all general rules. -/
def generated : List Pramatr := combos.filter wellformed

/-- How many malas each generated row carries (profile, order as generated). -/
def malaCount (p : Pramatr) : Nat :=
  (if p.anava then 1 else 0) + (if p.mayiya then 1 else 0) + (if p.karma then 1 else 0)

/-- TK-C1a: eight axis combinations. -/
theorem eight_combos : combos.length = 8 := by decide

/-- TK-C1b: seven Boolean rows survive the R1 model. -/
theorem seven : generated.length = 7 := by decide

/-- TK-C1c: mala-count profile of the seven rows, in generation order.
    Observed (not hand-set): the count theorem is `seven`; this records the
    shape. Generation order: (T,T,F)=2, (T,T,T)=3, (T,F,F)=1, (T,F,T)=2,
    (F,T,F)=1, (F,T,T)=2, (F,F,F)=0. -/
theorem profile : generated.map malaCount = [2, 3, 1, 2, 1, 2, 0] := by decide

/-- UNVERIFIED R-tier name proposal (counts do not depend on it).
    This mapping is incomplete and is not a validated traditional classification.
    sakala (3) · pralayākala (A+K) · vijñānākala (A) · mantra stations (pure
    adhvan, positional split — P-TK1b exception, flagged R) · śiva (0). -/
def unverifiedProposedLabel : Pramatr → String
  | ⟨true, true, true⟩   => "sakala"
  | ⟨true, false, true⟩  => "pralayakala"
  | ⟨true, false, false⟩ => "vijnanakala"
  | ⟨false, true, true⟩  => "mantra (R: positional)"
  | ⟨false, true, false⟩ => "mantresvara (R: positional)"
  | ⟨false, false, false⟩=> "siva"
  | ⟨true, true, false⟩  => "sakala-pure-karma-free (R: transitional)"
  | ⟨false, false, true⟩ => "ILL-FORMED (excluded by R1)"

end FormalTrika

-- blind/Kancuka.lean (from control/Kancuka.lean)

namespace FormalTrika

/-- The five coverings. -/
inductive Kancuka where
  | kala    -- limited doership (kiñcitkartṛtva)
  | vidya   -- limited knowledge (kiñcijjñatva)
  | raga    -- desire for the unfinished (attachment)
  | kalaTime-- temporal sequence (past/present/future division)
  | niyati  -- restriction (place/form/destiny fixity)
  deriving DecidableEq, Repr

/-- The infinite capacities they contract (R-tier gloss). -/
inductive Capacity where
  | allDoership    -- sarvakartṛtva
  | allKnowledge   -- sarvajñatva
  | satisfaction   -- pūrṇatva / self-sufficiency
  | eternity       -- nityatva
  | pervasion      -- vyāpakatva
  deriving DecidableEq, Repr

open Kancuka Capacity

def kancukas : List Kancuka := [.kala, .vidya, .raga, .kalaTime, .niyati]

/-- Each covering restricts exactly one capacity. -/
def restricts : Kancuka → Capacity
  | .kala     => .allDoership
  | .vidya    => .allKnowledge
  | .raga     => .satisfaction
  | .kalaTime => .eternity
  | .niyati   => .pervasion

/-- The tradition's count: 5. -/
theorem count_5 : kancukas.length = 5 := by decide

/-- The pairing covers 5 distinct capacities (no two coverings limit the same). -/
theorem pairings_distinct : ((kancukas.map restricts).eraseDups).length = 5 := by decide

end FormalTrika

-- blind/Recognition.lean (from control/Recognition.lean)

namespace FormalTrika

/-- Minimal AM0 state: five content bits + the σ parameter.
    (Content fields are Bool here so the whole space is checkable by decide;
    this is a structural model of the flip, not a phenomenology.) -/
structure Am0State where
  e : Bool  -- event-type marker
  p : Bool  -- accessibility profile
  h : Bool  -- history marker
  b : Bool  -- buffer marker
  o : Bool  -- intentional object marker
  s : Bool  -- σ: true = Sv(O) (exempted), false = ¬Sv(O) (recognized)
  deriving DecidableEq, Repr

/-- T_rec: recognition. Content untouched, σ flipped to recognized. -/
def recognize (m : Am0State) : Am0State := { m with s := false }

/-- Content equality (σ excluded). -/
def contentEq (a b : Am0State) : Bool :=
  a.e == b.e && a.p == b.p && a.h == b.h && a.b == b.b && a.o == b.o

/-- The whole state space: 2^6 = 64. -/
def allStates : List Am0State :=
  [true, false].flatMap fun e => [true, false].flatMap fun p =>
    [true, false].flatMap fun h => [true, false].flatMap fun b =>
      [true, false].flatMap fun o => [true, false].map fun s =>
        ⟨e, p, h, b, o, s⟩

/-- P-TK3a: recognition preserves content on every state. -/
theorem recognition_preserves_content :
    (allStates.filter fun m => contentEq m (recognize m)).length = 64 := by decide

/-- P-TK3b: recognition always lands in ¬Sv(O). -/
theorem recognition_lands_recognized :
    (allStates.filter fun m => !(recognize m).s).length = 64 := by decide

/-- P-TK3c: recognition is NOT information gain — content before and after is
    identical for every state (the tuple content is unchanged; only the
    operator's relation to its dependence flips). -/
theorem recognition_adds_nothing :
    allStates.all (fun m => contentEq m (recognize m)) = true := by decide

/-- S-SHARP1: contentEq discriminates — a pair differing in exactly one
    content field (o) is NOT content-equal. Without this, `-> ||` and
    `-> true` mutants survive the P-TK3 suite (found by mechanical sweep):
    the old theorems hold under weakened equality too. This theorem says
    the equality means what it says. -/
theorem contentEq_sharp :
    contentEq { e := true, p := false, h := false, b := false, o := false, s := true }
              { e := true, p := false, h := false, b := false, o := true, s := false } = false := by decide

end FormalTrika

-- blind/AnswerKey.lean (from control/AnswerKey.lean)

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

/-- KEY-GRACE: the śaktipāta term flag checks (pins the v35
    VERIFIED-QUOTE to the machine-checked surface; the evidence note
    carries the T content, the theorem only the flag). -/
theorem key_grace_term : key_grace_term_attested = true := by decide

/-- The 112 dhāraṇās (T-count). Refs: translation-work/vbt (GRETIL
    sa_vijñānabhairava vv1-162; vv24-135 = 112 dhāraṇās per
    vbt/lore-2026-11-04.md; legacy verse-count confusion documented there).
    ARGMAP-PINNED: vbt-p01 argmap. -/
def key_dharana_count : Nat := 112

/-- KEY-5: one hundred twelve. -/
theorem key_hundred_twelve_dharanas : key_dharana_count = 112 := by decide

end FormalTrika

-- blind/Tattva.lean (from control/Tattva.lean)

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
  | .purePrinciple => 7   -- Śiva, Śakti, Sadāśiva, Īśvara, Ananta, Śuddhavidyā, Puruṣa

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

end FormalTrika

-- blind/Transitions.lean (from recognition/Transitions.lean)

namespace FormalRecognition

set_option maxRecDepth 100000
set_option maxHeartbeats 2000000

/-- The recognition state: 7 positioning bits + 5 embodiment bits. -/
structure RecState where
  xdm  : Bool  -- exclusive self-determination Xᵢ
  exh  : Bool  -- standpoint-as-exhaustive eᵢ
  grnd : Bool  -- ground attribution gᵢ
  own  : Bool  -- exclusive ownership ωᵢ
  agy  : Bool  -- independent authorship αᵢ
  pol  : Bool  -- exclusive metacontrol Πᵢ
  ext  : Bool  -- externalization of the world
  body : Bool  -- body-process Oᵢ
  lim  : Bool  -- finite limitation Lᵢ
  fld  : Bool  -- local phenomenal field Dᵢ
  prv  : Bool  -- field privacy ∂Dᵢ
  wrld : Bool  -- organism-relative world Wᵢ
  deriving DecidableEq, Repr

/-- T_rec: de-exclusivize the 7 positioning bits; embodiment untouched. -/
def trec (m : RecState) : RecState :=
  { m with xdm := false, exh := false, grnd := false, own := false,
             agy := false, pol := false, ext := false }

/-- Acquisition (learning): rewrites a content bit, moves no σ.
    The discriminator — what recognition is NOT. -/
def acquire (m : RecState) : RecState := { m with body := !m.body }

/-- Bondage: limitation + exhaustive-identification + externalization. -/
def bondage (m : RecState) : Bool := m.lim && m.exh && m.ext

/-- Embodiment profile (the 5 kept bits). -/
def kept (m : RecState) : Bool × Bool × Bool × Bool × Bool :=
  (m.body, m.lim, m.fld, m.prv, m.wrld)

/-- The whole space: 2^12 = 4096. -/
def allRecStates : List RecState :=
  [true, false].flatMap fun x => [true, false].flatMap fun e =>
    [true, false].flatMap fun g => [true, false].flatMap fun o =>
      [true, false].flatMap fun a => [true, false].flatMap fun p =>
        [true, false].flatMap fun x2 => [true, false].flatMap fun b =>
          [true, false].flatMap fun l => [true, false].flatMap fun f =>
            [true, false].flatMap fun pv => [true, false].map fun w =>
              ⟨x, e, g, o, a, p, x2, b, l, f, pv, w⟩

/-- R-REC1a: content preserved on every state (removal, nothing added). -/
theorem trec_preserves_embodiment :
    (allRecStates.filter fun m => kept m == kept (trec m)).length = 4096 := by
  decide

/-- R-REC1b: bondage cleared on every state. -/
theorem trec_clears_bondage :
    (allRecStates.filter fun m => !(bondage (trec m))).length = 4096 := by
  decide

/-- R-REC1c: limitation retained on every state (no destruction of δᵢ). -/
theorem trec_retains_limitation :
    (allRecStates.filter fun m => (trec m).lim == m.lim).length = 4096 := by
  decide

/-- R-REC1d: applying this function twice has the same result as once.
    This alone says nothing about backsliding under other transitions. -/
theorem trec_idempotent :
    (allRecStates.filter fun m => trec (trec m) == trec m).length = 4096 := by
  decide

/-- R-REC2a: a state with the selected flags exists. No transition relation
    is defined here, so this does not prove that a state stays stuck. -/
theorem anava_stuck_exists :
    (allRecStates.filter fun m => m.exh && bondage m).length > 0 := by
  decide

/-- R-REC2b (māyīya): acquisition rewrites content — provably NOT T_rec.
    There are states where acquire changes embodiment but trec does not. -/
theorem acquire_is_not_recognition :
    (allRecStates.filter fun m =>
      (kept m != kept (acquire m)) && (kept m == kept (trec m))).length = 4096 := by
  decide

/-- R-REC2c: states with the selected positioning flags exist. No transition
    or self-loop is proved by this Boolean existence check. -/
theorem karma_loop_exists :
    (allRecStates.filter fun m =>
      m.xdm && m.exh && m.own && m.agy).length > 0 := by
  decide

end FormalRecognition

-- blind/NonEntail.lean (from recognition/NonEntail.lean)

namespace FormalRecognition

set_option maxRecDepth 100000
set_option maxHeartbeats 2000000

/-- The six contentions as flags. No constraints: any combination is a
    candidate position; entailments must be EARNED, never built in. -/
structure Chain where
  a : Bool  -- self-manifest
  b : Bool  -- first-personality / ownership
  c : Bool  -- ownership persists across time
  d : Bool  -- one enduring subject
  e : Bool  -- genuine freedom (svātantrya, not flexibility)
  f : Bool  -- one universal consciousness
  deriving DecidableEq, Repr

def allChains : List Chain :=
  [true, false].flatMap fun a => [true, false].flatMap fun b =>
    [true, false].flatMap fun c => [true, false].flatMap fun d =>
      [true, false].flatMap fun e => [true, false].map fun f =>
        ⟨a, b, c, d, e, f⟩

/-- R-REC3: the six one-step witnesses + the full A..E-without-F. -/
theorem aby_not_b : (allChains.filter fun m => m.a && !m.b).length > 0 := by
  decide
theorem b_not_c : (allChains.filter fun m => m.b && !m.c).length > 0 := by
  decide
theorem c_not_d : (allChains.filter fun m => m.c && !m.d).length > 0 := by
  decide
theorem d_not_e : (allChains.filter fun m => m.d && !m.e).length > 0 := by
  decide
theorem e_not_f : (allChains.filter fun m => m.e && !m.f).length > 0 := by
  decide
theorem abcde_without_f :
    (allChains.filter fun m =>
      m.a && m.b && m.c && m.d && m.e && !m.f).length > 0 := by
  decide

/-- The seven vimarśas as independent flags (V₁ manifestness … V₇
    unrestricted freedom). Independence: all 128 combos occur — unity
    of the seven is NOT given. -/
structure Vim7 where
  v1 : Bool
  v2 : Bool
  v3 : Bool
  v4 : Bool
  v5 : Bool
  v6 : Bool
  v7 : Bool
  deriving DecidableEq, Repr

def allVim7 : List Vim7 :=
  [true, false].flatMap fun a => [true, false].flatMap fun b =>
    [true, false].flatMap fun c => [true, false].flatMap fun d =>
      [true, false].flatMap fun e => [true, false].flatMap fun f =>
        [true, false].map fun g => ⟨a, b, c, d, e, f, g⟩

/-- R-REC4a: V₁–V₇ dissociable — all 128 combinations well-formed. -/
theorem vim7_independent : allVim7.length = 128 := by decide

/-- Co-presence on three points: U(x,y) = x,y co-present.
    Witness: U(0,1), U(1,2) hold; U(0,2) fails. Non-transitive. -/
def coPresent : Fin 3 → Fin 3 → Bool
  | 0, 0 => true  | 1, 1 => true  | 2, 2 => true
  | 0, 1 => true  | 1, 0 => true
  | 1, 2 => true  | 2, 1 => true
  | _, _ => false

/-- R-REC4b: co-presence is NOT transitive. -/
theorem copresence_nontransitive :
    (coPresent 0 1 && coPresent 1 2 && !coPresent 0 2) = true := by decide

/-- Boolean equality toy: the three constraints are jointly unsatisfiable.
    This is not a general sheaf theorem; only one pair is exhibited below. -/
theorem no_global_section :
    ¬∃ (x y z : Bool), x = y ∧ y = z ∧ x ≠ z := by decide

theorem pairwise_satisfiable_xy :
    (∃ (x y : Bool), x = y) := by decide

end FormalRecognition

-- blind/Conjuncts.lean (from recognition/Conjuncts.lean)

namespace FormalRecognition

set_option maxRecDepth 100000
set_option maxHeartbeats 2000000

/-- The four conjuncts. -/
structure Conjuncts where
  trans : Bool  -- transformation of positioning
  reid  : Bool  -- reidentification (this is that)
  ver   : Bool  -- veridicality (it is so)
  stab  : Bool  -- stabilization (does not collapse)
  deriving DecidableEq, Repr

def recognitionHolds (k : Conjuncts) : Bool :=
  k.trans && k.reid && k.ver && k.stab

def allConjuncts : List Conjuncts :=
  [true, false].flatMap fun a => [true, false].flatMap fun b =>
    [true, false].flatMap fun c => [true, false].map fun d =>
      ⟨a, b, c, d⟩

/-- R-REC5a: exactly ONE of 16 combinations is recognition. -/
theorem recognition_unique :
    (allConjuncts.filter recognitionHolds).length = 1 := by decide

/-- R-REC5b–e: dropping any ONE conjunct loses recognition. -/
theorem drop_transformation_loses :
    (allConjuncts.filter fun k =>
      (!k.trans && k.reid && k.ver && k.stab) && recognitionHolds k).length = 0 := by
  decide
theorem drop_reidentification_loses :
    (allConjuncts.filter fun k =>
      (k.trans && !k.reid && k.ver && k.stab) && recognitionHolds k).length = 0 := by
  decide
theorem drop_veridicality_loses :
    (allConjuncts.filter fun k =>
      (k.trans && k.reid && !k.ver && k.stab) && recognitionHolds k).length = 0 := by
  decide
theorem drop_stabilization_loses :
    (allConjuncts.filter fun k =>
      (k.trans && k.reid && k.ver && !k.stab) && recognitionHolds k).length = 0 := by
  decide

/-- Generic Recog(a,b) over two presented items (Fin 2 keeps it finite). -/
structure RecogInst where
  present    : Bool  -- a is present
  acquainted : Bool  -- prior acquaintance with b
  identify   : Bool  -- a identified as b
  a : Fin 2
  b : Fin 2
  deriving DecidableEq, Repr

def recogHolds (r : RecogInst) : Bool :=
  r.present && r.acquainted && r.identify && (r.a == r.b)

def allRecogInsts : List RecogInst :=
  [true, false].flatMap fun p => [true, false].flatMap fun q =>
    [true, false].flatMap fun i => ([0, 1] : List (Fin 2)).flatMap fun a =>
      ([0, 1] : List (Fin 2)).map fun b => ⟨p, q, i, a, b⟩

/-- R-REC5f: misidentification — a≠b never recognizes, however certain. -/
theorem misidentification_never_recognizes :
    (allRecogInsts.filter fun r => (r.a != r.b) && recogHolds r).length = 0 := by
  decide

/-- The five Śaiva axioms as flags; Full = Part-ground + all five.
    Part = shared ground with distinct tokens (ground : Bool equal,
    subjects : Fin 2 distinct — coherent, exhibited). -/
structure TargetState where
  pi_pi   : Bool  -- process-inexternal identity holds (D≡O)
  g1      : Bool  -- ground of subject 1
  g2      : Bool  -- ground of subject 2
  s1      : Fin 2 -- subject-token 1
  s2      : Fin 2 -- subject-token 2
  s1axiom : Bool
  s2axiom : Bool
  s3axiom : Bool
  s4axiom : Bool
  s5axiom : Bool
  deriving DecidableEq, Repr

def partHolds (t : TargetState) : Bool := (t.g1 == t.g2) && (t.s1 != t.s2)

def fullSiva (t : TargetState) : Bool :=
  partHolds t && t.s1axiom && t.s2axiom && t.s3axiom && t.s4axiom && t.s5axiom

def allTargets : List TargetState :=
  [true, false].flatMap fun p => [true, false].flatMap fun g1 =>
    [true, false].flatMap fun g2 =>
      ([0, 1] : List (Fin 2)).flatMap fun s1 =>
        ([0, 1] : List (Fin 2)).flatMap fun s2 =>
          [true, false].flatMap fun q1 => [true, false].flatMap fun q2 =>
            [true, false].flatMap fun q3 => [true, false].flatMap fun q4 =>
              [true, false].map fun q5 =>
                ⟨p, g1, g2, s1, s2, q1, q2, q3, q4, q5⟩

/-- R-REC6a: the participatory reading is coherent — shared ground with
    genuinely distinct tokens exists in the model. -/
theorem part_coherent_distinct_tokens :
    (allTargets.filter partHolds).length > 0 := by decide

/-- R-REC6b: one modeled state has PI true and unequal ground flags. A single
    witness does not establish full independence over all assignments. -/
theorem pi_independent_of_grounds :
    (allTargets.filter fun t => t.pi_pi && (t.g1 != t.g2)).length > 0 := by
  decide

/-- R-REC6c: Śiva requires S — Part without S₁ is NOT the full recognition. -/
theorem siva_requires_axioms :
    (allTargets.filter fun t => partHolds t && !t.s1axiom && fullSiva t).length = 0 := by
  decide

/-- Unus-ambo (R): a symmetric non-identity bond exists — 1×1 is not 1=1.
    Exhibit: mutual relatedness without numerical identity. -/
def bonded : Fin 2 → Fin 2 → Bool
  | _, _ => true  -- all mutually bonded (one relation, two relata)

theorem unus_ambu_not_identity :
    ((bonded 0 1 && bonded 1 0) && ((0 : Fin 2) != 1)) = true := by decide

end FormalRecognition

-- blind/Memory.lean (from recognition/Memory.lean)

namespace FormalRecognition

/-- The five memories. -/
structure Mem5 where
  m1 : Bool  -- retention
  m2 : Bool  -- continuity
  m3 : Bool  -- attribution
  m4 : Bool  -- autonoetic (first-personal recollection)
  m5 : Bool  -- identity (ownership as self)
  deriving DecidableEq, Repr

/-- Well-formed: M₄ requires its M₁–M₃ foundation (no foundationless
    autonoetic memory). M₅ floats free (the contested step). -/
def memWellformed (m : Mem5) : Bool :=
  !(m.m4 && !(m.m1 && m.m2 && m.m3))

def allMem5 : List Mem5 :=
  [true, false].flatMap fun a => [true, false].flatMap fun b =>
    [true, false].flatMap fun c => [true, false].flatMap fun d =>
      [true, false].map fun e => ⟨a, b, c, d, e⟩

def wellformedMems : List Mem5 := allMem5.filter memWellformed

/-- Foundation rule holds: no well-formed M₄ without M₁–M₃. -/
theorem m4_requires_foundation :
    (wellformedMems.filter fun m => m.m4 && !(m.m1 && m.m2 && m.m3)).length = 0 := by
  decide

/-- The converse of the encoded foundation rule does not follow. -/
theorem foundations_without_m4_exist :
    (wellformedMems.filter fun m => m.m1 && m.m2 && m.m3 && !m.m4).length > 0 := by
  decide

/-- R-REC7a: M₄ ⇏ M₅ — autonoetic memory without identity-ownership exists. -/
theorem m4_without_m5 :
    (wellformedMems.filter fun m => m.m4 && !m.m5).length > 0 := by
  decide

/-- Seeing vs enacting: Layer 3 (sees deception) and Layer 4 (enacts
    removal). Enacting requires seeing; seeing does not require enacting. -/
structure SeerDoer where
  sees   : Bool  -- Layer 3: deception seen through
  enacts : Bool  -- Layer 4: asmimāna removed, structure intact
  deriving DecidableEq, Repr

def seerWellformed (s : SeerDoer) : Bool := !(s.enacts && !s.sees)

def allSeerDoer : List SeerDoer :=
  [true, false].flatMap fun a => [true, false].map fun b => ⟨a, b⟩

def wellformedSeers : List SeerDoer := allSeerDoer.filter seerWellformed

/-- R-REC7b: Know ⟹̸ Enact — seeing without enacting exists (stream-enterer). -/
theorem sees_without_enacting :
    (wellformedSeers.filter fun s => s.sees && !s.enacts).length > 0 := by
  decide

/-- Enacting without seeing is ill-formed (no removal without seeing). -/
theorem no_enacting_without_seeing :
    (wellformedSeers.filter fun s => s.enacts && !s.sees).length = 0 := by
  decide

end FormalRecognition

-- blind/Tractatus.lean (from recognition/Tractatus.lean)

namespace FormalRecognition

set_option maxRecDepth 100000
set_option maxHeartbeats 2000000

/-- Support: which support-sets serve which contexts (two contexts).
    The file's theorem ∀D∃Σ ⊭ ∃S∀D, finite witness: each context has
    support, but NO support serves both (disjoint support). -/
def supports : Fin 2 → Fin 2 → Bool
  | 0, 0 => true  | 0, _ => false
  | 1, 1 => true  | 1, _ => false

/-- Every context has a support-set. -/
def contexts : List (Fin 2) := [0, 1]

theorem every_context_supported :
    (contexts.filter (fun c => contexts.any (fun s => supports c s))).length = 2 := by
  decide

/-- No universal support: no single S serves all contexts. -/
theorem no_universal_support :
    ¬∃ s : Fin 2, supports 0 s && supports 1 s = true := by decide

/-- Observer O(o): discriminates, preserves-uses, integrates. -/
structure Observer where
  disc : Bool  -- discriminates x,y in context c
  pres : Bool  -- preserves and uses the distinction
  integ : Bool -- integrates into model/action
  deriving DecidableEq, Repr

def isObserver (o : Observer) : Bool := o.disc && o.pres && o.integ

/-- Rec_1: knows distinction + relative dependence.
    Rec_2: + knows its own dependence on registering.
    FullRec: + no reification. Hierarchy: each requires the last. -/
structure RecLevel where
  r1 : Bool  -- Rec_1: Know_o[D] ∧ Know_o[RelDep]
  r2 : Bool  -- Rec_2: + Know_o[Dep(o, Reg)]
  fr : Bool  -- FullRec: + ¬Reif_o(o)
  deriving DecidableEq, Repr

def recWellformed (r : RecLevel) : Bool :=
  !(r.r2 && !r.r1) && !(r.fr && !r.r2)

def allRecLevels : List RecLevel :=
  [true, false].flatMap fun a => [true, false].flatMap fun b =>
    [true, false].map fun c => ⟨a, b, c⟩

def wellformedRecs : List RecLevel := allRecLevels.filter recWellformed

/-- Rec_1 without Rec_2 exists (knowing without self-inclusion). -/
theorem rec1_without_rec2 :
    (wellformedRecs.filter fun r => r.r1 && !r.r2).length > 0 := by decide

/-- R: Rec_2 ⇏ FullRec (the file's stated theorem — knowing dependence
    is not ceasing to reify). -/
theorem rec2_without_fullrec :
    (wellformedRecs.filter fun r => r.r2 && !r.fr).length > 0 := by decide

/-- Layers L1–L4: each requires the previous (inferential → structural →
    recursive self-inclusion → enacted de-reification). -/
structure Layers where
  l1 : Bool
  l2 : Bool
  l3 : Bool
  l4 : Bool
  deriving DecidableEq, Repr

def layersWellformed (l : Layers) : Bool :=
  !(l.l2 && !l.l1) && !(l.l3 && !l.l2) && !(l.l4 && !l.l3)

/-- Finite shadow only: two values cannot cover Fin 4. -/
theorem finite_missing : ∀ a b : Fin 4, ∃ y : Fin 4, y ≠ a ∧ y ≠ b := by decide

theorem fin_two (x : Fin 2) : x = 0 ∨ x = 1 := by
  have h : ∀ x : Fin 2, x = 0 ∨ x = 1 := by decide
  exact h x

/-- Every map from Fin 2 to Fin 4 misses a state. This does not establish a
    general no-self-model theorem or the philosophical T13 without further
    justified assumptions connecting that claim to these finite types. -/
theorem no_total_self_model :
    ∀ f : Fin 2 → Fin 4, ∃ y : Fin 4, ∀ x : Fin 2, f x ≠ y := by
  intro f
  obtain ⟨y, ha, hb⟩ := finite_missing (f 0) (f 1)
  refine ⟨y, ?_⟩
  intro x
  rcases fin_two x with hx | hx
  · simpa [hx] using Ne.symm ha
  · simpa [hx] using Ne.symm hb

/-- S/i/0/1 combinatorial shadow (H: S itself untouched): 0/1's entire
    content is relational — 0 means not-1, 1 means not-0. -/
theorem bit_content_relational : (false != true) && (!(false) == true) = true := by
  decide

/-- The path fork (it-from-bit): nodes manifest(0) difference(1)
    bounded(2) selfmodel(3) suffering(4) recognition(5).
    Edges: the chain plus appropriation 3→4 and reflexive 3→5. -/
def edge : Fin 6 → Fin 6 → Bool
  | 0, 1 => true  | 1, 2 => true  | 2, 3 => true
  | 3, 4 => true  | 3, 5 => true
  | _, _ => false

def reach1 (a b : Fin 6) : Bool := (a == b) || edge a b

/-- Bounded reachability: paths up to length 5 (diameter of the graph). -/
def reach : Nat → Fin 6 → Fin 6 → Bool
  | 0, a, b => (a == b)
  | n+1, a, b =>
    (a == b) || edge a b ||
    ([0, 1, 2, 3, 4, 5] : List (Fin 6)).any fun m => edge a m && reach n m b

/-- Both terminals reachable from manifestation (the fork is real). -/
theorem suffering_reachable : reach 5 0 4 = true := by decide

theorem recognition_reachable : reach 5 0 5 = true := by decide

/-- Without the reflexive edge, recognition is unreachable — the edge
    (not the chain) is load-bearing. -/
def edgeNoRefl : Fin 6 → Fin 6 → Bool
  | 0, 1 => true  | 1, 2 => true  | 2, 3 => true
  | 3, 4 => true
  | _, _ => false

def reachNR : Nat → Fin 6 → Fin 6 → Bool
  | 0, a, b => (a == b)
  | n+1, a, b =>
    (a == b) || edgeNoRefl a b ||
    ([0, 1, 2, 3, 4, 5] : List (Fin 6)).any fun m =>
      edgeNoRefl a m && reachNR n m b

theorem recognition_needs_reflexive_edge : reachNR 5 0 5 = false := by decide

end FormalRecognition

-- blind/Coords.lean (from recognition/Coords.lean)

namespace FormalRecognition

set_option maxRecDepth 100000
set_option maxHeartbeats 2000000

/-- The five contraction coordinates: K epistemic, A action-space,
    V value-space, T temporal horizon, C causal position. -/
inductive Coord where
  | kn | ac | va | ti | ca
  deriving DecidableEq, Repr

/-- The five kañcukas, logicframework order. -/
inductive Kancuka5 where
  | vidya | kala | raga | kalaTime | niyati
  deriving DecidableEq, Repr

open Coord Kancuka5

/-- Each kañcuka restricts exactly one coordinate (doc table). -/
def restrictsTo : Kancuka5 → Coord
  | .vidya    => .kn
  | .kala     => .ac
  | .raga     => .va
  | .kalaTime => .ti
  | .niyati   => .ca

def allK5 : List Kancuka5 := [.vidya, .kala, .raga, .kalaTime, .niyati]

/-- The mapping covers all five coordinates exactly once (bijective:
    no overlap, no gap — contraction is total and non-redundant).
    eraseDups: a colliding map covers fewer. -/
theorem coords_covered_once :
    ((allK5.map restrictsTo).eraseDups).length = 5 := by decide

/-- Agent: perspective exists only with restriction. -/
structure Agent where
  persp : Bool  -- particular perspective exists
  restr : Bool  -- restriction (contraction) present
  deriving DecidableEq, Repr

def agentWellformed (a : Agent) : Bool := !(a.persp && !a.restr)

def allAgents : List Agent :=
  [true, false].flatMap fun p => [true, false].map fun r => ⟨p, r⟩

/-- Witness: restricted perspective exists (the finite knower). -/
theorem restricted_perspective_exists :
    (allAgents.filter fun a => a.persp && a.restr).length > 0 := by decide

/-- The admitted states contain no unrestricted perspective. This follows
    from agentWellformed and does not establish the philosophical premise. -/
theorem no_unrestricted_perspective :
    ((allAgents.filter agentWellformed).filter fun a => a.persp && !a.restr).length = 0 := by decide

/-- One of the four raw Boolean combinations is excluded by the premise. -/
theorem one_raw_invalid_combination :
    (allAgents.filter fun a => !agentWellformed a).length = 1 := by decide

end FormalRecognition

-- blind/KancukaCorr.lean (from recognition/KancukaCorr.lean)

namespace FormalRecognition

/-- The five contraction coordinates (Coords.lean order). -/
inductive CorrCoord where
  | kn | ac | va | ti | ca
  deriving DecidableEq, Repr

/-- Decode-side felt markers (experience language, from the decode table). -/
inductive Felt where
  | pull         -- lobha-side want ("craving for the state")
  | stall        -- thina-side blockage ("i feel blocked")
  | churn        -- uddhacca-side agitation ("scrambling")
  | doubtStammer -- vicikiccha-side (have-it vs feel-it)
  | push         -- dosa-side (unknown structural signature)
  | urgency      -- hurry-pressure (kāla candidate, unestablished)
  | placedness   -- here-agency (niyati candidate, unestablished)
  deriving DecidableEq, Repr

open CorrCoord Felt

/-- The correspondence: partial by design. `none` = unknown, not absent. -/
def corr : Felt → Option CorrCoord
  | .pull         => some .va   -- rāga presents as pull (day-7 §§1-2, 4)
  | .stall        => some .ac   -- kalā presents as stall (day-7 #18)
  | .churn        => some .ac   -- R: agitation rides agency-loss (thin — flagged)
  | .doubtStammer => some .kn   -- R: conflicted knowing (vidyā-side, day-7 #20)
  | .push         => none
  | .urgency      => none
  | .placedness   => none

def allFelt : List Felt :=
  [.pull, .stall, .churn, .doubtStammer, .push, .urgency, .placedness]

/-- Firm row 1: pull maps to the value coordinate (rāga). -/
theorem corr_pull_raga : corr .pull = some .va := by decide

/-- Firm row 2: stall maps to the action coordinate (kalā). -/
theorem corr_stall_kala : corr .stall = some .ac := by decide

/-- R-tier row: doubt-stammer maps to the epistemic coordinate (vidyā). -/
theorem corr_doubt_vidya : corr .doubtStammer = some .kn := by decide

/-- Unknowns are explicit: three markers map to nothing. -/
theorem unknowns_explicit :
    corr .push = none ∧ corr .urgency = none ∧ corr .placedness = none := by
  decide

/-- Coverage is PARTIAL: 3 of 5 coordinates hit (ti, ca unmapped).
    The full-coverage prediction (F-CORR) is therefore NOT established by
    this table — it lives or dies on T-C1 + future decodes. -/
theorem coverage_partial :
    ((allFelt.filterMap corr).eraseDups.length = 3) := by decide

end FormalRecognition

-- blind/Grace.lean (from recognition/Grace.lean)

namespace FormalRecognition

/-- The minimal transition state: readiness (the conditions) + grace. -/
structure GraceState where
  ready : Bool  -- surrender/resolve/readiness present
  grace : Bool  -- the unconditioned step (śaktipāta-side, exogenous)
  deriving DecidableEq, Repr

/-- Flip iff BOTH hold. Neither alone suffices — that is the whole claim. -/
def gflip (m : GraceState) : Bool := m.ready && m.grace

def allGraceStates : List GraceState :=
  [true, false].flatMap fun r => [true, false].map fun g => ⟨r, g⟩

/-- Readiness alone never flips (the day-7 #26 structure). -/
theorem readiness_insufficient :
    (allGraceStates.filter fun m => m.ready && !m.grace && gflip m).length = 0 := by
  decide

/-- Grace alone never flips an unreadied state (no bypass). -/
theorem grace_insufficient_alone :
    (allGraceStates.filter fun m => !m.ready && m.grace && gflip m).length = 0 := by
  decide

/-- The biconditional, over all 4 states: flip ↔ ready ∧ grace. -/
theorem flip_iff_ready_and_grace :
    (allGraceStates.filter fun m => gflip m == (m.ready && m.grace)).length = 4 := by
  decide

/-- Both witnesses exist: a ready-but-unflipped state and a graced-but-unflipped one. -/
theorem both_gaps_exist :
    (allGraceStates.filter fun m => m.ready && !gflip m).length > 0 ∧
    (allGraceStates.filter fun m => m.grace && !gflip m).length > 0 := by
  decide

end FormalRecognition

-- blind/Upaya.lean (from recognition/Upaya.lean)

namespace FormalRecognition

/-- The minimal means-state. -/
structure MeansState where
  ready : Bool  -- the practitioner is ripe for the flip
  pure  : Bool  -- vikalpa purified (śākta precondition)
  deriving DecidableEq, Repr

def allMeansStates : List MeansState :=
  [true, false].flatMap fun r => [true, false].map fun p => ⟨r, p⟩

/-- Śāmbhava: immediate — flips wherever ready, no flag, no repetition. -/
def sambhavaReach (s : MeansState) : Bool := s.ready

/-- Śākta: needs readiness AND the purified-vikalpa flag. -/
def saktaReach (s : MeansState) : Bool := s.ready && s.pure

/-- Āṇava: needs readiness AND repeated application (n ≥ 2). -/
def anavaReach (s : MeansState) (n : Nat) : Bool := s.ready && 2 ≤ n

/-- Śāmbhava reaches from every ready state. -/
theorem sambhava_immediate :
    (allMeansStates.filter fun s => s.ready && sambhavaReach s).length = 2 := by
  decide

/-- Śākta is strictly narrower: a ready-but-impure state it cannot reach. -/
theorem sakta_needs_purity :
    (allMeansStates.filter fun s =>
      s.ready && !s.pure && sambhavaReach s && !saktaReach s).length > 0 := by
  decide

/-- Āṇava is strictly slower: one application never suffices, even ready. -/
theorem anava_needs_repetition :
    (allMeansStates.filter fun s =>
      s.ready && sambhavaReach s && !anavaReach s 1).length = 2 := by
  decide

/-- Two applications suffice wherever readiness holds. -/
theorem anava_two_suffice :
    (allMeansStates.filter fun s =>
      s.ready && anavaReach s 2).length = 2 := by
  decide

/-- Ordering (recorded as found): whatever āṇava reaches in 2, śāmbhava reaches. -/
theorem anava_within_sambhava :
    (allMeansStates.filter fun s =>
      anavaReach s 2 && !sambhavaReach s).length = 0 := by
  decide

/-- And śākta likewise (purity implies nothing beyond readiness for the immediate). -/
theorem sakta_within_sambhava :
    (allMeansStates.filter fun s =>
      saktaReach s && !sambhavaReach s).length = 0 := by
  decide

end FormalRecognition
