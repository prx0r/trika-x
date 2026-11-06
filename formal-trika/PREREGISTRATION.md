# Pre-registration — Formal Trika, arm A (control + first rung)

**Registered 2026-11-05** by the box agent for the owner. This file was written
**before** any Lean formalization code in this repo. It is never edited; a correction
is a new file (`PREREGISTRATION-<date>.md`) that cites this one. Method: Thon Ly's
formal-abhidhamma discipline (prereg → controls → mutation tests → verdicts plain).

## 0 · Source tiers (frontier T/R/E/C/H/X)

- **T (textual):** what the Sanskrit explicitly states — translation-work GOLD layers
  (T1/L0/argmap, `check.py` CANONICAL green): `tantrasara-a08` (93 units, kañcuka
  ground: kalā ×50, vidyā ×6, rāga ×3, kāla ×2, niyati ×1, kañcuka ×2 in T1),
  `tantrasara-a07` (tattva ladder), `paramarthasara` (saptadha-pramātṛ scheme),
  `phrdaya` (mala adjudication argmap), IPVV kriya/jñāna chunks (frozen T1 only).
- **R (reconstructed):** the strongest argument recoverable — owner's
  FORMALIZATION-OF-RECOGNITION (AM0: `m=(e,p,h,b,o,σ)`, `T_rec` σ-flip, 3 malas as
  formal failure modes), inexternalism (`D_i≡O_i*`, maximal-closure individuation),
  sciencetime (kāla as finite temporal access), ochema CSID.
- Every axiom/rule carries its tier. An R-rule may never promote itself to T.

## 1 · Definitions (same as Thon Ly, Trika-flavoured)

- **General rule:** a constraint over mala/kañcuka axes or capacity classes
  (e.g. *"kārma presupposes māyīya"*). It never names an individual pramātṛ.
- **Generated set:** the pramātṛ classes, each with its mala set, that satisfy all
  rules of the layer.
- **Compression ratio:** rule clauses in the Lean rule file (excluding datatype
  declarations) ÷ the number of pramātṛ rows generated.

## 2 · The control (known answer, run first)

**TK-C1 — the seven experients (saptapramātṛ).** Three binary mala axes —
āṇava (A) × māyīya (M) × kārma (K) — give 8 combinations; the all-absent
combination is Śiva, leaving the traditional **7**: sakala (A+M+K),
pralayākala (A+K, no M), vijñānākala (A only), mantra/mantreśvara/
mantramaheśvara (progressively purified stations, no malas, distinguished by
adhvan position — **R-tier**, not derived from the axes alone), śiva (none).
The rules must reproduce all 7 (+ śiva = 8 rows) exactly.

**TK-C2 — the known failure.** Delete the rule *"kārma presupposes māyīya
except in pralayākala"* (i.e. let K float free of M). The pralayākala row must
then come out wrong (merged with sakala or duplicated), and the theorem must
**fail to check**. If it still checks, the instrument is blind and nothing
below is reported.

## 3 · Predictions (made before any code)

| ID | Prediction | Confidence |
|---|---|---|
| **P-TK1** | At T+R: general mala rules generate **exactly 7+1** experient rows (7 named + śiva), `by decide` against the key collated from paramarthasara + tsa-a08 p03 (māyāgarbhādhikāriṇaḥ… vijñānākala… kalāpuṃviveka passages). | 0.55 |
| **P-TK1b** | P-TK1 requires **≥1 exception rule** naming a narrow class, not a general principle (candidate: the mantra-triad distinction is adhvan-positional, not mala-compositional — flagged R, not smuggled as T). | 0.7 |
| **P-TK2** | The 5 kañcukas (kalā, vidyā, rāga, kāla, niyati) formalize as **5 restrictions**, each pairing one infinite capacity with one finite form (tier: T for the five names in tsa-a08 T1; R for the capacity-pairing gloss). Count theorem: 5, `by decide`. | 0.65 |
| **P-TK3** | Recognition (T_rec σ-flip) formalizes as: content components (e,p,h,b,o) **unchanged**, σ flipped. Theorem: `recognize` preserves content equality, `by decide`/`rfl`. Tier: R (AM0 constructor-theoretic, from FORMALIZATION-OF-RECOGNITION, not from a root verse). | 0.6 |
| **P-TK4** | Compression ratio at control below **1.0** (fewer rule clauses than generated rows at 8). | 0.6 |

## 4 · Kill and reopen criteria

- **No rule set generates 7+1** → the transmitted composition is incomplete. That
  is reported as the result; the program continues to locate the missing rule.
- **The TK-C2 break does not fail** → the instrument is blind. Stop, fix, re-register.
- **A T-tier claim fails against the gold T1** → the mapping (not the text) is wrong;
  T1 is immutable, fix downstream (ipvv Law #1 applied to Trika: never edit the
  chunk, fix the formalization).
- **Cross-repo writes:** this repo reads translation-work/ipvv/gochema as evidence
  only. It never writes into those repos. A formalization that needs a source fix
  files it as a CLAIM, it does not patch the source.

## 5 · What this is not

Not a proof that Trika is true, and not a claim that it predicts physics. A Lean
`decide` verifies that stated definitions yield stated counts. Nothing more. Tier
labels distinguish root text, reconstruction, and our own definitions.
Heuristic scores (sanskritbench PASS, audit receipts) are never cited as semantic
proof — only `lean` checking a theorem counts here.
