#!/usr/bin/env python3
"""import_paper.py — vendor science papers with provenance (archive-first).

arxiv:<id> | pmid:<n> | pmc:<id> → metadata + PDF → bridge/science-sources/<id>/
with sha + provenance. What the essay gate cites; live search never sits
inside the gate. Stdlib only.

  python3 tools/import_paper.py arxiv:1310.7930
  python3 tools/import_paper.py pmid:42990000 --no-pdf
  python3 tools/import_paper.py --list
"""
import argparse
import hashlib
import html
import json
import re
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "bridge" / "science-sources"
UA = {"User-Agent": "trika-x-science-import/1.0"}


def get(url: str, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read() if binary else r.read().decode("utf-8", "replace")


def arxiv_meta(aid: str):
    x = get(f"https://export.arxiv.org/api/query?id_list={aid}")
    e = re.search(r"<entry>(.*?)</entry>", x, re.S)
    if not e:
        raise ValueError(f"arxiv id not found: {aid}")
    e = e.group(1)
    def one(pat):
        m = re.search(pat, e, re.S)
        return html.unescape(re.sub(r"\s+", " ", m.group(1))).strip() if m else ""
    return {"id": f"arxiv:{aid}", "title": one(r"<title>(.*?)</title>"),
            "authors": re.findall(r"<name>(.*?)</name>", e),
            "published": one(r"<published>(.*?)</published>"),
            "abstract": one(r"<summary>(.*?)</summary>"),
            "pdf": f"https://arxiv.org/pdf/{aid}.pdf"}


def pubmed_meta(pmid: str):
    x = get(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmid}&retmode=json")
    d = json.loads(x)["result"][pmid]
    return {"id": f"pmid:{pmid}", "title": d.get("title", ""),
            "authors": [a.get("name", "") for a in d.get("authors", [])],
            "published": d.get("pubdate", ""), "abstract": "",
            "pdf": f"https://pmc.ncbi.nlm.nih.gov/articles/{d.get('pmcrefcount', '')}/"
            if d.get("pmcrefcount") else ""}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("ref", nargs="?", default="")
    ap.add_argument("--no-pdf", action="store_true")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.list:
        if not OUT.is_dir():
            print("no vendors yet"); return 0
        for d in sorted(OUT.iterdir()):
            p = json.loads((d / "provenance.json").read_text())
            print(f"{d.name}: {p.get('title', '')[:70]}")
        return 0
    if not a.ref:
        print("need arxiv:<id> | pmid:<n> | pmc:<id>"); return 1
    kind, _, key = a.ref.partition(":")
    if kind == "arxiv":
        meta = arxiv_meta(key)
    elif kind == "pmid":
        meta = pubmed_meta(key)
    elif kind == "pmc":
        meta = {"id": f"pmc:{key}", "title": "", "authors": [],
                "published": "", "abstract": "",
                "pdf": f"https://pmc.ncbi.nlm.nih.gov/articles/PMC{key}/"}
    else:
        print(f"unknown scheme: {kind}"); return 1
    slug = meta["id"].replace(":", "-")
    dest = OUT / slug
    dest.mkdir(parents=True, exist_ok=True)
    pdf_sha, pdf_bytes = None, 0
    if not a.no_pdf and meta.get("pdf"):
        try:
            blob = get(meta["pdf"], binary=True)
            pdf_sha = hashlib.sha256(blob).hexdigest()
            pdf_bytes = len(blob)
            (dest / f"{slug}.pdf").write_bytes(blob)
        except Exception as e:
            print(f"PDF fetch failed (metadata kept): {str(e)[:80]}")
    prov = {"ref": a.ref, "fetched": time.strftime("%Y-%m-%d"),
            "title": meta["title"], "authors": meta["authors"],
            "published": meta["published"], "abstract": meta["abstract"][:2000],
            "pdf_url": meta.get("pdf", ""), "pdf_sha256": pdf_sha,
            "pdf_bytes": pdf_bytes}
    (dest / "provenance.json").write_text(json.dumps(prov, ensure_ascii=False, indent=1) + "\n")
    print(f"vendored {meta['id']}: {meta['title'][:70]}")
    print(f"  pdf: {pdf_bytes} bytes sha={str(pdf_sha)[:16] if pdf_sha else 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
