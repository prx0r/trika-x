"""Emit an explicitly unverified recognition inventory.

This program hashes source files; it does not invoke Lean, pin the cited
source documents, or make evidence suitable for a publication gate. Some
inventory entries are grouped labels rather than Lean declaration names.
See PEER-REVIEW-2026-11-06.md before connecting this output to another system.
"""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

FILES = [
    "recognition/Transitions.lean",
    "recognition/NonEntail.lean",
    "recognition/Conjuncts.lean",
    "recognition/Memory.lean",
]

THEOREMS = [
    # (theorem, file, scope, tier, source)
    ("trec_preserves_embodiment", "Transitions.lean", "4096 states", "R",
     "FORMALIZATION-OF-RECOGNITION.md: T_rec, tuple-identical"),
    ("trec_clears_bondage", "Transitions.lean", "4096 states", "R",
     "FORMALIZATION-OF-RECOGNITION.md: B_i cleared, L_i kept"),
    ("trec_retains_limitation", "Transitions.lean", "4096 states", "R",
     "recognitionexpounded.md: boundary reclassified, not destroyed"),
    ("trec_idempotent", "Transitions.lean", "4096 states", "R",
     "AM0: recognized stays recognized"),
    ("anava_stuck_exists", "Transitions.lean", "witness >0", "R",
     "mala table: O asserts Sv(O)"),
    ("acquire_is_not_recognition", "Transitions.lean", "4096 states", "R",
     "recognitionexpounded.md: decentring vs reconfiguration"),
    ("karma_loop_exists", "Transitions.lean", "witness >0", "R",
     "mala table: attractor-lock in Γ"),
    ("aby_not_b,b_not_c,c_not_d,d_not_e,e_not_f,abcde_without_f",
     "NonEntail.lean", "7 witnesses", "T-chain/R-model",
     "pushing/research/truthanother.md:9-24, truthagent.md:49-71"),
    ("vim7_independent", "NonEntail.lean", "128 combos", "R",
     "home-checkpointcharlie: V_1..V_7 dissociable"),
    ("copresence_nontransitive", "NonEntail.lean", "Fin 3 exhibit", "R",
     "home-checkpointcharlie: U non-transitive"),
    ("no_global_section", "NonEntail.lean", "Bool triad", "R",
     "home-checkpointcharlie: local ⇏ global section"),
    ("pairwise_satisfiable_xy", "NonEntail.lean", "witness", "R",
     "sheaf warning: pairs cohere"),
    ("recognition_unique", "Conjuncts.lean", "1 of 16", "R",
     "recognitionandsiva.md: 4-conjunct"),
    ("drop_*_loses (x4)", "Conjuncts.lean", "0 matches each", "R",
     "recognitionandsiva.md: conjunct necessity"),
    ("misidentification_never_recognizes", "Conjuncts.lean", "0 matches", "R",
     "recognitionandsiva.md: Recog(a,b), a=b required"),
    ("part_coherent_distinct_tokens", "Conjuncts.lean", "witness >0", "R",
     "DAIMON-CONTACT: participatory reading coherent"),
    ("pi_independent_of_grounds", "Conjuncts.lean", "witness >0", "R",
     "isvara.md: three readings; PI settles no ground"),
    ("siva_requires_axioms", "Conjuncts.lean", "0 matches", "R",
     "recognitionandsiva.md: S1-S5 load-bearing"),
    ("unus_ambu_not_identity", "Conjuncts.lean", "Fin 2 exhibit", "R",
     "DAIMON-CONTACT: 1x1 vs 1=1"),
    ("m4_requires_foundation", "Memory.lean", "0 violations", "R",
     "ESSAY-RECOGNITION: M1-3 -> M4"),
    ("m4_without_m5", "Memory.lean", "witness >0", "R",
     "ESSAY-RECOGNITION: M4 ⇏ M5"),
    ("sees_without_enacting", "Memory.lean", "witness >0", "R",
     "ESSAY-RECOGNITION: Layer 3 vs Layer 4"),
    ("no_enacting_without_seeing", "Memory.lean", "0 violations", "R",
     "ESSAY-RECOGNITION: gradation law"),
]

keys = {"key_format": "trika-recognition-unverified-inventory/2",
        "intended_lean_toolchain": "leanprover/lean4:v4.34.1",
        "verification": "NOT_RUN",
        "source_pins": "UNRESOLVED",
        "integration_ready": False,
        "files": {},
        "theorems": []}

for f in FILES:
    p = os.path.join(ROOT, f)
    with open(p, "rb") as fh:
        h = hashlib.sha256(fh.read()).hexdigest()
    keys["files"][f] = {"sha256": h}

for name, fil, scope, tier, src in THEOREMS:
    keys["theorems"].append(
        {"inventory_label": name, "file": fil, "scope": scope,
         "tier": "R", "original_tier_label": tier,
         "unverified_source_note": src, "status": "NOT_CHECKED"})

print(json.dumps(keys, indent=1, sort_keys=True))
