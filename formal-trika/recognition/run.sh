#!/bin/sh
# Formal Recognition run harness (mirrors control/run.sh).
# Every rung file must CHECK; every Broken twin must FAIL.
# Exit 0 only if all hold.
cd "$(dirname "$0")"
LEAN="${LEAN:-lean}"
pass=0; fail=0
check() {
  if LEAN_PATH=. $LEAN "$1" 2>/dev/null; then echo "PASS $1"; pass=$((pass+1));
  else echo "FAIL $1"; fail=$((fail+1)); fi
}
mustfail() {
  if LEAN_PATH=. $LEAN "$1" >/dev/null 2>&1; then echo "BLIND $1 (break CHECKED)"; fail=$((fail+1));
  else echo "PASS $1 (break fails, as required)"; pass=$((pass+1)); fi
}
check Transitions.lean
check NonEntail.lean
check Conjuncts.lean
check Memory.lean
check Tractatus.lean
check Coords.lean
mustfail BrokenTrans.lean
mustfail BrokenNonEntail.lean
mustfail BrokenConjuncts.lean
mustfail BrokenMemory.lean
mustfail BrokenReach.lean
mustfail BrokenCoords.lean
echo "== $pass passed, $fail failed =="
[ "$fail" -eq 0 ]
