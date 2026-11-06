# Essay ↔ Tension ↔ Formalisation ↔ Science

Brainstorm recorded 2026-11-06. Question: essays map to pushing type —
sessions resolving tensions, grounded in trika-x formalisation — and how
Trika links to science using our theories and seeds.

## 1. The circuit already half-exists

- svread `lingua.py` declares **tension the hub**: `tension:<id>` resolves
  with sidecar links to essays/videos/packs/evidence.
- `pushing-catalog.json`: 57 sessions, records carry a `tension` field.
- Expansion essays carry chunk + theorems + tracks — but **no tension
  field**. They float: grounded in formalisation, untied to any tension.
- CRUX docs (CRUX-03/04) are doctrinal tensions with spans and verdicts —
  the natural tension-type for expansion essays.

Missing links (all small, all explicit):

```
tension --resolves/loosens--> essay (at most one tension per essay) --grounds--> theorems --binds--> spans
   ^                                                        |
   +-- personal (private, consent-gated)                   +-- science
   +-- doctrinal (CRUX docs, public)                           (papers as counterparts)
```

## 2. Essay ↔ pushing mapping

An expansion essay IS a pushing: machine-compiled, claim-frozen, reviewed.
Proposal (formal lane, no cross-lane writes):

- `essay.json` gains `tension: {id, relation}` (SINGULAR — one essay
  resolves at most one tension, per TENSIONS-ENDGAME.md law 3).
  relation ∈ {resolves, loosens}.
- Compiler flag `--tension tension:slug` (explicit only, never mined).
- IDs resolve through lingua `tension:<id>` at check time, fail-closed.
- **Privacy law**: personal tensions (`visibility: private`) are
  unresolvable from expansion essays — check fails with
  `tension-private`. Only public cruxes + consented tensions link.
  Diary stays private; consent per use, revocable.

## 3. What we already hold (science side)

Theories (local, read today):

- `BRIDGES-LEVIN.md`: 5 Trika↔Levin bridges (bioelectric pattern as
  spanda/sheath models) + levin shelf has nerve/tadpole/single-cell papers.
- Aperture counterparts with **PubMed IDs** baked into verses.
- QRI shelf, Doyle X2 shelf, Tymoczko/Solms/Seth shelves.
- `LAWOFONE-TRIKA-NOTE.md` (F8), `CHANNELING-SABDA-NOTE.md`,
  densities/adhvan track (F11) — each a Trika→science hypothesis with
  a named counterpart, not vibes.

Seeds → science domains (research-tracks F1–F11): F3 consciousness
(IIT/GWT via ConTraSt bench), F4 morphogenesis (Levin), F5 deep-time,
F7/F11 mala/densities (affective neuroscience), F8 LoO (physics),
F9 odyssey (comparative), F10 mirror suite.

Collections (R2, verified live):

- `research-datasets/bridge-essays/`: bridge records joining named
  esoteric concepts to PMC/PubMed papers (e.g. phase-14-nonordinary:
  ayahuasca/near-death/psychedelic papers, each with source_ids,
  concepts, prerequisites). ~76 under arxiv/ + top-level files.
- `atlas-sources/informationphilosopher/`: full Doyle mirror
  (freedom/indeterminism/responsibility pages, walker-matter-to-life
  PDF+txt, CIMC whitepaper, download.log).
- `atlas-sources/pdfs/`: Corbin/mundus-imaginalis, ibn-arabi-barzakh.
- LQG shelf is LOCAL (`/root/damn/research-library/frontier-physics/`: 576lqg.md + 30 sources + tetrahedron-lqg docs) — corrected 2026-11-06, see SCIENCE-COLLECTION.md.

## 4. Science MCP vs archive — decision: archive-first, thin lookup

- **Archive wins** for writing: deterministic, hash-pinned, offline,
  no API drift, provenance auditable. Papers enter as files with shas
  + provenance records, exactly like Sanskrit sources.
- **Live APIs verified reachable** (arxiv export, PubMed eutils both
  green from box). So import-by-ID is cheap and honest.
- **No science MCP yet.** What we need is `import_paper.py` (CLI):
  `arxiv:<id> | pmid:<n> | pmc:<id>` → fetch metadata + PDF →
  store under `bridge/science-sources/<id>/` with sha + provenance →
  immediately usable via compiler `--research`. MCP (if ever) is a
  thin wrapper over the archive + this importer — never a live-search
  dependency inside the essay gate.
- First imports should serve open tracks: F3 (consciousness papers
  behind ConTraSt contrasts), F4 (Levin lab papers), F11 (affective
  neuroscience for mala/densities), F8 (physics for LoO).

## 5. Ordered next steps

1. `tension` field (singular) + `--tension` flag + `tension-private` check (formal).
2. Essay↔tension edges into `expansion-graph.json` (formal).
3. `tools/import_paper.py` (arxiv/pmid/pmc → vendored + provenance).
4. `SCIENCE-COLLECTION.md` index of everything above (one page, shas).
5. First science-grounded essay: one track, papers vendored, claims
   citing paper IDs exactly like theorem names.
