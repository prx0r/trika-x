#!/usr/bin/env python3
"""eligibility.py — E3: practice-unit eligibility gate (rules, tested).

Three outcomes, fail-closed:
  study            — textual/contemplative; nothing to enact (or unknown).
  doable           — provisional keyword match, NOT authorization to practise.
  requires-diksha  — mantra-dīkṣā, kuṇḍalinī awakening, nyāsa with bīja,
                     deity installation, antinomian/transgressive rite markers.
Unknown and caution-bearing inputs fall to study. Keyword matches cannot
establish a practice's safety, source accuracy, or a person's readiness.
Application.lean checks a stipulated model; it does not validate this gate.
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
CAUTION = [(r"retention|kumbhaka|breath.{0,12}(stop|hold)|stop.{0,12}breath", "breath retention: source and individual safety review required"),
           (r"kuṇḍalinī|intense visual|energy ris", "intense practice: source and individual safety review required"),
           (r"eyes closed.*long|darkness.*hour", "extended sensory withdrawal: source and individual safety review required")]


def classify(technique="", upaya="", trains=""):
    blob = f"{technique}\n{upaya}\n{trains}"
    for pat in DIKSHA:
        if re.search(pat, blob, re.IGNORECASE):
            return {"eligibility": "requires-diksha", "rule": f"disha-marker:{pat[:28]}",
                    "cautions": [c for _, c in CAUTION if re.search(_, blob, re.IGNORECASE)] or
                    ["traditionally conferred; steps withheld pending teacher"]}
    cautions = [c for pat, c in CAUTION if re.search(pat, blob, re.IGNORECASE)]
    if cautions:
        return {"eligibility": "study", "rule": "caution-marker:review-required",
                "cautions": cautions}
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
