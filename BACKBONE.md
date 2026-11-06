# BACKBONE — openpatala as the identity spine (wired 2026-11-06)

**Thesis (owner):** from openpatala we ingest Sanskrit works and start the
full chain — translations, essays, videos, teacher, books. Status: WIRED
on this box (queryable), ADOPTED by bridge + treeka + source-map;
downstream ID propagation audited with specs where IDs are missing.

## The flow (each arrow runs)

```
ingest (GRETIL/MIRI/file → works/editions/etexts/passages)
  │  tools/openpatala_ingest.py (87 works; Mode B for new files)
  ▼
translate (translation-work layers per chunk; passages ledger = chunk IDs)
  │  passages.jsonl locators == DB passages.citation_value (verified)
  ▼
formalize (trika-x Lean per chunk; EVIDENCE locators)
  │  bridge --db resolves chunk → work/edition/etext rows (tested)
  ▼
argue (argmap nodes → crux queue → treeka; 909 passages keyed)
  │  treeka formal column; gap report drives queue
  ▼
essay (Scholar: work/target + signoff + rights + bridge + DOI)
  │  IDs PRESENT (best-in-class). Missing: openpatala IDs in bundle (spec §5)
  ├─► videos (packs → factory): packs carry PROSE basis only (spec §5)
  ├─► teacher (relay passages): headers + short quotes (adequate; DB IDs future)
  └─► books (Zenodo bundle): work/commit/reader_url (spec §5 for openpatala IDs)
```

## DB contents (box, 2026-11-06)

works 522 (260 availability + 184 dossiers + 78 workdir rows) ·
editions 87 · etexts 87 (file:// artifacts, sha-pinned) · passages 909 ·
assertions 442 · ext-ids 121 · witnesses 0 (no data anywhere — R2 audit).
Reruns idempotent (verified all-skipped). Loader bug caught live
(citation_value got work_id — fixed + migrated via DELETE+reingest).

## §5 specs for owning lanes (IDs missing downstream)

1. **Packs** (factory lane): `evidence_refs: [{work, locator, ledger_sha,
   snapshot_rev}]` in scene_manifest (fail-closed: render refuses packs
   without refs). Current prose basis stays as description, not identity.
   STATUS 2026-11-06: unbuilt (federation commit is the swarm skill only).
2. **Videos**: render receipts carry pack evidence_refs through (which
   pack rev rendered which video). STATUS: unbuilt.
3. **Books** (translation-work zenodo_publish.py): provenance.json gains
   `openpatala_work_id`, `edition_id`, `ledger_sha256` (look up
   svread/source-map.json at bundle time — file exists). STATUS 2026-11-06:
   PR #9 implements work_id + mapping + record_sha + edition_label; no
   edition_id by design (CANDIDATE strings, recorded refusal); open, green.
4. **Teacher** (nibbanahelp lane): relay passage headers may cite DB work
   IDs when convenient; no schema change (additive field only, ask first
   per their rules). STATUS: untouched.
5. **Lingua** (svread, shared language): work/chunk records carry the
   openpatala block as of svread PR #9 (open, green) — resolve_ref and
   ref_links surface identity to MCP clients. Formalisation dimension
   (theorem refs) is a follow-up needing a grammar decision, not built.

## Boundaries (unchanged)

Witnesses UNPINNED everywhere (table empty; resolver hard-enforces).
Editions are CANDIDATE (dossier/GRETIL strings, not collations).
Bytes live on disk/R2 (DB holds hashes + URIs, never blobs).
R2 dump needs PG18; box builds schema from migrations (recipe in
bridge/README). Lanes respected: no translation-work/ipvv/svread/
nibbanahelp/deitybody/sanskrithelp files written from this track.
