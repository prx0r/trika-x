#!/usr/bin/env python3
"""unit_to_score.py — practice-unit/1 → syllabus steps (deitybody JSON contract).

Plug pattern per deitybody AGENTS.md rule 8 (JSON contracts, never merge).
Maps a rendered unit's R-gloss technique into syllabus step kinds
(breathe-in/out, hold, visualize, focus, repeat, unclassified) WITHOUT
timings/cues/loci (reviewer fills those in compile_syllabus.py — the
model never writes numbers). Source refs + eligibility ride through.
Fail-closed: requires-diksha units emit NO steps (STUDY block with
conditions) so no compiler can turn them into practicable events.
Usage: python3 formal-trika/tools/unit_to_score.py --unit U.json --out S.json
"""
import argparse
import json
import re
from pathlib import Path

KIND_RULES = [
    ("hold", r"hold|stop|retention|kumbhaka| arrest"),
    ("breathe-in", r"inhal|pUraka|breathe in"),
    ("breathe-out", r"exhal|recaka|breathe out"),
    ("repeat", r"chant|mantra|japa|recit|repeat|dedicat"),
    ("visualize", r"visualiz|imagin|pictur|behold|glyph"),
    ("focus", r"watch|observ|feel|sense|gaze|listen|attention|dissolv|void|spacious"),
]


def kind_of(text):
    for kind, pat in KIND_RULES:
        if re.search(pat, text, re.IGNORECASE):
            return kind
    return "unclassified"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--unit", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    u = json.loads(a.unit.read_text(encoding="utf-8"))
    elig = (u.get("eligibility") or {}).get("eligibility", "study")
    tech = " ".join(s.get("text", "") for s in u.get("steps", []))
    # Study-only until a real review boundary exists (merged PR #4 law):
    # no rendered mode authorizes practice; eligibility stays a provisional
    # keyword label carried alongside, never an authorization.
    if elig == "requires-diksha":
        steps = []
        gate = {"mode": "STUDY", "practice_authorized": False,
                "note": "Traditionally conferred; no practicable steps emitted.",
                "conditions": u.get("safety", [])}
    else:
        steps = [{"id": f"{u.get('unit_id')}-s1", "kind": kind_of(tech),
                  "title": (u.get("technique_R") or "")[:80],
                  "cue": "TODO-cue (reviewer)", "dur": None,
                  "region": "TODO-region (reviewer)"}]
        gate = {"mode": "STUDY", "practice_authorized": False,
                "note": "Draft for source study; practice has not been authorized.",
                "provisional_eligibility": elig}
    doc = {"id": f"{u.get('unit_id')}-syllabus", "kind": "syllabus/1",
           "from_unit": u.get("unit_id"), "from_sha": u.get("unit_sha256"),
           "source_refs": u.get("source_refs", []),
           "eligibility": elig, "gate": gate, "steps": steps,
           "provenance": "assembled from practice-unit (R-gloss); timings/cues/loci REVIEWER-filled downstream"}
    a.out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"syllabus {doc['id']}: {len(steps)} steps, gate {gate['mode']} -> {a.out}")


if __name__ == "__main__":
    raise SystemExit(main())
