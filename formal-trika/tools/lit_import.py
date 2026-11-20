#!/usr/bin/env python3
"""lit_import.py — vendor DOI metadata (and abstract) with provenance.

  python3 tools/lit_import.py 10.1007/s10441-020-09400-0
  python3 tools/lit_import.py --from-candidates lit-candidates.json --limit 5

Stores bridge/lit/<slug>/meta.json only. No paywalled full text. The abstract is
what the source itself published, with its sha; a hash is not a licence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.request
from pathlib import Path

UA = "svatantrya-lit/1.0 (mailto:research@svatantrya.net)"
OUT = Path(__file__).resolve().parent.parent / "bridge" / "lit"


def fetch(doi: str) -> dict:
    req = urllib.request.Request("https://api.crossref.org/works/" + doi, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        m = json.loads(r.read().decode("utf-8", "replace"))["message"]
    title = " ".join(m.get("title") or [""])
    authors = [f"{a.get('given','')} {a.get('family','')}".strip() for a in m.get("author", [])]
    year = None
    for k in ("published-print", "published-online", "issued"):
        p = (m.get(k) or {}).get("date-parts") or [[]]
        if p and p[0] and p[0][0]:
            year = p[0][0]; break
    abstract = re.sub(r"<[^>]+>", " ", m.get("abstract", "") or "")
    abstract = re.sub(r"\s+", " ", abstract).strip()
    return {"doi": doi, "title": title, "authors": authors, "year": year,
            "container": " ".join(m.get("container-title") or []),
            "publisher": m.get("publisher", ""), "url": m.get("URL", ""),
            "rights": m.get("license", []), "abstract": abstract}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("doi", nargs="?", default="")
    ap.add_argument("--from-candidates", type=Path, default=None)
    ap.add_argument("--limit", type=int, default=5)
    a = ap.parse_args()
    dois = [a.doi] if a.doi else []
    if a.from_candidates:
        d = json.loads(a.from_candidates.read_text(encoding="utf-8"))
        dois += [c["doi"] for c in d.get("candidates", []) if c.get("doi")][:a.limit]
    if not dois:
        print("need a DOI or --from-candidates"); return 1
    for doi in dois:
        try:
            meta = fetch(doi)
        except Exception as e:
            print(f"{doi}: fetch failed ({e})"); continue
        slug = re.sub(r"[^a-z0-9]+", "-", (meta["title"] or doi).lower()).strip("-")[:60] or "untitled"
        d = OUT / slug
        d.mkdir(parents=True, exist_ok=True)
        meta["abstract_sha256"] = hashlib.sha256(meta["abstract"].encode()).hexdigest()
        meta["format"] = "svread-lit-source/1"
        (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"imported {doi} -> bridge/lit/{slug}/meta.json ({len(meta['abstract'])} abstract chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
