# Peer review: formal Trika as part of the evidence system

**Status: review in progress; do not consume the generated inventory as proof or as a publication gate.**

Reviewed against `trika-x` base `817ca21`, `translation-work` `e05e640`,
`ipvv` `48f2a5c`, and `gochema` `8a9422e`. These are the versions inspected,
not source-edition pins. The preregistration files are historical records and
are not altered by this review.

## Release blockers

1. The original `formal-trika/tools/emit_keys.py` labeled every inventory entry
   `decide-checked` without running Lean. Some entries group several theorems
   or are not declaration names, and cited sources are not content-pinned.
   It now emits an explicitly unverified inventory, not evidence keys.
2. `recognition/run.sh` accepts *any* compiler failure as a successful
   mutation control, including a missing compiler or a syntax error. The same
   problem exists in `control/run.sh`.
3. At IPVV `48f2a5c`, `tools/qp_acom/receipts.py::transition` uses `all` on
   the caller-supplied gate list, which means an empty list passes and can
   apply a state change; `settle` also accepts it. Reproduced with an empty
   list, no evidence, and a state-changing `apply` callback. A receipt with
   `passed: true` by itself is therefore not proof of a required check. The
   kernel returns unsigned receipts unless a separate authority signs them;
   `verify_receipt` permits an absent signer. Gate coverage, a signature and
   authority must be required at the integration boundary before using a
   receipt as publishing authority. This review does not modify IPVV.
4. Reproduction with Lean 4.34.1: `recognition/Tractatus.lean` has parser and
   decidability failures; `recognition/Coords.lean` has a false theorem.
   The old runner reports the six broken twins as expected failures without
   establishing why they failed.

Further findings, fixes, reproduction instructions and limits follow in the
next review checkpoint.
