#!/usr/bin/env python3
"""claim.py — rung task claims (no collisions, lead sees all).

Ports AxiomMath CONTRIBUTING's claim-before-you-start: a blueprint (exact
statement + intended Lean + declarations to use/extend + proof outline) is
filed BEFORE modeling, so swarm efforts don't collide and the lead can
approve or redirect. Statuses: open -> approved (lead) -> done | dropped.
Approval is a repo edit by the lead (or PR review), never self-approval.

  python3 tools/claim.py open ladder-law --blueprint-file /tmp/bp.md [--claimant box]
  python3 tools/claim.py list
  python3 tools/claim.py close ladder-law "merged as L-LAD1-3"
Ledger: data/rung-claims.jsonl (append-only; status flips by rewriting the row).
"""
import argparse
import datetime
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
LEDGER = HERE / "data" / "rung-claims.jsonl"


def read():
    rows = []
    if LEDGER.is_file():
        for line in LEDGER.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write(rows):
    LEDGER.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    o = sub.add_parser("open")
    o.add_argument("slug")
    o.add_argument("--blueprint-file", required=True, type=Path)
    o.add_argument("--claimant", default="box")
    c = sub.add_parser("close")
    c.add_argument("slug")
    c.add_argument("note", default="")
    sub.add_parser("list")
    a = ap.parse_args()
    rows = read()
    if a.cmd == "list":
        for r in rows:
            print(f"{r['slug']} [{r['status']}] {r['claimant']} {r.get('closed_note','')}")
        return 0
    if a.cmd == "open":
        if any(r["slug"] == a.slug and r["status"] in ("open", "approved") for r in rows):
            print(f"ERROR: claim {a.slug} already live (no collisions)")
            return 1
        bp = a.blueprint_file.read_text(encoding="utf-8")
        rows.append({"slug": a.slug, "claimant": a.claimant, "status": "open",
                     "blueprint_sha256": hashlib.sha256(bp.encode()).hexdigest(),
                     "blueprint": bp[:2000],
                     "date": datetime.date.today().isoformat(), "closed_note": ""})
        write(rows)
        print(f"claimed {a.slug} (open — needs lead approval)")
        return 0
    for r in rows:
        if r["slug"] == a.slug and r["status"] in ("open", "approved"):
            r["status"] = "done"
            r["closed_note"] = a.note
            write(rows)
            print(f"closed {a.slug}")
            return 0
    print(f"ERROR: no live claim {a.slug}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
