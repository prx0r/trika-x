#!/usr/bin/env python3
"""eligibility.py — E3: practice-unit eligibility gate (rules, tested).

Three outcomes, fail-closed:
  study            — textual/contemplative; nothing to enact (or unknown).
  doable           — plain breath/attention/posture; caution attached as needed.
  requires-diksha  — mantra-dīkṣā, kuṇḍalinī awakening, nyāsa with bīja,
                     deity installation, antinomian/transgressive rite markers.
Unknown ALWAYS falls to study, never doable (fail-closed). Formal backing:
Application.lean :: unready_unreachable (¬ready ⟹ no flip under any means)
— the compiler's study-fallback is the applied face of that theorem.
Keyword rules are R-tier heuristics over entry text; the gate is a
compiler aid, not a guru. A `requires-diksha` unit hides steps behind
the teacher notice.
Usage: python3 formal-trika/tools/eligibility.py --technique "..." --upaya "..."
"""
import argparse
import re

DIKSHA = [r"dīkṣā|diksha|initiation", r"bīja|bija|seed[-\s]?mantra",
          r"kuṇḍalinī|kundalini.*awaken", r"nyāsa|nyasa",
          r"deity installation|murti.*install|prāṇa pratiṣṭhā",
          r"transgressive|antinomian|pañcamakāra|forbidden substances",
          r"guru.*confer|conferred by (a|the) guru|secret mantra"]
DOABLE = [r"breath|prāṇāyāma|inhal|exhal|retention|kumbhaka",
          r"attention|watch|observe|gaze|listen|feel|sense",
          r"posture|sit|stand|walk|eyes (open|closed|half)",
          r"recit|chant|mantra (repetition|japa)\b", r"visualiz|imagin|pictur"]
CAUTION = [(r"retention|kumbhaka|breath.{0,12}(stop|hold)|stop.{0,12}breath", "breath retention: not in pregnancy or with high blood pressure; keep short, stop on dizziness"),
           (r"kuṇḍalinī|intense visual|energy ris", "intense practice: not during acute mental-health crisis; keep sits short; stop if distressed"),
           (r"eyes closed.*long|darkness.*hour", "sensory withdrawal: sit supported; not while driving-equivalent tasks follow")]


def classify(technique="", upaya="", trains=""):
    blob = f"{technique}\n{upaya}\n{trains}"
    for pat in DIKSHA:
        if re.search(pat, blob, re.IGNORECASE):
            return {"eligibility": "requires-diksha", "rule": f"disha-marker:{pat[:28]}",
                    "cautions": [c for _, c in CAUTION if re.search(_, blob, re.IGNORECASE)] or
                    ["traditionally conferred; steps withheld pending teacher"]}
    for pat in DOABLE:
        if re.search(pat, blob, re.IGNORECASE):
            return {"eligibility": "doable", "rule": f"doable-marker:{pat[:28]}",
                    "cautions": [c for p, c in CAUTION if re.search(p, blob, re.IGNORECASE)]}
    return {"eligibility": "study", "rule": "no-enactment-markers (fail-closed)",
            "cautions": []}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--technique", default="")
    ap.add_argument("--upaya", default="")
    ap.add_argument("--trains", default="")
    a = ap.parse_args()
    import json
    print(json.dumps(classify(a.technique, a.upaya, a.trains), ensure_ascii=False))


if __name__ == "__main__":
    raise SystemExit(main())
