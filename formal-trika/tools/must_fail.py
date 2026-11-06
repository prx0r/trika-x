#!/usr/bin/env python3
"""Accept a mutation only when the intended `by decide` theorem is false.

Negative controls are hand-written models, so matching the theorem statement
does not prove that the mutant differs only in the intended definition. Review
that semantic difference too. No arbitrary compiler error counts as a pass.
"""
import argparse
import os
from pathlib import Path
import re
import subprocess
import sys

EXPECTED_VERSION = "Lean (version 4.34.1,"


def statement(path, theorem):
    text = Path(path).read_text(encoding="utf-8")
    pattern = (r"(?m)^theorem\s+" + re.escape(theorem) +
               r"\s*:\s*(.*?)\s*:=\s*by\s+(decide)\b")
    matches = list(re.finditer(pattern, text, re.DOTALL))
    if len(matches) != 1:
        raise ValueError(f"expected exactly one by-decide theorem {theorem} in {path}")
    match = matches[0]
    return re.sub(r"\s+", "", match.group(1)), text.count("\n", 0, match.start(2)) + 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", required=True)
    parser.add_argument("--positive", required=True)
    parser.add_argument("--mutant", required=True)
    parser.add_argument("--theorem", required=True)
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()
    try:
        version = subprocess.run([args.lean, "--version"], text=True,
                                 capture_output=True, timeout=args.timeout)
        if version.returncode != 0 or not version.stdout.startswith(EXPECTED_VERSION):
            raise ValueError("Lean 4.34.1 is required")
        positive, _ = statement(args.positive, args.theorem)
        mutated, proof_line = statement(args.mutant, args.theorem)
        if positive != mutated:
            raise ValueError("positive and mutant theorem statements differ")
        env = os.environ.copy()
        env["LEAN_PATH"] = str(Path(args.mutant).resolve().parent)
        run = subprocess.run([args.lean, args.mutant], text=True,
                             capture_output=True, timeout=args.timeout, env=env)
        output = run.stdout + run.stderr
        errors = list(re.finditer(r"(?m)^(.+?):(\d+):(\d+): error(?:\([^\n)]*\))?:", output))
        expected = (run.returncode == 1 and len(errors) == 1 and
                    Path(errors[0].group(1)).resolve() == Path(args.mutant).resolve() and
                    int(errors[0].group(2)) == proof_line and
                    "Tactic `decide` proved that the proposition" in output and
                    "is false" in output)
        if not expected:
            raise ValueError("mutant did not fail at the expected false proposition\n" + output)
        print(f"PASS {args.mutant}: {args.theorem} is false in mutant")
        return 0
    except (OSError, subprocess.TimeoutExpired, ValueError) as exc:
        print(f"FAIL {args.mutant}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
