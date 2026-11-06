#!/usr/bin/env python3
"""review_status.py — Core/Frontier tier metadata for every theorem.

Stolen fair from AxiomMath/Stacks (StacksCore human-reviewed vs
StacksFrontier AI-written-compiles-unreviewed). Every non-mutant theorem
gets exactly one row: Frontier by default. Core promotion is disabled until
an authenticated, revision-bound scholar decision can be verified. A name
and reason supplied on the command line do not establish that decision.
--check fails on missing, stale, malformed or unsupported Core rows (CI).

  python3 tools/review_status.py                       # regenerate (keeps promotions)
  python3 tools/review_status.py --check                # CI gate
  python3 tools/review_status.py --promote "File :: thm"  # currently refuses
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "data" / "review-status.json"


def theorems():
    out = set()
    for d in ("control", "recognition"):
        for f in sorted((HERE / d).glob("*.lean")):
            if f.name.startswith("Broken"):
                continue
            text = f.read_text(encoding="utf-8")
            for m in re.finditer(r"(?m)^theorem\s+([A-Za-z0-9_]+)", text):
                out.add(f"{f.name} :: {m.group(1)}")
    return sorted(out)


def load():
    if OUT.is_file():
        return json.loads(OUT.read_text(encoding="utf-8"))
    return {"format": "trika-review-status/1", "rows": {}}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--promote", default="")
    ap.add_argument("--reviewer", default="")
    ap.add_argument("--reason", default="")
    a = ap.parse_args()
    doc = load()
    if not isinstance(doc, dict) or doc.get('format') != 'trika-review-status/1' or not isinstance(doc.get('rows'), dict):
        print('ERROR: invalid review-status document')
        return 1
    thms = theorems()
    if not thms:
        print('ERROR: no positive theorems found')
        return 1
    if a.promote:
        print('ERROR: Core promotion is disabled until authenticated, revision-bound review is implemented')
        return 1
    missing = [t for t in thms if t not in doc['rows']]
    stale = [k for k in doc['rows'] if k not in thms]
    invalid = [k for k, row in doc['rows'].items()
               if not isinstance(row, dict) or row.get('tier') != 'Frontier']
    if a.check:
        if missing or stale or invalid:
            print(f'REVIEW-STATUS INVALID: missing={len(missing)} stale={len(stale)} invalid_or_unverified_core={len(invalid)}')
            return 1
        print(f'review-status: {len(thms)} theorems, 0 Core / {len(thms)} Frontier')
        return 0
    if invalid:
        print(f'ERROR: {len(invalid)} malformed or unverified Core rows require review')
        return 1
    changed = False
    for t in missing:
        doc["rows"][t] = {"tier": "Frontier", "reviewer": None,
                          "reason": "machine-proposed, unreviewed", "date": None}
        changed = True
    for k in stale:
        del doc["rows"][k]
        changed = True
    if changed or not OUT.is_file():
        OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n")
    core = sum(1 for r in doc["rows"].values() if r["tier"] == "Core")
    print(f"review-status: {len(thms)} theorems, {core} Core / {len(thms)-core} Frontier -> {OUT.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
