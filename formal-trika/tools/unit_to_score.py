#!/usr/bin/env python3
"""unit_to_score.py — practice-unit/1 → syllabus steps (deitybody JSON contract).

Plug pattern per deitybody AGENTS.md rule 8 (JSON contracts, never merge).
Produces a study-only syllabus record with no executable steps. This prototype
cannot verify source interpretation, review or practice authorization; input
eligibility and status strings do not establish any of those decisions.
Usage: python3 formal-trika/tools/unit_to_score.py --unit U.json --out S.json
"""
import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--unit", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    u = json.loads(a.unit.read_text(encoding="utf-8"))
    elig = (u.get("eligibility") or {}).get("eligibility", "study")
    steps = []
    gate = {"mode": "STUDY", "practice_authorized": False,
            "note": "Source study only; no executable practice steps are emitted.",
            "conditions": u.get("safety", [])}
    doc = {"id": f"{u.get('unit_id')}-syllabus", "kind": "syllabus/1",
           "from_unit": u.get("unit_id"), "from_sha": u.get("unit_sha256"),
           "source_refs": u.get("source_refs", []),
           "eligibility": elig, "gate": gate, "steps": steps,
           "provenance": "study-only record from practice-unit; source and practice review remain open"}
    a.out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"syllabus {doc['id']}: {len(steps)} steps, gate {gate['mode']} -> {a.out}")


if __name__ == "__main__":
    raise SystemExit(main())
