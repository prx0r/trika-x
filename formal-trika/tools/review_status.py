#!/usr/bin/env python3
"""review_status.py — Core/Frontier tier metadata for every theorem.

Stolen fair from AxiomMath/Stacks (StacksCore human-reviewed vs
StacksFrontier AI-written-compiles-unreviewed). Every non-mutant theorem
gets exactly one row: Frontier by default; Core only via --promote with
--reviewer + --reason (scholar/human review — never self-promotion, never
batch-promotion). --check fails if any theorem lacks a row (CI).

  python3 tools/review_status.py                       # regenerate (keeps promotions)
  python3 tools/review_status.py --check                # CI gate
  python3 tools/review_status.py --promote "File :: thm" --reviewer NAME --reason "..."
"""
import argparse
import datetime
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
    thms = theorems()
    if a.promote:
        if not a.reviewer.strip() or not a.reason.strip():
            print("ERROR: promotion needs --reviewer + --reason (never self-promote)")
            return 1
        if a.promote not in thms:
            print(f"ERROR: unknown theorem {a.promote}")
            return 1
        doc["rows"][a.promote] = {"tier": "Core", "reviewer": a.reviewer.strip(),
                                  "reason": a.reason.strip(),
                                  "date": datetime.date.today().isoformat()}
        OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n")
        print(f"promoted {a.promote} -> Core")
        return 0
    changed = False
    for t in thms:
        if t not in doc["rows"]:
            doc["rows"][t] = {"tier": "Frontier", "reviewer": None,
                              "reason": "machine-proposed, unreviewed", "date": None}
            changed = True
    stale = [k for k in doc["rows"] if k not in thms]
    for k in stale:
        del doc["rows"][k]
        changed = True
    if a.check:
        missing = [t for t in thms if t not in doc["rows"]]
        if missing or stale:
            print(f"REVIEW-STATUS STALE: missing={len(missing)} stale={len(stale)}")
            return 1
        core = sum(1 for r in doc["rows"].values() if r["tier"] == "Core")
        print(f"review-status: {len(thms)} theorems, {core} Core / {len(thms)-core} Frontier")
        return 0
    if changed or not OUT.is_file():
        OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n")
    core = sum(1 for r in doc["rows"].values() if r["tier"] == "Core")
    print(f"review-status: {len(thms)} theorems, {core} Core / {len(thms)-core} Frontier -> {OUT.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
