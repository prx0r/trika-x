#!/bin/sh
# Only an expected false proposition counts as a passed negative control.
cd "$(dirname "$0")" || exit 2
LEAN="${LEAN:-lean}"
if ! command -v "$LEAN" >/dev/null 2>&1 || ! "$LEAN" --version | grep -q '^Lean (version 4\.34\.1,'; then
  echo "FAIL: Lean 4.34.1 is unavailable" >&2
  exit 2
fi
"$LEAN" -DwarningAsError=true -o Mala.olean Mala.lean || exit 1
"$LEAN" -DwarningAsError=true -o Kancuka.olean Kancuka.lean || exit 1
"$LEAN" -DwarningAsError=true -o Recognition.olean Recognition.lean || exit 1
"$LEAN" -DwarningAsError=true -o Tattva.olean Tattva.lean || exit 1
"$LEAN" -DwarningAsError=true MalaFuel.lean || exit 1
"$LEAN" -DwarningAsError=true Pratyahara.lean || exit 1
"$LEAN" -DwarningAsError=true Reversal.lean || exit 1
"$LEAN" -DwarningAsError=true AnswerKey.lean || exit 1
"$LEAN" -DwarningAsError=true Tattva.lean || exit 1
"$LEAN" -DwarningAsError=true TattvaInventory.lean || exit 1
LEAN_PATH=. "$LEAN" -DwarningAsError=true Pramatr.lean || exit 1
LEAN_PATH=. "$LEAN" -DwarningAsError=true Avarana.lean || exit 1
echo "PASS Boolean row count and profile (not a classification proof)"
echo "PASS AnswerKey counts (key data, not derived)"
echo "PASS stipulated Tattva group-size sum (model only)"
echo "PASS candidate named Tattva inventory (model only)"
echo "PASS Avarana covering-chain (cross-course ascent + exhibited partial order)"
echo "PASS MalaFuel burn dynamics (terminate, monotone strength, grace ignition)"
echo "PASS Pratyahara interval mechanics (aC vowels, haL consonants, markers excluded)"
echo "PASS Reversal order claims (semivowel + span flips, comparison pilot)"
python3 ../tools/must_fail.py --lean "$LEAN" --positive Pramatr.lean --mutant Broken.lean --theorem seven || exit 1
python3 ../tools/must_fail.py --lean "$LEAN" --positive Kancuka.lean --mutant BrokenKancuka.lean --theorem pairings_distinct || exit 1
python3 ../tools/must_fail.py --lean "$LEAN" --positive Tattva.lean --mutant BrokenTattva.lean --theorem thirty_six || exit 1
python3 ../tools/must_fail.py --lean "$LEAN" --positive TattvaInventory.lean --mutant BrokenTattvaInventory.lean --theorem pure_excludes_maya || exit 1
python3 ../tools/must_fail.py --lean "$LEAN" --positive Recognition.lean --mutant BrokenSharp.lean --theorem contentEq_sharp || exit 1
python3 ../tools/must_fail.py --lean "$LEAN" --positive Avarana.lean --mutant BrokenAvarana.lean --theorem course_ascends || exit 1
python3 ../tools/must_fail.py --lean "$LEAN" --positive MalaFuel.lean --mutant BrokenFuel.lean --theorem grace_ignites || exit 1
python3 ../tools/must_fail.py --lean "$LEAN" --positive Pratyahara.lean --mutant BrokenSutra.lean --theorem ac_vowels || exit 1
python3 ../tools/must_fail.py --lean "$LEAN" --positive Reversal.lean --mutant BrokenReversal.lean --theorem semi_reversed || exit 1
