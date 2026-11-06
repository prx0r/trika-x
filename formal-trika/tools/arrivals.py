#!/usr/bin/env python3
"""arrivals.py — session-start rhythm against a faster upstream lane.

Read-only (unless --rebuild). Compares translation-work HEAD against our
pins: bridge/passages.snapshot.json revision + argmap-nodes translation_work
revisions. Prints DRIFT lines when upstream moved past a pin. --rebuild
re-runs nodes/queue/treeka (derived data only; snapshot re-pin stays a
deliberate manual step via build_passage_snapshot.py after EVIDENCE edits).

Exit 0 with verdict lines; exit 1 only when --tw is not a git checkout.
Their swarm lands mid-session — run this first, every session.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRIDGE = HERE.parent / "bridge"
DATA = HERE.parent / "data"


def head(tw: Path) -> str:
    r = subprocess.run(["git", "-C", str(tw), "rev-parse", "HEAD"],
                       capture_output=True, text=True)
    if r.returncode:
        print(f"ERROR: {tw} is not a git checkout", file=sys.stderr)
        raise SystemExit(1)
    return r.stdout.strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tw", type=Path, default=Path("/root/translation-work"))
    ap.add_argument("--rebuild", action="store_true")
    a = ap.parse_args()
    h = head(a.tw)
    snap = json.loads((BRIDGE / "passages.snapshot.json").read_text(encoding="utf-8"))
    srevs = set()
    files, nodes = 0, 0
    with (DATA / "argmap-nodes.jsonl").open(encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            nodes += 1
            r = json.loads(line).get("translation_work_revision", "")
            if r and r != "UNKNOWN":
                srevs.add(r)
    print(f"upstream HEAD: {h[:12]}")
    print(f"snapshot pin:  {snap.get('revision', '')[:12]} "
          f"{'CURRENT' if snap.get('revision') == h else 'DRIFT — re-pin deliberately'}")
    only = sorted(srevs)
    print(f"nodes revs:    {', '.join(r[:12] for r in only) or 'none'} "
          f"({nodes} nodes) {'CURRENT' if srevs == {h} else 'DRIFT — rebuild'}")
    if a.rebuild:
        for tool in ("argmap_nodes.py", "crux_queue.py", "treeka.py"):
            r = subprocess.run([sys.executable, str(HERE / tool)], capture_output=True, text=True)
            tail = (r.stdout.strip().splitlines() or ["?"])[-1]
            print(f"{tool}: {'OK' if r.returncode == 0 else 'FAIL'} — {tail[:120]}")
            if r.returncode:
                return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
