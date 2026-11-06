#!/usr/bin/env python3
"""crux_queue.py — B4: crux-candidate queue (argmap uncertainties + pushing probes).

Merges two evidence-only sources (never invents questions):
  1. formal-trika/data/argmap-nodes.jsonl units with non-empty uncertainties
     (701) — each becomes a candidate with work/locator/verse/question/text.
  2. ipvv pushing corpus (*.md probes/sessions, indexed by path) — pointers
     for human/agent triage, not parsed claims.
Priority: uncertainties on works with registry references first; a reference
is not source entailment or verified formal coverage. Pushing pointers are
optional and untriaged. Paths are relative to the supplied pushing directory.
Output: formal-trika/data/crux-queue.jsonl (ranked) + summary line.
Usage: python3 formal-trika/tools/crux_queue.py [--pushing PATH]
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from treeka import formal_references

HERE = Path(__file__).resolve().parent.parent
def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--nodes", type=Path, default=HERE / "data" / "argmap-nodes.jsonl")
    ap.add_argument("--pushing", type=Path, help="optional ipvv pushing directory")
    ap.add_argument("--out", type=Path, default=HERE / "data" / "crux-queue.jsonl")
    a = ap.parse_args()
    cands = []
    if a.pushing is not None and not a.pushing.is_dir():
        raise ValueError(f'pushing directory not found: {a.pushing}')
    nodes = [json.loads(l) for l in a.nodes.read_text(encoding='utf-8').splitlines() if l.strip()]
    evidence = json.loads((HERE / 'EVIDENCE.json').read_text(encoding='utf-8'))
    referenced_works = {work for work, _ in formal_references(evidence)}
    if any(c.get('locator') == 'vbt' for e in evidence.get('entries', {}).values()
           for c in e.get('chunks', [])):
        referenced_works.add('vbt')  # work-level only
    for n in nodes:
        for u in n.get("uncertainties", []) or []:
            if not isinstance(u, str) or not u.strip():
                continue
            pri = (2 if n.get('locator') == 'UNKNOWN' else
                   0 if n.get('work') in referenced_works else 1)
            cands.append({"kind": "argmap-uncertainty", "priority": pri,
                          "work": n.get("work"), "locator": n.get("locator"),
                          "cross_work": n.get("cross_work"), "verse_id": n.get("verse_id"),
                          "locator_status": n.get("locator_status"),
                          "source_file": n.get("source_file"),
                          "source_file_sha256": n.get("source_file_sha256"),
                          "ledger_sha256": n.get("ledger_sha256"),
                          "translation_work_revision": n.get("translation_work_revision"),
                          "source_checkout_state": n.get("source_checkout_state"),
                          "question": n.get("question"), "text": u.strip()})
    if a.pushing is not None:
        git = subprocess.run(['git', '-C', str(a.pushing), 'rev-parse', 'HEAD'],
                             text=True, capture_output=True)
        revision = git.stdout.strip() if git.returncode == 0 else None
        status = subprocess.run(['git', '-C', str(a.pushing), 'status', '--porcelain', '--untracked-files=all'],
                                text=True, capture_output=True) if revision else None
        checkout = ('CLEAN' if status and status.returncode == 0 and not status.stdout else
                    'DIRTY' if status and status.returncode == 0 else 'UNVERIFIED')
        for fp in sorted(a.pushing.rglob("*.md")):
            if fp.name == "INDEX.json":
                continue
            area = fp.parent.name
            cands.append({"kind": "pushing-probe", "priority": 3,
                          "work": None, "locator": None, "cross_work": None,
                          "verse_id": None, "area": area,
                          "question": None, "text": None,
                          "path": fp.relative_to(a.pushing).as_posix(),
                          "sha256": hashlib.sha256(fp.read_bytes()).hexdigest(),
                          "ipvv_revision": revision, "source_checkout_state": checkout})
    cands.sort(key=lambda c: (c["priority"], str(c.get("work")), str(c.get("verse_id"))))
    with open(a.out, "w", encoding="utf-8") as fh:
        for i, c in enumerate(cands):
            c["rank"] = i + 1
            fh.write(json.dumps(c, ensure_ascii=False) + "\n")
    by_kind = {}
    for c in cands:
        by_kind[c["kind"]] = by_kind.get(c["kind"], 0) + 1
    print(f"candidates: {len(cands)} {by_kind}; pushing included: {a.pushing is not None} -> {a.out}")


if __name__ == "__main__":
    raise SystemExit(main())
