# FEDERATION — the openpatala-centred MCP system (manual, 2026-11-07)
*Status: CANONICAL. Topology + live-state table (2026-11-07 audit; gateway row live 2026-11-14).

 One agent entry point. Openpatala is the identity root; every other system
 is a child MCP. The parent multiplexes, prefixes, routes FailOpen, and serves
 identity + a navigation guide itself. Machine proposes, human disposes.
 Nothing here auto-signs, auto-publishes, auto-ships, or grants rights.

 Companion docs: PARENT-CONTRACT-SPEC-2026-11-07.md (contract),
 FORMAL-MCP-SPEC-2026-11-07.md (formal tools), LAYER-NAMES-SPEC-2026-11-07.md
 (internal/external layer names), docs/log/PROCESS-NOTES-2026-11-07.md (§4–§4n, the
 session log), BACKBONE.md (identity spine), OPERATIONS.md (box manual).

## 1. Architecture (one diagram)

 ```text
 Agent (1 MCP connection)
   │  stdio NDJSON: initialize / tools/list / tools/call
   ▼
 federation_gateway.py  (trika-x, reference parent)
   │  tools/list  -> local tools + <child>__<tool> for every live child
   │  tools/call  -> route by first segment; Unknown tool on miss;
   │                   FailOpen (dead child excluded, never fatal)
   ├─ openpatala__resolve / openpatala__coverage   (local, source-map backed)
   ├─ federation__guide                            (local, navigation map)
   ├─ scholar__*        svread Scholar MCP (33 tools, evidence/claims/audit)
   ├─ bookfactory__*    bookfactory bf_mcp (22 tools, draft-only + gated builds)
   ├─ translation__*    translation-work shastra (14 tools, no push/signoff ever)
   ├─ video__*          videofactory vf_* (18 tools, gated renders; ship defaults proposed False)
   └─ formal__*         (specced; trika-x formal-trika read-only tools)
 ```

 Registry rule: one MCP per repo; openpatala is the parent. New lane = one
 config entry (data/federation-children.json, FEDERATION_CONFIG override),
 never a parent rewrite. Prefixes are applied at multiplex time
 (`prefixMode`-style); children keep their local names.

## 2. Live state (verified 2026-11-07 — API and DB agree exactly)

 | Table | Rows | Note |
 |---|---|---|
 | works | 555 | 544 box + 11 Abhinavagupta lost/attested (seed:trika) |
 | passages | 909 | = translation-work ledger total (17 re-keyed to tw workdirs, §6) |
 | editions | 102 | 101 ingest + KSTS-23 Tantraloka (seed) |
 | etexts | 87 | sha-pinned, bytes on disk/R2, never blobs in DB |
 | assertions | 1559 | 1512 box + 47 Abhinavagupta (STATUS=reported on lost only) |
 | translations | 121 | 16 atlas (external) + 5 Tantraloka biblio + 101 ours |
 | people | 20 | 12 atlas + 8 (Abhinavagupta + translators) |
 | witnesses | 0 | UNPINNED box-wide (NGMPP/manuscript eyes outstanding) |

 API: `127.0.0.1:8821` (`PYTHONPATH=. nohup python3 -m uvicorn
 patala.api:app --port 8821 --host 127.0.0.1`, log /tmp/openpatala-api-8821.log).
 `/health` ok; `/v1/works`, `/v1/works/{id}`, `/v1/bundle/{id}` verified live
 (works + Tantraloka + paramarthasara + lost-kramakeli).
 Port note: 8801–8806 + 8799 are squatted by a 35-day-old stray
 `http.server` fleet (pids 22143xx, ochemapp dirs — NOT ours, left alone).
 R2 (`patala` bucket): `openpatala/box-2026-11-06/` manifest + PG15-readable
 dump (115,225 B, works 544/assertions 1532 at build) + repo tarball; SHAs
 match trika-x bridge/README. R2 `openpatala.dump` (248 KB) is schema-only
 (needs PG18). No uploads made.

