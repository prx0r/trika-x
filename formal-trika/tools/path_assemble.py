#!/usr/bin/env python3
"""path_assemble.py — E4: assemble pathways from units + three spines.

A pathway = question (why/what) → āhṇika (where the text answers) →
practice (what to do with the body). Path IDs extend the lingua grammar:
path:trika/<slug>; units referenced by unit_id (never inlined, never
renumbered — renames keep alias, cf. DATA-MODEL principles).
Fail-closed law (SYLLABUS-COMPILER step 3): requires-diksha units render
as STUDY with the tradition's own conditions quoted, never as DIY
checklists. Prereq DAG = spine order + eligibility flags.
Usage: python3 formal-trika/tools/path_assemble.py --units U1.json [U2...]
       --spine ts-six|ta-37|body-8 --slug NAME --out path.json
"""
import argparse
import hashlib
import json
from pathlib import Path

SPINES = {
    "ts-six": ["own-nature", "why-not-seen", "what-binds", "how-to-see",
               "how-to-practice", "what-remains"],
    "ta-37": [f"ahnika-{i:02d}" for i in range(1, 38)],
    "body-8": ["ordinary", "mapped", "mantra-body", "deity-body",
               "cosmos-body", "install-cadence", "month-review", "embody"],
}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--units", nargs="+", type=Path, required=True)
    ap.add_argument("--spine", choices=list(SPINES), required=True)
    ap.add_argument("--slug", required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    units = [json.loads(p.read_text(encoding="utf-8")) for p in a.units]
    items, edges = [], []
    prev = None
    for i, u in enumerate(units):
        elig = u.get("eligibility", {}).get("eligibility", "study")
        if elig == "requires-diksha":
            render = {"mode": "STUDY",
                      "note": "Traditionally conferred: steps withheld pending teacher. "
                              "Study the source span; do not self-initiate.",
                      "conditions": u.get("safety", [])}
        else:
            render = {"mode": "PRACTICE" if elig == "doable" else "STUDY",
                      "unit": u.get("unit_id"), "safety": u.get("safety", [])}
        items.append({"n": i + 1, "unit_id": u.get("unit_id"),
                      "spine_station": SPINES[a.spine][i % len(SPINES[a.spine])],
                      "eligibility": elig, "render": render,
                      "source_refs": u.get("source_refs", [])})
        if prev:
            edges.append([prev, u.get("unit_id")])
        prev = u.get("unit_id")
    path = {"path_id": f"path:trika/{a.slug}", "kind": "pathway/1",
            "spine": a.spine, "items": items, "prereq_edges": edges,
            "status": "review"}
    path["path_sha256"] = hashlib.sha256(
        json.dumps(path, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    a.out.write_text(json.dumps(path, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    diy = sum(1 for it in items if it["render"]["mode"] == "PRACTICE"
              and it["eligibility"] == "requires-diksha")
    assert diy == 0, "diksha unit rendered DIY — fail-closed violated"
    print(f"path {path['path_id']}: {len(items)} items, {len(edges)} edges -> {a.out}")


if __name__ == "__main__":
    raise SystemExit(main())
