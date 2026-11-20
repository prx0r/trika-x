/-
  Formal Trika — AUROBINDO-NOTATION: the type-level skeleton of the notation
  proposed in M. Alan Kazlev & Claude, "Contraction and Descent: A Formal
  Notation for Aurobindonian and Kashmir Shaivite Metaphysics" (September 2026).

  KIND: SPEC / DATA. This file declares the notation's logical types and the
  paper's structural distinctions. It does NOT model the traditions, derive
  any traditional count, or assert that the paper's proposed homologies hold.

  What this file IS:
    - the type inventory (ground, aspects, contraction state, grades, planes,
      vehicles, movements, nondualities, limits, composites);
    - two definitional facts the paper states outright (five kañcukas are a
      component of the contraction state; density opens at the Overmind, i.e.
      native density is zero for ℋ0–ℋ3 and positive from ℋ4).
  What it is NOT:
    - a proof of saṅkoca, of the independence of ℋ and 𝒫, or of any
      Aurobindonian or Śaiva claim;
    - a checked build. STATUS: BUILT — verified locally on Lean 4.34.1
      (leanprover/lean4:v4.34.1) on 2026-11-20, exit 0, warnings as errors.
      CI compiles every non-Broken frontier file (formal-checks.yml,
      "Frontier models"). Re-run `lean formal-trika/frontier/AurobindoNotation.lean`
      before citing compiler status from a different toolchain.
  Provenance: the paper's own §9/§11 states the homologies are tentative and
  that aggregation F, centring persistence, density onset, and composition are
  open. Those opens are preserved here rather than closed.

  Naming: `ℋ` (hypostatic series) and `𝒫` (density series) are kept as
  `HGrade` / `DensityPlane`; `σ` (contraction state) as `ContractionState`.
  The scalar magnitude is an argument of `Notation`, never a primitive fact.
-/
namespace FormalTrika

/-! ## §2 Ground: two primitive glyphs and two inseparable aspects -/

/-- The two top primitives are *not* values: ◌ (Unmanifest) and ◯ (nondual
    ground). They are left as parameters of the notation's carrier types;
    assigning them a Lean value would contradict §2.1. -/
structure GroundAspects where
  /-- φ, luminosity (prakāśa). Ordinal stand-in, per §1.2. -/
  phi : Nat
  /-- ν, reflexivity (vimarśa). Inseparable from φ; never a second entity. -/
  nu : Nat
  deriving DecidableEq, Repr

/-- §2.3 — three logically independent senses of "nonduality". -/
inductive Nonduality where
  | henological      -- the ground has no second (a claim about the ground)
  | immanent         -- the ground is not other than what it manifests
  | phenomenological -- knower and known not separate in a locus's state
  deriving DecidableEq, Repr

/-! ## §3 Contraction: three malas + five kañcukas + karman -/

/-- §3.2 — the three impurities. -/
inductive Mala where
  | anava   -- root sense of being a finite part
  | mayiya  -- differentiated perception (through māyā + kañcukas)
  | karma   -- residue of action
  deriving DecidableEq, Repr

/-- §3.2 — the five sheaths. `kalaTime` avoids clashing with karman's `karma`. -/
inductive Kancuka where
  | kala      -- kalā: limits omnipotence → limited agency
  | vidya     -- vidyā: limits omniscience → limited knowing
  | raga      -- rāga: limits fullness → desire/attachment
  | kalaTime  -- kāla: limits eternity → time
  | niyati    -- niyati: limits all-pervasiveness → spatial/causal restriction
  deriving DecidableEq, Repr

/-- §3.2 — the contraction state σᵢ, component by component. The paper's
    vector is (σāṇava, m₁…m₅, κ); each entry is an ordinal degree, not a
    measured quantity (§1.2). -/
structure ContractionState where
  anava     : Nat
  kala      : Nat
  vidya     : Nat
  raga      : Nat
  kalaTime  : Nat
  niyati    : Nat
  karma     : Nat
  deriving DecidableEq, Repr

/-- All seven components at their zero degree. `σ = 0` in the paper's notation
    means this vector is zero (no contraction), not that a scalar vanished. -/
def ContractionState.zero : ContractionState :=
  ⟨0, 0, 0, 0, 0, 0, 0⟩

