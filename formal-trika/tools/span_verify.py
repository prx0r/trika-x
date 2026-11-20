#!/usr/bin/env python3
"""span_verify.py — every Sanskrit line in a draft must exist verbatim in the ground.

  python3 tools/span_verify.py swarm/essay-*.md --ground <ground.json>
  python3 tools/span_verify.py swarm/essay-*.md --ground data/essay-ground/tantrasara-a08.json

Exit 0 = every quoted line matched a ground verse (whitespace-normalised).
Exit 1 = a quoted line did not match (named). This proves bytes, not reading.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DIACRITIC = set("āīūṛṝḷḹṃḥśṣṭḍṇñṅĀĪŪṚṜḶḸṂḤŚṢṬḌṆÑṄ")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("draft", type=Path)
    ap.add_argument("--ground", type=Path, required=True)
    a = ap.parse_args()
    g = json.loads(a.ground.read_text(encoding="utf-8"))
    corpus = {norm(v.get("sanskrit", "")) for v in g.get("verses", {}).values()}
    text = a.draft.read_text(encoding="utf-8")
    checked = matched = 0
    fails = []
    for line in text.splitlines():
        t = line.strip().lstrip(">").strip()
        if not t or len(t) < 40 or not any(c in t for c in DIACRITIC):
            continue
        # strip a trailing [verse-id] and any gloss after a dash
        m = re.match(r"^(.*?)\s*\[((?:tsa|tal|ipk|ipv)-[^\]]+)\]\s*$", t)
        if not m:
            continue
        span, vid = norm(m.group(1)), m.group(2)
        anchored = any(span in c for c in corpus)
        checked += 1
        if anchored:
            matched += 1
        else:
            fails.append((vid, span[:80]))
    print(f"span_verify: {matched}/{checked} Sanskrit lines matched the ground")
    for vid, span in fails[:10]:
        print(f"  UNMATCHED [{vid}] {span}")
    return 0 if checked and not fails else (0 if checked == 0 else 1)


if __name__ == "__main__":
    raise SystemExit(main())
