#!/bin/sh
# Check every positive and require the intended false proposition in each mutant.
cd "$(dirname "$0")" || exit 2
LEAN="${LEAN:-lean}"
if ! command -v "$LEAN" >/dev/null 2>&1 || ! "$LEAN" --version | grep -q '^Lean (version 4\.34\.1,'; then
  echo "FAIL: Lean 4.34.1 is unavailable" >&2
  exit 2
fi
pass=0; fail=0
check() {
  if LEAN_PATH=. "$LEAN" -DwarningAsError=true "$1"; then echo "PASS $1"; pass=$((pass+1));
  else echo "FAIL $1"; fail=$((fail+1)); fi
}
mustfail() {
  if python3 ../tools/must_fail.py --lean "$LEAN" --positive "$1" --mutant "$2" --theorem "$3"; then
    pass=$((pass+1)); else fail=$((fail+1)); fi
}
check Transitions.lean
check NonEntail.lean
check Conjuncts.lean
check Memory.lean
check Tractatus.lean
check Coords.lean
mustfail Transitions.lean BrokenTrans.lean trec_preserves_embodiment
mustfail NonEntail.lean BrokenNonEntail.lean abcde_without_f
mustfail Conjuncts.lean BrokenConjuncts.lean misidentification_never_recognizes
mustfail Memory.lean BrokenMemory.lean m4_requires_foundation
mustfail Tractatus.lean BrokenReach.lean recognition_needs_reflexive_edge
mustfail Coords.lean BrokenCoords.lean coords_covered_once
echo "== $pass passed, $fail failed =="
[ "$fail" -eq 0 ]