## 3. Parent gateway (reference implementation, trika-x lane)

 - `formal-trika/tools/federation_gateway.py` — stdio NDJSON parent. Spawns
   children from config, sends full MCP `initialize` (custom servers ignore
   extras, SDK servers get what they need), aggregates `tools/list` with
   `<child>__` prefixes (dedup, skip pre-prefixed), routes `tools/call` by
   first segment with timeouts, FailOpen on dead children ("Unknown tool"
   leaks nothing), local `openpatala__*` + `federation__guide`.
 - `formal-trika/data/federation-children.json` — default child commands
   (local /root paths). Override: `FEDERATION_CONFIG=/path/to.json`.
 - `formal-trika/tests/test_federation_gateway.py` — 6 tests GREEN:
   prefixed aggregation (live scholar 33 + live bookfactory 22), local
   identity incl. UNRESOLVED, routing through to both children, dead/unknown
   → Unknown tool (incl. unprefixed `vf_launch` must NOT resolve), guide.
 - `formal-trika/tools/federation_pretest.py` — static contract checks
   (prefix uniqueness, banned-name scan with exact/prefix matching — substring
   scan falsely flagged "relationships" for "ship", fixed — routing model,
   UNRESOLVED→draft-only). GREEN (26 expected tools).

 Register (opencode.jsonc): one entry pointing at federation_gateway.py,
 restart client. Children fill in as their SDKs/paths land; the parent needs
 no changes. Wire note: shastra (FastMCP) + vf/openpatala (`mcp` SDK legacy
 import paths) do not start on this box (deps absent — not chased);
 bookfactory bf_mcp is stdlib-only and runs anywhere (verified live).
 Child working trees were never touched (read via origin/master; one
 disposable /tmp worktree, removed + pruned).

## 4. Navigation (what an agent does, in order)

 `federation__guide` returns this; the flow is verify-first (step 2 before 3):
  1. `openpatala__resolve {work}` — known? ledger + identity block.
     UNRESOLVED = draft-only downstream, always.
  2. `formal__trace {work, target}` — the machine-checked chain FIRST
     (Lean theorems + receipts), then `scholar__passage_evidence` for the
     Sanskrit + layers in plain words: draft-translation, literal-gloss
     (meaning-forks live here), argument-map, reading-translation, essence,
     register-render, final-translation, song. Machine keys
     (T1/L0/ARGMAP/L2/C1/C2/L3/L4) still work; legend + blurbs in
     formal-trika/data/layer-names.json.
     Resolver: formal-trika/tools/layer_names.py (fail-closed).
 3. `scholar__audit_draft / link_claims / pushback` — check a draft. Machine
    report until a human adopts it; never a verdict.
 4. `translation__status {work}` (shastra) — registry state, proof, swarm.
    Writes never push, sign off, or mark final (server-enforced).
 5. `bookfactory__*` — draft previews (`quote_preview` explicitly draft-only);
    `stage`/`inspect` are gated builds. Nothing ships via MCP.
 6. `video__*` — `vf_gate`/`vf_triage` to read state; `vf_launch`/`vf_queue`
    ship ONLY gated+approved renders (videofactory#1 proposes explicit
    opt-in defaults). Seal/ears stay owner-only, never exposed.
 7. `openpatala__coverage` — how much of the corpus is bridged.

