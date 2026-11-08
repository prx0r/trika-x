#!/usr/bin/env python3
"""trace_all.py — compile trika-trace/1 bundles for every ledger locator.

Turns the 13 hand-compiled traces into a corpus-wide index. Reads only:
translation-work ledgers/layers/proofs, openpatala box DB, trika-x EVIDENCE,
svread scholar projections. Writes only formal-trika/data/traces/.

  python3 formal-trika/tools/trace_all.py                 # compile all works
  python3 formal-trika/tools/trace_all.py --works phrdaya,tantrasara-a08
  python3 formal-trika/tools/trace_all.py --limit 5       # smoke
  python3 formal-trika/tools/trace_all.py --index-only    # rebuild index

Verdicts are the compiler's: COMPLETE / PARTIAL / UNKNOWN. A locator that
cannot compile is an ERROR in the report, never a silent pass.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE))

from trace_bundle import (DSN_DEFAULT, OUTDIR, SV_DEFAULT, TW_DEFAULT,  # noqa: E402
                          compile_bundle)


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def ledgers(tw: Path) -> list[tuple[str, list[str]]]:
    out = []
    for p in sorted(tw.glob("*/passages.jsonl")):
        work = p.parent.name
        targets = []
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                if row.get("locator"):
                    targets.append(row["locator"])
        if targets:
            out.append((work, targets))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tw", default=str(TW_DEFAULT))
    ap.add_argument("--sv", default=str(SV_DEFAULT))
    ap.add_argument("--dsn", default=DSN_DEFAULT)
    ap.add_argument("--out", default=str(OUTDIR))
    ap.add_argument("--works", default="", help="comma-separated work dirs")
    ap.add_argument("--limit", type=int, default=0, help="max locators")
    ap.add_argument("--no-db", action="store_true")
    ap.add_argument("--index-only", action="store_true",
                    help="rebuild index from existing bundles, no compile")
    a = ap.parse_args()

    tw, sv, out = Path(a.tw), Path(a.sv), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    wanted = {w.strip() for w in a.works.split(",") if w.strip()}

    entries, errors = [], []
    counts: dict[str, int] = {}
    t0 = time.time()

    if not a.index_only:
        done = 0
        for work, targets in ledgers(tw):
            if wanted and work not in wanted:
                continue
            for target in targets:
                if a.limit and done >= a.limit:
                    break
                try:
                    bundle, rc = compile_bundle(
                        work, target, tw, sv, a.dsn, use_db=not a.no_db)
                except Exception as e:  # noqa: BLE001 — report, never pass
                    errors.append({"work": work, "target": target,
                                   "error": f"{type(e).__name__}: {e}"})
                    continue
                if rc != 0 or not bundle:
                    errors.append({"work": work, "target": target,
                                   "error": "compile refused",
                                   "problems": bundle.get("open_problems", [])})
                    continue
                text = json.dumps(bundle, ensure_ascii=False, sort_keys=True,
                                  indent=1)
                path = out / f"{work}-{target}.json"
                path.write_text(text + "\n", encoding="utf-8")
                verdict = bundle.get("verdict", "UNKNOWN")
                counts[verdict] = counts.get(verdict, 0) + 1
                theorems = [t.get("theorem") for t in
                            (bundle.get("formal", {}) or {}).get("theorems", [])
                            if t.get("theorem")]
                entries.append({
                    "work": work, "target": target,
                    "immutable_id": (bundle.get("chunk", {}) or {})
                    .get("immutable_id"),
                    "verdict": verdict,
                    "caveats": bundle.get("caveats", []),
                    "gaps": bundle.get("gaps", []),
                    "theorems": theorems,
                    "file": f"traces/{path.name}",
                    "sha256": sha((text + "\n").encode()),
                })
                done += 1
        if a.limit and done >= a.limit:
            print(f"trace_all: limit {a.limit} reached", file=sys.stderr)

    if a.index_only:
        for path in sorted(out.glob("*.json")):
            if path.name == "index.json":
                continue
            raw = path.read_bytes()
            b = json.loads(raw)
            ch = b.get("chunk", {}) or {}
            verdict = b.get("verdict", "UNKNOWN")
            counts[verdict] = counts.get(verdict, 0) + 1
            entries.append({
                "work": ch.get("work"), "target": ch.get("target"),
                "immutable_id": ch.get("immutable_id"),
                "verdict": verdict,
                "caveats": b.get("caveats", []),
                "gaps": b.get("gaps", []),
                "theorems": [t.get("theorem") for t in
                             (b.get("formal", {}) or {}).get("theorems", [])
                             if t.get("theorem")],
                "file": f"traces/{path.name}",
                "sha256": sha(raw),
            })

    entries.sort(key=lambda e: (e.get("work") or "", e.get("target") or ""))
    index = {
        "format": "trika-traces-index/1",
        "note": ("Trika-x side index (svread publishes its own via emit_verify). "
                 "Each entry is a trika-trace/1 bundle: source -> layers -> "
                 "proofs -> formal -> citing essays, hash-pinned. COMPLETE means "
                 "every applicable hop resolved; PARTIAL names its gaps. "
                 "Re-verify: trace_bundle.py --verify <file>."),
        "count": len(entries),
        "verdicts": dict(sorted(counts.items())),
        "errors": errors,
        "entries": entries,
    }
    (out / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, sort_keys=True, indent=1) + "\n",
        encoding="utf-8")

    works = len({e["work"] for e in entries})
    secs = round(time.time() - t0, 1)
    print(f"trace_all: {len(entries)} bundles across {works} works "
          f"in {secs}s; verdicts {dict(sorted(counts.items()))}; "
          f"errors {len(errors)}")
    print(f"trace_all: index -> {out / 'index.json'}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
