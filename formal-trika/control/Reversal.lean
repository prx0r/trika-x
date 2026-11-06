/-
  Formal Trika — P-REV: two order-reversal claims, checked (comparison pilot).

  Source (link-first, © ALL RIGHTS RESERVED — no copying): Pradīpaka,
  "Tattva-s & Sanskrit" p.504 — kañcuka semivowels run va,la,ra,ya
  against alphabet ya,ra,la,va; tattvas 12–36 run ma..ka against
  alphabet ka..ma. Practitioner register: COMPARISON CONTROL, never
  authority. Alphabet order below is the public-domain varṇamālā
  (consonant span), not copied expression.

  What this file IS: order arithmetic (`List.reverse` checks) + a twin
  that must refuse on a swapped pair.
  What it is NOT: doctrine, entailment, or a second key for OUR Tattva
  (same root tradition). Finite lists; `decide` inside scope only.
-/
namespace FormalTrika

/-- Standard consonant order ka..ha (varṇamālā, public domain). -/
def alphabetC : List String :=
  ["ka", "kha", "ga", "gha", "ṅa", "ca", "cha", "ja", "jha", "ña",
   "ṭa", "ṭha", "ḍa", "ḍha", "ṇa", "ta", "tha", "da", "dha", "na",
   "pa", "pha", "ba", "bha", "ma", "ya", "ra", "la", "va",
   "śa", "ṣa", "sa", "ha"]

/-- The page's kañcuka semivowel order (factual row, URL on record). -/
def semiHis : List String := ["va", "la", "ra", "ya"]

/-- The page's tattva 12–36 letter order (factual row, URL on record). -/
def spanHis : List String :=
  ["ma", "bha", "ba", "pha", "pa", "na", "dha", "da", "tha", "ta",
   "ṇa", "ḍha", "ḍa", "ṭha", "ṭa", "ña", "jha", "ja", "cha", "ca",
   "ṅa", "gha", "ga", "kha", "ka"]

/-- P-REV1: semivowel order is exactly the alphabet's reversed. -/
theorem semi_reversed :
    semiHis = ["ya", "ra", "la", "va"].reverse := by decide

/-- P-REV2: the 25-letter span is exactly alphabet ka..ma reversed. -/
theorem span_reversed :
    spanHis = ((alphabetC.dropWhile fun s => s != "ka").takeWhile fun s => s != "ya").reverse := by decide

end FormalTrika
