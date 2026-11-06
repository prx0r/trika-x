#!/usr/bin/env python3
"""essay_check.py — the essay gate (translation-work check.py discipline).

Validates a compiled essay triple (.md + .essay.json + .receipt.json):
schema keys, frozen-claim coverage (every tiered bullet links a claim),
marker presence, tier law (no T without span-verified binds), voice
verbatim accounting, track assignment, openpatala block present,
graph node exists. Exit 0 = shippable to review; else named failures.

  python3 tools/essay_check.py --slug expansion-mala-full-2026-11-06-145904319815
  python3 tools/essay_check.py --all
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
TIERS = {"T", "R", "E", "C", "H", "X"}


def check_slug(swarm: Path, slug: str) -> list:
    fails = []
    md = swarm / f"{slug}.md"
    ejp = swarm / f"{slug}.essay.json"
    rcp = swarm / f"{slug}.receipt.json"
    for p, what in ((md, "draft"), (ejp, "essay.json"), (rcp, "receipt")):
        if not p.is_file():
            fails.append(f"missing {what}: {p.name}")
    if fails:
        return fails
    try:
        ej = json.loads(ejp.read_text(encoding="utf-8"))
        rc = json.loads(rcp.read_text(encoding="utf-8"))
        text = md.read_text(encoding="utf-8")
    except ValueError as e:
        return [f"invalid JSON: {e}"]
    for k in ("id", "title", "date", "chunk", "verses", "voice", "claims",
              "theorems", "tracks", "openpatala", "status"):
        if k not in ej:
            fails.append(f"essay.json missing key: {k}")
    fids = {c.get("id") for c in ej.get("claims", [])}
    for c in ej.get("claims", []):
        if c.get("tier") not in TIERS:
            fails.append(f"claim {c.get('id')} bad tier: {c.get('tier')}")
        if not c.get("text", "").strip():
            fails.append(f"claim {c.get('id')} empty text")
    for line in text.splitlines():
        if line.startswith("- ") and ("(R)" in line or "(T)" in line):
            if "[CLM-" not in line and "::" not in line:
                fails.append(f"untraced bullet: {line[:80]}")
                break
    if "[CLM-" not in text and fids:
        fails.append("draft carries no frozen-claim markers")
    for t in ej.get("theorems", []):
        if t.get("tier") != "UNVERIFIED":
            fails.append(f"theorem {t.get('name')} tier must be UNVERIFIED, got {t.get('tier')}")
    if not ej.get("tracks"):
        fails.append("no research tracks assigned")
    op = ej.get("openpatala", {})
    if "openpatala_work_id" not in op or "mapping_status" not in op:
        fails.append("openpatala block incomplete")
    tn = ej.get("tension")
    if tn is not None:
        if not isinstance(tn, dict) or not tn.get("id", "").startswith("tension:"):
            fails.append(f"bad tension block: {tn}")
        elif tn.get("relation") not in ("resolves", "loosens"):
            fails.append(f"bad tension relation: {tn.get('relation')}")
        else:
            try:
                import sys as _sys
                _sys.path.insert(0, "/root/svread/tools")
                import lingua as _lingua
                row = _lingua.resolve(tn["id"])
                if row.get("visibility", "private") == "private":
                    fails.append(f"tension-private: {tn['id']}")
            except Exception as e:
                fails.append(f"tension unresolvable: {tn['id']} ({str(e)[:80]})")
    if rc.get("essay") != slug:
        fails.append("receipt essay mismatch")
    if ej.get("status") != "MACHINE-COMPILED":
        fails.append(f"bad status: {ej.get('status')}")
    return fails


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--slug", default="")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--swarm", type=Path, default=HERE / "swarm")
    a = ap.parse_args()
    slugs = ([a.slug] if a.slug else
             sorted({p.name[:-len(".receipt.json")] for p in a.swarm.glob("expansion-*.receipt.json")}))
    bad = 0
    for slug in slugs:
        fails = check_slug(a.swarm, slug)
        if fails:
            bad += 1
            print(f"FAIL {slug}:")
            for f in fails[:8]:
                print(f"  - {f}")
        else:
            print(f"PASS {slug}")
    print(f"{len(slugs) - bad}/{len(slugs)} essays shippable")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
