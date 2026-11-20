# Aurobindo notation — type-level intake

> **Status: SPEC / BUILT.** The Lean skeleton
> (`frontier/AurobindoNotation.lean`) was compiler-verified locally on Lean 4.34.1
> on 2026-11-20 (exit 0, warnings as errors), and CI compiles every non-Broken
> frontier file. This does not establish the paper's homologies.

## 1. Source

M. Alan Kazlev and Claude (Opus 5.5), **“Contraction and Descent: A Formal
Notation for Aurobindonian and Kashmir Shaivite Metaphysics”**, September 2026,
22 pp. Citation only — no local copy is committed.

This is a *proposal*, not a translation witness and not a Trika authority. Its own
§9 and §11 mark the cross-tradition homologies as tentative and leave aggregation,
centring persistence, density onset and composition open. Those opens are kept
open below.

## 2. What was taken over

The notation's rule is that **typeface signals logical type** (§1.2): primitives
are unique glyphs, scalars are lowercase Greek, structured states are bold
vectors, totals are Greek capitals, operators are script capitals. The Lean file
keeps the types and drops the typography:

| Paper | Lean (`FormalTrika`) | Note |
|---|---|---|
| ◌ Unmanifest / ◯ ground | parameters of `Notation (Ground Locus : Type)` | primitives get no value (§2.1) |
| `◯ = ⟨φ, ν⟩` | `GroundAspects` (`phi`, `nu`) | inseparable pair; never two entities |
| henological / immanent / phenomenological nonduality | `Nonduality` | three independent senses (§2.3) |
| `σᵢ = (σāṇava, m₁…m₅, κ)` | `ContractionState` (7 `Nat` fields) | ordinal degrees, not measurements |
| three malas | `Mala` | `anava`, `mayiya`, `karma` |
| five kañcukas | `Kancuka` | `kala`, `vidya`, `raga`, `kalaTime`, `niyati` |
| `αᵢ = 𝒮(◯ᵢ; σᵢ)`, `◯ᵢ = 𝒞ᵢ(◯)` | `Notation.contract`, `Notation.centre` | kept as parameters, not axioms |
| scalar magnitude `σᵢ = F(σᵢ)` | `Notation.magnitude` | `F` deliberately uninterpreted (§11) |
| hypostatic series ℋ₀…ℋ₆ | `HGrade` | Unmanifest → One → Saccidānanda → Supermind → Overmind → Daimonic → Nature |
| native density `ρnat` | `nativeDensity` | zero for ℋ₀–ℋ₃, positive from ℋ₄ |
| density series 𝒫 | `DensityPlane` | noetic / pathic / orectic / physical |
| vehicles `K_{i,ℓ}` | `Vehicle` | eidolic / zoetic / hylic |
| lower limits | `LowerLimit` | Hylē / Hylic / Inconscient — same referent, distinct meanings |
| five movements | `Movement` | procession, densification, involution, evolution, liberation |
| composite loci | `Composite` | ordinal whole-ν vs parts-ν only |

## 3. Two claims encoded as finite checks

1. **Five kañcukas** — `kancukaCount = 5` (`kancuka_count_is_five`). A roster
   check on the type inventory; it does not derive the count from Śaiva sources.
2. **Density opens at the Overmind** — `nativeDensity` is `false` for ℋ₀–ℋ₃ and
   `true` from ℋ₄, so exactly three grades carry native density
   (`density_opens_at_overmind`). This encodes the paper's §5.4 claim, *not* the
   Śaiva alternative in §5.5 (density beginning at māyā, one step lower).

`five_movements` is likewise a roster check.

## 4. What is deliberately *not* formalized

- **Independence of ℋ, 𝒫 and σ** — the paper's central proposal (§5.1). Stating
  it as three independent coordinates would be a modelling decision, not a
  transcription; it needs its own prereg.
- **Aggregation `F`** (§3.1, §11) — only the type `ContractionState → Nat` is
  fixed. Equal weighting vs āṇava-priority is open.
- **The seven pramātṛs as σ-regions** (§3.3) — the paper leaves Pralayākala's
  exact composition source-dependent; not encoded.
- **Centring persistence at liberation** (§4.2) — encoded as “either” in prose,
  not as a theorem.
- **Composite-locus composition rule** (§9) — the paper states the problem; the
  `Composite` structure only compares ν.
- **The Śaiva/Aurobindo disagreement on density onset** (§5.5) — the Lean file
  encodes Aurobindo's placement. The alternative should be a parameter, not a
  silent default, if this rung is ever promoted.
- **Any claim that the homologies are true.** Tentative rows (esp. Supermind ↔
  Sadāśiva–Īśvara, Overmind ↔ Śuddhavidyā) are paper proposals.

## 5. Verify (Lean 4.34.1 — run, plus the CI frontier step)

```sh
lean --version   # must be the version in ../lean-toolchain
lean formal-trika/frontier/AurobindoNotation.lean
```

No `lake` dependencies are required, matching the other `frontier/` files. If
`lean` is outside `PATH`, set `LEAN` per `formal-trika/README.md`. Ran clean locally on 2026-11-20 (exit 0, warnings as errors), and the
`formal-checks.yml` "Frontier models" step compiles it on every PR. A file
that stops building fails CI like any other rung.

## 6. Relationship to existing rungs

- `recognition/Coords.lean` already types the five kañcukas as coordinates
  (K/A/V/T/C). This file is compatible but does not import it: the paper's σ has
  seven components (three malas + five kañcukas + karman), while `Coords.lean`
  covers the five kañcukas only. A later rung could reconcile the two by adding
  mala components to the coordinate vector.
- `TRIKA-METHOD.md` / `PREREGISTRATION-TEMPLATE.md`: if this notation is promoted
  from spec to a claimed result, it needs a prereg with kill criteria; the open
  questions in §4 are the natural first batch.
- `PHONEMIC-BODY-SPEC.md`: no direct overlap; the paper's axes are metaphysical,
  not phonematic.
