/-
  Formal Trika — N-NYASA: MUTANT: nadiphanta order replaced by shabdarashi (must fail order_chief ONLY).

  T-tier ground: TĀ-15 nyāsa complex (tal-a15-p12); MV 3.36–41 order
  (MIRI M00160, na→pha); matrika_body_map v2 + malini_order.json (both
  frozen; deitybody data). Design history: varga→limb RULES (7 general
  clauses) CANNOT be checked against a single per-phoneme table without
  circularity (rules partition what the table lists) — recorded, rules
  kept for downstream body pages, unchecked status labeled. What IS
  checked: totality of both maps, ka-varga uniformity as observed shape,
  order difference + multiset conservation, and cross-map divergence
  count (the duality, quantified).

  What this file IS: mapping inventories + order/multiset/divergence
  checks over two frozen keys. Feeds body pages when green.
  What it is NOT: nyāsa efficacy, siddhi/medical claims, mātṛ-future.
  Finite model; `decide` inside scope only.
-/
namespace FormalNyasa

/-- GENERAL RULES (unchecked by theorem — need a second key; kept for
    downstream use and documented as R): varga → limb. -/
inductive Varga where
  | vowel | ka | ca | taRetro | taDent | pa | semi | sibil
  deriving DecidableEq, Repr

def limb : Varga → String
  | .vowel => "head"
  | .ka => "right upper limb"
  | .ca => "left upper limb"
  | .taRetro => "right lower limb"
  | .taDent => "left lower limb"
  | .pa => "torso / trunk"
  | .semi => "deeper constituents"
  | .sibil => "deep constituents / generative"

def members : Varga → List String
  | .vowel => ["a", "ā", "i", "ī", "u", "ū", "ṛ", "ṝ", "ḷ", "ḹ",
               "e", "ai", "o", "au", "aṃ", "aḥ"]
  | .ka => ["ka", "kha", "ga", "gha", "ṅa"]
  | .ca => ["ca", "cha", "ja", "jha", "ña"]
  | .taRetro => ["ṭa", "ṭha", "ḍa", "ḍha", "ṇa"]
  | .taDent => ["ta", "tha", "da", "dha", "na"]
  | .pa => ["pa", "pha", "ba", "bha", "ma"]
  | .semi => ["ya", "ra", "la", "va"]
  | .sibil => ["śa", "ṣa", "sa", "ha", "kṣa"]

def allVargas : List Varga :=
  [.vowel, .ka, .ca, .taRetro, .taDent, .pa, .semi, .sibil]

/-- KEY DATA: mātṛkā locus per phoneme (body map v2). -/
def locusOf : String → String
  | "a" => "forehead" | "ā" => "mouth" | "i" => "right eye"
  | "ī" => "left eye" | "u" => "right ear" | "ū" => "left ear"
  | "ṛ" => "right nostril" | "ṝ" => "left nostril" | "ḷ" => "right cheek"
  | "ḹ" => "left cheek" | "e" => "lower teeth" | "ai" => "upper teeth"
  | "o" => "lower lip" | "au" => "upper lip" | "aṃ" => "crown (śikhā)"
  | "aḥ" => "tongue"
  | "ka" => "right shoulder" | "kha" => "right arm" | "ga" => "right hand"
  | "gha" => "right fingers" | "ṅa" => "right nails"
  | "ca" => "left shoulder" | "cha" => "left arm" | "ja" => "left hand"
  | "jha" => "left fingers" | "ña" => "left nails"
  | "ṭa" => "right hip" | "ṭha" => "right thigh" | "ḍa" => "right knee"
  | "ḍha" => "right shank" | "ṇa" => "right toes"
  | "ta" => "left hip" | "tha" => "left thigh" | "da" => "left knee"
  | "dha" => "left shank" | "na" => "left toes"
  | "pa" => "right side" | "pha" => "left side" | "ba" => "back"
  | "bha" => "belly" | "ma" => "heart"
  | "ya" => "skin" | "ra" => "blood" | "la" => "flesh" | "va" => "sūtra (sinews)"
  | "śa" => "bone" | "ṣa" => "marrow" | "sa" => "śukra / generative fluid"
  | "ha" => "prāṇa" | "kṣa" => "generative organ"
  | _ => "UNPLACED"

