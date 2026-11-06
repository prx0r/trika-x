# TRIKA-SCIENCE-MAP — the merge (brainstorm v1, 2026-11-06)

Thesis: the whole point is the mapping from the formalisation of Trika
to science. Each row: Trika node (theorem where formalised) × science
counterpart (paper where held) × relation × status. Relations:
ISOMORPHISM (same structure, both sides formal) · COUNTERPART (named
mechanism) · CONTRAST (disagrees — ConTraSt style, still data) ·
OPEN (hypothesis, paper owed) · IMPORT-OWED (paper known, not vendored).

## The map

| # | Trika node | Science counterpart | Relation | Status / holding |
|---|---|---|---|---|
| 1 | Tetrahedron K₄ (`Tetrahedron.lean`, T-TET1–3 + twins) | LQG quantum tetrahedron — Bianchi/Donà/Speziale arXiv:1009.3402; Bianchi&Haggard arXiv:1102.5439; Engle-Livine-Rovelli vertex. Lead counterpart: **Etera Livine** (ENS Lyon, 159 papers per INSPIRE; the quantum-tetrahedron program: boundary state 2007, holomorphic factorisation 2010, hyperbolic closure 2015/16, 6j self-duality 2019; 4 PDFs already in `576lqg-sources/`) | ISOMORPHISM | GROUNDED — 30 PDFs vendored, `576lqg.md` states the mapping, `compute_576_lattice.py` computes |
| 2 | 36 tattvas / 576 lattice / FCC | Dense packings of Platonic/Archimedean solids (×2 PDFs); causal sets (Sorkin axioms + directions + cosmology ×3); Wolfram hypergraph (×2); amplituhedron | COUNTERPART | GROUNDED (papers held) — formal side PARTIAL (lattice.py exists, no Lean lattice yet) |
| 3 | Spanda / vimarśa (sheath/pulse models) | Levin bioelectric patterning — nerve/tadpole/single-cell papers; constructor theory of information (Deutsch) | COUNTERPART | GROUNDED — `BRIDGES-LEVIN.md` 5 bridges; track F4 |
| 4 | Pratyabhijñā / recognition | IIT/GWT via ConTraSt bench contrasts; ORION benchmark | CONTRAST | GROUNDED (bench runs) — track F3; IMPORT-OWED: primary IIT/GWT papers |
| 5 | Mala (anava/karma/maya) — `Mala.lean :: count_3`, realms B1–B3 | Affective neuroscience; psychedelic/PMC corpus (phase-14: ayahuasca, NDE, psilocybin dose-response) | COUNTERPART | PARTIAL — bridge records held (R2), Lean side formal, join NOT yet written; tracks F7/F11 |
| 6 | Kāla / adhvan (time, courses) | Constructor theory of time (Marletto); causal-set cosmology; 6-edge K₄ gluing (spinfoam) | COUNTERPART | GROUNDED (papers held) — formal side OPEN; track F5 |
| 7 | Svātantrya / free will | Doyle two-stage model — indeterminism + responsibility pages | COUNTERPART | GROUNDED (mirror vendored) — essay unwritten |
| 8 | Nonordinary rendering | PMC/PubMed psychedelic + NDE corpus (bridge-essays phase-14) | COUNTERPART | HELD (76 arxiv/ + top-level bridges) — essay unwritten |
| 9 | Rasa / valence / camatkāra | Tymoczko geometry of music; Albers color; QRI shelf | COUNTERPART | HELD (rasa/ shelf) — `RASA-VALENCE-INTO-ESSAY.md` exists locally, not yet compiled |
| 10 | Māyā / measurement / observer cut | QM interpretations (Maudlin, Rovelli relational) | OPEN | IMPORT-OWED — no Maudlin/Rovelli PDF held (only a Rovelli-bridge txt); first `import_paper.py` customer |
| 11 | Upāyas (anava/sakta/sambhava/anupaya) | Contemplative neuroscience (meditation HRV — bridge record held: `bridge-arxiv-effect-of-meditation-on-heart-rate-variability`) | COUNTERPART | HELD — join unwritten |
| 12 | FCC / 570 morontia bodies / 6 edges | Spinfoam vertex (4-simplex gluing); stabilizer entropy of quantum tetrahedra (PDF held) | ISOMORPHISM (claimed) | OPEN — `576lqg.md` claims, `decisive_test_symmetry.py` exists; needs Lean statement before essay may cite |

## How the merge ships (mechanics, already half-built)

- Claims cite paper IDs exactly like theorem names (`arxiv:1009.3402`
  with the same standing as `Mala.lean :: count_3`). Essay gate checks
  both: theorems against EVIDENCE registry, papers against
  `bridge/science-sources/` provenance.
- `--research` corpus already accepts local dirs; science shelves enter
  the same way Sanskrit shelves do. No special-casing.
- Each map row becomes a track-tagged essay seed (F3/F4/F5/F7/F8/F10/F11);
  CONTRAST rows are first-class (a failed bridge is data, per F-log convention).
- Rule carried over: no essay may cite a row marked OPEN — the paper
  must be vendored or the claim stays out.

## First three builds (ordered)

1. Row 10 import run: `import_paper.py` vendors Maudlin + Rovelli +
   Bianchi/Donà/Speziale canonical versions → science-sources/ seed.
2. Row 5 join essay: mala formalisation × phase-14 corpus (F7/F11) —
   first science-grounded expansion essay.
3. Row 12 hardening: Lean statement of the K₄↔quantum-tetrahedron
   claim or downgrade ISOMORPHISM → COUNTERPART (honesty before beauty).
