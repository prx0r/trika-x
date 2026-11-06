# Peer review: formal Trika inside the evidence system

**Verdict: useful finite-model experiments; not ready to authorize publication or to describe as machine-checked doctrine.** The proof repairs and stricter test runner in this PR are reviewable now. The source bridge, receipt hardening, human interpretation and integration described below are **not implemented by this PR**. Do not use the generated inventory as proof or a publication gate.

## Scope and reproducible snapshots

Review base: [trika-x `817ca21`](https://github.com/prx0r/trika-x/tree/817ca21eb29d620d27580babc05cd92364633556); [translation-work `e05e640`](https://github.com/prx0r/translation-work/tree/e05e640e192a2ea5a317ba76b0f802f4f54e98cc); [IPVV `48f2a5c`](https://github.com/prx0r/ipvv/tree/48f2a5c5fc757c3b620b0216c0901f519875d3e4); [svread `e437503`](https://github.com/prx0r/svread/tree/e437503dea6478a94538d5569d2bf0c5d0a1a074); [sanskritbench `7bd466d`](https://github.com/prx0r/sanskritbench/tree/7bd466dc2d509b8d15b995e531ecacc6b942f949); [openpatala `4147a19`](https://github.com/prx0r/openpatala/tree/4147a198d4d91acca2784cca9865ef02c1d7970f); [gochema `8a9422e`](https://github.com/prx0r/gochema/tree/8a9422e851e9f587a64ba9c3b1800ddf2a0c71d7); and [cg `e374b0b`](https://github.com/prx0r/cg/tree/e374b0b4d9f454ab32b3ac9480581c82d9adb82e). These are repository versions inspected, not source-edition pins or claims that every subsystem is production-tested. This was a code and architecture review, not a complete Sanskritist review of the corpus, production audit, or review of every repository listed in the vision.

## Findings and dispositions

### P0 · Unchecked inventory was labeled checked — fixed here

The original `formal-trika/tools/emit_keys.py` unconditionally emitted `decide-checked`, even with Lean absent. It hashed files but never ran Lean or resolved/pinned the quoted source documents. Several “theorems” were grouped labels, not Lean declaration names. An integrator could mistake an inventory row for proof.

The exporter now uses a new, incompatible `trika-recognition-unverified-inventory/2` format: `verification: NOT_RUN`, `source_pins: UNRESOLVED`, `integration_ready: false`, and `NOT_CHECKED` for every entry. Its source descriptions are unverified notes and are not authority to promote a reconstruction to textual evidence. Nothing consumes this output as a gate in this PR.

### P0 · Mutant failures were counted for the wrong reason — fixed here, with a residual limit

Both old shell runners treated any nonzero exit as an expected failure; missing Lean, a parser error or a crash could be reported as a passing negative control. They now require Lean 4.34.1 and the expected `decide`-proved-false diagnostic at the named theorem, in the named mutant, on the proof line, with the same theorem statement as the positive version. Other errors, changed theorem statements, missing executables, timeouts and extra errors fail closed. Warnings are errors during checking, including Lean's warning for `sorry`.

The mutant models remain hand-written: matching statements and the intended false result **do not prove that only the intended definition changed**. Review each model difference, and eventually generate the mutation mechanically or verify its complete diff. The script also assumes a trusted Lean executable: a version string alone does not attest the binary. A proof artifact intended for publication must enumerate each theorem's axioms and reject `sorryAx` and unapproved axioms.

### P0 · qprivately receipts do not yet provide the promised integration boundary — follow-up in IPVV

At the pinned [receipts.py](https://github.com/prx0r/ipvv/blob/48f2a5c5fc757c3b620b0216c0901f519875d3e4/tools/qp_acom/receipts.py):

- `transition(..., gate_ids=[])` reports `passed: true` and calls `apply`; `settle` also accepts an empty gate list. This was reproduced with no evidence and a changed state. The vision's unconditional “no ungated transitions” claim does not hold at this kernel interface.
- `settle(receipt, evidence)` reruns gate predicates but does not compare the supplied evidence to the receipt's `evidence_root`. A receipt created from one fresh evidence item settled successfully with a different fresh item. The root itself is currently built from evidence IDs, not independently verified canonical evidence bytes.
- `verify_receipt` permits an absent signer, and signature verification alone cannot establish that a signer has the required role. A receipt ID is a truncated 16-hex-character SHA-256 prefix; the signature binds that ID, not a full-length digest. These are kernel behaviors, not evidence that a particular deployed publishing route is exploitable.
- Gate results do not carry the registered `program_hash`; settlement does not verify that a mandatory gate set and exact predicate versions were the ones executed, or independently recompute the authorized post-state.

**Required follow-up:** the authority/publishing boundary must resolve the nonempty required gate set from trusted, versioned policy (never caller choice), pin each program hash, authenticate and re-hash canonical evidence bytes, compare their root, verify an authorized signature over a versioned full-length receipt digest, bind/replay the intended state transition and prevent replay. Preserve old receipt verification under its original protocol; do not silently reinterpret its truncated IDs as full hashes. Add negative tests for empty/omitted/unknown gates, swapped or altered evidence, changed gate code, unsigned or untrusted signer, wrong role, stale input and a mismatched post-state. No IPVV files are changed here.

### P0 · cg runs and gates are not yet proof-grade — follow-up in cg

The proposed evolution-lab connection must not treat a current cg run ID as
an attestation of a Lean result. In pinned [runner.py](https://github.com/prx0r/cg/blob/e374b0b4d9f454ab32b3ac9480581c82d9adb82e/cogym_kernel/kernel/runner.py), the fallback event hash commits to the step and action ID, but not the executor result. `ActionResult` does not supply a `receipt_hash`; `RunReceipt.run_id` in [contracts.py](https://github.com/prx0r/cg/blob/e374b0b4d9f454ab32b3ac9480581c82d9adb82e/cogym_kernel/kernel/contracts.py) also excludes metrics. Two real local executions with identical action/seed/spec but different executor output and scores produced **the same run ID**. This is not proof of deterministic replay.

In [loop.py](https://github.com/prx0r/cg/blob/e374b0b4d9f454ab32b3ac9480581c82d9adb82e/cogym_kernel/evo/loop.py), an empty suite yields `gate_ok: true` because `all([])` is true; reproduced directly. The configured `gates_value` is not used by that comparison. In [ids.py](https://github.com/prx0r/cg/blob/e374b0b4d9f454ab32b3ac9480581c82d9adb82e/cogym_kernel/kernel/ids.py), installing optional `blake3` changes the algorithm from SHA-256 without changing the ID prefix, so identical inputs can have different IDs across environments. Finally, `policy.initialize(world.world_spec)` receives the `oracle_hash` despite the evaluator-only comment; this exposes the hash, not necessarily the oracle contents.

**Required follow-up:** reject empty suites, enforce the declared gate policy, bind canonical action results and scored outputs to a versioned, algorithm-labeled run digest, and verify replay against those bytes. Keep oracle metadata out of policy-facing inputs if evaluator-only separation is required. Test changed executor output, score, oracle, compiler and gate version; missing `blake3`; empty suite; and replay mismatch. Keep historical IDs readable under their original rules rather than silently changing their meaning. No cg files are changed here.

### P1 · Scholar's “current” is not authenticated evidence — follow-up in svread

The [Scholar claim table](https://github.com/prx0r/svread/blob/e437503dea6478a94538d5569d2bf0c5d0a1a074/mcp/claims.py) is explicitly advisory, which is good: it makes no claim of entailment, review or signature. However, `link` accepts caller-supplied `source_revs` and marks a marker `CURRENT` even if it does not resolve to a chunk. `check_stale` retains that state when no current source revision can be fetched. Reproduced with an arbitrary revision and an empty current revision map. This is not a finding that the existing publisher accepts it as authorization; it is a reason not to use it as one.

**Required follow-up:** resolve revisions from a trusted source registry and return `UNRESOLVED`/`UNKNOWN` when unavailable, while retaining the recorded revision for history. Verify the actual referenced bytes and permissions, then invalidate links and revision-specific sign-offs when dependencies change. Test fabricated markers, missing/revoked sources, changed bytes under an ID, stale essay text and source version changes. Keep the existing `audit.py` distinction: quotation match is not entailment or peer review.

### P1 · Seven Boolean rows are not seven textual persons — corrected labeling, open scholarly work

`control/Pramatr.lean` generates eight bit patterns and excludes one by a proposed rule. That proves an arithmetic result about its definitions; it does **not** establish a bijection with the textual seven. The purported positional distinction between the mantra classes is not represented by three mala bits. The old optional `traditionalName` omitted Mantramaheśa and included an additional proposed transitional label; it has been renamed `unverifiedProposedLabel` so it is not exposed as an established classification.

The immutable [original preregistration](formal-trika/PREREGISTRATION.md) also simultaneously says “seven named + Śiva = eight” and includes Śiva in its list of seven. [Tantrasāra a09's argument map](https://github.com/prx0r/translation-work/blob/e05e640e192a2ea5a317ba76b0f802f4f54e98cc/tantrasara-a09/data/tsa-a09.argmap.json) lists seven including Śiva and Mantramaheśa; compare the [GRETIL Tantrasāra](https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/html/sa_abhinavagupta-tantrasAra.htm). The translation-work source record still marks the OpenPāṭala mapping and edition as candidate and the witness as unknown; its rights field records a noncommercial source. A scholar must check the edition, passage, witnesses, rights and model-to-text mapping. Do not replace the bit labels with an unreviewed “correct” mapping.

The preregistered TK-C2 says to remove a different rule and inspect the Pralayākala row; the actual mutant removes the implemented R1 and tests only the row count. The current mutation is useful for *that* model, but it does not establish that the original control passed as preregistered. See [the correction record](formal-trika/PREREGISTRATION-2026-11-06.md). The base Git history places preregistration and code in the same initial commit; the asserted earlier authoring order cannot be independently established from that history.

### P1 · Several names overstate what the models prove — scope clarified, model work remains

- `Transitions.lean`: `anava_stuck_exists` and `karma_loop_exists` exhibit states satisfying flags; neither defines or proves a stuck transition or loop. Idempotence of one function does not prove no other transition can reverse it.
- `NonEntail.lean`: A–F and the seven V flags are unconstrained Boolean assignments. Their witnesses show non-entailment *under those model assumptions*, not a philosophical result independent of assumptions. The chain is owner-authored R material, not a Sanskrit root-text T claim. The equality example is not a general sheaf theorem; only one pair is explicitly exhibited.
- `Conjuncts.lean`: one PI/ground assignment is a witness, not a full independence theorem. The `unus_ambu` exhibit chooses an always-true relation; it does not settle the philosophical interpretation.
- `Memory.lean` had a prose implication backwards. The actual model says M4 requires M1–M3; it also admits M1–M3 without M4. The comment and a counterexample theorem now make that explicit.
- `Coords.lean` asserted that zero of *all* four raw bit pairs violated a restriction, but one does. The revised theorem says zero **admitted** states violate the assumption; a separate theorem records one excluded raw pair. This proves the consequence of the encoded premise, not the premise itself.
- `Tractatus.lean` had two syntax failures and a function-space `Decidable` failure. Its repaired `Fin 2 → Fin 4` theorem is a finite non-surjection; it is not a general theorem about minds or all self-models.
- `control/Kancuka.lean` called a mapped-list length check “distinct”: list mapping preserves length even for collisions. It now uses `eraseDups` and includes a collision mutant.

## Cross-system contract before formal claims enter an essay

Use the existing products and their own identity schemes; do not invent a second ledger or silently equate SHA, Merkle, Git and qp IDs.

| Step | Required evidence | Honest outcome |
|---|---|---|
| OpenPāṭala / source record | Work, edition, witness and exact source byte hash, selectors and rights; record candidate/unknown fields instead of inventing them. | `SOURCE_BOUND`, `CANDIDATE` or `UNRESOLVED`; identity is not philological truth. |
| translation-work | Exact source ID + passage/segment + layer version/hash, schema and applicable existing deterministic gates; explicit grounds for competing readings. | The checked data and its review state. A green schema/gate is not a guarantee of meaning. |
| trika-x | Exact file/hash and named theorem, model/assumptions, trusted Lean/toolchain identity, actual command and output, dependency/axiom audit, and positive plus intended mutation results. | `MODEL_CHECKED` only for the stated proposition in this model. No key is emitted by the present inventory. |
| cg, if used | Nonempty pinned suite, sealed oracle, exact compiler and gate versions, committed action **results** and scores, algorithm-labeled digest, independent replay. | Research run with auditable results; not a substitute for source or human review. |
| Human bridge | A versioned, citable mapping from the selected passage and interpretation to formal premises; role, scope and disagreement recorded. | An explicitly assessed textual or interpretive claim. Lean does not supply this bridge. |
| qp authority | Mandatory versioned gates, verified evidence bytes and roots, full signed digest, authorized actor and replayed state transition. | An authorized receipt for that exact scope, not a new proof of translation or doctrine. |
| Scholar / essay | Exact draft revision, paragraph claim and source/model references; source and style permissions; review against that revision; human sign-off through the existing account flow. | A citable essay with clear human/agent authorship, review status and rights. Private drafts, review and voice stay private absent an explicit grant. |

Any changed source bytes, translation layer, model, theorem statement, compiler/policy or essay revision must make downstream assessments and approvals stale or unresolved, without deleting earlier versions. Missing mappings or revoked consent must fail closed for the affected use. No model proof grants rights, proves factual entailment, supplies human identity, or automatically publishes a scholar's work.

Practical first slice: choose one rights-cleared source passage, one exact layer revision, one named theorem and its mutation, then have a scholar explicitly review the mapping. First harden/retest qp and Scholar as above; then exercise source → layer → Lean artifact → authorized receipt → revision-bound essay citation, including changed source, false mutant, missing evidence, denied permission and stale-signoff failures. Until that exists, display formal artifacts as research records only.

## What this PR checked

The original control runner appeared green, but recognition had four positive files check and two fail. With the pinned Lean 4.34.1 distribution, the repaired `control/run.sh` passes its positive files and both intended negative controls; `recognition/run.sh` passes all six positive files and all six intended negative controls. The Python regression tests exercise absent compiler, wrong version, successful mutant, syntax/wrong-line/extra errors, changed theorem statements and unverified inventory labeling. See [the run guide](formal-trika/README.md) for commands and limits. No live service, production publishing route, scholar sign-off, or external-source philological verification was tested.
