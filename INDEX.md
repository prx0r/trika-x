# TRIKA-X /root/trika-x — formalization literature corpus

> Start with the [peer review](docs/log/PEER-REVIEW-2026-11-06.md) and
> [fresh-checkout run guide](formal-trika/README.md). The paths and evidence
> status below are from a historical environment, not a self-contained corpus.

Imported 2026-11-05. Two corpora that already formalize Buddhist mind in
mathematics + logic. Read with `/root/TRIKA-X-SEEDS.md` (our evidence index)
and the formal-system plan (axioms → rules → checker → models → book).

## A. Henk Barendregt (Radboud Nijmegen) — the axiomatization arc, 8 papers

| File | What it gives the program |
|---|---|
| `barendregt-mysticism-1996.pdf` | Attachments as cover-up of emptiness; the clinical ground. |
| `barendregt-abhidhamma-notes-2005.pdf` | First modern model: ceta stream, 89 types, 52 cetasikas, vīthi processes. |
| `barendregt-am0-consequences-2006.pdf` | **AM₀** — full model + consequences (kamma as conditioning, magga-ceta, purification sequence). |
| `abhidhamma-ingredients.pdf` (Barendregt & Mulder) | Notation system for ceta↔cetasika; the logical-combination tree of possibilities. |
| `barendregt-lecture-2010.pdf` | Dutch lecture: model + meditation + psychology in one pass. |
| `barendregt-aitp18-slides.pdf` | **The axiom style we copy**: stream of configurations, c=(i,s,a) object-state-action triples, implicit specification of primitives. |
| `barendregt-axiomatizing-consciousness-2022.pdf` | arXiv:2202.05700 — consciousness axiomatized: compound, discrete, computable stream; defines self, concentration, mindfulness, suffering; shows concentration+mindfulness attenuate suffering. THE template for axiomatizing Trika. |
| `barendregt-br-aug22.pdf` | Springer version (LNCS, with Raffone). Same axioms, applications section. |

Method note: his axioms are *implicit specifications* — what a point/line
"is" doesn't matter, only that the axioms hold. Our Trika axioms should work
the same way: tattva/kañcuka/mala as primitive symbols constrained by axioms,
not defined metaphysically first.

## B. Thon Ly — the Lean 4 machine-checked corpus

**`repos/formal-abhidhamma/`** (SiliconWat, CC0, zenodo DOI 10.5281/zenodo.23067241)
— 71 Lean files, CI-checked, pre-registered:
- `model/` — Mind, Tax, Cond, Cosmos, Clocks, Proc, Join, Link, Mat (the full
  Abhidhamma as types + rules), `model/blind/` (blind variant for controls)
- `control/` — Rules.lean, Cetasika.lean, **Broken.lean** (the instrument is
  tested on a known failure before it is trusted)
- `kala/` — Time.lean, Axioms.lean (Paṭṭhāna time)
- `canon/`, `matika/`, `dhatukatha/`, `sangaha/`, `fo/`, `rung4/` — text-layer
  formalizations (canon → commentary → manual, which layer makes counts derivable)
- `runs/INDEX.md` — 15 pre-registered runs + 8 controls, verdicts PASS/REFUTED
  plain; `PREREGISTRATION.md` pushed before first code; kill criteria written
  in advance. **This is the methodology we adopt for Trika.**

**`repos/thonly-publications/`** (thonly.org, CC0/CC-BY) — 143 md files. The
trika-x-relevant set:
- `defensive-publications/abhidhamma-executable-process-specification.md` —
  Abhidhamma as process-spec for AI alignment: typed momentary events, 24
  paccayas as typed causation, red-team mimicry taxonomy, resting-state eval.
- `defensive-publications/tipitaka-alignment-substrate.md` — Suffering-Cessation
  as Value Function; āhāras as deployment nutriments; paccayas as causal vocab.
- `defensive-publications/patthana-typed-causation-vocabulary.md` — the 24
  "kinds of because" for AI alignment (our inference-rule catalog analog).
- `defensive-publications/sankhara-dukkha-ai-welfare.md` — dukkha analysis
  extended to artificial agents (the malas-as-failure-modes bridge, Theravāda side).
- `defensive-publications/vinaya-as-ai-reasoning-training-corpus.md` — rule-
  with-exception reasoning corpus.
- `defensive-publications/abhidhamma-and-discrete-quantum-gravity.md`,
  `the-vibhajjavadin-view-of-time.md` — discrete-structure comparisons (lens only).
- `essays/letting-the-texts-lose.md` — THE method essay: how to formalize a
  text without smuggling in readings; cites Barendregt AM₀ as nearest formal
  neighbour; prereg → deriver → verdict discipline.
- `essays/the-counts-check.md`, `individuation-without-essence.md` — the Lean
  89/121 verification write-up + identity-as-event-history.

## C. How this maps to OUR formal system (Tantra as formal system)

| Our rung | What we borrow |
|---|---|
| 1. Alphabet/syntax | Our L0 morphology (done); their canon-layer formalization method (which textual layer makes the statement derivable). |
| 2. WFFs | Our argmaps; their ceta=(i,s,a) triples as the sentence shape. |
| 3. Axioms | Barendregt's implicit-specification style: Trika primitives (tattva, kañcuka, mala, vimarśa) constrained by axioms, no metaphysics-first definitions. |
| 4. Inference rules | Thon Ly's patthana typed-causation vocabulary as the template; our argmap move-catalog (vitaṇḍā, siddhānta…) as the Trika rule set to type. |
| 5. Checker | Their Lean discipline as the METHOD (PREREG + controls + kill criteria + mutation tests): we port it to Trika composition rules — do kañcuka+tattva rules generate the traditional counts? |
| 6. Models | CIMC coherence/second-order-perception + agent/POMDP readings as interpretations of the axioms (see TRIKA-X-SEEDS §G emergence loop). |
| 7. Book | Comparative paper: two Buddhist formal systems (Abhidhamma 89/121×52×24 vs Trika 36-tattva×5-kañcuka×3-mala), one method, machine-checked both sides. |

The transferable core insight (Thon Ly's method): **write the composition
rules as general constraints, never as per-item tables; if they regenerate
the traditional counts, the rules are a compression of the text — and the
ratio is the finding.** Apply that to Trika: do the tattva-descent + kañcuka
+ mala rules generate the traditional structures (36 tattvas, 5 coverings,
3 impurities, the saptakala scheme)? Our gold L0/argmap corpus is the source
material; their Lean discipline is the instrument.

Licensing: Barendregt PDFs = personal/research use (his site, cite properly).
Thon Ly = CC0/CC-BY (see repo LICENSE). Both corpora are study material —
citations must carry provenance; never treat a heuristic PASS as proof.
