#!/usr/bin/env python3
"""essay_query.py — query compiled essays as data (not prose).

Reads swarm/expansion-*.essay.json records. Filters by tier, chunk,
track, theorem. Answers: which claims at which tier ground which chunk?
Which essays mine a track? What cites a theorem?

  python3 tools/essay_query.py --tier R --chunk tsa08-p02
  python3 tools/essay_query.py --track F7
  python3 tools/essay_query.py --theorem "Mala.lean :: count_3"
  python3 tools/essay_query.py --unbound  (T-theorems without span binds)
"""
import argparse
import glob
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def load():
    out = []
    for fp in sorted((HERE / "swarm").glob("expansion-*.essay.json")):
        try:
            out.append(json.loads(fp.read_text(encoding="utf-8")))
        except ValueError:
            continue
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tier", default="")
    ap.add_argument("--chunk", default="")
    ap.add_argument("--track", default="")
    ap.add_argument("--theorem", default="")
    ap.add_argument("--unbound", action="store_true")
    a = ap.parse_args()
    n_e = n_c = 0
    for e in load():
        claims = e.get("claims", [])
        if a.tier:
            claims = [c for c in claims if c.get("tier") == a.tier]
        if a.chunk and a.chunk not in (e.get("chunk") or ""):
            continue
        if a.track and a.track not in (e.get("tracks") or []):
            continue
        if a.theorem and a.theorem not in [t.get("name") for t in e.get("theorems", [])]:
            continue
        if a.unbound:
            claims = [c for c in claims if True]
            thms = [t.get("name") for t in e.get("theorems", [])]
            if not thms:
                continue
            print(f"{e['id']}: binds owed for {', '.join(thms)}")
            n_e += 1
            continue
        if not claims and (a.tier or a.chunk or a.track or a.theorem):
            continue
        n_e += 1
        for c in claims:
            n_c += 1
            print(f"{e['id']} :: {c.get('id')} [{c.get('tier')}] {c.get('text', '')[:90]}")
    print(f"essays: {n_e}, claims shown: {n_c}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
