#!/usr/bin/env python3
"""compose_bridge.py — join pinned chunk ledgers to candidate work records.

Read-only. For each work in bridge/passages.snapshot.json (chunk pins with
immutable passage IDs), resolves the workdir from the ledger path, then reads
the translation-work lane's canonical mapping + uniform source record:

  COMPOSED    record/map candidate IDs and recorded dossier hashes agree
  PARTIAL     record without mapping, or mapping without RECORDED record
  DOUBLE-GAP  neither (source bytes + mapping both missing)
  CONFLICT    recorded work IDs, candidate IDs, statuses or hashes disagree

Writes bridge/composition-<date>.json. This table is what bridge_resolve --db
consumes conceptually (chunk -> workdir -> candidate work). Dossier bytes,
edition, witness, identity and textual entailment are not checked here.
"""
import argparse
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

import bridge_resolve

HERE = Path(__file__).resolve().parent
BRIDGE = HERE.parent / "bridge"


def classify(workdir, mapping, record):
    """Compare claims in metadata; never infer that a dossier is verified."""
    if not isinstance(mapping, dict) or (record is not None and not isinstance(record, dict)):
        return 'CONFLICT'
    record = record or {}
    mstatus = mapping.get('mapping_status')
    rstatus = record.get('status')
    if record and record.get('work') != workdir:
        return 'CONFLICT'
    if mapping and mapping.get('work') != workdir:
        return 'CONFLICT'
    if mstatus == 'CANDIDATE':
        wid, dossier = mapping.get('openpatala_work_id'), mapping.get('dossier')
        digest = dossier.get('sha256') if isinstance(dossier, dict) else None
        if not isinstance(wid, str) or not wid.strip() or not isinstance(digest, str) or not re.fullmatch(r'[0-9a-f]{64}', digest):
            return 'CONFLICT'
        if rstatus == 'RECORDED':
            rop = record.get('openpatala')
            if (not isinstance(rop, dict) or rop.get('work_id') != wid or
                    rop.get('mapping_status') != mstatus or rop.get('dossier_sha256') != digest):
                return 'CONFLICT'
            return 'COMPOSED'
        return 'PARTIAL'
    if rstatus == 'RECORDED':
        return 'PARTIAL'
    return 'DOUBLE-GAP'


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tw", type=Path, default=Path("/root/translation-work"))
    ap.add_argument("--out", type=Path, default=None)
    a = ap.parse_args()
    snap = json.loads((BRIDGE / "passages.snapshot.json").read_text(encoding="utf-8"))
    bridge_resolve.verify_ledgers(a.tw, snap)
    map_bytes = (a.tw / 'source-maps' / 'openpatala.json').read_bytes()
    tmap = json.loads(map_bytes)
    tworks = tmap.get("works", tmap)
    if not isinstance(tworks, dict):
        raise ValueError('invalid OpenPatala work map')
    rows = []
    for key in sorted(snap["works"]):
        s = snap["works"][key]
        workdir = Path(s.get("ledger", "")).parts[0] if s.get("ledger") else key
        mapping = tworks.get(workdir, {})
        m = mapping if isinstance(mapping, dict) else {}
        rec = None
        rp = a.tw / workdir / "source" / "record.json"
        rec_sha = None
        if rp.is_file():
            try:
                rec_bytes = rp.read_bytes()
                rec = json.loads(rec_bytes)
                rec_sha = hashlib.sha256(rec_bytes).hexdigest()
            except ValueError:
                rec = {'status': 'INVALID-JSON'}
        mstatus = m.get("mapping_status")
        record = rec if isinstance(rec, dict) else {}
        rop = record.get('openpatala') if isinstance(record.get('openpatala'), dict) else {}
        rstatus = record.get("status", "NO-SOURCE-RECORD")
        wid = m.get("openpatala_work_id") or rop.get("work_id")
        dossier = m.get('dossier') if isinstance(m.get('dossier'), dict) else {}
        verdict = classify(workdir, mapping, rec)
        rows.append({"snapshot_key": key, "workdir": workdir,
                     "passages": len(s.get("passages", [])),
                     "mapping_status": mstatus, "record_status": rstatus,
                     "openpatala_work_id": wid,
                     "dossier_sha256": dossier.get("sha256"), 'record_sha256': rec_sha,
                     "volumes": len(record.get("volumes", [])) if isinstance(record.get('volumes', []), list) else 0,
                     "verdict": verdict})
    from collections import Counter
    counts = dict(Counter(r["verdict"] for r in rows))
    doc = {"format": "trika-bridge-composition/1",
           "date": datetime.date.today().isoformat(),
           "snapshot_revision": snap.get("revision"),
           'mapping_sha256': hashlib.sha256(map_bytes).hexdigest(),
           'scope': 'candidate metadata consistency only; dossier bytes, edition and witness not checked',
           "counts": counts, "rows": rows}
    out = a.out or BRIDGE / f"composition-{doc['date']}.json"
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"snapshot works: {len(rows)}; " + "; ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    print(f"matching ledger bytes x candidate work metadata -> {out.name}")
    return 1 if counts.get('CONFLICT') else 0


if __name__ == "__main__":
    raise SystemExit(main())
