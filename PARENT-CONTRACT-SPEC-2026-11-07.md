# PARENT CONTRACT — openpatala as federated MCP parent (spec v1, 2026-11-07)

 Status: REFERENCE IMPLEMENTATION (trika-x only, 2026-11-07). Child lanes
 (translation / book / video / scholar / formal) implement their own MCPs;
 this file froze the contract they conform to without cross-repo writes.
 Implementation: formal-trika/tools/federation_gateway.py (stdio parent:
 prefixed tools/list, FailOpen routing, local openpatala__* + guide) +
 data/federation-children.json (default child commands, FEDERATION_CONFIG
 override) + tests/test_federation_gateway.py (11 tests GREEN, 2026-11-08:
 five live children + local families, dead child excluded, unknown = Unknown
 tool, guide prefixes match the real surface, catalog matches live when all
 children are up). Live surface: **104 tools / 8 families** — machine
 catalog `formal-trika/data/mcp-catalog.json`, regenerate with
 `tools/mcp_catalog.py --write`, gate with `--check`. Operations guide:
 `MCP-OPS.md`. Machine proposes, human disposes.

## 0. Identity root (the one key)

`openpatala_work_id` (box DB `works.id`: `tantrasara`, `tantraloka-a15`,
`ipvv`, flat works). Every federated record carrying work identity carries:

```json
{"openpatala_work_id": "<id|UNRESOLVED>", "ledger_sha256": "<hex|UNRESOLVED>",
 "edition_label": "<string|CANDIDATE>", "witness": "UNPINNED"}
```

Rules: `UNRESOLVED`/`CANDIDATE`/`UNPINNED` are valid states, never silently
promoted. Missing/UNRESOLVED = draft-only downstream (no ship, sell, post,
or publish). ISBN lives ONLY on print assets at OWNER-SHIP (a worker emitting
an ISBN is a defect). Social `post_id` is written ONLY by the runtime receipt
after human confirm. Witness siglum acceptance = `bridge_resolve` printing a
siglum; until then every witness field stays UNPINNED (T18/T19 BLOCKED stands).

## 1. Topology (one MCP per part, one parent)

```
openpatala-federation (parent: openpatala__* + federated tools/list, tools/call)
  ├─ openpatala_mcp__*  5  resolve/bundle/search/frontier/health (box DB)
  ├─ translation__*    16  status/gates/validate/swarm_* (shastra lane)
  ├─ scholar__*        33  evidence/audit/PUSHBACK/account (svread/mcp)
  ├─ bookfactory__*    22  draft/preview only, no ship (bookfactory)
  ├─ video__*          18  vf_* state/gates; gated renders only (videofactory)
  └─ formal__*          7  bridge/evidence/table/gaps/runs/axioms/trace (read-only)
  federation__guide     1  in-process navigation guide
```

Children hold zero auth. Parent enforces allow/deny + per-agent keys.
Transports: children stay stdio (`python3 mcp/server.py`); parent is a tiny
stdio→stdio router (drop-in `mcp-gateway`/`context-forge` binary later for
HTTP + dashboard). Adding a lane = add one child entry, never a parent rewrite.

## 2. Naming (prefixMode prefixed, no silent collisions)

Tool names on the wire are `<child>__<tool>`: `openpatala__resolve`,
`openpatala_mcp__get_health`, `translation__status`,
`scholar__passage_evidence`, `bookfactory__quote_preview`,
`video__vf_status`, `formal__gaps`. Prefixes are literal child ids — there is
no `book__*` or `openpatala-mcp` prefix. Registration rejects collisions
(same public name from two children = refuse both until renamed). Unprefixed
names never resolve. Unentitled/unknown = `Unknown tool` (caller cannot probe
what exists).

## 3. Failure (FailOpen on children, fail-closed on identity)

One child down → rest still serve; all down → error. Timeouts/blocks/empties
are ERRORS, never passes. Identity resolution failure (`UNRESOLVED` work,
byte-mismatch ledger, missing proof) fails the dependent call closed
(`CANDIDATE`/`UNRESOLVED`/`BLOCKED` status, never invented IDs).

## 4. Banned surface (must not exist anywhere in the federation)

`ship`, `render`, `seal`, `publish`, `send`, `spend`, `post`, `isbn_issue`,
`grant_rights`, `signoff`, `submit`. Publication/signoff stay explicit human
actions in their home systems (Scholar bridge, factory owner gates). The
federation pre-test scans every child `tools/list` for these substrings and
fails the suite if any appear.

## 5. What the parent serves today (read-only)

- `openpatala__resolve {work}` → work/edition/etext/passage counts +
  contract block (§0). Source: box DB if reachable, else `source-map.json`
  candidate state. Never invents a siglum.
- `openpatala__coverage {work}` → DB passages vs local ledger rows.
- `federation__guide {}` → navigation instructions (prefixes above).
- `openpatala__coverage {work}` → DB passages vs local ledger rows.
- Federated `tools/list` (prefixed union) + `tools/call` (route by prefix).
- No account tools, no Qwen, no drafts. Account/Qwen stay in scholar-mcp
  behind `SCHOLAR_SESSION_COOKIE` + explicit `consent_to_ai`.

## 6. Acceptance (static pre-tests, no live servers needed)

`tools/federation_pretest.py`: (a) prefix uniqueness across the
representative surface; (b) banned action-name scan (exact/prefix, never
substring); (c) down-child routing table returns rest-or-error (pure
function); (d) contract-block fixture: `UNRESOLVED` in → draft-only out.
Green = contract holds. The representative list is a fixture, not the
catalog: live truth is `data/mcp-catalog.json` (104 tools).

 Non-goals: no second ledger, no second ID scheme (openpatala IS identity),
 no auto-anything, no cross-scholar style mixing, no non-Trika expansion
 until the loop closes, no claiming the model is the mind.
