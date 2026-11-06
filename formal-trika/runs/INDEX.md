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

This table records the local rerun; the PR also runs the checks on GitHub
Actions. Neither is a signed release receipt. The hand-written mutation
models and the textual bridges still require review.

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

## Arm B — decode rung (2026-11-06, box agent; prereg PREREGISTRATION-DECODE-RUNG.md committed before code)

Toolchain: Lean 4.34.1, `run.sh` harnesses (warnings as errors, must_fail with
same-statement mutants). Statistics: stdlib Fisher exact over vendored
`formal-trika/data/day-*.jsonl` (144 moments, days 1–7 lived decodes,
machine-proposed, owner-unreviewed; no diary verbatim vendored).

| Run | Kind | Verdict | Lean / tool | Question |
|---|---|---|---|---|
| `recognition/` F-CORR | run | **PASS** | KancukaCorr.lean (7 felt markers → 5 coords, partial) | Correspondence consistent? Firm rows pull→va, stall→ac, doubt→kn? |
| `recognition/` F-CORR-mutant | control (known failure) | **PASS** | BrokenCorr.lean (pull mis-mapped) | Does the mis-map refuse `corr_pull_raga`? Yes. |
| `recognition/` F-GRACE | run | **PASS** | Grace.lean (flip ↔ ready ∧ grace, 4 states) | Readiness/grace each necessary, jointly sufficient? |
| `recognition/` F-GRACE-mutant | control (known failure) | **PASS** | BrokenGrace.lean (transition severed) | Does the severed model refuse `flip_iff_ready_and_grace`? Yes — exactly one error at the named proposition (harness rejects multi-error mutants; conjunct-drop variants break 3 theorems, recorded here not in CI). |
| `recognition/` F-UPAYA | run | **PASS** | Upaya.lean (śāmbhava 1-step, śākta+pure, āṇava n≥2) | Three means distinct? Orderings recorded as found (āṇava, śākta ⊆ śāmbhava reach). |
| `recognition/` F-UPAYA-mutant | control (known failure) | **PASS** | BrokenUpaya.lean (purity dropped) | Does the dropped precondition refuse `sakta_needs_purity`? Yes. |
| T-C1 | pilot stat | **HOLDS** | tools/tc1_cooccurrence.py, p=0.0462 one-sided, 26 arcs | lobha-headline arcs co-occur with thina/churn-headline arcs above chance? 3/3 thin arcs carry lobha; thin never without lobha. n=26, single diarist — pilot only. |
| T-C4 | pilot audit | **HOLDS** | TREC-AUDIT-DAY1-7.md | Claimed-recognition (3×3/4) vs state-craving (0/4)? Separation holds, n=4. S=0 throughout (no stabilization evidence yet). |
| T-C3 | pilot audit | **KEPT** | GRACE-AUDIT-DAY1-7.md | 5/5 grace-clauses keep the variable (residual unconditioned step). Kill not triggered. |
| T-C2 | agreement | **UNRESOLVED** | UPAYA-CRITERIA.md | Rater-1 pass recorded; rater-2 pending (need ≥0.6). |
| F-CORR coverage | run | **PARTIAL** | `coverage_partial` (3/5 coords) | ti (time) and ca (placedness) felt signatures unestablished — explicit nones, not forces. Full coverage NOT claimed. |

Harness totals at this commit: control green (incl. BrokenKancuka), recognition
18/18 (9 check + 9 mustfail). New-rung prereg preceded code in-commit-order
(prereg commit, then model commits). Nothing here is a publication gate;
inventory stays NOT_RUN per the PR's evidence boundary.

## Arm C — sharpness (2026-11-06, box agent; prereg PREREGISTRATION-ARMC.md committed before verification)

Machine receipt: `runs/runs.jsonl` (rev-pinned; all green at arm-C HEAD).
M-KEY: AnswerKey collates 5 tradition figures (5 kañcukas / 36 tattvas /
7 experients / 5 followers / 112 dhāraṇās) with per-figure status; excluded
list names our constructs. HOLDS.
M-BLIND: `vocab.py` extracts 26 types into a Lean-checking Vocab.lean;
BLIND.md + T-C2-RATER2-SHEET ready; no blind run yet (lead-agent work). HOLDS (instrument).
M-TABLE: TABLE.md covers all 76 theorems incl. 2 marked scaffolds, with
hand plain-English readings; `table.py --check` green. HOLDS.
M-LEDGER: record_run.py appends rev-pinned harness exits (this section cites it). HOLDS.
M-GREEN: control (incl. AnswerKey) + recognition 18/18 + test_tools 4/4 + vocab/table checks + tc1 hold. HOLDS.
R13 tightened per books (root lobha/dosa; nibbanahelp check_factors, re-verified, no decode breakage).
Thon-pattern audit: KancukaCorr.corr rows stay KEY (stipulated + evidence-pinned, never derived);
`unverifiedProposedLabel` stays provisional; thina/middha root-link gap closed in the linter.

