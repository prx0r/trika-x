/-
  Formal Trika — P-SUTRA: the 14 Māheśvara-sūtras as interval mechanics.

  T-tier ground (CANDIDATE-EDITION): standard 14-sūtra sequence; pin
  pending GRETIL/MIRI Aṣṭādhyāyī verification before publication use.
  The rung checks INTERNAL consistency only (marker disjointness,
  interval regeneration) — edition-independent.

  What this file IS: 43 sounds + 14 marker tokens in sūtra order;
  pratyāhāra = sounds strictly between first phoneme and marker;
  exemplar regenerations (aC vowels, haL consonants) + exclusion.
  What it is NOT: Pāṇinian semantics, word derivation, or Trika
  doctrine. Study backbone: pratyāhāra classes are study sets.
  Finite model; `decide` inside scope only.
-/
namespace FormalTrika

/-- Symbols: speech sounds vs meta-markers (anubandhas). -/
inductive Sym where
  | sound (name : String)
  | mark (name : String)
  deriving DecidableEq, Repr

/-- The 14 sūtras concatenated (sounds + anubandha markers, in order).
    s1 a-i-u-Ṇ · s2 ṛ-ḷ-K · s3 e-o-Ṅ · s4 ai-au-C · s5 ha-ya-va-ra-Ṭ ·
    s6 la-Ṇ · s7 ña-ma-ṅa-ṇa-na-M · s8 jha-bha-Ñ · s9 gha-ḍha-dha-Ṣ ·
    s10 ja-ba-ga-ḍa-da-Ś · s11 kha-pha-cha-ṭha-tha-ca-ṭa-ta-V ·
    s12 ka-pa-Y · s13 śa-ṣa-sa-R · s14 ha-L. -/
def sivasutra : List Sym :=
  [.sound "a", .sound "i", .sound "u", .mark "Ṇ",
   .sound "ṛ", .sound "ḷ", .mark "K",
   .sound "e", .sound "o", .mark "Ṅ",
   .sound "ai", .sound "au", .mark "C",
   .sound "ha", .sound "ya", .sound "va", .sound "ra", .mark "Ṭ",
   .sound "la", .mark "Ṇ",
   .sound "ña", .sound "ma", .sound "ṅa", .sound "ṇa", .sound "na", .mark "M",
   .sound "jha", .sound "bha", .mark "Ñ",
   .sound "gha", .sound "ḍha", .sound "dha", .mark "Ṣ",
   .sound "ja", .sound "ba", .sound "ga", .sound "ḍa", .sound "da", .mark "Ś",
   .sound "kha", .sound "pha", .sound "cha", .sound "ṭha", .sound "tha",
   .sound "ca", .sound "ṭa", .sound "ta", .mark "V",
   .sound "ka", .sound "pa", .mark "Y",
   .sound "śa", .sound "ṣa", .sound "sa", .mark "R",
   .sound "ha", .mark "L"]

/-- Sounds from first phoneme `a` up to (excluding) marker `m`
    (pratyāhāra mechanics: first sound included, markers terminate and
    are never included). -/
def pratyaahara (a m : String) : List String :=
  let rest := (sivasutra.dropWhile fun s => match s with
    | .sound n => n != a
    | .mark _ => true)
  let inside := rest.takeWhile fun s => match s with
    | .sound _ => true
    | .mark n => n != m
  (inside.filterMap fun s => match s with | .sound n => some n | .mark _ => none)

/-- All pratyāhāras formed by every (first-sound, marker) pair. -/
def allPratyaaharas : List (String × String × List String) :=
  (sivasutra.filterMap fun s => match s with | .sound n => some n | .mark _ => none).flatMap fun a =>
    ["Ṇ", "K", "Ṅ", "C", "Ṭ", "M", "Ñ", "Ṣ", "Ś", "V", "Y", "R", "L"].map fun m =>
      (a, m, pratyaahara a m)

/-- P-SUT1: a..C = exactly the 9 vowels. -/
theorem ac_vowels :
    pratyaahara "a" "C" = ["a", "i", "u", "ṛ", "ḷ", "e", "o", "ai", "au"] := by decide

/-- P-SUT2: ha..L minus markers = 34 consonants. -/
theorem hal_consonants :
    (pratyaahara "ha" "L").length = 34 := by decide

/- Deep enumeration below needs raised maxRecDepth for kernel
   reduction; still `decide`, no axioms beyond the standard three. -/
set_option maxRecDepth 100000

/-- P-SUT3: no marker belongs to any pratyāhāra. -/
theorem markers_excluded :
    (allPratyaaharas.flatMap fun p => p.2.2.filter fun n =>
      ["Ṇ", "K", "Ṅ", "C", "Ṭ", "M", "Ñ", "Ṣ", "Ś", "V", "Y", "R", "L"].contains n).length = 0 := by decide

/-- P-SUT4a: 43 sounds in the inventory. -/
theorem inventory_43 :
    ((sivasutra.filter fun s => match s with | .sound _ => true | .mark _ => false)).length = 43 := by decide

/-- P-SUT4b: 13 distinct marker kinds (Ṇ twice). -/
theorem markers_13 :
    (((sivasutra.filterMap fun s => match s with | .mark n => some n | .sound _ => none)).eraseDups).length = 13 := by decide

end FormalTrika
