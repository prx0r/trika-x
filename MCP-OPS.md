# MCP-OPS — operating guide for the trika federation (2026-11-08)

*Measured against the live gateway on 2026-11-08. Every number here comes from
`tools/mcp_catalog.py` → `formal-trika/data/mcp-catalog.json`. If this doc and
the catalog disagree, the catalog wins and this doc is stale — regenerate both.*

---

## 0. What exists (one paragraph)

One stdio parent, `openpatala-federation` (`formal-trika/tools/federation_gateway.py`),
multiplexes five child MCPs plus two local tool families. It exposes **104 tools
across 8 families**, prefix-renamed `<child>__<tool>` so nothing collides.
Children are started as subprocesses from `formal-trika/data/federation-children.json`;
a dead child is FailOpen (excluded, calls to it error), never fatal. The parent
is **read-mostly routing, not an auth boundary**: write tools that already
exist in a home system stay there, and publication/signoff tools do not exist
anywhere in the federation.

---

## 1. Topology (measured)

```
openpatala-federation  (stdio NDJSON; parent)
  ├─ openpatala      2   openpatala__resolve, openpatala__coverage   (in-process, box DB)
  ├─ formal          7   formal__trace|bridge|evidence|table|gaps|runs|axioms (in-process, read-only)
  ├─ federation      1   federation__guide                          (in-process)
  ├─ openpatala_mcp  5   resolve/get_bundle/search/get_frontier/get_health
  ├─ scholar        33   evidence, audit_draft, PUSHBACK, sources, reviews, account
  ├─ translation    16   status, gates, validate, concepts, lore, swarm_*
  ├─ bookfactory    22   overview, quote_preview, check_lane, read_*, stage (draft/preview)
  └─ video          18   vf_status, vf_gate, vf_triage, vf_queue, vf_launch (gated)
```

Prefixes are literal child ids. There is **no `book__*` and no
`openpatala-mcp__*`** — those were doc drift, fixed 2026-11-08. If a call says
`Unknown tool`, check the prefix in the catalog first.

---

## 2. Quickstart

### Parent (normal agent use)

```sh
cd /root/trika-x
python3 formal-trika/tools/federation_gateway.py
```

Speaks MCP JSON-RPC over stdio, one JSON object per line. Minimum handshake:

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"openpatala__resolve","arguments":{"work":"tantrasara"}}}
```

### Alternate child set (tests, degraded boxes)

```sh
FEDERATION_CONFIG=/path/to/children.json python3 formal-trika/tools/federation_gateway.py
```

Config shape is `trika-federation-children/1` (see
`formal-trika/data/federation-children.json`): `{children: {name: {cmd, cwd}}}`.
Any missing/unstartable child is excluded from `tools/list`.

### Direct child (debugging only)

```sh
python3 /root/openpatala/patala/mcp_server.py              # box DB identity tools
python3 /root/svread/mcp/scholar_server.py                 # scholar evidence/account
python3 /root/translation-work/mcp_server.py --serve       # shastra lane
python3 /root/bookfactory/bf_mcp/server.py                 # draft/preview
python3 /root/videofactory/vf_mcp_server.py                # gated video
```

Children hold no auth. Account/Qwen tools live in scholar-mcp behind its own
session cookie + explicit consent; they are not opened by the parent.

---

## 3. Tool catalog (families; full list in mcp-catalog.json)

| Family | Count | Read/write character | Owner lane | Notes |
|---|---|---|---|---|
| `openpatala` | 2 | read | trika-x | local; DB if reachable else source-map candidate state |
| `formal` | 7 | read-only, deterministic | trika-x | no Lean/EVIDENCE/ledger writes ever |
| `federation` | 1 | read | trika-x | guide |
| `openpatala_mcp` | 5 | read | openpatala | identity root; `get_health` = box DB counts |
| `scholar` | 33 | read + private draft/account writes | svread | no signoff/publish tools exposed |
| `translation` | 16 | read + lane-internal writes | translation-work | `swarm_*` never pushes/signs off |
| `bookfactory` | 22 | draft/preview + gated stage | bookfactory | nothing ships via MCP |
| `video` | 18 | state + gated renders | videofactory | `vf_launch/vf_queue` only on gated+approved renders |

Banned **action** names are rejected by exact/prefix match, never substring:
`ship, render, seal, publish, send, spend, post, isbn, isbn_issue,
grant_rights, signoff, submit`. Read-only lists such as
`scholar__list_published_essays` and a factory's own `video__vf_publish` are
not the banned action and stay allowed.

---

## 4. Behaviour contract (what callers can rely on)

1. **FailOpen on children, fail-closed on identity.** One child down → the rest
   serve. Calls routed to the dead child return `Unknown tool`.
2. **Unknown is unknown.** Bad prefix, unprefixed name, or an unauthenticated
   account tool → `Unknown tool`; callers cannot probe what exists.
3. **Invalid arguments are clean errors.** A schema/validation error is
   returned as a tool error, never as empty success (e.g. video tools require
   `project`).
4. **Status vocabulary is fixed.** `UNRESOLVED`, `CANDIDATE`, `UNPINNED`,
   `BLOCKED`, `PARTIAL` are valid states and are never silently promoted.
   `formal__bridge` always reports `witness_status: UNPINNED` until a real
   siglum exists.
5. **No prefix guessing.** `formal__bridge` resolves exact ledger locators only;
   invented/stale/ambiguous locators error.

---

## 5. Verify it yourself

```sh
cd /root/trika-x

