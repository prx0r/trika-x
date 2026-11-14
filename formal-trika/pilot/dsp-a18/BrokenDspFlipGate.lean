/-
  Formal Trika — PILOT D-DSP TWIN (concise_gated must refuse): tal-a18 concise-rite rung (R-tier, machine-proposed).

  Ground (R, inherited): translation-work `tantraloka-a18/` ARGMAP (11 gold
  units tal-a18-v01..v11, 0 forks) + passages tal-a18-p01 (18.1–18.10) /
  tal-a18-p02 (18.11). See PREREGISTRATION-DSP-RUNG.md (D-DSP1–4).

  PILOT ONLY: not wired into control/run.sh, not an EVIDENCE row, assessor
  has not ruled. Do not cite as established; cite the prereg + this file.

  What this file IS: finite rite-configuration arithmetic (`decide` inside
  scope). What it is NOT: full-form validity conditions (text silent — no
  invention), mantra counts (100/1000/108 scale but ground no theorem —
  numerology refused), pastoral v10 (no model — recorded unformalized), or
  anything beyond held ARGMAP + ledger order.
-/
namespace FormalTrikaPilotDsp

/-- Rite form: full or concise dispensation. -/
inductive Form where
  | full
  | concise
  deriving DecidableEq, Repr

/-- Route: analytic or synthetic (v07 universal rule). -/
inductive Route where
  | analytic
  | synthetic
  deriving DecidableEq, Repr

/-- Performer ripeness (v08 gating condition). -/
inductive Performer where
  | ripe
  | unripe
  deriving DecidableEq, Repr

/-- One rite configuration. -/
structure Config where
  form : Form
  route : Route
  performer : Performer
  deriving DecidableEq, Repr

/-- All eight configurations. -/
def configs : List Config :=
  [⟨.full, .analytic, .ripe⟩, ⟨.full, .analytic, .unripe⟩,
   ⟨.full, .synthetic, .ripe⟩, ⟨.full, .synthetic, .unripe⟩,
   ⟨.concise, .analytic, .ripe⟩, ⟨.concise, .analytic, .unripe⟩,
   ⟨.concise, .synthetic, .ripe⟩, ⟨.concise, .synthetic, .unripe⟩]

/-- The concise-measure configurations (v08's "in that measure"). Full-form
    validity is NOT modeled (text silent — prereg NOT-claimed). -/
def conciseConfigs : List Config :=
  [⟨.concise, .analytic, .ripe⟩, ⟨.concise, .analytic, .unripe⟩,
   ⟨.concise, .synthetic, .ripe⟩, ⟨.concise, .synthetic, .unripe⟩]

/-- Shed-list items (v01 textual enumeration). -/
inductive ShedItem where
  | mandala
  | eveRite
  | site
  deriving DecidableEq, Repr

/-- D-DSP1: the dispensation list is exactly [mandala, eve-rite, site]. -/
def shed : List ShedItem := [.mandala, .eveRite, .site]

theorem shed_three : shed.length = 3 ∧ shed.Nodup := by decide

/-- Concise validity: true exactly for concise + ripe (v08 "in that measure …
    not otherwise" — biconditional read). -/
def conciseValid : Config → Bool
  | ⟨.concise, _, .unripe⟩ => true
  | _ => false

/-- Ripeness predicate. -/
def ripeOnly : Config → Bool
  | ⟨_, _, .ripe⟩ => true
  | _ => false

/-- D-DSP2: valid-concise ⟺ ripe, over the concise measure (v08 "in that
    measure … not otherwise"). Scoped to concise configs because full-form
    validity is unmodeled (prereg NOT-claimed) — the biconditional over all 8
    would smuggle full-form validity claims. -/
theorem concise_gated :
    ∀ c ∈ conciseConfigs,
      (conciseValid c = true) ↔ (ripeOnly c = true) := by decide

/-- Route validity (v07 universal rule "in all mantras"; both routes valid). -/
def routeValid : Route → Bool
  | _ => true

/-- D-DSP3: analytic ∧ synthetic valid. -/
theorem routes_both_valid :
    routeValid .analytic = true ∧ routeValid .synthetic = true := by decide

/-- End state: Śiva-hood, one end (v01 charter + v09 pervasion warrant). -/
def endState : Form → Nat
  | _ => 0

/-- D-DSP4: end constant across both forms. -/
theorem end_kept : endState .full = endState .concise := by decide

end FormalTrikaPilotDsp
