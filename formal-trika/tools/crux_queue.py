#!/usr/bin/env python3
"""crux_queue.py — B4: crux-candidate queue (argmap uncertainties + pushing probes).

Merges two evidence-only sources (never invents questions):
  1. formal-trika/data/argmap-nodes.jsonl units with non-empty uncertainties
     (701) — each becomes a candidate with work/locator/verse/question/text.
  2. ipvv pushing corpus (*.md probes/sessions, indexed by path) — pointers
     for human/agent triage, not parsed claims.
Priority: uncertainties on formally-covered works first (adjacent to Lean),
then formal-armed works, then the rest; pushing pointers last (untriaged).
Output: formal-trika/data/crux-queue.jsonl (ranked) + summary line.
Usage: python3 formal-trika/tools/crux_queue.py [--pushing PATH]
"""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
FORMAL_WORKS = {"tsa08", "tsa07", "param", "phr", "vbt", "spanda"}


def work_key(loc):
    return (loc or "UNKNOWN").split("-")[0].lower() if loc != "UNKNOWN" else "unknown"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pushing", type=Path, default=Path("/root/ipvv/site/data/pushing"))
    ap.add_argument("--out", type=Path, default=HERE / "data" / "crux-queue.jsonl")
    a = ap.parse_args()
    cands = []
    nodes = [json.loads(l) for l in (HERE / "data" / "argmap-nodes.jsonl").read_text().splitlines() if l.strip()]
    for n in nodes:
        for u in n.get("uncertainties", []) or []:
            if not isinstance(u, str) or not u.strip():
                continue
            wk = work_key(n.get("locator"))
            pri = 0 if wk in FORMAL_WORKS else (1 if n.get("locator") != "UNKNOWN" else 2)
            cands.append({"kind": "argmap-uncertainty", "priority": pri,
                          "work": n.get("work"), "locator": n.get("locator"),
                          "cross_work": n.get("cross_work"), "verse_id": n.get("verse_id"),
                          "question": n.get("question"), "text": u.strip()})
    if a.pushing.is_dir():
        for fp in sorted(a.pushing.rglob("*.md")):
            if fp.name == "INDEX.json":
                continue
            area = fp.parent.name
            cands.append({"kind": "pushing-probe", "priority": 3,
                          "work": None, "locator": None, "cross_work": None,
                          "verse_id": None, "area": area,
                          "question": None, "text": None,
                          "path": str(fp)})
    cands.sort(key=lambda c: (c["priority"], str(c.get("work")), str(c.get("verse_id"))))
    with open(a.out, "w", encoding="utf-8") as fh:
        for i, c in enumerate(cands):
            c["rank"] = i + 1
            fh.write(json.dumps(c, ensure_ascii=False) + "\n")
    by_kind = {}
    for c in cands:
        by_kind[c["kind"]] = by_kind.get(c["kind"], 0) + 1
    print(f"candidates: {len(cands)} {by_kind} -> {a.out}")


if __name__ == "__main__":
    raise SystemExit(main())
