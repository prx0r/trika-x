# JOURNEY NOTE — trajectory surface, explicitly gated (2026-11-06)

**Status:** SPEC ONLY. No code, no ledger, no UI. Builds only on explicit
owner go (NEXT-STEPS 3.7). This note scopes what a journey would record so
the decision is concrete.

## What exists today that a journey would order

CRUX-WALKTHROUGH-01 (rāga↔lobha) → 02 (ego) → 03 (wombed faculties). Each is
already a trajectory entry in prose: chunk → formal → argument → essay →
PUSHBACK → honest remainder. A journey-ledger would be the ORDERED SET of
these receipts plus their kill conditions and revival triggers — nothing more.

## Proposed ledger shape (for owner review, not implementation)

- `journey.jsonl`: one row per walkthrough `{id, date, crux, chunks[],
  theorems[], claim_table_sha, pushback_models[], remainder[], kills[]}`.
- Trajectory queries it must answer: what did we claim, what killed it,
  what would revive it. No new IDs (reuses locators + theorem keys + shas).
- vis-mode / jev / trajectory rendering: gated separately; ledger first,
  rendering only if the ledger proves useful for 90 days.

## Explicit non-goals (even after go)

No auto-advance (ledger never promotes tiers), no diary ingestion without
consent re-confirmation, no scholar-facing surface until P-TK1 rules land.
The ledger records; humans dispose — same law.
