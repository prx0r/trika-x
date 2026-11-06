#!/usr/bin/env python3
"""work_inventory.py — full translation-work estate inventory + DB record.

Walks every work dir (top-level + mystics/* sub-works), classifies
(work/infra/group), records per-layer presence + counts, writes
data/work-inventory.json, and (with --db) upserts missing works rows +
HAS_LAYER assertions + a derivation_activity row into the box openpatala
DB. Read-only wrt translation-work. Idempotent DB writes.
Usage: python3 formal-trika/tools/work_inventory.py [--db] [--out PATH]
"""
import argparse
import glob
import hashlib
import json
from pathlib import Path

TW = Path("/root/translation-work")
HERE = Path(__file__).resolve().parent.parent
INFRA = {"logs", "lore", "process", "skills", "source-maps", "tests",
         "voice-scripts", "schemas", "tools", "docs"}
SOURCE_VARIANTS = ["SOURCE.sha", "SOURCE.txt", "SOURCE.md", "source.txt",
                   "source/record.json", "source/edition.json",
                   "source/manifest.json"]


def layers(wd: Path):
    def any_glob(*pats):
        out = []
        for p in pats:
            out.extend(glob.glob(str(wd / p)))
        return out

    L = {}
    L["passages"] = len(any_glob("passages.jsonl"))
    L["T1"] = len(any_glob("T1*.md"))
    L["L0"] = len(any_glob("data/*.l0.json", "cm/l0cm*.json"))
    L["argmap_json"] = len(any_glob("data/*.argmap.json"))
    L["argmap_md"] = len(any_glob("ARGMAP.md"))
    L["L2"] = len(any_glob("L2*.md", "L2.md"))
    L["c1"] = len(any_glob("c1", "c1/*", "*C1*.md", "C1.md"))
    L["scholar"] = 1 if (wd / "scholar").is_dir() else 0
    L["gate"] = len(any_glob("GATE.json"))
    L["source"] = next((v for v in SOURCE_VARIANTS if (wd / v).is_file()), "")
    return L


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", action="store_true")
    ap.add_argument("--dsn", default="postgresql://patala:patala@localhost:5432/openpatala")
    ap.add_argument("--out", type=Path, default=HERE / "data" / "work-inventory.json")
    a = ap.parse_args()
    works = {}
    for d in sorted(TW.iterdir()):
        if not d.is_dir() or d.name.startswith("."):
            continue
        if d.name in INFRA:
            works[d.name] = {"kind": "infra", "layers": {}}
            continue
        if d.name == "mystics":
            works["mystics"] = {"kind": "group", "layers": {}}
            for s in sorted(d.iterdir()):
                if s.is_dir():
                    works[f"mystics/{s.name}"] = {"kind": "work", "layers": layers(s)}
            continue
        works[d.name] = {"kind": "work", "layers": layers(d)}
    n_work = sum(1 for v in works.values() if v["kind"] == "work")
    n_ledger = sum(1 for v in works.values()
                   if v["kind"] == "work" and v["layers"].get("passages"))
    doc = {"works": works,
           "summary": {"dirs": len(works), "works": n_work,
                       "with_ledger": n_ledger,
                       "without_ledger": [k for k, v in sorted(works.items())
                                          if v["kind"] == "work"
                                          and not v["layers"].get("passages")]}}
    a.out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"dirs: {len(works)} (works {n_work}, ledger {n_ledger}); "
          f"no-ledger works: {len(doc['summary']['without_ledger'])} -> {a.out}")
    if a.db:
        import psycopg2
        from psycopg2.extras import Json
        con = psycopg2.connect(a.dsn)
        cur = con.cursor()
        w_ins = a_ins = 0
        for name, spec in sorted(works.items()):
            if spec["kind"] != "work":
                continue
            cur.execute("INSERT INTO works (id, preferred_title, work_type, external_ids) "
                        "VALUES (%s,%s,'TEXT',%s) ON CONFLICT (id) DO NOTHING RETURNING id",
                        (name, name, Json({"estate": "translation-work"})))
            if cur.fetchone():
                w_ins += 1
            for layer, val in sorted(spec["layers"].items()):
                aid = f"tw-inv:{name}:{layer}"
                cur.execute(
                    "INSERT INTO assertions (id, subject_id, predicate_uri, literal, "
                    "epistemic_mode, asserted_by, recorded_at, lifecycle, created_from_event) "
                    "VALUES (%s,%s,'patala:hasLayer',%s,'observed','work-inventory',NOW(),'ACTIVE',"
                    "'seed:work-inventory-2026-11-06') "
                    "ON CONFLICT (id) DO NOTHING RETURNING id",
                    (aid, name, json.dumps({"present": bool(val), "count": val if isinstance(val, int) else 0})))
                if cur.fetchone():
                    a_ins += 1
        cur.execute(
            "INSERT INTO derivation_activities (id, activity_type, inputs, outputs, software, started_at, completed_at) "
            "VALUES (%s,'estate-inventory',%s,%s,%s,NOW(),NOW()) "
            "ON CONFLICT (id) DO NOTHING RETURNING id",
            (f"tw-inventory-{len(works)}works",
             Json({"works": n_work}), Json({"works_rows": w_ins, "assertions": a_ins}),
             Json({"tool": "formal-trika/tools/work_inventory.py"})))
        con.commit()
        print(f"db: works +{w_ins}, assertions +{a_ins} (idempotent rerun = +0)")
        con.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
