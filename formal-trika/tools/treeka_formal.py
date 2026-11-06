#!/usr/bin/env python3
"""treeka_formal.py — the Treeka formal column (read-only gap report).

For each translation-work chunk: formal_status + argument coverage.
  formalized — chunk cited by >=1 Lean theorem/KEY in EVIDENCE.json
  armed      — same work has formal coverage, this chunk not directly cited
  unarmed    — no formal coverage in this work at all

Plus per chunk: argmap unit count (units whose verse falls in the chunk's
verse range), L2 presence. Gap report lists: unarmed chunks, argued-but-
unformalized chunks, works with zero formal coverage.

Usage: python3 tools/treeka_formal.py [--tw PATH] [--json]
Read-only by default (writes nothing; use --json for machine output).
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
EV = json.loads((HERE / "EVIDENCE.json").read_text(encoding="utf-8"))
TW = Path(sys.argv[sys.argv.index("--tw") + 1]
          if "--tw" in sys.argv else "/root/translation-work")


def verse_range(s):
    m = re.match(r"\s*(\d+)\.(\d+)\s*-\s*(\d+)\.(\d+)\s*$", s or "")
    if m:
        a, b, c, d = map(int, m.groups())
        return (a, b, c, d)
    m = re.match(r"\s*(\d+)\s*-\s*(\d+)\s*$", s or "")
    if m:
        a, b = map(int, m.groups())
        return (0, a, 0, b)
    return None


def in_range(verse_num, rng):
    # verse_num like 8 / "8" / "v35" / 35 ; rng ((ch1,v1),(ch2,v2)) chapter-aware
    if verse_num is None or rng is None:
        return False
    m = re.search(r"(\d+)$", str(verse_num))
    if not m:
        return False
    v = int(m.group(1))
    (c1, v1, c2, v2) = rng
    if c1 == c2 == 0:
        return v1 <= v <= v2
    # chapter-scoped ranges (e.g. 8.1-8.17): match verse within chapter span
    # when chapter unknown, fall back to plain verse span of v1..v2
    return v1 <= v <= v2


def work_chunks(work_dir):
    out = []
    pf = work_dir / "passages.jsonl"
    if not pf.is_file():
        return out
    for line in pf.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        out.append({"locator": r.get("locator"), "verses": r.get("verses"),
                    "immutable_id": r.get("immutable_id")})
    return out


def argmap_verses(work_dir):
    counts = {}
    for f in sorted((work_dir / "data").glob("*.argmap.json")) if (work_dir / "data").is_dir() else []:
        try:
            rows = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        items = rows if isinstance(rows, list) else rows.get("units", [])
        for u in items:
            v = u.get("verse", u.get("verse_num"))
            counts[v] = counts.get(v, 0) + 1
    return counts


def has_l2(work_dir, locator):
    # L2 per-chunk files or a single L2 doc mentioning the chunk
    pats = list(work_dir.glob("L2-*.md")) + list(work_dir.glob("L2.md"))
    if not pats:
        return None  # unknown layout
    blob = "".join(p.read_text(encoding="utf-8", errors="ignore")[:20000] for p in pats)
    return locator in blob or locator.replace("-", "") in blob


def main():
    cited = {}
    for key, e in EV["entries"].items():
        for c in e.get("chunks", []):
            loc = c.get("locator")
            if loc and loc != "vbt":
                cited.setdefault(loc, []).append(key.split(" :: ")[-1])
    works_with_formal = set()
    for loc in cited:
        for w in ("tsa08", "tsa07", "param", "phr", "vbt", "spanda"):
            if loc.startswith(w):
                works_with_formal.add(w)
    rows = []
    for work in sorted(EV["works"]):
        wdir = TW / {"tsa08": "tantrasara-a08", "tsa07": "tantrasara-a07",
                      "param": "paramarthasara", "phr": "phrdaya",
                      "vbt": "vbt", "spanda": "spanda"}[work]
        amap = argmap_verses(wdir)
        for ch in work_chunks(wdir):
            loc = ch["locator"]
            rng = verse_range(ch["verses"])
            n_arg = sum(n for v, n in amap.items() if in_range(v, rng))
            if loc in cited:
                status = "formalized"
            elif work in works_with_formal:
                status = "armed"
            else:
                status = "unarmed"
            rows.append({"locator": loc, "verses": ch["verses"],
                         "immutable_id": ch.get("immutable_id"),
                         "formal": status,
                         "formal_refs": cited.get(loc, []),
                         "argmap_units": n_arg,
                         "has_l2": has_l2(wdir, loc)})
    if "--json" in sys.argv:
        print(json.dumps(rows, indent=1))
        return 0
    print(f"{'chunk':12} {'verses':10} {'formal':11} {'argmaps':7} L2  refs")
    for r in rows:
        refs = ",".join(r["formal_refs"][:2]) + ("…" if len(r["formal_refs"]) > 2 else "")
        print(f"{r['locator']:12} {str(r['verses']):10} {r['formal']:11} "
              f"{r['argmap_units']:<7} {r['has_l2']} {refs}")
    unarmed = [r["locator"] for r in rows if r["formal"] == "unarmed"]
    armed = [r["locator"] for r in rows if r["formal"] == "armed"]
    noarg = [r["locator"] for r in rows if not r["argmap_units"]]
    print(f"\ncoverage: {len([r for r in rows if r['formal']=='formalized'])}/{len(rows)} formalized, "
          f"{len(armed)} armed, {len(unarmed)} unarmed")
    print("UNARMED (no formal refs in work):", ", ".join(unarmed) or "-")
    print("ARMED (work covered, chunk not cited):", ", ".join(armed) or "-")
    print("NO ARGMAP UNITS:", ", ".join(noarg) or "-")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
