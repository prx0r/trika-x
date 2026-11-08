# AGENTS.md — Ochema

## What this repo is (read this first)

This is **not a software project**. There is no package.json, no build,
no test suite, no CI, no deploy. It is a **living research object**: a
formal thesis about consciousness ("the Ochema thesis") maintained as
Markdown documents + JSON metadata, under constant adversarial review.
The currency of the project is *content integrity* — versions, grades,
registries, logs — not code.

The core claim: the same process-architecture (discrete moments of
determination through exclusion, an invariant surviving the moments,
time derived from the state, a compatibility condition at threshold) is
independently recovered at **8 levels of inspection** (math → quantum
gravity → quantum measurement → information → biology → phenomenology →
consciousness theory → experiential corpus).

## Read order for new agents

1. `OCHEMA-MANUAL.md` — THE system handover (v2.0.0). Directory map,
   routines, grading, audit protocol, session state. **Read this first.**
2. `the-unified-formal-framework.md` — the thesis itself (Parts 0, 1, 2,
   9 first).
3. `ochemamath.md` §0–§2 — the formal core (von Neumann algebras,
   Tomita–Takesaki, thermal time).
4. `the-occhema-object/updates/LOG.md` — the versioned history.
5. `.crush/MEMORY.md` — the session-bridge memory file (auto-loaded in
   Crush sessions via `crushrc`).

## The three registries (the state of truth)

| Registry | Path | What it tracks |
|---|---|---|
| Confrontations | `the-occhema-object/confrontations/REGISTRY.md` | Every theory/paper run against the thesis, verdict + grade |
| Evidence | `the-occhema-object/evidence/TREE.md` | Every claim with supports/negations, strength-graded. **The GAPS list is the research agenda** |
| Concepts | `concepts/REGISTRY.md` | Live formal cores + essay renderings |

## Directory map (what's where)

- **The canon (top level):** `the-unified-formal-framework.md` (thesis),
  `ochemamath.md` (math), `frontier-math.md`, `the-moment.md`,
  `the-orchestration.md`, `rendition.md`, `OCHEMA-MAGNUM-OPUS.md`,
  `PRACTICE-LAYER.md`, `THE-RASA-THEORY.md`, `THE-COLLECTIVE-FIELD.md`.
- **`the-occhema-object/`** — the git-object. `meta/ro.json` (**the
  version lives here**), `sections/` (00–08 working copies of thesis
  parts), `confrontations/<slug>.md`, `evidence/TREE.md`,
  `updates/LOG.md` (append-only memory). Its own `README.md` is STALE
  (says v1.1.0, outdated structure) — do not trust it; use the manual.
- **`concepts/<name>/`** — concept objects: `core.md` (the formal
  theorem, graded), `concept.json` (metadata), `essays/whattheheckis-<name>-vN.md`
  (renderings). Exemplar: `concepts/time/`. Pipeline manifest:
  `concepts/QUEUE.md`; process foundation: `concepts/PROCESS-NOTES.md`.
- **`formalised-theories/`** — the lineage: IPIT → MEPIT → OCHEMA →
  REPM → CSID (numbered 01–05).
- **`references/`** — corpora and deep-dives: `576lqg/` (24 LQG papers),
  `tegmark/` (24 papers), `cannon/research/` (channeled corpus),
  `evidence-mine/`, `valence-lineage/`, `plant-cognition/`, `urantia-book/`
  (LaTeX source), plus top-level `*.md` deep-dives.
- **`beings/`** — the Law of One / Ra analysis (15+ files).
- **`game/`** — game blueprints + notes (the "myth engine"); docs are
  speculative design, not thesis claims.
- **`essayvizport.d/`** — the active port project (EssayViz → Skia
  renderer), status PLANNED, 4 phase docs + acceptance criteria. This
  is the one place with real engineering content.
- **`EssayViz/`** — large binary assets (epubs, zips, PDFs, film packs).
  Do NOT read these files; they are source corpora. `scripts/occhema-snapshot.py`
  is the only project script.
- **`crushrc`** — Crush config: `option context-path .crush/MEMORY.md`
  (auto-loads project memory every session).

## The version chain & update protocol (the most important workflow)

Any thesis change (confrontation, evidence, concept, section, correction)
requires:

1. Make the content change (e.g. new `confrontations/<slug>.md`).
2. Update the relevant registry (REGISTRY.md / TREE.md / concepts/REGISTRY.md).
3. Append to `updates/LOG.md` — **append-only, dated, versioned header**.
4. Bump `meta/ro.json` `current_version` (and add a `history` entry).

Version semantics: **patch** (x.y.z→x.y.z+1) = corrections/registry
fixes; **minor** (x.y→x.y+1) = new confrontations/evidence/concepts;
**major** (x→x+1) = new layer/theorem/structural change.

The version chain must stay consistent: `ro.json current_version` ↔
`LOG.md` latest header ↔ files on disk. Audit procedure + quick commands
are in `OCHEMA-MANUAL.md` §10.

**⚠️ Version drift exists today:** `ro.json` says 1.25.0, the manual
claims 1.27.0, commit d441d07 says v1.26.0. Never trust a single file
for the current version — cross-check with the audit commands.

## Grading discipline (never relax)

- **A** theorem/proof-grade · **B** confirmed (replicated) · **C**
  converging evidence · **D** plausible · **E** speculative.
- Identifications with consciousness are always C–E, labeled.
- The numerology 576/570 stays **rejected** (−−−, on record). Do not
  rehabilitate it; the `references/576lqg/*.py` scripts are the
  verification record of that rejection.
