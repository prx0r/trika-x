#!/usr/bin/env python3
"""lit_search.py — find candidate scholarship via OpenAlex (stdlib only).

  python3 tools/lit_search.py "causality Abhinavagupta" --limit 10
  python3 tools/lit_search.py "Fitness Beats Truth" --out lit-candidates.json

Returns title, year, authors, DOI, open-access URL and citation count. This is
discovery, not evidence: nothing here is a claim until imported and read.
"""
from __future__ import annotations

import argparse
import json
import urllib.parse
import urllib.request
from pathlib import Path

UA = "svatantrya-lit/1.0 (mailto:research@svatantrya.net)"


def search(q: str, limit: int) -> list[dict]:
    url = ("https://api.openalex.org/works?search=" + urllib.parse.quote(q) +
           f"&per-page={max(1, min(50, limit))}&mailto=research@svatantrya.net")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.loads(r.read().decode("utf-8", "replace"))
    out = []
    for w in d.get("results", []):
        authors = [a.get("author", {}).get("display_name", "") for a in w.get("authorships", [])][:6]
        oa = (w.get("open_access") or {}).get("oa_url") or ""
        out.append({"title": w.get("title") or w.get("display_name") or "",
                    "year": w.get("publication_year"),
                    "authors": authors,
                    "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
                    "cited_by": w.get("cited_by_count", 0),
                    "open_access_url": oa,
                    "type": w.get("type", "")})
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("query")
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--out", type=Path, default=None)
    a = ap.parse_args()
    rows = search(a.query, a.limit)
    doc = {"format": "svread-lit-candidates/1", "query": a.query, "count": len(rows), "candidates": rows}
    if a.out:
        a.out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"lit-candidates -> {a.out} ({len(rows)})")
    else:
        print(json.dumps(doc, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