/-- KEY DATA: Mālinī locus per phoneme (malini_order.json body_map). -/
def mlocusOf : String → String
  | "na" => "śikhā" | "ṛ" => "śiromālā" | "ṝ" => "śiromālā"
  | "ḷ" => "śiromālā" | "ḹ" => "śiromālā" | "tha" => "mastaka"
  | "ca" => "right eye" | "dha" => "left eye" | "ī" => "nose"
  | "ṇa" => "ears" | "u" => "ear (right)" | "ū" => "ear (left)"
  | "ba" => "mouth (vaktra)" | "ka" => "teeth" | "kha" => "teeth"
  | "ga" => "teeth" | "gha" => "teeth" | "ṅa" => "teeth"
  | "i" => "tongue" | "a" => "speech (vāk)" | "va" => "throat"
  | "bha" => "right shoulder" | "ya" => "left shoulder" | "ḍa" => "right arm"
  | "ḍha" => "left arm" | "ṭha" => "hands" | "jha" => "fingers right hand"
  | "ña" => "fingers left hand" | "ja" => "trident prongs"
  | "ra" => "trident shaft" | "ṭa" => "skull (kapāla)" | "pa" => "heart"
  | "cha" => "right chest" | "la" => "left chest" | "ā" => "milk (kṣīra)"
  | "sa" => "jīva" | "aḥ" => "general prāṇa" | "ha" => "particular prāṇa"
  | "ṣa" => "belly" | "kṣa" => "navel" | "ma" => "buttocks / hips"
  | "śa" => "guhya" | "aṃ" => "right thigh" | "ta" => "left thigh"
  | "e" => "right knee" | "ai" => "left knee" | "o" => "right shank"
  | "au" => "left shank" | "da" => "right foot" | "pha" => "left foot"
  | _ => "UNPLACED"

def allPhonemes : List String := allVargas.flatMap members

/-- N-NYASA1: ka-varga Mālinī uniformity (observed shape, MODEL — the one
    varga sharing a single locus; mirrors the profile precedent). -/
theorem ka_uniform :
    ((members .ka).filter fun p => mlocusOf p == "teeth").length = 5 := by decide

/-- N-NYASA2a: mātṛkā totality — 50 distinct phonemes placed. -/
theorem matrika_total :
    ((allPhonemes.filter fun p => decide (locusOf p != "UNPLACED")).eraseDups).length = 50 := by decide

/-- N-NYASA2b: Mālinī totality — 50 distinct phonemes placed. -/
theorem malini_total :
    ((allPhonemes.filter fun p => decide (mlocusOf p != "UNPLACED")).eraseDups).length = 50 := by decide

/-- N-NYASA3: divergence count — phonemes whose two maps disagree
    (quantifies the duality; same-system identity would score 0). -/
theorem maps_diverge :
    ((allPhonemes.filter fun p => decide (locusOf p != mlocusOf p)).eraseDups).length = 50 := by decide

/-- KEY DATA: nādiphānta order (malini_order.json, MV 3.37–41). -/
def nadiphanta : List String :=
  ["a", "ā", "i", "ī", "u", "ū", "ṛ", "ṝ", "ḷ", "ḹ",
   "e", "ai", "o", "au", "aṃ", "aḥ",
   "ka", "kha", "ga", "gha", "ṅa", "ca", "cha", "ja", "jha", "ña",
   "ṭa", "ṭha", "ḍa", "ḍha", "ṇa", "ta", "tha", "da", "dha", "na",
   "pa", "pha", "ba", "bha", "ma", "ya", "ra", "la", "va",
   "śa", "ṣa", "sa", "ha", "kṣa"]

/-- Standard śabdarāśi order (public-domain varṇamālā). -/
def shabdarashi : List String :=
  ["a", "ā", "i", "ī", "u", "ū", "ṛ", "ṝ", "ḷ", "ḹ",
   "e", "ai", "o", "au", "aṃ", "aḥ",
   "ka", "kha", "ga", "gha", "ṅa", "ca", "cha", "ja", "jha", "ña",
   "ṭa", "ṭha", "ḍa", "ḍha", "ṇa", "ta", "tha", "da", "dha", "na",
   "pa", "pha", "ba", "bha", "ma", "ya", "ra", "la", "va",
   "śa", "ṣa", "sa", "ha", "kṣa"]

/-- N-NYASA4a: the orders differ (nādiphānta chief among mixings). -/
theorem order_chief : nadiphanta != shabdarashi := by decide

/-- N-NYASA4b: same multiset (conservation). -/
theorem multiset_kept :
    (nadiphanta.filter fun p => shabdarashi.contains p).length = 50
    && nadiphanta.length = 50 && shabdarashi.length = 50 := by decide

end FormalNyasa
