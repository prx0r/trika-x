/-
  Formal Recognition — tractatus/observer chain (R, H-marked where due).

  From `observer proofo` (D/S/O/R architecture, T1–T14, Rec_1/Rec_2/FullRec,
  4 layers, T13 cardinality bound), `siobserver` (S/i/0/1, 50 props — the
  combinatorial shadow only; S itself is H, never formalized here),
  `logicframework`/`logicframework2` (M→D→B→N→W→R, kañcuka coords, R-grades),
  `it from bit from siva` (the fork: appropriation→suffering vs
  reflexive-recognition→agency-without-ownership).

  What IS formalized: support-set locality (no global S — the file's own
  negative theorem), the Rec_1/Rec_2/FullRec hierarchy with its stated
  non-entailments, layer requirements, the cardinality bound, the path fork.
  What is NOT: S, phenomenality, universalization (marked H in-file too).
-/
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
