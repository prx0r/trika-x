#!/usr/bin/env python3
"""biblio_sweep.py — per-work scholarship inventory (Abhinavagupta first).

Read-only across lanes. For every Abhinavagupta work (dossiers with AUTHOR
Abhinavagupta + translation-work workdirs), reports what scholarship exists
IN OUR LANES: dossier assertions/ext-ids, record edition/rights, lore links,
translation state, formal theorems, svread projection — and names what's
missing (editions, translations, papers, ours). Missing bibliography is
data (gap lists), never silence, never invented URLs.

  python3 tools/biblio_sweep.py [--tw PATH] [--out FILE]
Writes data/biblio-abhinavagupta.json {works{}, gaps, counts}.
"""
import argparse
import glob
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
OP = Path(os.environ.get("OPENPATALA_CHECKOUT", "/root/openpatala"))
TW = Path("/root/translation-work")
SV = Path("/root/svread")


def dossiers():
    out = {}
    for fp in sorted((OP / "data" / "gold").glob("PTCND_sa_abhinavagupta-*.json")):
        try:
            d = json.loads(fp.read_text(encoding="utf-8"))
        except ValueError:
            continue
        auth = [a.get("literal") for a in d.get("assertions", [])
                if a.get("predicate") == "AUTHOR"]
        if any("Abhinavagupta" in (x or "") for x in auth):
            out[d.get("work_id")] = d
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tw", type=Path, default=TW)
    ap.add_argument("--sv", type=Path, default=SV)
    ap.add_argument("--out", type=Path, default=HERE / "data" / "biblio-abhinavagupta.json")
    a = ap.parse_args()
    doss = dossiers()
    try:
        tmap = json.loads((a.tw / "source-maps" / "openpatala.json").read_text(encoding="utf-8")).get("works", {})
    except (OSError, ValueError):
        tmap = {}
    try:
        reg = {(w.get("work") or w.get("id")): w
               for w in json.loads((a.tw / "REGISTRY.json").read_text(encoding="utf-8")).get("works", [])}
    except (OSError, ValueError):
        reg = {}
    try:
        links = json.loads((a.tw / "lore" / "links.json").read_text(encoding="utf-8")).get("works", {})
    except (OSError, ValueError):
        links = {}
    ev = json.loads((HERE / "EVIDENCE.json").read_text(encoding="utf-8"))
    works = {}
    for wid, d in sorted(doss.items()):
        ext = [(x.get("scheme"), x.get("identifier")) for x in d.get("external_identifiers", [])]
        # translation-work workdirs whose map entry points at this dossier
        wds = sorted(w for w, m in tmap.items()
                     if isinstance(m, dict) and m.get("openpatala_work_id") == wid)
        recs = {}
        for w in wds:
            rp = a.tw / w / "source" / "record.json"
            try:
                r = json.loads(rp.read_text(encoding="utf-8")) if rp.is_file() else None
            except ValueError:
                r = {"status": "INVALID-JSON"}
            recs[w] = {"record": (r or {}).get("status"),
                       "edition": ((r or {}).get("edition") or {}).get("label"),
                       "rights": ((r or {}).get("rights") or {}).get("status"),
                       "registry": (reg.get(w) or {}).get("status"),
                       "projection": (a.sv / "data" / "scholar" / f"{w}.json").is_file()}
        # formal coverage per work lives in treeka.json (formal_refs by
        # work:locator); joined at review time, not duplicated here.
        works[wid] = {
            "title": d.get("title"),
            "assertions": len(d.get("assertions", [])),
            "predicates": sorted({x.get("predicate") for x in d.get("assertions", [])}),
            "external_ids": ext,
            "mapped_workdirs": wds,
            "records": recs,
            "lore_links": sorted(links.keys() & set(wds)),
            "bibliography": {"editions": [], "translations": [], "papers": [], "ours": []},
            "gaps": ["editions bibliography", "translations bibliography",
                     "papers bibliography", "our publications (none yet)"],
        }
    doc = {"format": "trika-biblio-sweep/1", "date": __import__("datetime").date.today().isoformat(),
           "dossiers": len(doss), "works": works,
           "counts": {"dossiers": len(doss),
                      "mapped_workdirs": sum(len(v["mapped_workdirs"]) for v in works.values())}}
    a.out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n")
    print(f"dossiers: {len(doss)}; mapped workdirs: {doc['counts']['mapped_workdirs']} -> {a.out.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
