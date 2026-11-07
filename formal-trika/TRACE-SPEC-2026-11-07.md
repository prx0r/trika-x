# TRACE SPEC — trika-trace/1: one Sanskrit passage, fully traceable (2026-11-07)

 Status: SPEC + reference implementation (trika-x only). Reads translation-work,
 openpatala box DB, trika-x EVIDENCE, svread projections. Writes NOTHING outside
 trika-x/formal-trika/data/traces/. Never invents: missing links are UNKNOWN,
 mismatches are FAIL. Machine proposes, human disposes.

## Why (owner's words, kept separate)

 Formalise from the Sanskrit upwards so ChatGPT etc. can trace it: every claim
 an agent answers with must resolve down to source bytes through recorded,
 re-checkable hops — never a bare citation, never a laundered PASS.

## The chain (each hop: bytes + hash + status + where to re-fetch)

 0. chunk identity — work (translation-work dir), locator (passages.jsonl,
    exact match only), immutable_id (pt:pid:...). Unknown/invented locators
    are rejected, never prefix-resolved (bridge law).
 1. source — ledger `sanskrit` field bytes (sha256 recorded) + SOURCE.sha /
    source/record.json cross-check when present (match = BOUND, absent =
    UNKNOWN with reason, mismatch = FAIL). Edition label + status
    (CANDIDATE until collated), witness UNPINNED until manuscript eyes.
 2. openpatala identity — box DB rows keyed by immutable_id
    (passages.id), plus work editions/etexts. Missing rows = UNRESOLVED
    (never auto-created). Witnesses 0 box-wide (stated, not hidden).
 3. layers — per-song data/<song>.<layer>.json content hashes (t1, l0,
    argmap, l2, c1, l3, l4, c2 as present). Missing layer = UNKNOWN for
    that layer, never assumed from neighbours.
 4. proofs — proof/proof-<song>.json (deterministic_gate per chunk where
    present) + GATE.json chunk entries. PASS/BLOCKED recorded verbatim;
    BLOCKED stays blocking; no heuristic PASS is semantic proof.
 5. formal — EVIDENCE.json entries citing the locator (theorem id,
    kind KEY/RULE/..., via, tier, status) + runs-ledger rev. MODEL_CHECKED
    only inside the stated finite scope; KEY rows are counts, not proofs.
 6. essays — scholar projection essays whose TEXT contains the locator
    (verbatim mention only — NOT claim support; claim support needs
    essay-claim/1 + audit, a different tool). Author, rights, signoff state
    recorded as-is (SELF_ATTESTED ≠ reviewed ≠ verified).

 ## Verdict rules (fail-closed)

 - COMPLETE iff every applicable hop is BOUND/PASS/CHECKED (or explicitly
   not-applicable with reason, e.g. no C2 authored).
 - PARTIAL with named UNKNOWNS otherwise. Missing data is never filled by
   analogy, neighbouring passages, or model guess.
 - --verify re-runs every hash read + gate lookup against the live files and
   diffs the bundle: any byte change, changed gate, or changed mapping =
   FAIL (exit non-zero) with the first divergence named. Changed upstream
   bytes make downstream approvals stale — recorded, never auto-healed.

 ## Non-goals

 No new IDs (immutable_id + work:locator stay canonical), no writes to other
 repos' files or DB schemas, no training signal, no legitimacy beyond what
 each hop's own gate establishes. The bundle is a compiler of existing
 receipts, not a new authority.
