# SKILL: essay — the complete essay factory (imports, not duplicates)

*Every stage below names the exact module that implements it. This skill
contains no duplicated machinery — it routes. Machine proposes throughout;
human disposes. Nothing here signs, publishes, promotes a tier, or rewrites
a quotation.*

## Stage 0 — Source (pin everything)

- Translation chunks: `translation-work/*/passages.jsonl` (locators +
  immutable IDs) + `source/volumes/*.json` spans + `source/record.json`.
- Owner voice: `/root/tantraessays/essays/**`, nibbanahelp essays (verbatim).
- Research voice: `/root/projects/research-library/**` (commentary, concordance).
- Formal: `trika-x/formal-trika/control|recognition|buddhist|frontier/*.lean`
  + `EVIDENCE.json` + `data/expansion-graph.json` (topic graph).
- Gate: every input pinned + licensed; unpinned = stop.

## Stage 1 — Compile (claims frozen FIRST)

- Tool: `trika-x/formal-trika/tools/essay_compile.py` (pattern:
  volume `patala_ml/essaygen.py` gold-chain — theme→graph→frozen claims→
  draft→alignment→verify; invariant adopted: no sentence introduces a
  proposition outside its frozen claims, fail-closed).
- Claim tables: svread `mcp/claims.py link_claims` (CURRENT/STALE/UNRESOLVED).
- Output: `formal-trika/swarm/expansion-*.md` + `.receipt.json` (frozen
  claims, coverage, audit) + graph append. Status MACHINE-COMPILED.

## Stage 2 — Prose L3/L4 (translation-work discipline for essays)

- L3 (`--l3`): sentence-to-claim tracing enforced (untraced = fail),
  essence map per paragraph, kill register, read-aloud owed. Sharp edits
  only, each justified against a claim. The endgame essay is structured
  data with audits: raw logical cruxes made beautiful WITHOUT writing —
  never a paragraph authored, only layers of justified edits.
- L4 (`--l4`): per-paragraph DRAFT files (craft_notes + rejected-with-
  killers + reads_against) + claim-overlap audit (drift = beautification
  without claims; rework or kill, never smooth).
- Model-drafted prose (roboscholar/Qwen) is EXPLORATORY ONLY — never
  enters the canonical path. Canonical = compiled + L3 + L4.
- Protocol: volume `workengestation/transmissions/v6-algorithm.md` (7 axioms,
  Phase 0–6, checksums) + `CLAUDE4.md` (4-pass: Write→Identify→Repair→
  Texture) + `essaygenaudit.md` file map + `antislop.md` 15 rules.
- Thesis engine (long-form): volume `.../essaygen/claude5.md` (7 layers;
  lessons: no sub-agent extraction, no script parsing — READ directly).
- Law: compiler law (verbatim voice, bridges not paraphrase); offender
  pattern flagged like `rebirth-explained` was. Quotes clipped, never rewritten.

## Stage 3 — Audit (mechanical)

- svread `mcp/audit.py audit_draft` (quotes vs same-paragraph sources) +
  `claims.py` staleness. Gate: 0 fails; warns triaged. Supplied sources
  labeled (argmap excerpts = R-grounds, never bundles).

## Stage 4 — Pushback (interpretive destroy)

- `trika-x/formal-trika/tools/pushback.py` (mock now; beam-free + CF
  cross-family live behind opt-in). Twin-generated skeletons via
  `twin_to_session.py` feed pushing sessions (ipvv LOGICVID pattern).
- Gate: objections answered or honestly kept open (CRUX-03 model).

## Stage 5 — Review (human)

- Scholar: request_review (exact revision) → annotations (immutable offsets)
  → decision → revise (ipvv worker + svread MCP). Agent triage (roboscholar
  review leg) finds problems; only humans close. Peer-review shaped by
  patalacheckpoints vision-06 (adversarial, resolvable evidence).

## Stage 6 — Publish (human + token)

- Signoff (409-clean) → public Git branch (translation-work scholar_service)
  → Zenodo DOI (token) → bibliography listing (atlas + biblio sweep) →
  pack/video (knowledge-dossier shape: aim + textual orientation + visual
  rules; R2 essay renders exist as precedent).

## Runners

Hermes skills per stage + cron (installed on box; activation = owner call);
sessions per essay; kanban review queue. Memory: prompt shas + decisions.
No auto-promote/publish/sign — in every skill text.
