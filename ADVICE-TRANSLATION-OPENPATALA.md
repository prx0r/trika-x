# ADVICE — translation-work reads openpatala (for the translation agent)

**From:** formal-trika (box agent). **For:** translation-work lane (pull,
don't let me push — your repo, your rules, crystal skill stays law).
**Purpose:** use the box openpatala DB as the identity backbone for
translation work: which work/edition/text a chunk belongs to, with
hashes, without guessing.

## 0. Connect (read-only — enforced, not asked)

```
DSN: see OPENPATALA_READER_DSN in /root/.env (role tw_reader)
Allows: SELECT on all tables. Refuses: every write (tested).
Full-access DSN stays with box ops; you don't need it.
```

## 1. Cookbook (copy-paste SQL; psycopg2 or psql)

```sql
-- Which openpatala work is my workdir? (6 dossier-mapped + 81 workdir keys + 260 availability)
SELECT id, preferred_title FROM works WHERE id = 'tantrasara-a08'
   OR id = 'PTCND_sa_abhinavagupta-tantrasAra';

-- Edition(s) recorded for a work (CANDIDATE strings, not collations)
SELECT id, title, external_ids FROM editions WHERE work_id = 'PTCND_sa_abhinavagupta-tantrasAra';

-- Source bytes for a chunk's work (hash-verify on read!)
SELECT artifact_id FROM etexts WHERE work_id = 'tantrasara-a08';
-- then: SELECT digests, storage_uri FROM artifacts WHERE id = '<artifact>';
-- then: sha256sum the file at storage_uri; compare with digests->sha256.
-- NEVER trust bytes you didn't re-hash.

-- All chunks of a work (passage registry == your passages.jsonl locators)
SELECT citation_value, id FROM passages WHERE work_id = 'tantrasara-a08' ORDER BY order_key;

-- Layer inventory for a work (what exists: T1/L0/argmap/L2/C1/scholar/gate/source)
SELECT literal FROM assertions WHERE subject_id = 'tantrasara-a08'
  AND predicate_uri = 'patala:hasLayer';

-- Start a new work: is anything already recorded?
SELECT id FROM works WHERE id ILIKE '%kularatnoddyota%';
```

End-to-end example (tantrasara-a08 tsa08-p03): passages → id
`pt:pid:ts:a08:7f9e4b3307f2` → work PTCND_sa_abhinavagupta-tantrasAra →
editions (GRETIL Nirnaya Sagara 1918 string) → etexts → artifact sha →
re-hash SOURCE.txt. Every step checkable; try `bridge_resolve.py
chunk:tsa08-p03 --db` to see it assembled.

## 2. How to do it well

1. **Read joins, not dumps:** works → editions → etexts → artifacts →
   passages. The chain is the point; single tables lie by omission.
2. **Hash-verify bytes on every read** (artifact digests). Disk rots,
   checkouts move; the hash is the only truth.
3. **Pin revisions alongside everything you derive:** DB snapshot time
   (`SELECT now()` at session start) + `git rev-parse HEAD` for
   translation-work + openpatala + trika-x. A finding without revs is a rumor.
4. **Cite IDs, not bytes:** `PTCND_…`, edition ids, passage immutable_ids,
   artifact shas. Bytes stay on disk/R2; IDs travel.
5. **Refresh after pulls:** repos move under you. Re-run (all idempotent,
   reruns +0): `openpatala_seed.py`, `openpatala_ingest.py`,
   `work_inventory.py --db`. If counts change, say which rev moved.
6. **New Sanskrit work?** Don't hand-roll rows: `openpatala_ingest.py
   --file X.txt --work KEY --edition "..." --title "..."` (Mode B), or
   file an intake note shaped like `INTAKE-REQUEST-sivasutras.md`
   (14-line micro-intake precedent: minimal source + what it unblocks).

## 3. Clean-data rules (the ones that bite)

- **Never write openpatala tables** (role forbids it anyway). Derived data
  lives in YOUR ledgers (passages.jsonl, argmaps, C1) with openpatala IDs
  cited — never the reverse.
- **Availability ≠ edition.** 260 availability rows say a translation
  EXISTS somewhere; they are not edition records and carry no bytes.
- **Edition strings are CANDIDATE** (GRETIL/Muktabodha labels), never
  collations. Witnesses table is EMPTY box-wide — do not invent sigla;
  record `witness: unknown` explicitly (your SOURCE pattern already does).
- **Dossier events are stubs** (ID+type only) — never treat as history.
- **No second ID scheme.** Chunk locators + immutable_ids + openpatala
  work ids already join everything. A new numbering is a new confusion.
- **Registry ≠ formalized.** 909 passages are an inventory; 8 have Lean
  theorems. Never cite inventory as proof (our treeka labels this; keep
  yours labeled too).
- **Bytes ≠ truth.** Hash-checked bytes prove integrity, not philological
  correctness, review, or rights. Rights live in SOURCE records + lane
  policy, never in the DB.

## 4. Don'ts (learned the hard way, all REAL incidents)

- Don't run audits against a missing checkout and report success
  (fail on zero works — fixed in our tools; check yours).
- Don't reformat human-maintained JSON by whole-file dump (line-surgery
  only; diffs must stay reviewable).
- Don't trust enumeration order as doctrine (profiles, lists, orders are
  OURS until a scholar rules).
- Don't let `all([])` pass a gate, don't let caller-supplied revs mark
  CURRENT, don't let unsigned receipts authorize (all fixed here; audit
  yours for the same shapes).
- Don't copy © texts as sources (Pradīpaka, MIRI terms per file);
  comparison controls + links only.

## 5. What's ready for you now vs what needs a human

READY: box DB (544 works, 909 passages, 87 etexts hashed), source-map.json
(87 ledgers), layer inventory per work, intake-request pattern, chain
receipts. NEEDS HUMAN: witness eyes, P-TK1/ti-ca/rater-2 rulings, dīkṣā
policy, sign-offs, Zenodo token. Machine proposes; you propose better;
human disposes — same law both lanes.
