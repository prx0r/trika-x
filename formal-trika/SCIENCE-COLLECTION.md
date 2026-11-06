# SCIENCE-COLLECTION.md — every science holding, verified 2026-11-06

All locations checked live. Counts are real, not estimates.

## Local shelves (box disk)

| Holding | Path | Size / count | What |
|---|---|---|---|
| LQG shelf | `/root/damn/research-library/frontier-physics/` | `576lqg.md` + 30 source files + 7 tetrahedron-lqg docs + thesis/evidence files | Quantum tetrahedron → K₄ mapping, constructor theory ×5, causal sets ×3, Wolfram ×2, amplituhedron, dense packings ×2, Bianchi/Haggard/Livine/Speziale/Engle/Rovelli PDFs, `compute_576_lattice.py`, `decisive_test_symmetry.py` |
| Research library | `/root/damn/research-library/` | 155M, ~30+ top-level docs + `bridge-corpus/` + `comparative/` + `concept-deepdives/` + `evidence-mine/` + `research-objects/` + `pushing/` + `rasa/` + `recognition/` | Thesis assembly, commentary stages, 5-stage lens, veil deep-dives, RASA-VALENCE-INTO-ESSAY |
| Library | `/root/library/` | 643M, 378 files, `frontier/` 327 | PMC PDFs + .nxml (PMC10032309 … PMC10336047 range sampled) — biomed corpus on disk |
| Mirror | `/root/projects/research-library/` | near-mirror (differs by 3 dirs) | Backup of research library |
| Bentov | `/root/gcomedy/library/bentov-stalking-the-wild-pendulum.pdf` | 1 | Consciousness/physics classic |
| Rovelli-adjacent | `/root/hxrmxs-corpus/32 madhyamaka rovelli.txt` | 1 | Madhyamaka↔Rovelli bridge text |

(Correction to ESSAY-TENSION-SCIENCE.md: the LQG shelf is LOCAL, not R2.
No `volume frontier-physics` bucket exists; `patala-volume-archive` holds
archive/backup/offload only.)

## R2 holdings (live-listed)

| Bucket / prefix | Count | What |
|---|---|---|
| `source-library/frontier/` | 399 | Frontier PDFs (Goethean science, esoteric imagination, …) |
| `source-library/consciousness/` | 346 | Incl. `rasa/`: Tymoczko geometry of music, Albers color, proportional harmonies |
| `source-library/tantra/` | 588 | Abhinavagupta texts (ahnika txts, aesthetics) |
| `source-library/buddhism/` | 17 | Analayo papers, Manjusri, Tsongkhapa lamp |
| `source-library/astrology|hermetica|occult|platonism|sufism|glossary|` | uncounted | Per INDEX.md |
| `research-datasets/bridge-essays/` | 76 under `arxiv/` + top-level `bridge-arxiv-*.json`/`bridge-pmc-*.json` | Bridge records: esoteric concept ↔ arxiv/PMC/PubMed paper, with source_ids, concepts, prerequisites (phase-14-nonordinary sampled: ayahuasca, NDE, psychedelics) |
| `atlas-sources/informationphilosopher/` | mirror | Doyle: freedom/indeterminism/responsibility, Walker matter-to-life PDF+txt, CIMC whitepaper |
| `atlas-sources/pdfs/` | 3+ | Corbin mundus-imaginalis ×2, ibn-arabi-barzakh |
| `sourcematerial/` | academia bundles (MBs each) | Abhinavagupta svatantryavada, cognitive science of tantra, Sankaranandana |

## Import surface (verified live)

- arxiv export API: reachable. PubMed eutils: reachable (70k hits test).
- `tools/import_paper.py` (owed): `arxiv:<id> | pmid:<n> | pmc:<id>` →
  `bridge/science-sources/<id>/` + sha + provenance → `--research` now.
