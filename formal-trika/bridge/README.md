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