# 1. conformance (spawns the gateway + five children; 11 tests)
python3 -m unittest formal-trika.tests.test_federation_gateway -v

# 2. static contract (prefixes, banned names, routing, identity block)
python3 tools/federation_pretest.py

# 3. machine catalog drift gate
python3 tools/mcp_catalog.py --check

# 4. spot calls (expect OK, not Unknown)
#    openpatala__resolve {work: tantrasara}
#    formal__bridge {chunk: chunk:tsa08-p03}
#    openpatala_mcp__get_health {}
#    translation__status {work: tantrasara-a08}
#    scholar__list_works {}
#    bookfactory__factory_overview {}
#    video__vf_status {}
```

A healthy box prints: 11 tests OK; pretest GREEN (28 representative tools);
catalog SHARP (104 tools, 8 families).

---

## 6. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `Unknown tool: 'coverage'` under translation | tool name is `translation__status`/`translation__gates`, not coverage | list `translation__*` from the catalog |
| `Unknown tool` for `book__*` | wrong prefix; it is `bookfactory__*` | use catalog names |
| `Unknown tool` for `health` | it is `openpatala_mcp__get_health` | use full prefixed name |
| child missing from `tools/list` | child cmd/cwd wrong or deps absent (FailOpen hides it) | run the child directly; fix `federation-children.json` |
| `openpatala__resolve` says UNRESOLVED | box DB unreachable or work not seeded | check `openpatala_mcp__get_health`; else source-map candidate state is honest |
| validation errors on video/book calls | required args missing (`project`, `work`) | pass them; errors are clean |
| "Passage unavailable or withheld" | passage is BLOCKED/private for that reader path | not a bug — fail-closed by design |

The gateway needs only the stdlib. Direct children may need `mcp` / lane deps;
`openpatala` local tools need `psycopg2` and the box DB.

---

## 7. Known gaps (recorded, not hidden)

- **stdio only.** No HTTP transport, no dashboard, no per-agent entitlements
  yet (parent contract §1 plans them; not built).
- **Identity coverage is thin, not fake.** Box DB has 555 works / 909 passages
  / 0 witnesses; adapters still discover nothing upstream. `UNRESOLVED` and
  `UNPINNED` are the honest answers.
- **Catalog describes the full federation.** On a box with a dead child,
  `mcp_catalog.py --check` reports drift by design; re-run `--write` only when
  the missing child is expected to be permanently absent.
- **`scholar__passage_evidence` can answer "Passage unavailable or withheld"**
  when the reader surface withholds a passage — correct behaviour, not an MCP
  failure.

---

## 8. Change protocol

Any change to a tool name, prefix, or family count:

1. update the child or gateway;
2. `python3 tools/mcp_catalog.py --write` (captures the new surface);
3. update §1/§3 of this file and the relevant spec (`FORMAL-MCP-SPEC`,
   `PARENT-CONTRACT`) in the same commit;
4. run the three verification commands in §5;
5. commit with `feat(mcp):` or `docs(mcp):` and paste the catalog counts in the
   body.