## 5. Abhinavagupta corpus (complete knowledge, honestly labelled)

 Extant (translation-work → box DB, all wired): Tantrasara ×22 ahnikas,
 Tantraloka ×37 (14 gold), Paramarthasara, IPVV (49 chunks, frozen T1),
 stotras/hymns (bhairavastava, kramastotra, anuttarastika,
 bodhapancadasika, paramarthacarca, anubhavanivedana, dehastha, …),
 abhinavabharati + ipvv-vivrti-vimarsini (source-only, no pipeline yet).
 External translations (atlas seeds): Tantraloka Dyczkowski + Singh/
 Maheshvarananda; Tantrasara Chakravarty; Paratrimsika-vivarana Singh (+
 Torella Italian in biblio); Vijnanabhairava Singh/Baumer/Silburn; Sivasutra
 ×3; Spandakarika; Malinivijayottara Vasudeva (partial).
 Tantraloka dossier-equivalent (seed): KSTS-23 edition + Gnoli (complete
 Italian) / Silburn+Padoux (partial) / Dupuche (TA-29 first English) /
 Lakshmanjoo (partial) — Dyczkowski row REMOVED as duplicate of atlas t0.
 Lost works (reported, finding-aid provenance, verify via Rastogi/Torella/
 GRETIL before stronger claims): Purvapancika, Kramakeli,
 Sivashaktyavinabhava-stotra, Sivadrishti-locana, Padarthapravesha-nirnaya-
 tika, Prakirnavivarana, Kavyakautukavivarana. Attested-unverified:
 Tantroccaya, Tantravatadhanika, Kathamukha-tilaka, Bhedavada-vidarana.
 NO edition/witness/etext claims for any of these. Dossiers (8 provider
 PTCND_sa_abhinavagupta-* incl. Vimarshini, Paramarthasara, Tantrasara)
 untouched — candidate side preserved, never promoted.
 Ours translations: `seed:ours:<work>:t0` ×101 (71 OURS-GOLD-
 MACHINE-PROPOSED / 30 OURS-PENDING; machine-proposed, human review pending;
 GATE.json per work is the gate). Loader: formal-trika/tools/
 seed_abhinavagupta.py (+ data/abhinavagupta-corpus.json), dry-run default,
 --apply idempotent; skip-guard prevents atlas duplicates.

## 6. Repairs made this session (all recorded, bytes unchanged)

 17 passages + 3 editions + 3 etexts lived under dossier keys
 (PTCND_sa_abhinavagupta-paramArthasAra/-tantrasAra) instead of translation-
 work workdirs — the ingest's dossier-mapped key vs the federation canonical
 (REGISTRY-FEDERATION + DB-BACKBONE: DB work ids match translation-work
 dirs). Fix: UPDATE work_id → paramarthasara (12), tantrasara-a07 (1),
 tantrasara-a08 (4); same for the 6 edition/etext rows (ids already tw-keyed).
 Immutable ids/locators identical before/after; totals still 909; bridge
 --check green; API chains work. Map + dossiers untouched (candidate links).
 Patalacheckpoints dedup audit (§4e): volume /mnt/HC_Volume_106959365 is the
 Aug-14 ancestor (live descends from it); no lost-works registry and no
 ours-status anywhere on disk — the seeds are new, not duplicates; the one
 real duplicate found (Dyczkowski t3) was deleted + skip-guarded.

## 7. Schemas (internal vs external)

 Internal codes NEVER change (validators, gates, ledgers, packs, lingua,
 treeka key on them; test_codes_stable fails on rename). Public names are
 ADDITIVE (`{code, public}` together, accept either). Bare renames need a
 major version. Box tables carry no CHECK constraints beyond types/FKs;
 JSON side: openpatala patala/schemas/v2 (22 files) covers identity/ledger
 plumbing but has NO translation/work/edition/person/passage schemas, and
 its assertion.json does NOT describe live rows (id pattern, predicate_uri
 shape, asserted_by enum all differ) — openpatala lane to reconcile; the DB
 de-facto conventions (matching work-inventory precedent) are what the seeds
 follow. translations.schema_uri default points at a non-existent v2 file —
 dangling reference, recorded not fixed (their lane). Layer order is settled
 in practice: stack.json v1.3.0 + schemas/LAYER_ORDER + check.py green
 (CANONICAL); the REVIEW spec's L200/C2-ordering P0 stays open for the
 translation lane to rule on.

## 8. Gaps & non-goals (explicit)

 Witnesses 0 box-wide (NGMPP/manuscript eyes). Human gates: P-TK1 ruling,
 rater-2, Zenodo token, diksa policy, journey go, 71 gold reviews. SDK gaps
 (FastMCP/mcp-legacy) are lanes' to install. 8801 squatter cleanup = owner
 call (not ours to kill). Disk 95% (3.9G free as of 2026-11-08) — pressure is outside our
 targets (projects 6.3G etc.); no deletions without owner eyes. Scholar
 N1/sessions mining, organism, Bayesian legitimacy, second ledgers/IDs,
 non-Trika expansion: all parked. pm2 scholar-memos crash-loop = scholar
 lane (flagged, not fixed).

