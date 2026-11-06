#!/usr/bin/env python3
"""axiom_audit.py — SOTA Lean axiom hygiene gate (static pass; no Lean needed).

Fails closed on anything that would smuggle unsoundness past `decide`:
  - `sorry` / `sorryAx` (placeholder proofs elaborate to an axiom)
  - `axiom ` declarations (custom axioms; theorems valid only relative to them)
  - `native_decide` (introduces per-invocation axioms + Lean.ofReduceBool /
    Lean.trustCompiler; external checkers cannot replay them)
  - `Lean.ofReduceBool` / `trustCompiler` mentions

This is the static half of the audit. The dynamic half runs on a Lean box:
each theorem must `#print axioms` to exactly
[propext, Classical.choice, Quot.sound] (see README § audit). CI runs this
file on every push (no toolchain needed); `control/run.sh` + `recognition/
run.sh` remain the kernel-verdict gates on a pinned-Lean runner.

Usage: python3 tools/axiom_audit.py [--check]
  --check: exit nonzero on violation (CI mode). Default prints report.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
SOURCES = [str(f.relative_to(HERE)) for d in ("control", "recognition")
           for f in sorted((HERE / d).glob("*.lean"))]

PATTERNS = [
    (re.compile(r"\bsorry\b"), "sorry (elaborates to sorryAx)"),
    (re.compile(r"sorryAx"), "sorryAx"),
    (re.compile(r"(?m)^\s*axiom\s+\w+"), "custom axiom declaration"),
    (re.compile(r"\bnative_decide\b"), "native_decide (trustCompiler/ofReduceBool)"),
    (re.compile(r"ofReduceBool"), "Lean.ofReduceBool"),
    (re.compile(r"trustCompiler"), "Lean.trustCompiler"),
]


def audit():
    violations = []
    for rel in SOURCES:
        text = (HERE / rel).read_text(encoding="utf-8")
        for pat, label in PATTERNS:
            for m in pat.finditer(text):
                line = text.count("\n", 0, m.start()) + 1
                violations.append(f"{rel}:{line}: forbidden {label}")
    return violations


def main():
    violations = audit()
    print(f"files scanned: {len(SOURCES)}")
    print(f"expected axioms (dynamic half): [propext, Classical.choice, Quot.sound]")
    print(f"forbidden markers: sorry, sorryAx, axiom-decl, native_decide, "
          f"ofReduceBool, trustCompiler")
    if violations:
        for v in violations:
            print("VIOLATION:", v)
        return 1
    print("axiom_audit: CLEAN (static half; kernel verdict still needs pinned Lean)")
    return 0 if "--check" in sys.argv else 0


if __name__ == "__main__":
    raise SystemExit(main())
