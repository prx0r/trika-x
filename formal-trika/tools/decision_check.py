#!/usr/bin/env python3
"""decision_check.py — B2: decision-trail read-only checker.

Reports per work: scholar ledger presence (versions/reviews/decisions/
promotions) and layer-accept decision coverage. Writing layer-accept
decisions at ingest is the owning lane's job (translation-work); this
tool only measures file and marker presence. It does not verify signatures,
authorization or any submission gate.
Usage: python3 formal-trika/tools/decision_check.py [--tw PATH]
"""
import argparse
import json
import sys
from pathlib import Path

FILES = ["versions.jsonl", "reviews.jsonl", "decisions.jsonl",
         "promotions.jsonl", "essays"]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tw", type=Path, default=Path("/root/translation-work"))
    a = ap.parse_args()
    works = sorted(p.parent.name for p in a.tw.glob("*/passages.jsonl"))
    if not works:
        print(f"ERROR: no passage ledgers found under {a.tw}", file=sys.stderr)
        return 1
    with_ledger, layer_accept = [], []
    for w in works:
        s = a.tw / w / "scholar"
        if not s.is_dir():
            continue
        have = [f for f in FILES if (s / f).exists()]
        with_ledger.append((w, have))
        dec = s / "decisions.jsonl"
        if dec.is_file():
            try:
                rows = [json.loads(l) for l in dec.read_text().splitlines() if l.strip()]
            except (OSError, json.JSONDecodeError) as exc:
                print(f"ERROR: cannot read decisions from {dec}: {exc}", file=sys.stderr)
                return 1
            if any(str(r.get("subject", "")).startswith("layer-accept:") for r in rows
                   if isinstance(r, dict)):
                layer_accept.append(w)
    print(f"works: {len(works)}; with scholar ledger: {len(with_ledger)}; "
          f"with layer-accept decisions: {len(layer_accept)}")
    print("Marker presence is not a verified signature or authorization.")
    for w, have in with_ledger:
        print(f"  ledger: {w} [{', '.join(have)}]")
    if len(with_ledger) < len(works):
        missing = [w for w in works
                   if w not in {x[0] for x in with_ledger}]
        print(f"GAP: {len(missing)} works without scholar ledger "
              f"(paramarthasara pattern not rolled out):")
        print("  " + ", ".join(missing[:20]) +
              (f" (+{len(missing)-20} more)" if len(missing) > 20 else ""))
    missing_decisions = sorted(set(works) - set(layer_accept))
    print(f"GAP: {len(missing_decisions)} works have no layer-accept marker "
          "(presence does not establish signoff).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