## 9. File map (everything this system is)

 | Artifact | Where | Version |
 |---|---|---|
  | Gateway (parent server) | trika-x/formal-trika/tools/federation_gateway.py | stdio NDJSON; all 5 children live (115 tools 2026-11-14, scholar 41); serves formal__trace |
 | Children config | trika-x/formal-trika/data/federation-children.json | trika-federation-children/1 |
 | Gateway tests (11 GREEN incl. live trace, guide prefixes, catalog) | trika-x/formal-trika/tests/test_federation_gateway.py | — |
 | Trace compiler + verifier | trika-x/formal-trika/tools/trace_bundle.py | trika-trace/1 |
 | Trace spec | trika-x/formal-trika/TRACE-SPEC-2026-11-07.md | trika-trace/1 |
 | Trace tests (7 GREEN incl. negatives) | trika-x/formal-trika/tests/test_trace_bundle.py | — |
 | Example trace bundles (VERIFIED) | trika-x/formal-trika/data/traces/ | trika-trace/1 |
 | Contract pre-tests (GREEN) | trika-x/tools/federation_pretest.py | — |
 | Parent contract | trika-x/PARENT-CONTRACT-SPEC-2026-11-07.md | spec v1 → impl. status |
 | Formal MCP spec | trika-x/FORMAL-MCP-SPEC-2026-11-07.md | v3 implemented (7 tools) |
 | Machine catalog + probe | trika-x/tools/mcp_catalog.py, formal-trika/data/mcp-catalog.json | trika-mcp-catalog/1 |
 | MCP operations guide | trika-x/MCP-OPS.md | — |
 | Layer names + resolver + tests | trika-x/formal-trika/data/layer-names.json, tools/layer_names.py, tests/test_layer_names.py | trika-layer-names/1, 6 tests GREEN |
 | Layer adoption spec | trika-x/LAYER-NAMES-SPEC-2026-11-07.md | spec v1 |
 | Abhinavagupta seed + data | trika-x/formal-trika/tools/seed_abhinavagupta.py, data/abhinavagupta-corpus.json | seed:trika:abhinavagupta-corpus:1 |
 | Session log | trika-x/docs/log/PROCESS-NOTES-2026-11-07.md (§4–§4n) | dated entries |
 | Box DB (live) | postgres openpatala (555/909/102/87/1559/121/20/0) | replays from seeds (see §10) |
 | Openpatala API | :8821 (uvicorn, /tmp/openpatala-api-8821.log) | v1.0.0 |
 | Upstream code | prx0r/openpatala (wiggly), translation-work, svread, bookfactory, videofactory | lanes own; read-only here |
 | Proposals filed | videofactory#1 (ship/publish defaults) | their disposition |

## 10. Reproduce from scratch (the whole box state, no dumps needed)

 ```sh
 # DB (order matters; all idempotent, ON CONFLICT DO NOTHING)
 python3 trika-x/formal-trika/tools/openpatala_seed.py        # availability + gold dossiers
 python3 trika-x/formal-trika/tools/openpatala_ingest.py     # 87 ledgers -> works/editions/etexts/passages
 python3 trika-x/formal-trika/tools/seed_atlas_biblio.py --apply   # people/editions/translations (atlas)
 python3 trika-x/formal-trika/tools/seed_abhinavagupta.py --apply  # people/works/assertions/edition/translations (trika)
 # BB: re-key 17 passages + 6 edition/etext rows to tw workdirs (SQL in PROCESS-NOTES §4d)
 # API
 cd /root/openpatala && PYTHONPATH=. nohup python3 -m uvicorn patala.api:app --port 8821 --host 127.0.0.1 &
 # Gateway (one MCP entry for the agent)
 python3 trika-x/formal-trika/tools/federation_gateway.py   # FEDERATION_CONFIG override optional
 # Verify
 python3 trika-x/formal-trika/tools/evidence_check.py && python3 trika-x/formal-trika/tools/table.py --check \
  && python3 trika-x/formal-trika/tools/bridge_resolve.py --check --tw /root/translation-work \
  && python3 -m unittest discover -s trika-x/formal-trika/tests && curl -s 127.0.0.1:8821/health
 ```
