#!/usr/bin/env python3
"""incidence_matrix.py — passagetheorem incidence (coverage you can compute).

Mirrors Thon Ly's class–feature incidence check structurally: rows are
passages (treeka work:locator keys), columns are Lean theorems, cell = 1
iff the theorem's EVIDENCE entry cites the passage. Margins report coverage
both ways (theorems per passage, passages per theorem). Uncovered passages
and unreferenced theorems print as the honest remainder.

  python3 tools/incidence_matrix.py
Writes data/incidence.json {rows, cols, sparse cells, margins}. Exit 0.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def main() -> int:
    treeka = json.loads((HERE / "data" / "treeka.json").read_text(encoding="utf-8"))
    ev = json.loads((HERE / "EVIDENCE.json").read_text(encoding="utf-8"))
    rows = sorted(treeka.get("works", {}))
    cols = sorted(k for k in ev.get("entries", {}))
    loc_theorems = {}
    for key, e in ev.get("entries", {}).items():
        for c in e.get("chunks", []) or []:
            loc_theorems.setdefault(c.get("locator", ""), []).append(key)
    # locator -> treeka keys containing it (suffix match on :locator)
    cells, row_cov = [], {}
    for rk in rows:
        loc = rk.split(":", 1)[-1] if ":" in rk else rk
        hits = sorted(loc_theorems.get(loc, []))
        row_cov[rk] = hits
        for h in hits:
            cells.append([rk, h])
    col_cov = {c: sorted(rk for rk in rows
                         if c in row_cov.get(rk, [])) for c in cols}
    bare_passages = [rk for rk in rows if not row_cov[rk]]
    lone_theorems = [c for c in cols if not col_cov[c]]
    doc = {"format": "trika-incidence/1",
           "passages": len(rows), "theorems": len(cols), "cells": len(cells),
           "cells_sparse": cells,
           "bare_passages": len(bare_passages), "lone_theorems": lone_theorems,
           "note": "incidence = EVIDENCE chunk cites only; argmap/treeka links are separate columns"}
    (HERE / "data" / "incidence.json").write_text(
        json.dumps(doc, ensure_ascii=False, indent=1) + "\n")
    print(f"incidence: {len(rows)} passages x {len(cols)} theorems = {len(cells)} cells; "
          f"bare: {len(bare_passages)}; lone theorems: {len(lone_theorems)}")
    if lone_theorems[:8]:
        print("lone:", ", ".join(lone_theorems[:8]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
