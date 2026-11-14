# SESSION RECEIPT — 2026-11-14 (PR review sweep + ChatGPT-MCP path)

*Append-only. For the next agent: start here, then the PRs.*

## Merged (CI green, no reviewer active, verified locally after merge)

| PR | What | Local verify |
|---|---|---|
| trika-x #10 | treeka_report --work scopes every summary count | 5/5 tests OK |
| trika-x #9 | essay claims bind to ledger passage (span+digest+edition) | 14/14 tests OK; essay_derive 6 essays, 0 BROKEN |
| openpatala #1 | banners on superseded 08-17 plans | check.py GREEN + 2 recorded BLOCKED (on that branch pre-merge) |

## Fixed + pushed, or commented (not merged — decision owed)

- **trika-x #11 (PrakriyaSlice)**: CI failed on `PACK.is_file()` PermissionError
  at import (`/root` EACCES on runner). Fixed with the existing OSError-safe
  helper (1 line, commit `1174c55`, pushed). Local proof: absent-pack run
  skips 4/4, PermissionError-stubbed import survives. **Merge blockers
  recorded on the PR**: (1) evidence_check 49 PROBLEMS — PrakriyaSlice
  theorems lack EVIDENCE entries (206 vs 155; honest coverage stays 16/154);
  wire entries, exempt generated files, or keep unregistered — decide first.
  (2) 26 chunk-verse bridge JSONs need translation-work lane eyes.
- **openpatala #2 (biblio search)**: validated read-only on a scratch worktree
  (removed after). check.py GREEN. MCP tools/list: 8 tools. Filters work;
  **the `q` path crashes**: `search_bibliography(q='tantra')` → IndexError at
  `patala/db/store.py:293`, suspected unescaped `%TITLE%`/`%ALIAS%` literals
  at `store.py:227` vs psycopg2 params. Exact repro + suspected one-line fix
  posted on the PR. Do not merge until q-path is fixed + re-smoked.
  `get_bibliography_dossier`/facets unexercised (stopped at first crash).

## Opened this session

- **trika-x #12 (hygiene)**: catalog regen 104→112 tools (scholar 33→41, all
  read/prove, no banned actions), 7 live docs updated, ENDGAME second vision
  committed, drift receipt F1–F4. Needs rebase past #9/#10 (no file overlap,
  should merge clean) — or merge as-is, GitHub will confirm.
- **trika-x #13 (bridge, ChatGPT path)**: `tools/mcp_bridge.py` + unittest +
  MCP-OPS §9. Stdlib-only Streamable HTTP (POST /mcp, GET SSE, DELETE
  session), protocol 2025-06-18 with 2024-11-05 fallback, read sheaf of 26
  allowlisted, writes refuse `-32001` (OAuth not issued), limits 60s / 10
  concurrent / 64KB. Selftest green; live probe 112 tools with 26/26 sheaf
  present (one run saw 25/26 — boot transient, FailOpen working).

## ChatGPT-as-MCP: honest status

| Piece | Status | Owner |
|---|---|---|
| Registry + sheaves | done but stale (says 109/scholar 38; live 112/41) | svread lane refresh |
| Bridge | built + proven (#13), localhost only | trika-x, this session |
| Tunnel / hostname | not configured | owner |
| OAuth + write sheaf | design fixed, not built | worker (ipvv) lane |
| openpatala biblio tools in federation | blocked on PR #2 q-path fix | openpatala lane |

Order: land #12 → land #13 → tunnel → read sheaf live on ChatGPT → OAuth →
write sheaf. The bridge binds 127.0.0.1 by design; exposing it is an owner call.

## Box warnings (do not ignore)

- **Disk 98% (2.0G free).** Only /tmp scraps were safe to clear. Big trees
  (`/root/projects` 6.3G, media checkouts, `/tmp/opencode/restore-misc`)
  need owner eyes before any reclaim. tau/Mutate cannot run at this headroom.
- **Freshness DRIFT**: openpatala works 555→1034 / editions 102→581 (ingest
  with no receipt — provenance owed before canon), formal theorems 157→206
  (49 unregistered, see #11), svread manifest 7078→11109. Ledger NOT
  rewritten; recording new numbers without provenance would launder them.
- Nightly verify log left untracked (`docs/log/nightly-verify.log`).

*Machine proposes. Human disposes. BLOCKED is never PASS.*
