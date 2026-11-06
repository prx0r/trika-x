# Formal Trika runs — the track record

> **2026-11-06 review correction:** The table below is the original historical
> report, not evidence that the preregistered TK-C1/C2 or traditional
> classification has been established. See
> [correction](../PREREGISTRATION-2026-11-06.md) and
> [review](../../PEER-REVIEW-2026-11-06.md).

## Review rerun (Lean 4.34.1)

| Check | Result | Scope |
|---|---|---|
| `control/run.sh` | PASS | Four positive files plus two intended-false mutation controls; Boolean model only. |
| `recognition/run.sh` | PASS | Six positive files and six intended-false mutation controls; finite models only. |
| `python3 -m unittest discover -s formal-trika/tests -v` | PASS | Inventory status and fail-closed mutation-runner regressions. |
| Missing Lean negative control | PASS | Runner exits 2 before emitting any mutation PASS. |

This is a local rerun, not a signed or independently reproduced CI receipt.
The hand-written mutation models and the textual bridges still require review.

## Original historical report

Prereg: `PREREGISTRATION.md` (2026-11-05, before any code). Lean 4.34.1, no
dependencies for `control/`. Verdicts plain: PASS/FAIL/REFUTED, breaks required.

| Run | Kind | Verdict | Lean | Question |
|---|---|---|---|---|
| `control/` TK-C1 | control (known answer) | **PASS** | Mala/Pramatr/Kancuka/Recognition.lean | Do 3 mala axes generate the saptapramātṛ (8 combos → 7 well-formed, profile 2-3-1-2-1-2-0)? |
| `control/` TK-C2 | control (known failure) | **PASS** | Broken.lean (R1 deleted) | Does deleting R1 break the count? Yes — 8 ≠ 7, `decide` refuses. |
| `control/` P-TK2 | run | **PASS** | Kancuka.lean | 5 kañcukas, 5 distinct capacity-pairings? |
| `control/` P-TK3 | run | **PASS** | Recognition.lean | Does T_rec preserve content on all 64 states and land in ¬Sv(O)? |

Compression at control: 1 rule clause (R1) ÷ 7 rows ≈ 0.14 (P-TK4 holds).
P-TK1b confirmed structurally: the mantra-triad split is adhvan-positional,
not mala-compositional — flagged R, not derived.
