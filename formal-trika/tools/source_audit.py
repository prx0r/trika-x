#!/usr/bin/env python3
"""source_audit.py — B1: uniform source-record audit across translation-work.

Read-only. Phase 1 (original contract): for every work dir carrying
passages.jsonl, reports which uniform-source-record variant exists or
explicit unknown. Phase 2 (step-1 reconciliation): validates every
<work>/source/record.json against the svatantrya-source-record/1 schema
(status RECORDED/NO-SOURCE-RECORD, required keys) across the whole
102-work universe, not just passage works. Phase 3: map<->record
consistency vs source-maps/openpatala.json (reported, never failed —
their builder owns timing). No work may be silent about its origin.
Usage: python3 formal-trika/tools/source_audit.py [--tw PATH]
Exit 0 with coverage lines (1 when no ledgers at all, as before).
"""
import argparse
import json
import sys
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
    ledgers = sorted(a.tw.glob("*/passages.jsonl"))
    if not ledgers:
        print(f"ERROR: no passage ledgers found under {a.tw}", file=sys.stderr)
        return 1
    for ledger in ledgers:
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
    print("Record presence is not edition, witness, rights or content verification.")
    if gaps:
        print("GAP (no source record):")
        for g in gaps:
            print(f"  {g}")
    phase2(a.tw)
    return 0


RECORD_STATUSES = {"RECORDED", "NO-SOURCE-RECORD"}
RECORD_KEYS = {"format", "work", "status", "openpatala", "witness"}


def phase2(tw: Path) -> None:
    """Validate uniform records universe-wide + map<->record consistency."""
    recs = sorted(tw.glob("*/source/record.json"))
    recorded, nosource, invalid = [], [], []
    mismatches = []
    tmap = {}
    try:
        tmap = json.loads((tw / "source-maps" / "openpatala.json").read_text(encoding="utf-8")).get("works", {})
    except (OSError, ValueError, AttributeError):
        tmap = {}
    for rp in recs:
        work = rp.parts[-3]
        try:
            d = json.loads(rp.read_text(encoding="utf-8"))
        except ValueError:
            invalid.append(work)
            continue
        if d.get("format") != "svatantrya-source-record/1" or not RECORD_KEYS <= set(d):
            invalid.append(work)
            continue
        if d.get("status") == "RECORDED":
            recorded.append(work)
        elif d.get("status") == "NO-SOURCE-RECORD":
            nosource.append(work)
        else:
            invalid.append(f"{work}(status={d.get('status')})")
            continue
        if isinstance(tmap, dict) and work in tmap:
            mstatus = tmap[work].get("mapping_status")
            rstatus = (d.get("openpatala") or {}).get("mapping_status")
            wid_map, wid_rec = tmap[work].get("openpatala_work_id"), (d.get("openpatala") or {}).get("work_id")
            if mstatus != rstatus or (wid_map or wid_rec) and wid_map != wid_rec:
                mismatches.append(f"{work}: map={mstatus}/{wid_map} vs record={rstatus}/{wid_rec}")
    print(f"uniform records: {len(recs)}; RECORDED: {len(recorded)}; "
          f"NO-SOURCE-RECORD: {len(nosource)}; invalid: {len(invalid)}")
    if invalid:
        print("INVALID record.json:")
        for w in invalid:
            print(f"  {w}")
    if tmap:
        print(f"map<->record mismatches: {len(mismatches)} (reported only; their builder owns timing)")
        for m in mismatches:
            print(f"  {m}")
    else:
        print("canonical map absent; consistency check skipped")
    return None


if __name__ == "__main__":
    raise SystemExit(main())