- The channeled corpus is **Tier-4**: hypothesis generator only, never
  evidence.
- A claim with 3 supports + 1 strong negation is **CONTESTED**, not
  supported. Negations are always shown at full strength (asymmetry rule).

## Conventions

- **Files:** kebab-case slugs. Confrontations `confrontations/<slug>.md`
  (e.g. `tcf-hinge-preexists.md`); evidence
  `evidence/<layer>-<claim>-<source>.md`; concept essays
  `whattheheckis-<name>-vN.md` (new version = old archived).
- **Confrontation format:** date, added-in version, exact quotes with
  sources, per-invariant verdict (VALIDATES / ALIGNS / CHALLENGES /
  REFUTES / NEUTRAL), grade, verdict table.
- **Essays are renderings, not sources.** The concept `core.md` is the
  source of truth; when the core updates, the essay re-renders (new
  version, old archived). Never edit the essay to change the theory.
- **The thesis can change** — a confrontation that forces a refinement
  is a success (the Friesen rule). Honesty events (self-rejections of
  overclaims) are logged, e.g. v1.15.1, tcf-hinge-preexists.
- **Git commits** follow the version: messages like
  `v1.26.0: <summary of what was integrated>`.
- Prose style: heavy use of tables, A/B/C/D/E grades, "GAP" markers in
  evidence files, layer references (L1–L8), invariant names (moment-triad,
  exclusion, invariant, time-from-state, orchestration law, harmonic ladder).

## Commands

```bash
# State snapshotter (the only real project script)
python3 scripts/occhema-snapshot.py            # print snapshot JSON
python3 scripts/occhema-snapshot.py --write    # write meta/operation-state.json

# 576-lattice verification scripts (the rejected numerology, on record)
python3 references/576lqg/compute_576_lattice.py
python3 references/576lqg/decisive_test_symmetry.py

# Urantia book build (self-contained LaTeX subproject)
cd references/urantia-book && make             # xelatex; includes ../utils/Bible.make (external, may not exist)

# Version-chain audit (from OCHEMA-MANUAL.md §10)
grep '^## v' the-occhema-object/updates/LOG.md | head -1
python3 -c "import json; print(json.load(open('the-occhema-object/meta/ro.json'))['current_version'])"
ls the-occhema-object/confrontations/ | grep -v REGISTRY
```

No linters, no formatters, no tests. Verification = the audit protocol
(manual §10) + the append-only LOG.

## External directories (NOT in this repo)

The manual and documents reference sibling projects at
`/root/projects/`: `blog/` (research objects, skills in
`blog/hermes/skills/` — the routines ochema-dreaming,
confrontation-registry, evidence-registry, concept-object, peer-review,
yogi-spotlight, source-to-essay), `essayviz-workspace/` (the Skia
renderer fork), `tantraloka/`, `starweavers/`, `sanskritree/` (also at
`/mnt/HC_Volume_106427611/sanskritree/truth/`). Don't grep the repo for
these; use the absolute paths.

## Gotchas

- **~~Pending fixes from the external review~~** **APPLIED v1.31.0/v1.31.1 (2026-08-04)** — the two known-broken claims are corrected in the documents:
  - `ochemamath.md` §6.3: the false "finite-dimensional modular flow is trivial" claim is replaced by the implementation-underdetermination argument (C, not theorem); the CIMC "defeat by theorem" verdict is withdrawn and regraded.
  - `the-unified-formal-framework.md` Part 1/L1: the "global section iff H¹(U, ℱ) = 0" claim is corrected to "[o(s)] ≠ 0 ⟹ no global bearer section; vanishing is not sufficient" and demoted to research target (no sheaf constructed).
  - **v1.31.1 additions (peer-review round 3):** the "law-changing transition" discriminator is WITHDRAWN (state-dependent dynamics ≠ law-changing dynamics; the higher-order map x ↦ Φ_x is a fixed law); the universality-class framing is demoted to E (no RG map / fixed point / shared invariant constructed); the Manicka–Pai–Levin experiment is correctly identified as frog embryonic brain (conditional dynamics under one model — evidence FOR one law, not F → F′); the KMS falsification experiment is marked not-mathematically-defined pending an explicit algebra/state/group/observables construction; Pratyabhijñā recognition is recognized as Ochema's own formalization (σ-flip), not independent textual evidence.
- **Version drift** (see above) — always audit before relying on a version.
- **Stale docs:** `the-occhema-object/README.md` and `SOURCE-MANUAL.md`
  are superseded by `OCHEMA-MANUAL.md`.
- **Huge binary trees** (`EssayViz/`, `references/*/` PDFs/epubs/zips) —
  never read or grep them wholesale; they are corpora. The 576lqg/tegmark
  PDFs are inputs, the analyses are in the `.md` files.
- **Session continuity:** Crush sessions don't inherit context. `.crush/MEMORY.md`
  is the bridge — update it at the end of any session (state changes,
  pending work, decisions). It also lists the current PENDING FIXES.
- **Daily dreaming routine** (manual §2.1) is the heartbeat: REVIEW →
  INGEST → CONNECT → CONFRONT & INTEGRATE → PRODUCE → LOG & BUMP. When
  asked to "do the daily," follow it exactly.
- The most externally-supported claim is the **valence claim** (ν_i =
  −dF/dt; Joffily & Coricelli 2013 + 5 derivations). The unrun original
  experiment is the **spectral-quality conjecture** (quality = spec(K)).
  The **bridge-frontier** (math→felt bridges, L5→L6 χ-gap) is the
  current focus.
