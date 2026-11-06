# Amendment — E-AVAR redesign (chain tautology found by the mutant)

**Date:** 2026-11-06, same session, BEFORE any recorded run. This amends
PREREGISTRATION-AVARANA-RUNG.md (not edited) — the prereg's E-AVAR1–3
assumed the ladder list itself could bear the check. It cannot:

**Finding:** as first written, `covers` read positions from the same
`ladder` list that `links` enumerates — so `chain_linked` held for ANY
ordering (tautological). The BrokenAvarana twin (swap two groups) did
not fail at `chain_linked`; `must_fail.py` correctly rejected the twin
for not isolating the named proposition. The instrument worked; the
rung design was wrong. No PASS was recorded; nothing to correct downstream.

**Redesign (implemented):** `covers` derives from an INDEPENDENT rule —
course-rank ascent (gross 0 < subtle 1 < mind 2 < impure 3 < pure 4),
grounded in the v3–v22 magnitude ladder, not in the list order. This
reveals the genuine textual shape: the ladder is PARTIALLY ordered
(sense/action/mind/intellect/ego/nature share course .mind; v23 does not
rank within a course). New predictions replace E-AVAR1–3:

| ID | Prediction | Confidence |
|---|---|---|
| E-AVAR1r | `course_ascends`: every cross-course adjacent pair strictly ascends in rank. | 0.8 |
| E-AVAR2r | `partial_order_honest`: an intra-course adjacent pair exists (underdetermination exhibited in-model, not forced). | 0.85 |
| E-AVAR3r | BrokenAvarana (covering↔purePrinciple swap) fails `course_ascends` and ONLY it. | 0.85 |

Kill rules and scope from the original prereg stand. The v9 embedding
rule remains the designed size-key rung.
