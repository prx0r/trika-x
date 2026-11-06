#!/usr/bin/env python3
"""compose_bridge.py — join chunk-level ledger pins to work-level openpatala truth.

Read-only. For each work in bridge/passages.snapshot.json (chunk pins with
immutable passage IDs), resolves the workdir from the ledger path, then reads
the translation-work lane's canonical mapping + uniform source record:

  COMPOSED    record RECORDED + mapping CANDIDATE + dossier sha pinned
  PARTIAL     record without mapping, or mapping without RECORDED record
  DOUBLE-GAP  neither (source bytes + mapping both missing)

Writes bridge/composition-<date>.json. This table is what bridge_resolve --db
consumes conceptually (chunk -> workdir -> openpatala work). Exit 0.
"""
import argparse
import datetime
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRIDGE = HERE.parent / "bridge"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tw", type=Path, default=Path("/root/translation-work"))
    ap.add_argument("--out", type=Path, default=None)
    a = ap.parse_args()
    snap = json.loads((BRIDGE / "passages.snapshot.json").read_text(encoding="utf-8"))
    tmap = json.loads((a.tw / "source-maps" / "openpatala.json").read_text(encoding="utf-8"))
    tworks = tmap.get("works", tmap)
    rows = []
    for key in sorted(snap["works"]):
        s = snap["works"][key]
        workdir = Path(s.get("ledger", "")).parts[0] if s.get("ledger") else key
        m = tworks.get(workdir, {}) if isinstance(tworks.get(workdir), dict) else {}
        rec = None
        rp = a.tw / workdir / "source" / "record.json"
        if rp.is_file():
            try:
                rec = json.loads(rp.read_text(encoding="utf-8"))
            except ValueError:
                rec = {"status": "INVALID-JSON"}
        mstatus = m.get("mapping_status")
        rstatus = (rec or {}).get("status", "NO-SOURCE-RECORD")
        wid = m.get("openpatala_work_id") or (rec or {}).get("openpatala", {}).get("work_id")
        dossier = (m.get("dossier") or {})
        if rstatus == "RECORDED" and mstatus == "CANDIDATE" and dossier.get("sha256"):
            verdict = "COMPOSED"
        elif rstatus == "RECORDED" or mstatus == "CANDIDATE":
            verdict = "PARTIAL"
        else:
            verdict = "DOUBLE-GAP"
        rows.append({"snapshot_key": key, "workdir": workdir,
                     "passages": len(s.get("passages", [])),
                     "mapping_status": mstatus, "record_status": rstatus,
                     "openpatala_work_id": wid,
                     "dossier_sha256": dossier.get("sha256"),
                     "volumes": len((rec or {}).get("volumes", [])) if isinstance(rec, dict) else 0,
                     "verdict": verdict})
    from collections import Counter
    counts = dict(Counter(r["verdict"] for r in rows))
    doc = {"format": "trika-bridge-composition/1",
           "date": datetime.date.today().isoformat(),
           "snapshot_revision": snap.get("revision"),
           "counts": counts, "rows": rows}
    out = a.out or BRIDGE / f"composition-{doc['date']}.json"
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"snapshot works: {len(rows)}; " + "; ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    print(f"chunk pins (ours) x work truth (theirs) -> {out.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
