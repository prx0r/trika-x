# FORMAL-MCP SPEC — trika-x read-only tools (spec v1, 2026-11-07)

 Status: SPEC (no server code yet). All tools read-only, deterministic,
 fail-closed. No Lean writes, no EVIDENCE writes, no translation-work writes
 via MCP. Machine proposes, human disposes. Tiers ride every claim (T/R/E/
 C/H/X); R never promotes itself; only `decide` proves (inside its finite
 scope).

## Tools

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

Static: tool names prefixed `formal__`, no banned substrings (ship/render/
publish/grant/sign), schemas frozen. Live: spot-check `formal__bridge
chunk:tsa08-p03` → dossier + UNPINNED; `formal__gaps` → same 13/154 covered
set as `evidence_check`; unknown chunk → clean error.
