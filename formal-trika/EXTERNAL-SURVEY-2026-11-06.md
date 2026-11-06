# EXTERNAL SURVEY — eight repos reviewed for the endgame (2026-11-06)

Sources: repo READMEs/model cards/papers via live fetch, all claims below
traced to those pages. Licenses noted per item — nothing adopted yet.

## 1. MIDF/eGangotri Sanskrit OCR (`tadad/midf-sanskrit-ocr`, HF)

Kraken BLLA segmenter + PP-OCRv6 recognizer, CPU-runnable
(`uvx ... ocr.py page.jpg`), 3.45% CER on 220-page panel, review-risk
triage scores per page, honest limits (single-manuscript panel, segmenter
not fully manuscript-unseen). eGangotri source data CC-0. Dataset
`midf-egangotri-sanskrit` (369k). VERDICT: the witness pipeline.
USE: NGMPP microfilm pages → OCR → transcription candidates → volume
spans → record wiring. First unblocks the witness column (0 everywhere).

## 2. MITRA-lexicon (`dharmamitra/dharmamitra-lexicon`, GH + paper)

2.18M headwords / 10.4M attestations, DCS lemmas, senses ranked by count,
every sense linked to sentence pairs + offsets. sa-en-by-sa slice is
CC BY-SA 4.0 (92% of attestations); code MIT; alignment model on HF;
live UI at lexicon.dharmamitra.org. Buddhist-corpus caveat: Trika
coverage must be measured, not assumed. VERDICT: L0 grounds at scale.
USE: L0 OPTIONS grounds (frequency-ranked senses + attestations as the
`grounds + source` fields); fork-adjudication support; coverage-measure
Trika overlap first (sample 200 Trika tokens vs lexicon hit rate).

## 3. Axiom Lean stacks (`AxiomMath/Stacks` + CFSG + PrimeGapsLib, GH)

16M lines Lean, Mathlib-based, Lean 4.34.0-rc2 (≈ our 4.34.1). Two tiers:
StacksCore (human-reviewed) vs StacksFrontier (AI-written, compiles,
UNREVIEWED) — our T/R tiers at scale, independently invented. Proof maps
+ issue-claimed agent swarms + comparator verification + no-sorry/
no-native_decide CI (= our axiom audit). VERDICT: method validation +
steals. USE: (a) adopt `formalization.yaml`-style tier metadata for
EVIDENCE (machine-readable reviewed/unreviewed split); (b) proof-map
task claiming for swarm rungs; (c) cite as precedent in Scholar review
that kernel-checked ≠ faithful (their MLQ coverage states it plainly).

## 4. Samskritam.ai (site + GH, Sriram Subramanian, IISc)

DCS word analyses + Vidyut (2000+ Aṣṭādhyāyī rules) checking every word;
benchmark graded by RULE not model (recitation-tested unmemorized texts,
secret seed, reviewed keys, stated limits). VERDICT: L0 pilot + metric
discipline. USE: (a) wire our existing `vidyut_candidates` MCP tool into
the L0-as-terms pilot (Sohoni/Huet-backed, NEXT-STEPS 4.8); (b) copy the
benchmark discipline for tau/metrics (secret seed, rule-graded, reviewed
keys, published limits) — the template our metric gates lack.

## 5. Xiaomi-OCR-0 (`xiaomi-research/Xiaomi-OCR-0`, GH, Apache-2.0)

0.8B VLM, #1 Real5-OmniDocBench, MCP service + Agent Skill pattern,
Ollama-local (~1.8GB). Caveat: modern-doc benchmarks; Devanagari/
manuscript performance UNPROVEN; Ollama route experimental without
parity guarantee. VERDICT: print-edition complement, not manuscript
solution. USE: GRETIL/Muktabodha print PDFs → Markdown (tables as OTSL);
benchmark against MIDF pipeline on one eGangotri page before trusting;
adopt their MCP+Skill packaging pattern for our own OCR service IF built.

## 6. Worktrunk (`max-sixty/worktrunk`, GH, MIT/Apache)

Git worktree CLI for parallel agents (branch-named worktrees, hooks,
LLM commits, PR workflow). VERDICT: immediate ops upgrade. USE: swarm
lanes in isolated worktrees (ralph + assessor + PR branches) without
checkout collisions; hooks for gate-on-commit. Install: cargo/brew,
minutes, zero risk (no repo changes required).

## 7. NVIDIA auto-ontology (`NVIDIA/auto-ontology`, GH, Apache-2.0)

Semantic layer over DBs (terms → columns, relationships, certified
definitions) exposed via MCP/CLI/API; certify flow (draft → test → certify);
Postgres + pgvector + helm weight. VERDICT: pattern, not deployment.
USE: treat openpatala as the ontology (works/editions/witnesses = terms,
assertions = relationships); copy the draft→certify→fold-back loop for
our identity curation; MCP exposure pattern for agent context. Do NOT
adopt the infra (our box needs no helm chart).

## 8. VedOCR (`Suyashkb/VedOCR`, GH)

Expert-annotated Pada-pāṭha OCR dataset (segmentation challenges of
analytical Vedic text), not an engine. VERDICT: supporting eval.
USE: hard-case eval set for any śāstric OCR attempt (compound-splitting
stress); method notes for span-boundary disputes. Pair with (1): MIDF
engine + VedOCR hard cases.

## Priority order for us

Witness pipeline (1) → L0 grounds (2) → method steals (3) → L0 pilot +
metric discipline (4) → print OCR trial (5) → worktrunk install (6) →
ontology pattern (7) → eval data (8). Items 1–4 change what the machine
can prove; 5–8 change how fast or cleanly.
