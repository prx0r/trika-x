# Witness status (2026-11-06): work→dossier VERIFIED, siglum BLOCKED

- `bridge_resolve chunk:tsa08-p03` now returns the full chain: passage →
  work ID `PTCND_sa_abhinavagupta-tantrasAra` → dossier
  `gold/PTCND_sa_abhinavagupta-ta.json` (3 assertions: TITLE/AUTHOR/…,
  0 events) → **witness_records: 0**, status stays UNPINNED.
- Finding: dossiers in this checkout carry identity assertions only —
  no witness list, no sigla, anywhere checked. The DB resolver path
  needs Postgres + populated witnesses table (empty box-wide).
- Acceptance (brief §7 item 4: siglum printed) NOT MET. Exact next step:
  witness records ingested into openpatala (their lane) or a working
  resolver against populated data; then `witness` fields fill and
  `--check` verifies them. Nothing on my side can print what doesn't exist.
