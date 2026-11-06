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
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import bridge_resolve

HERE = Path(__file__).resolve().parent.parent
EV = json.loads((HERE / "EVIDENCE.json").read_text(encoding="utf-8"))
DEFAULT_TW = Path(os.environ.get("TRANSLATION_WORK", HERE.parent.parent / "translation-work"))


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
        raise ValueError(f"missing passage ledger: {pf}")
    for line in pf.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        out.append({"locator": r.get("locator"), "verses": r.get("verses"),
                    "immutable_id": r.get("immutable_id")})
    if not out:
        raise ValueError(f"empty passage ledger: {pf}")
    return out


def argmap_verses(work_dir):
    counts = {}
    files = sorted((work_dir / "data").glob("*.argmap.json")) if (work_dir / "data").is_dir() else []
    if not files:
        return None
    for f in files:
        rows = json.loads(f.read_text(encoding="utf-8"))
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
    return True if locator in blob or locator.replace("-", "") in blob else None


def verify_input(tw):
    """Require the pinned checkout, clean work inputs, and exact ledger bytes."""
    snapshot = bridge_resolve.read_json(bridge_resolve.SNAPSHOT_PATH)
    bridge_resolve.inventory(snapshot, bridge_resolve.read_json(bridge_resolve.MAP_PATH), EV)
    bridge_resolve.verify_ledgers(tw, snapshot)
    def git(*args):
        r = subprocess.run(["git", "-C", str(tw), *args], capture_output=True, text=True)
        if r.returncode:
            raise ValueError(f"translation-work is not an accessible Git checkout: {r.stderr.strip()}")
        return r.stdout.strip()
    revision = git("rev-parse", "HEAD")
    if revision != snapshot["revision"]:
        raise ValueError(f"translation-work revision {revision} differs from pinned {snapshot['revision']}")
    dirs = sorted({str(Path(x["ledger"]).parent) for x in snapshot["works"].values()})
    if git("status", "--porcelain", "--", *dirs):
        raise ValueError("translation-work inputs have uncommitted changes")
    return revision


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tw", type=Path, default=DEFAULT_TW)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        revision = verify_input(args.tw)
        return report(args.tw, args.json, revision)
    except (OSError, json.JSONDecodeError, ValueError, TypeError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


def report(tw, json_output, revision):
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
        wdir = tw / {"tsa08": "tantrasara-a08", "tsa07": "tantrasara-a07",
                      "param": "paramarthasara", "phr": "phrdaya",
                      "vbt": "vbt", "spanda": "spanda"}[work]
        amap = argmap_verses(wdir)
        for ch in work_chunks(wdir):
            loc = ch["locator"]
            rng = verse_range(ch["verses"])
            n_arg = sum(n for v, n in amap.items() if in_range(v, rng)) if amap is not None and rng is not None else None
            if loc in cited:
                status = "formalized"
            elif work in works_with_formal:
                status = "armed"
            else:
                status = "unarmed"
            rows.append({"locator": loc, "verses": ch["verses"],
                         "immutable_id": ch.get("immutable_id"),
                         "formal": status,
                         "formal_basis": "curated registry reference; not source entailment",
                         "translation_work_revision": revision,
                         "formal_refs": cited.get(loc, []),
                         "argmap_units": n_arg,
                         "has_l2": has_l2(wdir, loc)})
    if json_output:
        print(json.dumps(rows, indent=1))
        return 0
    print(f"translation-work: {revision}; formalized = registry reference, not verified entailment")
    print("Argmap counts and L2 matches are scans; no match does not prove absence.")
    print(f"{'chunk':12} {'verses':10} {'formal':11} {'argmaps':7} L2  refs")
    for r in rows:
        refs = ",".join(r["formal_refs"][:2]) + ("…" if len(r["formal_refs"]) > 2 else "")
        print(f"{r['locator']:12} {str(r['verses']):10} {r['formal']:11} "
              f"{str(r['argmap_units']):7} {r['has_l2']} {refs}")
    unarmed = [r["locator"] for r in rows if r["formal"] == "unarmed"]
    armed = [r["locator"] for r in rows if r["formal"] == "armed"]
    noarg = [r["locator"] for r in rows if r["argmap_units"] == 0]
    unknown = [r["locator"] for r in rows if r["argmap_units"] is None]
    print(f"\ncoverage: {len([r for r in rows if r['formal']=='formalized'])}/{len(rows)} formalized, "
          f"{len(armed)} armed, {len(unarmed)} unarmed")
    print("UNARMED (no formal refs in work):", ", ".join(unarmed) or "-")
    print("ARMED (work covered, chunk not cited):", ", ".join(armed) or "-")
    print("NO MATCHED ARGMAP UNITS:", ", ".join(noarg) or "-")
    print("ARGMAP SCAN UNKNOWN:", ", ".join(unknown) or "-")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
