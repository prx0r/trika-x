#!/usr/bin/env python3
"""formal_sketch_check.py — the four mechanical gates for a formal sketch.

A formal sketch (translation-work FORMAL-STAGE proposal) is machine-proposed
Lean plus must-fail twins plus a manifest. This tool runs every gate that
needs no judgment, so the assessor spends judgment only where judgment lives:

  1. sketch compiles on pinned Lean 4.34.1 with warnings-as-errors
  2. every twin refuses at its expected false proposition (must_fail,
     exactly-one-error rule)
  3. tiers declared (R-tier present), no T-tier promotion, kill conditions
     recorded in the manifest
  4. manifest ↔ file consistency (every theorem listed, every twin present);
     chunk locators verified against translation-work when available
     (WARNING when the checkout is absent, ERROR on mismatch)

Usage: python3 tools/formal_sketch_check.py <sketch-dir>
  <sketch-dir>/sketch.json manifest, *.lean next to it.
Exit 0 = all gates pass. Anything else prints the failing gate first.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MUST_FAIL = HERE / "must_fail.py"
TW = Path(os.environ.get("TRANSLATION_WORK", HERE.parent.parent.parent / "translation-work"))
EXPECTED_VERSION = "Lean (version 4.34.1,"


def fail(msg: str) -> int:
    print(f"FAIL: {msg}")
    return 1


def lean() -> str:
    exe = os.environ.get("LEAN", "lean")
    try:
        v = subprocess.run([exe, "--version"], text=True, capture_output=True,
                           timeout=60)
    except OSError:
        return ""
    return exe if v.returncode == 0 and v.stdout.startswith(EXPECTED_VERSION) else ""


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: formal_sketch_check.py <sketch-dir>")
        return 2
    d = Path(sys.argv[1])
    man_p = d / "sketch.json"
    if not man_p.is_file():
        return fail(f"no sketch.json in {d}")
    try:
        man = json.loads(man_p.read_text(encoding="utf-8"))
    except ValueError as e:
        return fail(f"sketch.json is not JSON: {e}")
    for k in ("sketch", "prereg", "tier", "kill", "theorems"):
        if k not in man:
            return fail(f"sketch.json missing key: {k}")
    if man["tier"] != "R":
        return fail(f"sketch tier must be R (machine-proposed), got {man['tier']!r}")
    if not man["kill"]:
        return fail("sketch.json records no kill conditions")
    sketch = d / man["sketch"]
    if not sketch.is_file():
        return fail(f"sketch file missing: {man['sketch']}")

    exe = lean()
    if not exe:
        return fail("Lean 4.34.1 unavailable (set LEAN or install the pinned toolchain)")

    # Gate 1: compiles, warnings as errors.
    r = subprocess.run([exe, "-DwarningAsError=true", str(sketch)], text=True,
                       capture_output=True, timeout=300)
    if r.returncode != 0:
        return fail(f"sketch does not compile:\n{r.stderr or r.stdout}")
    print(f"PASS gate 1: {sketch.name} compiles on pinned Lean")

    # File-level tier + promotion scan over sketch and twins.
    texts = {sketch.name: sketch.read_text(encoding="utf-8")}
    for thm, spec in man["theorems"].items():
        tp = d / spec.get("twin", "")
        if not tp.is_file():
            return fail(f"twin missing for {thm}: {spec.get('twin')}")
        texts[tp.name] = tp.read_text(encoding="utf-8")
    if not any("R-tier" in t for t in texts.values()):
        return fail("tier not declared (no R-tier note in sketch or twins)")
    for name, t in texts.items():
        for i, line in enumerate(t.splitlines(), 1):
            if ("T-tier" in line and
                    not re.search(r"\b(never|NOT|no |refus|must not)\b", line)):
                return fail(f"T-tier promotion in {name}:{i} (machine may never claim T)")
    print("PASS gate 3: R-tier declared, no T-tier promotion")

    # Gate 2: every twin refuses at its expected proposition.
    for thm in man["theorems"]:
        twin = d / man["theorems"][thm]["twin"]
        r = subprocess.run([sys.executable, str(MUST_FAIL), "--lean", exe,
                            "--positive", str(sketch), "--mutant", str(twin),
                            "--theorem", thm], text=True, capture_output=True,
                           timeout=300)
        if r.returncode != 0:
            return fail(f"twin for {thm} did not refuse as required:\n{r.stdout}\n{r.stderr}")
        print(f"PASS gate 2: twin refuses {thm}")
    print("PASS gate 2: all twins refuse (anti-vacuity holds)")

    # Gate 4: manifest <-> file consistency.
    found = re.findall(r"(?m)^theorem\s+([A-Za-z0-9_]+)", sketch.read_text(encoding="utf-8"))
    if set(found) != set(man["theorems"]):
        return fail(f"theorem set drift: file={sorted(found)} manifest={sorted(man['theorems'])}")
    print(f"PASS gate 4a: manifest matches file ({len(found)} theorems)")

    # Gate 4b: chunk locators resolve (when the translation-work checkout exists).
    chunks = sorted({c for spec in man["theorems"].values()
                     for c in spec.get("chunks", [])})
    ledgers = sorted(TW.glob("*/passages.jsonl"))
    if not ledgers:
        print("WARN gate 4b: translation-work checkout absent; chunk locators unchecked")
    else:
        missing = []
        for c in chunks:
            loc = c.split(":")[-1]
            ok = False
            for p in ledgers:
                try:
                    if loc in p.read_text(encoding="utf-8"):
                        ok = True
                        break
                except OSError:
                    continue
            if not ok:
                missing.append(c)
        if missing:
            return fail(f"chunk locators do not resolve: {missing}")
        print(f"PASS gate 4b: {len(chunks)} chunk locators resolve")
    print("ALL GATES PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
