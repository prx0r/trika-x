/- MUTANT: māyā is incorrectly counted as a pure tattva. -/
/-
  Candidate named inventory accompanying Tattva.lean's grouped arithmetic.
  It makes the categories explicit so a reviewer can inspect them; the list
  is curated data, not a derivation from Sanskrit. Tantrasāra 7.1, 7.9–21,
  8.16–17 and 8.73–89 are pointers for a passage-by-passage review; they are
  not a single verified critical-edition list of these 36 names.
  See SANSKRIT-FOUNDATION-REVIEW-2026-11-06.md.
-/
namespace FormalTattvaInventory

inductive Tattva where
  | siva | sakti | sadasiva | isvara | suddhavidya
  | maya | kalaPower | asuddhavidya | raga | kalaTime | niyati | purusa
  | prakrti | buddhi | ahamkara | manas
  | srotra | tvac | caksus | rasana | ghrana
  | vak | pani | pada | payu | upastha
  | sabda | sparsa | rupa | rasa | gandha
  | akasa | vayu | tejas | ap | prthivi
  deriving DecidableEq, Repr

open Tattva

/-- Candidate enumeration, in a conventional descending order. -/
def inventory : List Tattva :=
  [.siva, .sakti, .sadasiva, .isvara, .suddhavidya,
   .maya, .kalaPower, .asuddhavidya, .raga, .kalaTime, .niyati, .purusa,
   .prakrti, .buddhi, .ahamkara, .manas,
   .srotra, .tvac, .caksus, .rasana, .ghrana,
   .vak, .pani, .pada, .payu, .upastha,
   .sabda, .sparsa, .rupa, .rasa, .gandha,
   .akasa, .vayu, .tejas, .ap, .prthivi]

def pureTattvas : List Tattva :=
  [.siva, .sakti, .sadasiva, .isvara, .maya]

def kancukas : List Tattva :=
  [.kalaPower, .asuddhavidya, .raga, .kalaTime, .niyati]

/-- Māyā plus the five, in the six-cover reckoning of Tantrasāra 8.55. -/
def mayaSix : List Tattva := .maya :: kancukas

/-- These checks are about the declared finite inventory. -/
theorem named_tattvas_36 : inventory.length = 36 := by decide

theorem named_tattvas_unique : inventory.eraseDups.length = inventory.length := by decide

theorem named_tattvas_exhaustive : ∀ t : Tattva, t ∈ inventory := by
  intro t
  cases t <;> decide

theorem pure_count : pureTattvas.length = 5 := by decide

theorem kancuka_count : kancukas.length = 5 := by decide

theorem maya_six_count : mayaSix.length = 6 := by decide

theorem pure_excludes_maya : pureTattvas.contains .maya = false := by decide

theorem pure_and_kancukas_disjoint :
    pureTattvas.all (fun t => !kancukas.contains t) = true := by decide

end FormalTattvaInventory
