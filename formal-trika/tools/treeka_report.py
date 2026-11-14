#!/usr/bin/env python3
"""treeka_report.py — the Treeka view as a readable, queryable gap report.

Reads formal-trika/data/treeka.json (regenerate with treeka.py) and the
trace index, and prints works → passages → arguments → cruxes → essays +
gap lists (unargued, cruxless, essayless, unformalised, ambiguous).

  python3 formal-trika/tools/treeka_report.py                # full report
  python3 formal-trika/tools/treeka_report.py --work phrdaya
  python3 formal-trika/tools/treeka_report.py --queue        # rung queue only
  python3 formal-trika/tools/treeka_report.py --md out.md   # markdown file

Rung queue order is the published gap list (never taste): phr mala rows
first, then VBT clusters, then tsa08 remainder, then the rest alphabetically.
A passage is ARGUED (has argmap premises), CRUXED (has crux candidates),
ESSAYED (has citing essays), REFERENCED (EVIDENCE registry ref — unreviewed
association, not proof). Nothing here promotes a registry ref to a proof.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
TREEKA = HERE / "data" / "treeka.json"
TRACES = HERE / "data" / "traces" / "index.json"
QUEUE_PREFIXES = ("phrdaya:", "vbt:", "tantrasara-a08:", "tantrasara-a")


def load() -> dict:
    return json.loads(TREEKA.read_text(encoding="utf-8"))


def queue_key(key: str) -> tuple:
    for i, p in enumerate(QUEUE_PREFIXES):
        if key.startswith(p):
            return (i, key)
    return (len(QUEUE_PREFIXES), key)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--work", default="", help="filter by work prefix")
    ap.add_argument("--queue", action="store_true", help="rung queue only")
    ap.add_argument("--md", default="", help="write markdown to file")
    a = ap.parse_args()

    d = load()
    works = d.get("works", {})
    gaps = d.get("gaps", {})
    amb = d.get("ambiguous_locators", [])
    counts = d.get("counts", {})
    if a.work:
        # Scope EVERY corpus-wide list to the filtered passage set. The
        # printed summary must never mix filtered passages with corpus-wide
        # gap counts (the --work bug the external review caught).
        works = {k: v for k, v in works.items()
                 if k == a.work or k.startswith(a.work + ":")}
        gaps = {gk: [k for k in gv if k in works]
                for gk, gv in gaps.items()}
        amb = [x for x in amb
               if any(k.endswith(":" + x) for k in works)]
        counts = {"passages": len(works)}
        counts.update({gk: len(gv) for gk, gv in gaps.items()})
    unformal = [k for k, v in works.items()
                if not v.get("formal_reference")]

    lines: list[str] = []
    lines.append(f"Treeka gap report — {len(works)} passages, "
                 f"{counts}")
    lines.append(f"unargued={len(gaps.get('unargued', []))} "
                 f"cruxless={len(gaps.get('cruxless', []))} "
                 f"essayless={len(gaps.get('essayless', []))} "
                 f"unformalised={len(gaps.get('no_formal_reference', []))} "
                 f"ambiguous={len(amb)}")
    lines.append("formal_reference = registry association only, not proof.")

    if not a.queue:
        lines.append("")
        lines.append("work | passages(unargued) | cruxes | essays | "
                     "formal-refs")
        per: dict[str, dict] = {}
        for key, w in works.items():
            work = w.get("work", key.split(":")[0])
            r = per.setdefault(work, {"n": 0, "u": 0, "c": 0, "e": 0, "f": 0})
            r["n"] += 1
            if not w.get("argued"):
                r["u"] += 1
            r["c"] += w.get("cruxes", 0) or 0
            r["e"] += len(w.get("essays", []) or [])
            if w.get("formal_reference"):
                r["f"] += 1
        for work in sorted(per):
            r = per[work]
            lines.append(f"{work} | {r['n']} ({r['u']} unargued) | "
                         f"{r['c']} | {r['e']} | {r['f']}")

    lines.append("")
    lines.append("RUNG QUEUE (gap-list order): unformalised passages")
    for key in sorted(unformal, key=queue_key):
        w = works[key]
        arg = "argued" if w.get("argued") else "UNARGUED"
        cx = f"cruxes={w.get('cruxes', 0)}"
        lines.append(f"  {key} [{arg}, {cx}]")

    if amb and not a.queue:
        lines.append("")
        lines.append(f"AMBIGUOUS ({len(amb)}): recorded, never auto-resolving")
        for x in amb[:20]:
            lines.append(f"  {x}")
        if len(amb) > 20:
            lines.append(f"  ... +{len(amb) - 20} more (see treeka.json)")

    text = "\n".join(lines) + "\n"
    if a.md:
        Path(a.md).write_text(text, encoding="utf-8")
        print(f"treeka_report: wrote {a.md}")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
