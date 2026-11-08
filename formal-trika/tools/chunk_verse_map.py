#!/usr/bin/env python3
"""chunk_verse_map.py — consolidate per-work chunk<->verse maps into one file.

Reads formal-trika/bridge/chunk-verse-<work>-<date>.json (built by
chunk_verse.py, one per closable work) and writes
formal-trika/bridge/chunk-verse-map.json (trika-chunk-verse-map/1):
all CANDIDATE maps in one place for bridge consumers.

  python3 formal-trika/tools/chunk_verse_map.py --write   # regenerate
  python3 formal-trika/tools/chunk_verse_map.py --check   # fail on drift

Newest dated file wins per work. Nothing here is a verified edition or
witness claim: every work entry carries status CANDIDATE.
"""
from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
BRIDGE = HERE / "bridge"
OUT = BRIDGE / "chunk-verse-map.json"


def work_of(path: Path) -> str:
    stem = path.stem
    assert stem.startswith("chunk-verse-")
    rest = stem[len("chunk-verse-"):]
    # dated files end -YYYY-MM-DD; work dirs may contain dashes.
    import re
    m = re.fullmatch(r"(.+)-\d{4}-\d{2}-\d{2}", rest)
    return m.group(1) if m else rest


def build() -> dict:
    files: dict[str, Path] = {}
    for f in sorted(BRIDGE.glob("chunk-verse-*.json")):
        if f.name == OUT.name:
            continue
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if not isinstance(d, dict) or "chunks" not in d:
            continue
        files[work_of(f)] = f  # sorted glob: newest date wins
    out = {"format": "trika-chunk-verse-map/1",
           "note": ("Consolidated CANDIDATE chunk<->verse<->byte maps. "
                    "Regenerate with tools/chunk_verse_map.py --write. "
                    "Per-work sources: bridge/chunk-verse-<work>-<date>.json. "
                    "Nothing here is a verified edition or witness claim."),
           "works": {}}
    n = 0
    for work in sorted(files):
        d = json.loads(files[work].read_text(encoding="utf-8"))
        chunks = d.get("chunks", {})
        out["works"][work] = {
            "chunks": chunks,
            "manifests": d.get("manifests", []),
            "status": "CANDIDATE",
            "source_file": files[work].name,
        }
        n += len(chunks)
    out["works_total"] = len(out["works"])
    out["chunks_total"] = n
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--write", action="store_true")
    g.add_argument("--check", action="store_true")
    a = ap.parse_args()
    blob = (json.dumps(build(), ensure_ascii=False, sort_keys=True,
                       indent=1) + "\n")
    if a.write:
        OUT.write_text(blob, encoding="utf-8")
        print(f"chunk-verse-map: wrote {OUT}")
        return 0
    if a.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != blob:
            print("chunk-verse-map: DRIFT — run --write", file=sys.stderr)
            return 1
        print("chunk-verse-map: SHARP")
        return 0
    print(blob, end="")
    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(main())
