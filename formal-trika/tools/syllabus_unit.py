#!/usr/bin/env python3
"""syllabus_unit.py — E2: render ONE practice unit (syllabus compiler C1).

Input: a vbt-daily entry (R-tier gloss) + its source locator (T-tier span).
Output: a practice-unit JSON where EVERY field traces to a span or is
marked R/human-review. Rules (kept verbatim from the engine spec):
model never writes offsets/timings/numbers (steps carry NO seconds unless
sourced); never narrate the conditional or promised (signs/powers become
Ask pointers, not scripted promises); safety caps are compiler-side;
status stays `review` until a human signs off.
Usage: python3 formal-trika/tools/syllabus_unit.py --dharana 1 --out unit.json
"""
import argparse
import hashlib
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import eligibility as elig

HERE = Path(__file__).resolve().parent.parent
VBT = Path("/root/satsang-practice/pilot-inputs/vbt-daily.json")


def vbt_range(work="vbt"):
    out = []
    for line in Path(f"/root/translation-work/{work}/passages.jsonl").read_text().splitlines():
        if line.strip():
            r = json.loads(line)
            out.append((r.get("locator"), r.get("verses")))
    return out


def locate_verse(v, ranges):
    import re
    for loc, rng in ranges:
        m = re.fullmatch(r"\s*(\d+)\s*-\s*(\d+)\s*", rng or "")
        if m and int(m.group(1)) <= v <= int(m.group(2)):
            return loc
    return "UNKNOWN"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dharana", type=int, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    d = json.loads(VBT.read_text(encoding="utf-8"))
    entries = [e for e in d["entries"] if e.get("dharana") == a.dharana]
    if not entries:
        raise SystemExit(f"dhāraṇā {a.dharana} not in mapped set ({d['count_mapped']}/{d['count_total']})")
    e = entries[0]
    loc = locate_verse(int(e["verse"]), vbt_range())
    gate = elig.classify(e.get("technique", ""), e.get("upaya", ""), e.get("trains", ""))
    unit = {
        "unit_id": f"vbt-d{a.dharana:03d}",
        "kind": "practice-unit/1",
        "dharana": e["dharana"],
        "verse": e["verse"],
        "source_refs": [{"work": "vbt", "locator": loc, "verse": e["verse"],
                         "tier": "T-span (passage locator; verse text in T1, not quoted here)"}],
        "technique_R": e.get("technique"),
        "technique_provenance": "R-gloss (vbt-daily entry); NOT root text — verify against T1 span before teaching",
        "trains": e.get("trains"),
        "coord": e.get("coord"),
        "upaya": e.get("upaya"),
        "eligibility": gate,
        "steps": [{"n": 1, "text": e.get("technique", ""),
                   "from": "R-gloss (unscheduled: no seconds — model never writes timings)",
                   "seconds": None}],
        "safety": gate["cautions"] or ["no specific cautions triggered; generic sit guidance applies"],
        "ask_pointers": ["effects/signs/powers, if any arise, are Ask material — never scripted promises"],
        "status": "review",
    }
    unit["unit_sha256"] = hashlib.sha256(
        json.dumps(unit, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    a.out.write_text(json.dumps(unit, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"C1 unit {unit['unit_id']}: locator {loc}, eligibility {gate['eligibility']}, "
          f"status review -> {a.out}")


if __name__ == "__main__":
    raise SystemExit(main())
