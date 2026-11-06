# Passage bridge: exact locators, candidate identities

The bridge is a **locator inventory**, not a source-edition certificate or a
proof of a text's meaning. It stores no passage text or private diary content.
`passages.snapshot.json` contains exact IDs, ranges and SHA-256 hashes of the
six passage-ledger files at the recorded translation-work Git revision.
The mappings in `openpatala-map.json` are candidate work/edition links. Every
witness remains `UNPINNED` until an independent manuscript record and its
relationship to the text can be checked; a printed edition is not a witness.

```sh
python3 formal-trika/tools/bridge_resolve.py chunk:tsa08-p03
python3 formal-trika/tools/bridge_resolve.py --check --tw ../translation-work
python3 formal-trika/tools/bridge_resolve.py chunk:tsa08-p03 --tw ../translation-work
```

Without `--tw`, the result states `SNAPSHOT_ONLY`. With `--tw`, every ledger
must match the recorded bytes or the command fails. Even `BYTES_MATCH_SNAPSHOT`
does **not** validate source text, L0/argmap, rights, edition or the relation to
a witness. Unknown, invented, stale and ambiguous locators must not resolve by
prefix. The historical `vbt` work-level reference is explicitly labeled
`kind: work`, and `chunk:vbt` is not accepted as a passage.

To update after an upstream change, inspect the new source and provenance,
then run the generator against a clean tracked Git checkout. Review the JSON
diff and update `EVIDENCE.json` where needed; do not overwrite old source or
silently promote a candidate mapping:

```sh
python3 formal-trika/tools/build_passage_snapshot.py --tw ../translation-work \
  --output formal-trika/bridge/passages.snapshot.json
python3 formal-trika/tools/bridge_resolve.py --check --tw ../translation-work
```

On 2026-11-06, the available OpenPāṭala Tantrasāra gold dossier
`data/gold/PTCND_sa_abhinavagupta-ta.json` contained a work ID, title and
GRETIL external identifier, but **no witness records**. The API reads witnesses
from PostgreSQL; this checkout did not provide a running populated database.
This observation does not prove that no witnesses exist elsewhere. Do not
invent a siglum to satisfy a test. A future import must independently bind the
specific manuscript, its identifier, edition/transcription and exact evidence.

## R2 mirror (openpatala stack backup)

`s3://patala/openpatala/` holds a schema + repo mirror for bringing the stack
up on another box. **It is a schema backup, not the populated database.**

| File | What | sha256 |
|---|---|---|
| `openpatala.dump` | `pg_dump -Fc` of Postgres 18 DB `openpatala`. **Schema complete, all tables 0 rows** (11 MB DB, empty as of 2026-11-06). | `0d2d909c…3a9e8a3` |
| `openpatala-repo-2026-11-06.tar.gz` | Full `/root/openpatala` (code + docs + `data/gold` 764K + `data/evidence` + `translation-availability.json` [260 works] + both migration SQL files). | `9579e264…e183e2` |
| `SHA256SUMS.txt` + `OPENPATALA-README.md` | Verification + restore recipe. | — |

**Where the real data lives:** populated rows for works/etexts/ledger/discovery
tables are **not** in this dump. Row data lives with the GitHub repos the
owner keeps (`prx0r/patalacheckpoints`, `prx0r/openpatala`), not on this host.
Any box can recreate the schema from R2; data comes from GitHub.

Restore recipe (from `OPENPATALA-README.md`):
```sh
createdb openpatala
pg_restore -d openpatala openpatala.dump        # schema only
tar xzf openpatala-repo-2026-11-06.tar.gz -C /root/
# data: load per repo loader scripts; JSON seeds are in openpatala/data/
```

Verify before trusting: `sha256sum -c SHA256SUMS.txt` against downloaded files.
The two files above were verified round-trip on 2026-11-06 (downloaded hashes
match originals exactly).

## Local populated DB (box recipe, A-track 2026-11-06)

The R2 dump needs Postgres 18 (`pg_restore: unsupported version (1.16)`
on PG15). Same 34-table schema builds version-free from the repo's own
migrations; seeds are the JSON dossiers. Recipe (box-tested):

```sh
apt-get install -y postgresql
service postgresql start
su postgres -c "createdb openpatala"
su postgres -c "psql -c \"CREATE ROLE patala LOGIN PASSWORD 'patala';\""
cp /root/openpatala/migrations/*.sql /tmp/ && chmod 644 /tmp/*.sql
su postgres -c "psql -d openpatala -f /tmp/001_create_all_tables.sql"
su postgres -c "psql -d openpatala -f /tmp/002_add_missing_tables.sql"
su postgres -c "psql -d openpatala -c 'GRANT ALL ON ALL TABLES IN SCHEMA public TO patala;'"
su postgres -c "psql -d openpatala -c 'GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO patala;'"
python3 formal-trika/tools/openpatala_seed.py   # idempotent; see tool docstring
```

Seeded 2026-11-06: 444 works (260 availability + 184 gold dossiers),
442 assertions, 121 external identifiers; events SKIPPED by design
(dossier events are ID-only stubs — loading them would fabricate
content); editions/witnesses/etexts/passages 0 (no source data anywhere:
R2 dump empty, dossiers witness-free, registry witness-field-free).
DSN convention: `postgresql://patala:patala@localhost:5432/openpatala`.
Reruns are no-ops (ON CONFLICT DO NOTHING; verified (0,442)/(0,121)).
