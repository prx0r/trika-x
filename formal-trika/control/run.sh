#!/bin/sh
# Only an expected false proposition counts as a passed negative control.
cd "$(dirname "$0")" || exit 2
LEAN="${LEAN:-lean}"
if ! command -v "$LEAN" >/dev/null 2>&1 || ! "$LEAN" --version | grep -q '^Lean (version 4\.34\.1,'; then
  echo "FAIL: Lean 4.34.1 is unavailable" >&2
  exit 2
fi
"$LEAN" -o Mala.olean Mala.lean || exit 1
"$LEAN" -o Kancuka.olean Kancuka.lean || exit 1
"$LEAN" -o Recognition.olean Recognition.lean || exit 1
LEAN_PATH=. "$LEAN" Pramatr.lean || exit 1
echo "PASS Boolean row count and profile (not a classification proof)"
python3 ../tools/must_fail.py --lean "$LEAN" --positive Pramatr.lean --mutant Broken.lean --theorem seven || exit 1
python3 ../tools/must_fail.py --lean "$LEAN" --positive Kancuka.lean --mutant BrokenKancuka.lean --theorem pairings_distinct || exit 1
