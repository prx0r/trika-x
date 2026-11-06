#!/usr/bin/env python3
"""mutate_sweep.py — mechanical mutation sweep via jubnzv/Mutate.lean (SOTA).

Hand-written Broken*.lean twins remain the preregistered controls
(must_fail.py). This is the *additional* instrument the peer review
requires: matching theorem statements do not prove only the intended
definition changed, so a mechanical sweep checks what hand-written
mutants miss — surviving mutants = coverage gaps (add an invariant),
stillborn = ill-typed (skip), killed = constrained (good).

  SOTA: jubnzv/Mutate.lean (Lean >= 4.28, uses compiler frontend,
  in-process re-elaboration; `killed=.. survived=.. stillborn=..`,
  clean = survived 0 modulo provably-equivalent noise).

Usage (on a Lean box, Mutate.lean checked out alongside trika-x):
  MUTATE_LEAN=../Mutate.lean/Mutate.lean \
    python3 formal-trika/tools/mutate_sweep.py [--sample N --seed S]

Fails closed: missing Lean, wrong version, or missing Mutate.lean exits
nonzero before reporting any sweep PASS. A sweep with survived > 0 is a
finding (coverage gap), never a pass. Equivalent mutants are recorded as
such (undecidable in general); they do not count as killed.
"""
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
LEAN = os.environ.get("LEAN", "lean")
MUTATE = os.environ.get("MUTATE_LEAN", str(HERE.parent / "Mutate.lean" / "Mutate.lean"))
TARGETS = [str(f.relative_to(HERE)) for d in ("control", "recognition")
           for f in sorted((HERE / d).glob("*.lean"))
           if not f.name.startswith("Broken")]


def fail(msg):
    print(f"FAIL: {msg}", file=sys.stderr)
    return 2


def main():
    if not Path(MUTATE).exists():
        return fail(f"Mutate.lean not found at {MUTATE} "
                    f"(set MUTATE_LEAN; clone https://github.com/jubnzv/Mutate.lean)")
    try:
        v = subprocess.run([LEAN, "--version"], text=True, capture_output=True)
    except FileNotFoundError:
        return fail("Lean unavailable (set LEAN); missing compiler is never a sweep PASS")
    if "4.34.1" not in (v.stdout + v.stderr):
        return fail(f"Lean 4.34.1 required, got: {(v.stdout + v.stderr).strip()[:120]}")
    extra = sys.argv[1:]
    print(f"targets: {len(TARGETS)} files; Mutate.lean: {MUTATE}")
    print("hand-written must_fail controls remain authoritative; "
          "this sweep is additional (survived = finding, not pass)")
    for t in TARGETS:
        cmd = ["lake", "env", "lean", "--run", MUTATE, *extra, t]
        print("+", " ".join(cmd))
        r = subprocess.run(cmd, cwd=str(HERE))
        if r.returncode != 0:
            return fail(f"sweep error on {t} (rc={r.returncode}); "
                        f"see Mutate.lean output above")
    print("sweep complete: triage survived mutants as coverage gaps; "
          "record equivalent mutants explicitly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
