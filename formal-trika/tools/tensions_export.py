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
import json
import re
from pathlib import Path

TENSIONS = Path("/root/nibbanahelp/tensions")
OUT = Path("/root/trika-x/formal-trika/data/tensions-export.jsonl")
CLOSED = {"resolved", "closed"}


def parse_header(text):
    head = text.split("---", 1)[0] if "---" in text else text
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
    cands = []
    for fp in sorted(TENSIONS.glob("*.md")):
        try:
            h = parse_header(fp.read_text(encoding="utf-8"))
        except OSError:
            continue
        if h.get("visibility") != "public":
            continue
        status = (h.get("status") or "unknown").lower()
        cands.append({"kind": "lived-tension", "id": h.get("id", fp.stem),
                      "status": status, "open": status not in CLOSED,
                      "domain": h.get("domain"), "roots": h.get("roots", []),
                      "factors": h.get("factors", []),
                      "summary": (h.get("summary") or "")[:200]})
    OUT.write_text("\n".join(json.dumps(c, ensure_ascii=False) for c in cands) + "\n",
                   encoding="utf-8")
    print(f"tensions: {len(cands)} ({sum(1 for c in cands if c['open'])} open) -> {OUT}")


if __name__ == "__main__":
    raise SystemExit(main())
