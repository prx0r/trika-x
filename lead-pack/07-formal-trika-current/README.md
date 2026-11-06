# 07 — Formal-trika current state (checked 2026-11-06, Lean 4.34.1)

Toolchain: `/root/.elan` (4.34.1). Zero dependencies for `control/`. Prereg before code (`../PREREGISTRATION.md` P-TK1–4 + kill criteria; `../PREREGISTRATION-RECOGNITION.md` R-REC1–8).

## Control (GREEN — verified today)

- `control/Mala.lean` — 3 malas inductive, `count_3`
- `control/Pramatr.lean` — 3 binary axes → 8 combos; R1 (no free-floating karma) → 7 well-formed; profile `[2,3,1,2,1,2,0]`
- `control/Broken.lean` — R1 deleted → `seven` MUST fail (does fail — instrument not blind)
- `control/Kancuka.lean` — 5 coverings, 5 distinct capacity-pairings (P-TK2)
- `control/Recognition.lean` — AM0 σ-flip over 64 states: content preserved, always lands ¬Sv(O), adds nothing (P-TK3)
- `control/run.sh` — C1-must-check / C2-must-fail harness. Today: **TK-C1 PASS, TK-C2 PASS**
- Compression at control: 1 rule clause ÷ 7 rows ≈ 0.14 (P-TK4 holds). P-TK1b confirmed structurally (mantra-triad split is adhvan-positional R, not mala-compositional).

## Recognition rungs (4 GREEN, 2 RED — verified today per-file)

| File | Predictions | Today |
|---|---|---|
| `recognition/Transitions.lean` | R-REC1 (4096-state σ-laws: embodiment kept, bondage cleared, limitation retained, idempotent) + R-REC2 (mala pathologies: stuck / content-rewrite / self-loop, each distinct from T_rec) | **CHECK** |
| `recognition/NonEntail.lean` | R-REC3 (A⇏B⇏C⇏D⇏E⇏F, six one-step + A..E-without-F witnesses) + R-REC4 (V₁–V₇ independence 128, U non-transitive, no-global-section) | **CHECK** |
| `recognition/Conjuncts.lean` | R-REC5 (recognition unique 1/16, 4 drop-one theorems, misidentification) + R-REC6 (Part coherent, PI-independent, Śiva-requires-S) + R-REC8 (unus-ambo exhibit) | **CHECK** |
| `recognition/Memory.lean` | R-REC7 (M₄ requires M₁–M₃, M₄⇏M₅, sees-without-enacts exists, no enacts-without-sees) | **CHECK** |
| `recognition/Tractatus.lean` | observer O, Rec_1/Rec_2/FullRec hierarchy, layers L1–L4, T13 bound, path fork | **FAIL — syntax**: L77 `structure Layers where l1 : Bool l2 : Bool…` one-line fields don't parse; L31 `([0,1] : List (Fin 2))` literal; L86 `∀ f : Fin 2 → Fin 4` undecidable `∃`. Fix: multiline fields, explicit `(0 : Fin 2)`, Decidable/Fintype framing |
| `recognition/Coords.lean` | kañcuka→coordinate bijection + agent finitude | **FAIL — logic**: L67 `no_unrestricted_perspective` claims 0 violations but `decide` refutes (the `(persp,¬restr)` agent IS the 1 violation). Fix: assert `= 1` |
| Broken twins (`BrokenTrans/NonEntail/Conjuncts/Memory/Reach/Coords.lean`) | each MUST fail | **6/6 must-fail OK** (instrument not blind) |
| `recognition/run.sh` | all-must-check + all-must-fail | **10 passed, 2 failed** ( = 4 check + 6 mustfail OK vs 2 check FAIL) |
| `tools/emit_keys.py` | Lean counts → JSON keys (hashes) for qp evidence + cg oracle | exists, unrun this session |
| `runs/INDEX.md` | verdict ledger | **STALE — lists control only**; recognition rungs unrecorded. Lead agent: append rows per file above |

## Scope discipline

Every theorem carries its model size (64/4096/128…). A theorem about the finite model is not a theorem about minds. Heuristic scores never cited as proof — only `decide`.
