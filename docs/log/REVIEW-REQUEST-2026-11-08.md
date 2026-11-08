# REVIEW REQUEST — lead agent review (2026-11-08 evening)

**Scope:** 19 commits on `box/peer-review-batch` since `2c83925` (2026-11-07
process-notes + ROADMAP) through `649f42e`, now pushed to
`origin/box/peer-review-batch`, plus 3 new tags. PR diff is context; THIS file
is the ask. Everything below is what I am unsure about or suspect is flawed.
No defense offered; dispose freely.

## What was built (my claims — verify, do not trust)

1. **MCP hardening (M01–M05):** gateway serves 104 tools / 8 families; docs
   corrected (FORMAL-MCP v3, PARENT-CONTRACT prefixes, 98→104 counts);
   `tools/mcp_catalog.py` drift gate; 3 new gateway tests; `../../../MCP-OPS.md`.
   Claimed: 79 tests green, pretest GREEN, catalog SHARP.
2. **Corpus traces (Q05):** `trace_all.py` compiled 909 bundles (236 COMPLETE /
   673 PARTIAL), 0 errors, 4.2MB. Claimed: two samples re-verified.
3. **Freshness ledger:** every canonical number carries command + sha256;
   `--check` SHARP. Disk moved to context (non-gating).
4. **Rungs (Q08, N05, N06):** P-PHR4/P-PHR5 (phr-p05), P-VBT1 (8 forms),
   P-VBT2 (3 coords). Claimed: Lean compiles, 4 twins refuse, harness
   receipts `ab5dfcc` and `247d897` both exit 0/0/0. Coverage 16/154 (10%).
5. **Treeka (Q11):** refreshed index (refs 5→16 chunks), `treeka_report.py`
   + 3 tests. Claimed the committed index was stale and is now caught up.
6. **Propose pilot (Q13):** queue refreshed (882); one crux drafted
   (qwen3-30b) → audit → PUSHBACK (mistral-small); proposal only.
7. **Peer-review debt (Q14):** disposition ledger for LEAD 7 + REVIEW-REQUEST
   16 — recorder, not ruler.
8. **Disk (Q01):** +2.4G reclaimed (3 deletions, freeze-first, 1 skip with
   reason). No history rewritten (one amended-then-fixed commit disclosed
   in process notes: ochema gitlink caught and repaired pre-push).
9. **Northstar (N01–N10):** `essay_derive.py` chain audit (6/6 PARTIAL,
   0 BROKEN); chunk↔verse 23 CLOSED / 64 OPEN; decision audit 1/87 + 0/87;
   7 review packets queued.

## Method questions (need your ruling)

1. **Roster semantics:** P-PHR4/P-PHR5/P-VBT1/P-VBT2 are count-facts over
   held L2/ARGMAP/C1 text. Is this formalisation or bookkeeping? Does the
   `MODEL_CHECKED`-only contract hold, or am I smuggling interpretation?
2. **Twin quality:** each twin is a single roster deletion. Meaningful
   perturbation or self-graded ritual? (Second-encoder review still owed —
   say so if that blocks promotion.)
3. **`essay_derive` verdict rule:** explicit UNMAPPED = PARTIAL, missing =
   BROKEN. Right line, or too generous?
4. **Duplicate-map deletion:** 23 regenerated chunk↔verse files were
   byte-identical to the 11-06 versions — I deleted the reruns. Correct,
   or should regeneration be committed with dates?
5. **Treeka refresh honesty:** the committed index lacked refs that EVIDENCE
   already had. I called it stale and refreshed. Could the refresh instead
   be masking a regression in how refs are matched?
6. **Rung velocity vs depth:** 5 theorems in one session, all finite counts.
   Is this the right shape of progress, or count-fact theatre while the
   doctrine stands untouched?
7. **The rejected variant:** "p02 negates the 8 p01 terms" killed on held
   spans and recorded. Right call? Is the weaker P-VBT2 (3 coords) banked
   well enough, or is compound-splitting my own parsing?
8. **Push safety:** 19 commits + 3 tags pushed after a clean secrets scan.
   Anything in the pushed tree that should not be public?

## What I did NOT do (confirm these were right to leave)

- No svread-lane writes (909 packs unpublished there). No translation-work
  writes. No witness invention. No signoffs. No history edits. No disk
  deletions beyond the approved Tier 1. No quota spend beyond free rails.

## Roundup awaiting review (all lanes)

- trika-x: this 19-commit session + this packet (OPEN).
- Blocked on humans (unchanged): P-TK1, rater-2, ti/ca, NGMPP, Zenodo token,
  dīkṣā policy, cron install, token rotation.