/-- §3.2 — the five kañcukas are exactly the m₁…m₅ components. This is a
    roster check, not a derivation of the count from Śaiva sources. -/
def kancukaCount : Nat :=
  [Kancuka.kala, Kancuka.vidya, Kancuka.raga, Kancuka.kalaTime, Kancuka.niyati].length

theorem kancuka_count_is_five : kancukaCount = 5 := by decide

/-! ## §4 Centring: individuation without contraction -/

/-- §4.1 — the paper's two operators. `Ground`, `Locus`, their elements, and
    the aggregation `magnitude` are parameters: the notation specifies their
    *types and relations*, not their metaphysics (§1.1, §11). -/
structure Notation (Ground Locus : Type) where
  /-- 𝒮: contraction, αᵢ = 𝒮(◯ᵢ; σᵢ). -/
  contract : Ground → ContractionState → Locus
  /-- 𝒞ᵢ: centring, ◯ᵢ = 𝒞ᵢ(◯). Distinct from 𝒮 (§4.1). -/
  centre : Ground → Locus → Ground
  /-- F: the open aggregation of σᵢ to a scalar magnitude (§3.1, §11). -/
  magnitude : ContractionState → Nat

/-! ## §5 Two vertical series: hypostatic ℋ and density 𝒫 -/

/-- §5.2 — hypostatic grades. ℋ0 is the Unmanifest, ℋ1 the One, ℋ2 Saccidānanda,
    ℋ3 Supermind, ℋ4 Overmind, ℋ5 the Daimonic, ℋ6 Nature. -/
inductive HGrade where
  | h0 | h1 | h2 | h3 | h4 | h5 | h6
  deriving DecidableEq, Repr

/-- §5.4 — native density is zero for ℋ0–ℋ3; the Overmind (ℋ4) is the hinge at
    which density opens. `true` = native density is positive. -/
def nativeDensity : HGrade → Bool
  | .h0 | .h1 | .h2 | .h3 => false
  | .h4 | .h5 | .h6 => true

/-- The paper's explicit claim, as a finite roster check. -/
theorem density_opens_at_overmind :
    ([HGrade.h0, HGrade.h1, HGrade.h2, HGrade.h3, HGrade.h4,
      HGrade.h5, HGrade.h6].filter nativeDensity).length = 3 := by decide

/-- §5.3 — density planes, ordered by decreasing density ρ. -/
inductive DensityPlane where
  | noetic      -- intuition / illumined / higher mind
  | pathic      -- higher emotional being
  | orectic     -- the vital (will, drive, desire)
  | physical    -- eidolic, zoetic, hylic
  deriving DecidableEq, Repr

/-- §5.3, §5.7 — vehicles K_{i,ℓ}. The Hylic vehicle is the one death removes. -/
inductive Vehicle where
  | eidolic | zoetic | hylic
  deriving DecidableEq, Repr

/-- §5.6 — three lower limits that coincide in reference at Matter, not meaning. -/
inductive LowerLimit where
  | hyle         -- end of procession
  | hylic        -- extreme of density
  | inconscient  -- extreme of contraction (derived, not primitive)
  deriving DecidableEq, Repr

/-! ## §7 Five movements (not two pairs of opposites) -/

/-- §7.2 — procession, densification, involution, evolution, liberation. -/
inductive Movement where
  | procession | densification | involution | evolution | liberation
  deriving DecidableEq, Repr

def movementCount : Nat :=
  [Movement.procession, Movement.densification, Movement.involution,
   Movement.evolution, Movement.liberation].length

theorem five_movements : movementCount = 5 := by decide

/-! ## §9 Composite loci: ordinal comparison of whole vs parts -/

/-- The paper's four composite classes, distinguished only by how ν of the
    whole compares with ν of its parts (§9). -/
structure Composite where
  wholeNu : Nat
  partsNu : Nat
  deriving DecidableEq, Repr

/-- Egregore: the whole is *less* reflexively aware than its parts. -/
def Composite.isEgregore (c : Composite) : Bool := c.wholeNu < c.partsNu

/-- Organism / symnoon: the whole exceeds its parts. -/
def Composite.isSymnoon (c : Composite) : Bool := c.partsNu < c.wholeNu

end FormalTrika
