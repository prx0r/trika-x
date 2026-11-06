#!/usr/bin/env python3
"""map_agreement.py — reconcile our ledger map with translation-work's canonical map.

Read-only. Compares formal-trika/bridge/source-map.json (our ledger pointers
+ work-key guesses) against <tw>/source-maps/openpatala.json (their canonical
mapping, own lane — never written here). Per-work verdicts:

  AGREE-WORK      both claim the same openpatala work (key substring match)
  THEIRS-NEW      their CANDIDATE where we had UNRESOLVED (adopt, don't duplicate)
  MINE-PROPOSAL   our CANDIDATE-* where theirs is UNMAPPED (evidence for their agent)
  OPEN            neither side claims (honest gap)

Writes bridge/map-agreement-<date>.json (pinned revisions). Exit 0.
"""
import argparse
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRIDGE = HERE.parent / "bridge"


def norm(s: str) -> str:
    s = (s or "").lower()
    s = re.sub(r"^(ptcnd_)?sa_", "", s)
    return re.sub(r"[^a-z]", "", s)


def rev(p: Path) -> str:
    try:
        return subprocess.run(["git", "-C", str(p), "rev-parse", "HEAD"],
                              capture_output=True, check=True, text=True).stdout.strip()
    except Exception:
        return "UNKNOWN"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tw", type=Path, default=Path("/root/translation-work"))
    ap.add_argument("--out", type=Path, default=None)
    a = ap.parse_args()
    mine = json.loads((BRIDGE / "source-map.json").read_text(encoding="utf-8"))["works"]
    theirs = json.loads((a.tw / "source-maps" / "openpatala.json").read_text(encoding="utf-8"))
    tworks = theirs.get("works", theirs)
    rows = []
    for work in sorted(set(mine) | set(tworks)):
        m = mine.get(work, {})
        t = tworks.get(work, {}) if isinstance(tworks.get(work), dict) else {}
        mkey, mstatus = m.get("openpatala_work_key"), m.get("status")
        tstatus, tid = t.get("mapping_status"), t.get("openpatala_work_id")
        mn, tn = norm(mkey), norm(tid)
        if tid and mkey and mkey != "UNRESOLVED" and (mn in tn or tn in mn):
            verdict = "AGREE-WORK"
        elif tstatus == "CANDIDATE" and (not mkey or mkey == "UNRESOLVED"):
            verdict = "THEIRS-NEW"
        elif mstatus and mstatus.startswith("CANDIDATE") and tstatus != "CANDIDATE":
            verdict = "MINE-PROPOSAL"
        else:
            verdict = "OPEN"
        rows.append({"work": work, "mine_status": mstatus, "mine_work_key": mkey,
                     "theirs_status": tstatus, "theirs_work_id": tid, "verdict": verdict})
    from collections import Counter
    counts = dict(Counter(r["verdict"] for r in rows))
    doc = {"format": "trika-map-agreement/1",
           "date": datetime.date.today().isoformat(),
           "translation_work_revision": rev(a.tw),
           "trika_x_revision": rev(HERE.parent.parent) + "+dirty",
           "counts": counts, "rows": rows}
    out = a.out or BRIDGE / f"map-agreement-{doc['date']}.json"
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"works: {len(rows)}; " + "; ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    print(f"their canonical map is authoritative; our file is the ledger-side view -> {out.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