## Arm D — evidence chain (2026-11-06, box agent; branch arm-d-evidence-chain)

Formalization as the root of the argument tree: EVIDENCE.json pins every
theorem (74) or exemption (2 scaffolds) to chunk locators + R-sources +
lived decodes. `tools/evidence_check.py`: 22/22 chunk refs resolve against
translation-work passages.jsonl; coverage 7/45 gold chunks (15%) with the
38-chunk gap list = Treeka formal-column seed. TEACHER-INTERFACE.md specs
the assessor's contract (response discipline + build order); nothing there
is built. No PR stacked: this branch waits until PR #2 is reviewed.

## Machine receipts (generated by tools/runs-index.py — never edit by hand)

| At (UTC) | Rev | Lean | control | recognition | tc1 |
|---|---|---|---|---|---|
| 2026-11-06T04:42:19+00:00 | `1beb665` | 4.34.1 | OK | OK | OK |
| 2026-11-06T08:29:09+00:00 | `93dbf7a` | 4.34.1 | OK | OK | OK |
| 2026-11-06T09:10:45+00:00 | `93dbf7a` | 4.34.1 | OK | OK | OK |
| 2026-11-06T09:14:35+00:00 | `93dbf7a+` | 4.34.1 | OK | OK | OK |
| 2026-11-06T09:22:07+00:00 | `93dbf7a+` | 4.34.1 | OK | OK | OK |
| 2026-11-06T09:38:14+00:00 | `77bcdf4+` | 4.34.1 | OK | OK | OK |
| 2026-11-06T09:49:32+00:00 | `77bcdf4+` | 4.34.1 | OK | OK | OK |
| 2026-11-06T09:52:38+00:00 | `77bcdf4+` | 4.34.1 | OK | OK | OK |
| 2026-11-06T09:55:57+00:00 | `77bcdf4+` | 4.34.1 | OK | OK | OK |
| 2026-11-06T10:14:23+00:00 | `de6cb8a+` | 4.34.1 | OK | OK | OK |
| 2026-11-06T10:32:57+00:00 | `cce66a0+` | 4.34.1 | OK | OK | OK |
| 2026-11-06T10:35:16+00:00 | `cce66a0+` | 4.34.1 | OK | OK | OK |
| 2026-11-06T10:47:36+00:00 | `946ce3e+` | 4.34.1 | OK | OK | OK |
| 2026-11-06T10:57:19+00:00 | `9073a25+` | 4.34.1 | OK | OK | OK |
| 2026-11-06T11:22:45+00:00 | `90bec35+` | 4.34.1 | OK | OK | OK |
| 2026-11-06T11:28:58+00:00 | `c49096d+` | 4.34.1 | OK | OK | OK |
| 2026-11-06T11:37:13+00:00 | `7f0e4c3+` | 4.34.1 | OK | OK | OK |
| 2026-11-06T11:49:23+00:00 | `f6acafd+` | 4.34.1 | OK | OK | OK |
| 2026-11-06T12:04:18+00:00 | `64a11ec+` | 4.34.1 | OK | OK | OK |
| 2026-11-06T13:02:11+00:00 | `15120ae+` | 4.34.1 | OK | OK | OK |
| 2026-11-06T13:13:25+00:00 | `1f4c26e` | 4.34.1 | OK | OK | OK |
| 2026-11-06T13:45:41+00:00 | `d2db81c+` | 4.34.1 | OK | OK | OK |
| 2026-11-06T13:57:12+00:00 | `4ea4934+` | 4.34.1 | OK | OK | OK |
| 2026-11-06T14:00:22+00:00 | `4ea4934+` | 4.34.1 | OK | OK | OK |
| 2026-11-06T14:04:10+00:00 | `89ca3f2+` | 4.34.1 | OK | OK | OK |
| 2026-11-06T14:07:41+00:00 | `3512b5a+` | 4.34.1 | OK | OK | OK |
| 2026-11-06T14:35:18+00:00 | `7777074` | 4.34.1 | OK | OK | OK |

Exit 0 = all harnesses green at that rev. Generated from runs/runs.jsonl; edit that file, never this table.
