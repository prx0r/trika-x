#!/usr/bin/env python3
"""lit_harvest.py — harvest a seed paper's citations into grounded secondary claims.

Reads a pdftotext -layout paper, finds in-text citations (Author Year[: page]),
captures the sentence around each citation as a claim, and parses the reference
list. Output is honest: the claim is what the seed paper says, attributed as
"[Author Year, via seed]". It does not pretend we read the cited work.

  python3 tools/lit_harvest.py bridge/essay-gold/kaul-causal-reasoning-2022/paper.txt \
      --out bridge/essay-gold/kaul-causal-reasoning-2022/lit-seed.json
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

CITE = re.compile(
    r"(?P<auth>[A-Z][A-Za-zĀāĪīŪūṚṛṜṝḶḷṂṃḤḥŚśṢṣṬṭḌḍÑñṄṅ'’\-]+"
    r"(?:\s+(?:and|&)\s+[A-Z][A-Za-zĀāĪīŪūṚṛṜṝḶḷṂṃḤḥŚśṢṣṬṭḌḍÑñṄṅ'’\-]+)?)"
    r"\s*\(?(?P<year>\d{4}[a-z]?)\)?"
    r"(?::\s*(?P<page>\d+(?:[–-]\d+)?))?")
PAGE = re.compile(r"^\s*(?:\d{1,3}\s+.*\s+(\d{2,3})|(\d{2,3}))\s*$")
SENT = re.compile(r"(?<=[.!?])\s+")


def sentences_with_pages(text: str) -> list[tuple[str, str]]:
    out, page = [], ""
    buf = ""
    for line in text.splitlines():
        if PAGE.match(line):
            m = PAGE.match(line)
            page = m.group(1) or m.group(2) or page
            continue
        buf += " " + line
    for s in SENT.split(buf):
        s = re.sub(r"\s+", " ", s).strip()
        if s:
            out.append((s, page))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paper")
    ap.add_argument("--out", required=True)
    ap.add_argument("--seed", default="")
    a = ap.parse_args()
    text = Path(a.paper).read_text(encoding="utf-8", errors="replace")
    seed = a.seed or Path(a.paper).stem
    claims, seen = [], {}
    for sent, page in sentences_with_pages(text):
        for m in CITE.finditer(sent):
            auth, year = m.group("auth").strip(), m.group("year")
            if auth.lower() in {"see", "cf", "also", "and", "the"}:
                continue
            key = f"{auth} {year}"
            # Skip the seed paper citing itself constantly? keep it: useful.
            if key not in seen:
                seen[key] = {"citation": key, "author": auth, "year": year,
                             "pages": [], "claims": []}
            rec = seen[key]
            cp = m.group("page") or ""
            if cp and cp not in rec["pages"]:
                rec["pages"].append(cp)
            if len(rec["claims"]) < 3 and len(sent) <= 600:
                rec["claims"].append(sent)
    for k in seen:
        claims.append(seen[k])
    claims.sort(key=lambda x: (-len(x["claims"]), x["citation"]))
    doc = {
        "format": "svread-lit-seed/1",
        "seed": seed,
        "note": ("Claims are the seed paper's own sentences around each citation. "
                 "Attribute as [Author Year, via seed]; we have not read the cited work."),
        "count": len(claims),
        "citations": claims,
    }
    Path(a.out).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"lit-seed -> {a.out}: {len(claims)} citations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
