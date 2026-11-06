#!/bin/sh
# Formal Trika control runner (mirrors formal-abhidhamma control/run.sh).
# TK-C1 must CHECK; TK-C2 (rule R1 deleted) must FAIL. Exit 0 only if both hold.
cd "$(dirname "$0")"
LEAN="${LEAN:-lean}"
$LEAN -o Mala.olean Mala.lean || { echo "Mala.lean failed"; exit 1; }
$LEAN -o Kancuka.olean Kancuka.lean || { echo "Kancuka.lean failed"; exit 1; }
$LEAN -o Recognition.olean Recognition.lean || { echo "Recognition.lean failed"; exit 1; }
if LEAN_PATH=. $LEAN Pramatr.lean; then echo "TK-C1 PASS the seven experients: 8 combos, 7 well-formed, profile 2-3-1-2-1-2-0"; else echo "TK-C1 FAIL"; exit 1; fi
if LEAN_PATH=. $LEAN Broken.lean >/dev/null 2>&1; then echo "TK-C2 FAIL the break CHECKED - the instrument is blind"; exit 1; else echo "TK-C2 PASS deleting R1 breaks the count, as required"; fi
