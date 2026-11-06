#!/usr/bin/env python3
"""T-C1: felt<->structural co-occurrence test (prereg PREREGISTRATION-DECODE-RUNG.md).

Claim: lobha-headline clauses co-occur with thina/churn-headline clauses
within the same arc above chance (rāga presents as pull+stall).
Unit = arc (a day's section). Headline = heads[] in play/*.jsonl
(riders excluded by construction; churn only when explicitly flagged).

Fisher exact, one-sided (positive association). Stdlib only.
Usage: python3 tools/tc1_cooccurrence.py [play_dir]
"""
import json
import math
import sys
from pathlib import Path

PLAY = Path(sys.argv[1] if len(sys.argv) > 1
            else str(Path(__file__).resolve().parent.parent / "data"))


def load():
    arcs = {}
    for p in sorted(PLAY.glob("day-*.jsonl")):
        for line in p.read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("unmapped"):
                continue
            key = (r["day"], r["arc"])
            a = arcs.setdefault(key, {"lobha": False, "thin": False})
            heads, felt = r["heads"], r.get("felt", [])
            if "lobha" in heads:
                a["lobha"] = True
            if "thina" in heads or "middha" in heads or "churn" in felt:
                a["thin"] = True
    return arcs


def fisher_exact(a, b, c, d):
    """P(X >= a) one-sided for [[a,b],[c,d]]."""
    n = a + b + c + d
    r1, c1 = a + b, a + c

    def prob(x):
        return (math.comb(r1, x) * math.comb(n - r1, c1 - x)) / math.comb(n, c1)
    return sum(prob(x) for x in range(a, min(r1, c1) + 1))


def main():
    arcs = load()
    a = sum(1 for v in arcs.values() if v["lobha"] and v["thin"])
    b = sum(1 for v in arcs.values() if v["lobha"] and not v["thin"])
    c = sum(1 for v in arcs.values() if not v["lobha"] and v["thin"])
    d = sum(1 for v in arcs.values() if not v["lobha"] and not v["thin"])
    n = a + b + c + d
    p = fisher_exact(a, b, c, d)
    thin_arcs = sorted(k for k, v in arcs.items() if v["thin"])
    print(f"arcs: {n} (lobha+thin={a}, lobha-only={b}, thin-only={c}, neither={d})")
    print(f"thin/churn arcs: {thin_arcs}")
    print(f"lobha|thin rate: {a}/{a + c} vs lobha|no-thin rate: {b}/{b + d}")
    print(f"Fisher one-sided p = {p:.4f}")
    if p < 0.05:
        print("T-C1 HOLDS (pilot): pull+stall travel together — rāga bridge earns its keep")
    else:
        print("T-C1 NULL (pilot): no association — bridge stays hypothesis")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
