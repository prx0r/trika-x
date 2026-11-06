#!/usr/bin/env python3
"""station_pass.py — C7: rule-proposed station tags over 144 moments (thin).

STATION-TABLE criteria need conjunctions (pull+fog+positioning; clarity
WITHOUT content; teaching-voice) that the decode schema mostly lacks
(felt: pull/doubt/churn/stall/push only; means on 7/144; no fog,
planning, clarity, content, or voice fields). So this harness:
  - proposes tags ONLY where a stated rule fires, with rule + low/med conf,
  - leaves everything else UNTAGGED (record-don't-force, per sheet),
  - never overwrites existing tags, never writes decodes (proposals file),
  - reports the schema gap as the finding (station pass needs richer
    decodes or owner tagging; machine-proposed, owner-unreviewed).
Usage: python3 formal-trika/tools/station_pass.py [--out proposals.json]
"""
import argparse
import glob
import json
from pathlib import Path

DATA = Path("/root/trika-x/formal-trika/data")

RULES = [
    ("sakala?", lambda d: "pull" in (d.get("felt") or []) and (d.get("riders") or False),
     "pull+riders (fog/positioning fields absent — thin)", "low"),
    ("vijñānākala?", lambda d: "stall" in (d.get("felt") or []) and not (d.get("heads") or []),
     "stall-without-heads (clarity field absent — thinnest)", "low"),
    ("mantra-position?", lambda d: d.get("means") == "anava",
     "anava means tagged (recognition-riding-repetition inferred — thin)", "low"),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=Path("/tmp/station-proposals.json"))
    a = ap.parse_args()
    props, untagged, kept = [], 0, 0
    for fp in sorted(DATA.glob("day-*.jsonl")):
        for line in fp.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            d = json.loads(line)
            if d.get("station"):
                kept += 1
                continue
            hit = None
            for station, rule, why, conf in RULES:
                try:
                    if rule(d):
                        hit = {"day": d.get("day"), "n": d.get("n"),
                               "proposed": station, "rule": why, "conf": conf,
                               "proposed_by": "station_pass.py (machine, unreviewed)"}
                        break
                except (TypeError, AttributeError):
                    continue
            if hit:
                props.append(hit)
            else:
                untagged += 1
    a.out.write_text("\n".join(json.dumps(p, ensure_ascii=False) for p in props) + "\n",
                     encoding="utf-8")
    print(f"moments: 144; kept-existing: {kept}; proposed: {len(props)}; untagged: {untagged}")
    print("finding: decode schema lacks fog/planning/clarity/content/voice fields — "
          "station criteria mostly unmatchable; proposals are thin single-marker rules. "
          "Full pass needs richer decodes or owner tagging.")
    print(f"proposals -> {a.out} (separate file; decodes untouched)")


if __name__ == "__main__":
    raise SystemExit(main())
