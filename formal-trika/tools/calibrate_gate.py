#!/usr/bin/env python3
"""calibrate_gate.py — F2/F4: gate-vs-gold calibration on CPU (no model).

Runs sanskritbench's deterministic translation_proof gate (imported
read-only; nothing in sanskritbench is written) over:
  (a) gold positives (Mitrasamgraha test pairs) — expect PASS,
  (b) corrupted variants — expect BLOCKED:
      - hallucinated: gold english + unrelated padding (binding should catch)
      - truncated: first 30% of english (coverage should catch)
      - term-drift: repeated content words rendered inconsistently
      - source-repeat: candidate echoes the source (grounding should catch)
Reports per-dimension PASS rates + false-PASS (corrupted→PASS) and
false-BLOCK (gold→BLOCKED) rates, then stamps threshold version F4.
Usage: python3 formal-trika/tools/calibrate_gate.py [--n 200] [--seed 0]
"""
import argparse
import json
import random
import os
import sys
from pathlib import Path

SB = Path(os.environ.get("SANSKRITBENCH", "/root/sanskritbench"))
sys.path.insert(0, str(SB / "pipeline"))
import translation_proof as tp  # noqa: E402 (read-only import)

GOLD = SB / "data/benchmarks/mitrasamgraha/test.jsonl"
THRESHOLD_VERSION = "gate-thresholds/1"


def corrupt(kind, eng):
    words = eng.split()
    if kind == "hallucinated":
        pad = (" Moreover the king of the outer islands decreed seven new festivals "
               "and appointed twelve ministers to oversee the harvest calendar.")
        return eng + pad
    if kind == "truncated":
        return " ".join(words[: max(1, int(len(words) * 0.3))])
    if kind == "term-drift":
        out, flip = [], False
        for w in words:
            if len(w) > 5 and w[0].isupper():
                flip = not flip
                out.append(w.upper() if flip else w.lower())
            else:
                out.append(w)
        return " ".join(out)
    if kind == "source-repeat":
        return None  # caller substitutes the source itself
    raise ValueError(kind)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    rows = [json.loads(l) for l in GOLD.read_text().splitlines() if l.strip()]
    rng = random.Random(a.seed)
    sample = rng.sample(rows, min(a.n, len(rows)))
    dims = ["SOURCE_BINDING", "COVERAGE", "ABSTENTION", "TERM_CONSISTENCY",
            "CITATION_GROUNDING"]
    stats = {k: {"pass": 0, "n": 0} for k in
             ["gold"] + [f"corrupt:{k}" for k in
                         ("hallucinated", "truncated", "term-drift", "source-repeat")]}
    dimpass = {k: {d: 0 for d in dims} for k in stats}
    for r in sample:
        s, e = r["sanskrit"], r["english"]
        v = tp.verify_translation(s, e, gold=e)
        stats["gold"]["n"] += 1
        stats["gold"]["pass"] += v["deterministic_gate"] == "PASS"
        for d in dims:
            dimpass["gold"][d] += v["checks"][d]["PASS"]
        for kind in ("hallucinated", "truncated", "term-drift", "source-repeat"):
            c = s if kind == "source-repeat" else corrupt(kind, e)
            v = tp.verify_translation(s, c)
            k = f"corrupt:{kind}"
            stats[k]["n"] += 1
            stats[k]["pass"] += v["deterministic_gate"] == "PASS"
            for d in dims:
                dimpass[k][d] += v["checks"][d]["PASS"]
    print(f"n={len(sample)} seed={a.seed} thresholds={THRESHOLD_VERSION}")
    for k, st in stats.items():
        print(f"{k}: gate-PASS {st['pass']}/{st['n']} = {st['pass']/st['n']:.3f}")
    print("per-dimension PASS rates:")
    for k in stats:
        print(f"  {k}: " + " ".join(
            f"{d}={dimpass[k][d]/stats[k]['n']:.2f}" for d in dims))
    fp = stats["gold"]["pass"] / stats["gold"]["n"]
    fb = {k: stats[k]["pass"] / stats[k]["n"] for k in stats if k != "gold"}
    print(f"false-BLOCK (gold→BLOCKED): {1-fp:.3f}")
    print("false-PASS (corrupt→PASS): " + " ".join(f"{k}={v:.3f}" for k, v in fb.items()))
    print("verdict: " + ("GATE DISCRIMINATES (gold high, corrupt low)"
                          if fp > 0.8 and all(v < 0.3 for v in fb.values())
                          else "GATE NEEDS TUNING — see per-dimension rates"))


if __name__ == "__main__":
    raise SystemExit(main())
