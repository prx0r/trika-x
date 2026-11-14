# FORMAL-MCP SPEC — trika-x read-only tools (v3, 2026-11-08)
*Status: CANONICAL. v3 implemented; counts verified live. (2026-11-14.)

 Status: IMPLEMENTED — all seven tools live on the federation gateway
 (`formal__trace|bridge|evidence|table|gaps|runs|axioms`). Verified by
 `formal-trika/tests/test_federation_gateway.py::test_formal_tool_family`
 (every tool listed + answers; unknown chunk fails closed; witness stays
 UNPINNED) and by the machine catalog `formal-trika/data/mcp-catalog.json`
 (regenerate: `tools/mcp_catalog.py --write`; gate: `--check`).
 All tools read-only, deterministic, fail-closed. No Lean writes, no EVIDENCE
 writes, no translation-work writes via MCP. Machine proposes, human disposes.
 Tiers ride every claim (T/R/E/C/H/X); R never promotes itself; only `decide`
 proves (inside its finite scope).

## Tools

0. `formal__trace {work, target}` → LIVE. Full
   trika-trace/1 bundle for one chunk: source bytes hash, layer hashes,
   proof results, formal theorems (MODEL_CHECKED, in-scope only), citing
   essays (verbatim mention only). Verdict COMPLETE/PARTIAL + named gaps;
   BLOCKED stays BLOCKED. Unknown chunk → clean error. Backend:
   formal-trika/tools/trace_bundle.py (read-only; --verify re-checks).

1. `formal__bridge {chunk}` → work/edition/etext rows for a chunk locator
   (wraps `bridge_resolve.py chunk:X [--db]`). Returns locator, ledger sha,
   snapshot match (`SNAPSHOT_ONLY` without `--tw`, `BYTES_MATCH_SNAPSHOT`
   with clean tree), openpatala candidate block, `witness: UNPINNED` always.
   Unknown/invented/stale/ambiguous locators → error, never prefix-resolve.
2. `formal__evidence {theorem?}` → EVIDENCE rows (chunk locators, tier, run
   ref). Unknown theorem → list head + counts. Registry refs are NOT
   source-to-theorem entailments (labelled as such).
3. `formal__table {file?}` → TABLE readings (plain-English scope notes).
   Every theorem carries its `MODEL_CHECKED`-only scope; doctrine claims
   are out of scope by contract.
4. `formal__gaps {work?}` → Treeka formal column: per-passage
   `formalized / armed / unarmed` + gap lists (unargued, cruxless,
   essayless, unformalized) + ambiguous locators. This output IS the rung
   queue (gap-list order wins, never taste).
5. `formal__runs {run?}` → runs ledger verdicts
   (PASS/REFUTED/UNRESOLVED/PENDING) + receipts. No reruns via MCP.
6. `formal__axioms {}` → axiom audit state (CLEAN + file count + forbidden
   markers scanned). Kernel verdict still needs pinned Lean (4.34.1);
   static CLEAN ≠ proof.

## Gates (each tool)

- Invalid locator/work/theorem → `ValueError`, never empty success.
- Dirty tree or snapshot mismatch → `BYTES_MATCH` withheld, snapshot rev
  + dirty flag reported.
- Witness/edition fields → `CANDIDATE`/`UNPINNED`, never invented sigla.
- Timeouts/blocks/empties → ERROR, never data.

## Non-tools (never exposed)

`record_run`, `table` regen, `build_passage_snapshot`, `mutate_sweep`,
anything writing EVIDENCE/TABLE/runs/ledgers, anything invoking Lean with
write flags, anything touching translation-work/ipvv/svread repos.

## Acceptance

Static: tool names prefixed `formal__`, no banned action names (exact/prefix
match, never substring — `list_published_essays` is read-only and allowed),
schemas frozen. Live: `formal__bridge chunk:tsa08-p03` → dossier + UNPINNED;
`formal__gaps` → same 13/154 covered set as `evidence_check`; unknown chunk →
clean error. Machine catalog: 115 tools across 8 families (2026-11-14),
`mcp_catalog.py --check` SHARP.
