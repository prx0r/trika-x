#!/usr/bin/env python3
"""source_audit.py — B1: uniform source-record audit across translation-work.

Read-only. For every work dir carrying passages.jsonl, reports which
uniform-source-record variant exists (SOURCE.sha/txt, source/record.json,
source/edition*.json, data manifests) or explicit unknown. No work may be
silent about its origin (ENDGAME-BUILD-PLAN Phase 0.1).
Usage: python3 formal-trika/tools/source_audit.py [--tw PATH]
Exit 0 with a coverage line; lists the gap (works without any record).
"""
import argparse
import json
from pathlib import Path

VARIANTS = ["SOURCE.sha", "SOURCE.txt", "source/record.json",
            "source/edition.json", "source/manifest.json",
            "source/segments.json", "data/manifest.json"]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tw", type=Path,
                    default=Path("/root/translation-work"))
    a = ap.parse_args()
    total, ok, gaps = 0, 0, []
    kinds = {}
    for ledger in sorted(a.tw.glob("*/passages.jsonl")):
        wd = ledger.parent
        total += 1
        found = [v for v in VARIANTS if (wd / v).is_file()]
        # also accept any source/*.json record-ish file
        if not found:
            extra = sorted(p.name for p in (wd / "source").glob("*.json")
                           if p.is_file()) if (wd / "source").is_dir() else []
            if extra:
                found = [f"source/{extra[0]} (+{len(extra)-1})"]
        if found:
            ok += 1
            kinds[found[0].split("/")[0]] = kinds.get(found[0].split("/")[0], 0) + 1
        else:
            gaps.append(wd.name)
    print(f"works with passages: {total}; with source record: {ok}; gaps: {len(gaps)}")
    print("record-kind histogram:", dict(sorted(kinds.items())))
    if gaps:
        print("GAP (no source record):")
        for g in gaps:
            print(f"  {g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
