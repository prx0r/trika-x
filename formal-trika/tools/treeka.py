#!/usr/bin/env python3
"""treeka.py — B5: read-only assembler (works → passages → nodes → cruxes → essays).

Joins, never invents. Entries keyed work:locator (bare locators COLLIDE
across works: anu-* shared by anubhavanivedana/anuttarastika, par-*
shared by parapravesika/paramarthacarca — recorded in ambiguous).
  works:    svread/source-map.json (87 ledgers + bridge status)
  passages: translation-work/*/passages.jsonl (locator + verses)
  nodes:    formal-trika/data/argmap-nodes.jsonl (argued? = has premises)
  cruxes:   formal-trika/data/crux-queue.jsonl (cruxless? = no candidate)
  formal:   formal-trika/EVIDENCE.json chunks (formalized? = cited)
  essays:   translation-work/*/scholar/essays/*.json (essayless? per locator)
Output: formal-trika/data/treeka.json {works, gaps, ambiguous, counts}.
Gap report drives the crux queue (Phase 3.1): unargued passages,
cruxless arguments, essayless cruxes, unformalized chunks.
Usage: python3 formal-trika/tools/treeka.py [--tw PATH] [--out PATH]
"""
import argparse
import glob
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def load_jsonl(p):
    try:
        return [json.loads(l) for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip()]
    except OSError:
        return []


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tw", type=Path, default=Path("/root/translation-work"))
    ap.add_argument("--sourcemap", type=Path, default=Path("/root/svread/source-map.json"))
    ap.add_argument("--out", type=Path, default=HERE / "data" / "treeka.json")
    a = ap.parse_args()
    smap = json.loads(a.sourcemap.read_text(encoding="utf-8"))["works"]
    nodes = load_jsonl(HERE / "data" / "argmap-nodes.jsonl")
    queue = load_jsonl(HERE / "data" / "crux-queue.jsonl")
    ev = json.loads((HERE / "EVIDENCE.json").read_text(encoding="utf-8"))
    # formal pairs (workdir, locator): via EVIDENCE works chunks + ledger dir
    formal_pairs, formal_bare = set(), set()
    for wkey, spec in ev.get("works", {}).items():
        ledger = spec.get("ledger", "")
        wd = ledger.split("translation-work/")[-1].split("/")[0] if "translation-work/" in ledger else None
        for loc in spec.get("chunks", []):
            formal_bare.add(loc)
            if wd:
                formal_pairs.add((wd, loc))
    for e in ev.get("entries", {}).values():
        for c in e.get("chunks", []):
            if c.get("locator") not in (None, "vbt"):
                formal_bare.add(c["locator"])
    nodes_by_key, crux_by_key = {}, {}
    for n in nodes:
        nodes_by_key.setdefault((n.get("work"), n.get("locator")), []).append(n)
    for q in queue:
        if q.get("kind") == "argmap-uncertainty" and q.get("locator"):
            crux_by_key.setdefault((q.get("work"), q.get("locator")), []).append(q)
    seen_work, ambiguous = {}, set()
    for (w, loc) in list(nodes_by_key):
        if loc in seen_work and seen_work[loc] != w:
            ambiguous.add(loc)
        seen_work.setdefault(loc, w)
    essays_by_loc = {}
    for f in glob.glob(str(a.tw / "*" / "scholar" / "essays" / "*.json")):
        try:
            d = json.loads(Path(f).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        t = d.get("target") or d.get("entry", {}).get("target")
        if t:
            essays_by_loc.setdefault(t, []).append(Path(f).name)
    works, gaps = {}, {"unargued": [], "cruxless": [], "essayless": [], "unformalized": []}
    for workdir, meta in sorted(smap.items()):
        for line in (a.tw / workdir / "passages.jsonl").read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                p = json.loads(line)
            except json.JSONDecodeError:
                continue
            loc = p.get("locator")
            if not loc:
                continue
            key = f"{workdir}:{loc}"
            ns = nodes_by_key.get((workdir, loc), [])
            argued = any(n.get("premises") for n in ns)
            formalized = ((workdir, loc) in formal_pairs
                          or (loc in formal_bare and loc not in ambiguous))
            entry = {"work": workdir, "verses": p.get("verses"),
                     "argued": argued, "nodes": len(ns),
                     "cruxes": len(crux_by_key.get((workdir, loc), [])),
                     "formalized": formalized,
                     "essays": essays_by_loc.get(loc, []),
                     "bridge": meta.get("status", "?")}
            works[key] = entry
            if not argued:
                gaps["unargued"].append(key)
            elif not entry["cruxes"]:
                gaps["cruxless"].append(key)
            if not entry["essays"] and (argued or entry["cruxes"]):
                gaps["essayless"].append(key)
            if not entry["formalized"]:
                gaps["unformalized"].append(key)
    doc = {"works": works, "gaps": gaps, "ambiguous_locators": sorted(ambiguous),
           "counts": {"passages": len(works), **{k: len(v) for k, v in gaps.items()}}}
    a.out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"passages: {len(works)}; gaps: " +
          ", ".join(f"{k}={len(v)}" for k, v in gaps.items()) +
          f"; ambiguous: {len(ambiguous)} -> {a.out}")


if __name__ == "__main__":
    raise SystemExit(main())
