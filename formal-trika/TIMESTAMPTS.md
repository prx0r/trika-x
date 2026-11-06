# Timestamps — OpenTimestamps proofs on preregistrations

Each preregistration was stamped with `ots stamp` (hash-only leaves the box;
proofs complete on Bitcoin confirmation). Verify any time: `ots verify <file>.ots`.
Pending confirmations are normal — `ots upgrade` completes them.

| File | Stamped (UTC) | sha256 (first 16) | Status |
|---|---|---|---|
| PREREGISTRATION.md | 2026-11-06 08:00 | — | pending BTC |
| PREREGISTRATION-RECOGNITION.md | 2026-11-06 08:01 | — | pending BTC |
| PREREGISTRATION-2026-11-06.md | 2026-11-06 08:01 | — | pending BTC |
| PREREGISTRATION-ARMC.md | 2026-11-06 08:01 | — | pending BTC |
| PREREGISTRATION-DECODE-RUNG.md | 2026-11-06 08:01 | — | pending BTC |

The `.ots` receipts sit beside each file. After Bitcoin confirms, run
`ots upgrade <file>.ots` to embed the block-header path; then the proof is
self-contained and verifiable offline against any Bitcoin node.

Method note (from nibbanahelp's anchor system): OTS/Bitcoin attests via
SHA-256 proof-of-work (Grover halves to 128-bit — quantum-fair), not
signatures. A dead Bitcoin leaves the calendar receipts + block headers
checkable; plus we don't rely on it alone (ML-DSA + Nostr witnesses in
the nibbanahelp anchor stack cover the same principle).
