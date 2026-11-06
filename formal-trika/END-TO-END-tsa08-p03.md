# End-to-end receipt — tsa08-p03 (one-passage slice, 2026-11-06)

Proposed slice per PEER-REVIEW-2026-11-06 § "Practical first slice": one
source passage, exact layer revision, named theorem and mutation, and scholar
mapping review. Rights clearance and mapping review have not been established.
The receipt test uses self-asserted test evidence; it checks receipt mechanics,
not a verified source-to-proof-to-publication chain. Status of each link for
**tsa08-p03** (Tantrasāra a08, verses 8.39–8.64):

| Step | Evidence | Outcome |
|---|---|---|
| Passage locator | `bridge_resolve.py chunk:tsa08-p03` → `pt:pid:ts:a08:7f9e4b3307f2`, ledger sha `ee765be8…`, tw rev `e05e640` | `SNAPSHOT_ONLY` without `--tw`; `BYTES_MATCH_SNAPSHOT` with `--tw` |
| Source identity | GRETIL `gretil_tantrasara_clean.txt` (Nirnaya Sagara 1918), openpatala work `PTCND_sa_abhinavagupta-tantrasAra` | `CANDIDATE-EDITION` — NOT a witness |
| Witness | no manuscript record in available gold dossier; R2 dump is schema-only | `UNPINNED` — chain stops here for witness-grade claims |
| Layer revision | `tantrasara-a08/passages.jsonl` + argmap (kañcuka-six reckoning, kalā→agency, rāga functions) | ARGMAP-PINNED (T) |
| Named theorems | `Kancuka.lean :: count_5`, `pairings_distinct`; `Coords.lean :: coords_covered_once`; `KancukaCorr.lean :: corr_pull_raga`, `corr_stall_kala` | EVIDENCE.json entries present; T/T+R pins |
| Mutations | `BrokenKancuka.lean` (pairings collision) refuses `pairings_distinct`; `BrokenCorr.lean` refuses `corr_pull_raga` | must_fail PASS (last Lean-box run `93dbf7a`) |
| Crux walk | `CRUX-WALKTHROUGH-01` (rāga↔lobha): chunk → formal → argument → essay draft + claim table + PUSHBACK | chain RUNS; claim OPEN by design |
| Scholar mapping | human bridge review of passage→premise mapping | NOT DONE — the open item below |

## Negative tests exercised (all fail closed, suite green)

`test_bridge.py` (6/6): prefix locators rejected, `chunk:vbt` work-level
refused as passage, unknown locators nonzero-exit, tampered ledgers fail,
unverified witnesses unpromotable, stale/duplicate snapshots rejected.
`test_receipts_hardening.py` (ipvv, 11/11) covers the authority side.

## Remaining blockers

Witness pinning needs a populated openpatala database (the API reads
witnesses from PostgreSQL; this box has schema-only dump + repo mirror;
row data lives in GitHub `prx0r/patalacheckpoints`, `prx0r/openpatala`).
Until the resolver binds a specific manuscript + identifier +
edition/transcription, every downstream claim stays `CANDIDATE`, display
stays research-record-only, and no essay may cite Lean as doctrine.
Rights, exact source bytes, layer versions and scholar mapping review also
remain open. Do NOT invent a siglum to satisfy a test.
