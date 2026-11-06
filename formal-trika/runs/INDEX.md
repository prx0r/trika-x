# Formal Trika runs — the track record

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
