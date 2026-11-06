# R2 patala bucket audit — 2026-11-06 (box agent, owner-ordered)

Token: owner-supplied R2 S3 credentials (account `954612afb…`, 0600 at
`/root/.env`). **Owner: rotate this token — it was pasted
in chat and must be treated as exposed.**

## Question

Does `s3://patala` hold any populated openpatala witness/row data beyond
the documented empty-schema mirror (bridge/README.md: schema-only dump,
rows live in GitHub)?

## Method

boto3 via S3-compatible endpoint (aws-cli broken on box, boto3 per repo
rule). Full prefix inventory, then selective small-file download with
SHA-256 verification against committed manifests. 26 MB registry file
downloaded once, verified, then deleted (disk 99%).

## Findings

| Prefix | Objects | Bytes | What |
|---|---|---|---|
| `openpatala/` | 4 | 0.9 MB | schema dump + repo tarball + README + SHAs (all SHAs VERIFY) |
| `projects/openpatala/snapshots/2026-11-05/` | 2 | 0.7 MB | shallow clone mirror @ `4147a19` + manifest (SHA VERIFIES) |
| `releases/2026-08-14/` | 4 | 27.7 MB | `works.jsonl` 147,339 rows + parquet + manifest (SHA VERIFIES) |
| `source/` | 119 | 1.1 GB | GRETIL snapshots (tar.gz ×3 + manifests) + MITRASAMGRAHA test.jsonl — NOT downloaded (disk) |
| `staging/` | 5,613 | 2.3 GB | gretil mirror + more — NOT downloaded (disk) |
| `artifacts/registries/` | 92 | 31.5 MB | l0/l1/argmap/c1 registries — layer mirrors, not witnesses |
| `public/published/ipvv/` | 59 | 2.5 MB | IPVV published records (same set as ipvv-r2-staging) |
| `shared/` | 1 | 65 KB | atlas-corpus-export.json |
| `manuscripts/` `clones/` `objects/` | ~0 | — | empty / README-only (clone URLs, repos removed 2026-08-18) |

## Witness-data verdict: NONE FOUND (triple-confirmed)

1. **Dump is empty schema.** `openpatala.dump` (248 KB, SHA `0d2d909c…`
   VERIFIED) = `pg_dump -Fc`, 34 COPY table definitions (works, editions,
   witnesses, etexts, passages, events, ledger…). No postgres on box to
   `pg_restore`; binary framing confirms schema-only shape per committed
   README. No row data.
2. **Seeds have no witnesses.** `data/gold` (184 dossiers incl.
   `PTCND_sa_abhinavagupta-ta.json`) carries work IDs + external
   (GRETIL) identifiers, no manuscript records. `translation-availability.json`
   = 260 works availability, no witnesses.
3. **Registry has no witness fields.** `works.jsonl` schema is exactly
   `{id,title,work,author,source,license,status}` × 147,339 (19,620
   tantra-ish); 4 rows mention manuscripts only in TITLES
   (Bower/Spitzer/composite/list, all MACHINE_PROPOSED). SHA `1651110a…`
   VERIFIES against release manifest.

## Consequence for the bridge

`witness: UNPINNED` stands everywhere. What CAN advance without a
populated DB is now encoded in `bridge/witness-candidates.json`
(CANDIDATE pointers with NGMPP/FDM provenance for the 5 frontier targets
+ controls + current-work editions; resolver surfaces them advisory-only,
never promoting — tested). Genuine witness pins still require either (a)
a populated openpatala DB (row data per README lives in GitHub
`prx0r/patalacheckpoints` + `prx0r/openpatala`, not R2, not this box), or
(b) per-manuscript NGMPP verification recorded as new dated files.

## Not fetched (disk 99%, 882 MB free)

`source/` GRETIL tarballs, `staging/` mirror, `artifacts/` registries.
Fetch only with a named consumer and /tmp cleanup in the same session.
`/tmp/patala-r2/works.jsonl` (26 MB) deleted after verification.
