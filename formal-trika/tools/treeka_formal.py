#!/usr/bin/env python3
"""treeka_formal.py — the Treeka formal column (read-only gap report).

For each translation-work chunk: registry references + argument coverage.
  direct_reference — chunk named in at least one EVIDENCE.json entry
  work_reference   — another chunk in the work is named, but this one is not
  no_reference     — no passage in the work is named by an entry

These are registry associations, not evidence that the source was formalized,
the theorem was checked, or that any interpretation has been reviewed.

Plus per chunk: argmap unit count (units whose verse falls in the chunk's
verse range), L2 presence. Gap report lists: unarmed chunks, argued-but-
unreferenced chunks, works with zero registry references.

Usage: python3 tools/treeka_formal.py [--tw PATH] [--json]
Read-only by default (writes nothing; use --json for machine output).
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import bridge_resolve
import argmap_nodes

HERE = Path(__file__).resolve().parent.parent
EV = json.loads((HERE / "EVIDENCE.json").read_text(encoding="utf-8"))
DEFAULT_TW = Path(os.environ.get("TRANSLATION_WORK", HERE.parent.parent / "translation-work"))


def verse_range(s):
    span = argmap_nodes.parse_span(s)
    return span[1:] if span and span[0] == 'verse' else None


def in_range(verse_num, rng, single_chapter=None):
    """True/False only when the coordinate is comparable; otherwise None."""
    if rng is None:
        return None
    coord = (verse_num if isinstance(verse_num, tuple)
             else argmap_nodes.verse_coordinate({'verse': verse_num}))
    if coord is None:
        return None
    c1, v1, c2, v2 = rng
    if c1 is None and coord[0] is not None:
        return None
    if c1 is not None and coord[0] is None:
        if c1 != c2 or single_chapter != c1:
            return None
        coord = (single_chapter, coord[1])
    return argmap_nodes.contains(('verse', c1, v1, c2, v2), coord)


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
        if isinstance(rows, list):
            items = rows
        elif isinstance(rows, dict) and ('units' in rows or 'argmaps' in rows):
            items = rows.get('units', rows.get('argmaps'))
        else:
            return None  # unrecognized layout is not an empty argmap
        if not isinstance(items, list) or any(not isinstance(u, dict) for u in items):
            raise ValueError(f'invalid argmap units in {f}')
        for u in items:
            v = argmap_nodes.verse_coordinate(u)
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
                cited.setdefault(loc, []).append(key)
    works_with_formal = {
        work for work, spec in EV["works"].items()
        if any(loc in cited for loc in spec.get("chunks", []))
    }
    rows = []
    for work in sorted(EV["works"]):
        wdir = tw / {"tsa08": "tantrasara-a08", "tsa07": "tantrasara-a07",
                      "param": "paramarthasara", "phr": "phrdaya",
                      "vbt": "vbt", "spanda": "spanda"}[work]
        amap = argmap_verses(wdir)
        chunks = work_chunks(wdir)
        parsed = [verse_range(ch['verses']) for ch in chunks]
        chapters = {c for rng in parsed if rng for c in (rng[0], rng[2]) if c is not None}
        single_chapter = next(iter(chapters)) if len(chapters) == 1 else None
        for ch in chunks:
            loc = ch["locator"]
            rng = verse_range(ch["verses"])
            comparisons = [(in_range(v, rng, single_chapter), n) for v, n in amap.items()] if amap is not None and rng is not None else None
            n_arg = (sum(n for matched, n in comparisons if matched)
                     if comparisons is not None and all(matched is not None for matched, _ in comparisons)
                     else None)
            if loc in cited:
                status = "direct_reference"
            elif work in works_with_formal:
                status = "work_reference"
            else:
                status = "no_reference"
            rows.append({"locator": loc, "verses": ch["verses"],
                         "immutable_id": ch.get("immutable_id"),
                         "formal": status,
                         "formal_basis": "registry association only; no proof or source interpretation assessed",
                         "translation_work_revision": revision,
                         "formal_refs": cited.get(loc, []),
                         "argmap_units": n_arg,
                         "has_l2": has_l2(wdir, loc)})
    if json_output:
        print(json.dumps(rows, indent=1))
        return 0
    print(f"translation-work: {revision}; references are not checked source-to-model entailments")
    print("Argmap counts and L2 matches are scans; no match does not prove absence.")
    print(f"{'chunk':12} {'verses':10} {'formal':16} {'argmaps':7} L2  refs")
    for r in rows:
        refs = ",".join(r["formal_refs"][:2]) + ("…" if len(r["formal_refs"]) > 2 else "")
        print(f"{r['locator']:12} {str(r['verses']):10} {r['formal']:16} "
              f"{str(r['argmap_units']):7} {r['has_l2']} {refs}")
    unarmed = [r["locator"] for r in rows if r["formal"] == "no_reference"]
    armed = [r["locator"] for r in rows if r["formal"] == "work_reference"]
    noarg = [r["locator"] for r in rows if r["argmap_units"] == 0]
    unknown = [r["locator"] for r in rows if r["argmap_units"] is None]
    print(f"\nreferences: {len([r for r in rows if r['formal']=='direct_reference'])}/{len(rows)} direct, "
          f"{len(armed)} in referenced works, {len(unarmed)} in unreferenced works")
    print("NO REFERENCES IN WORK:", ", ".join(unarmed) or "-")
    print("ANOTHER PASSAGE REFERENCED:", ", ".join(armed) or "-")
    print("NO MATCHED ARGMAP UNITS:", ", ".join(noarg) or "-")
    print("ARGMAP SCAN UNKNOWN:", ", ".join(unknown) or "-")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
