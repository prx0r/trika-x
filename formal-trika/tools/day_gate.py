#!/usr/bin/env python3
"""day_gate.py — E5: day-gated journey truth (one truth, append-only).

Day N = count of DISTINCT posting dates (never calendar days, never wall
clock). Same-day re-posts keep N. Empty days never advance N. The log is
append-only JSONL: {day, date, unit_id, kind}. Query: current N + history.
Usage:
  python3 formal-trika/tools/day_gate.py --log J.jsonl post --date 2026-11-06 --unit vbt-d001 --kind practice
  python3 formal-trika/tools/day_gate.py --log J.jsonl status
"""
import argparse
import json
from pathlib import Path


def read_log(p):
    rows = []
    if p.is_file():
        for l in p.read_text(encoding="utf-8").splitlines():
            if l.strip():
                rows.append(json.loads(l))
    return rows


def current_n(rows):
    return len({r["date"] for r in rows})


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--log", type=Path, required=True)
    sub = ap.add_subparsers(dest="cmd", required=True)
    pp = sub.add_parser("post")
    pp.add_argument("--date", required=True)
    pp.add_argument("--unit", required=True)
    pp.add_argument("--kind", default="practice")
    sub.add_parser("status")
    a = ap.parse_args()
    rows = read_log(a.log)
    if a.cmd == "post":
        import re
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", a.date):
            raise SystemExit("date must be YYYY-MM-DD")
        n = current_n(rows) + (0 if any(r["date"] == a.date for r in rows) else 1)
        rows.append({"day": n, "date": a.date, "unit_id": a.unit, "kind": a.kind})
        a.log.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
        print(f"posted day {n} ({a.date}, {a.unit})")
    else:
        print(json.dumps({"day_N": current_n(rows), "posts": len(rows),
                          "dates": sorted({r["date"] for r in rows})},
                         ensure_ascii=False))


if __name__ == "__main__":
    raise SystemExit(main())
