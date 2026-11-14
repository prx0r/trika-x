# FINAL GREEN RECEIPT — 2026-11-14 (post-merge sweep, main)

*Everything below was run on `main` after all Tier-1 merges. This is the
"done" archive. Every number is reproducible by the command in its row.*

## Merged this session

| Repo | PR | What |
|---|---|---|
| trika-x | #12 | hygiene: catalog 112, ENDGAME vision, drift receipt |
| trika-x | #13 | HTTP bridge + public layer names + verification-first guide + e2e |
| trika-x | #14 | session receipt + endgame sweep |
| trika-x | #11 | PrakriyaSlice slice + fail-closed generated-certificate exemption |
| trika-x | #16 | provenance: 555→1034 identified (Muktabodha ingest), freshness SHARP |
| trika-x | #8 | closed (superseded) |
| openpatala | #2 | biblio search q-path crash fixed (%TITLE% escaping) + 3 new tools |
| svread | #49 | public layer names in gateway instructions + registry 198→210 |

## Gates (main, this session)

| Gate | Result | Command |
|---|---|---|
| Lean control | **53 PASS / 0 FAIL** | `sh formal-trika/control/run.sh` |
| Lean recognition | **26 passed / 0 failed** | `sh formal-trika/recognition/run.sh` |
| EVIDENCE | **206 theorems · 155 entries · 2 exemptions · 1 generated · 0 problems** | `tools/evidence_check.py` |
| Coverage | **16/154 chunks (10%)** — unchanged, honest | `tools/evidence_check.py` |
| TABLE | **rc=0** | `tools/table.py --check` |
| Axiom | **CLEAN (static)** | `tools/axiom_audit.py --check` |
| Freshness | **SHARP** (with documented provenance) | `tools/freshness.py --check` |
| MCP catalog | **SHARP, 115 tools / 8 families** | `tools/mcp_catalog.py --check` |
| Federation pretest | **GREEN (28)** | `tools/federation_pretest.py` |
| Full suite | **107 tests OK** | `python3 -m unittest discover -s formal-trika/tests` |
| Bridge E2E | **8/8** | `tools/bridge_e2e.py` |
| openpatala gate | **GREEN + 2 recorded BLOCKED** | `python3 check.py --status` |

## Notes on the 206 vs 157 theorem jump

49 are the generated `PrakriyaSlice.lean` certificate slice. They are NOT
EVIDENCE rows and NOT passage coverage: they prove structural well-formedness
of 44 DERIVED traces under a **bound receipt** (file+pack sha256, Lean 4.34.1,
exit 0). `evidence_check` now treats generated certificate files fail-closed:
receipt must exist, exit 0, and pin the exact committed file, else every theorem
in it is a PROBLEM. Tamper test: receipt exit_code→1 produces 1 PROBLEM;
restore → 0. Coverage stays honestly 16/154.

## Live public proof (no auth, from the internet)

```
POST https://formal.svatantrya.net/mcp  → initialize OK (2025-06-18)
  tools/list → 10 formal/treeka tools
  formal__trace tantrasara-a08/tsa08-p03 → verdict COMPLETE, theorems REGISTERED
POST https://sanskrit.svatantrya.net/mcp → initialize instructions now name
  layers in plain words (draft-translation, literal-gloss, argument-map,
  reading-translation, essence, register-render, final-translation, song)
```

Console `mcp.sanskrit.help` (bearer): **210 tools / 7 servers**, measured.

## Still open (unchanged, honestly)

- Formal coverage 16/154 — climbs only by prereg→model→twin→EVIDENCE per rung
  (scholar promotes).
- Witnesses 0 corpus-wide (needs manuscript eyes).
- 479 Muktabodha works are identity shells, rights NULL → **not publishable**
  until rights set; no loader receipt at ingest time.
- OAuth (per-user) not built — shared bearer; write sheaf owner-only.
- Practice scoring needs `SVATANTRYA_SESSION` (owner).
- Zenodo DOI token (owner). Directory submission (owner). Token rotation (owner).

*Machine proposes, human disposes. BLOCKED is never PASS.*
