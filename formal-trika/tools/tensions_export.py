#!/usr/bin/env python3
"""tensions_export.py — N3: nibbanahelp tensions → crux-candidate export (read-only).

Reads nibbanahelp/tensions/*.md headers (id/visibility/diarist/opened/
status/domain/roots/factors/summary); emits trika-x-side candidate list
for Treeka gap-merging. NEVER writes nibbanahelp (their lane, VOICE RULE:
bodies are the diarist's words — only headers + status flow here, never
body text). Private items are SKIPPED (visibility != public).
Open = status not in {resolved, closed}. Output: data/tensions-export.jsonl.
Usage: python3 formal-trika/tools/tensions_export.py
"""
import argparse
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TENSIONS = Path(os.environ.get('NIBBANAHELP_CHECKOUT', ROOT.parent.parent / 'nibbanahelp')) / 'tensions'
OUT = ROOT / 'data/tensions-export.jsonl'
CLOSED = {"resolved", "closed"}


def parse_header(text):
    # A file without the explicit header/body boundary is not safe to export:
    # treating its body as headers could disclose text or invent visibility.
    lines = text.splitlines()
    try:
        boundary = next(i for i, line in enumerate(lines) if line.strip() == '---')
    except StopIteration:
        return {}
    head = '\n'.join(lines[:boundary])
    d = {}
    for line in head.splitlines():
        m = re.match(r"([A-Za-z_]+):\s*(.*)$", line.strip())
        if m:
            d[m.group(1)] = m.group(2).strip()
    for k in ("roots", "factors", "factors_growing"):
        if isinstance(d.get(k), str):
            d[k] = [x.strip(" []'\"") for x in d[k].strip("[]").split(",") if x.strip()]
    return d


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--tensions', type=Path, default=TENSIONS)
    ap.add_argument('--out', type=Path, default=OUT)
    a = ap.parse_args()
    if not a.tensions.is_dir():
        raise SystemExit(f'tensions directory not found: {a.tensions}')
    cands = []
    for fp in sorted(a.tensions.glob("*.md")):
        h = parse_header(fp.read_text(encoding="utf-8"))
        if h.get("visibility") != "public":
            continue
        status = (h.get("status") or "unknown").lower()
        cands.append({"kind": "lived-tension", "id": h.get("id", fp.stem),
                      "status": status, "open": status not in CLOSED,
                      "domain": h.get("domain"), "roots": h.get("roots", []),
                      "factors": h.get("factors", []),
                      "summary": (h.get("summary") or "")[:200]})
    a.out.write_text("\n".join(json.dumps(c, ensure_ascii=False) for c in cands) + "\n",
                   encoding="utf-8")
    print(f"tensions: {len(cands)} ({sum(1 for c in cands if c['open'])} open) -> {a.out}")


if __name__ == "__main__":
    raise SystemExit(main())
