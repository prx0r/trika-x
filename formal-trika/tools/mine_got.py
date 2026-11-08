#!/usr/bin/env python3
"""mine_got.py — vendor geometryofthinking.com articles with provenance.

WordPress.com sitemap -> fetch article pages -> extract entry-content ->
markdown + images list + provenance JSON. Rerunnable, polite, stdlib only.

  python3 tools/mine_got.py --list                 (enumerate sitemap URLs)
  python3 tools/mine_got.py --all                  (fetch all articles)
  python3 tools/mine_got.py --only the-tetrahedron (slug substring filter)

Output: imports/geometryofthinking/<slug>.md + <slug>.prov.json + INDEX.md
"""
import argparse
import hashlib
import html
import re
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "imports" / "geometryofthinking"
SITE = "https://geometryofthinking.com"
SKIP = ("/about/", "/index/", "/model-making/", "/more-model-making/")


def get(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "trika-x-research-miner/1.0"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", "replace")


def sitemap_urls():
    x = get(SITE + "/sitemap.xml")
    return re.findall(r"<loc>([^<]+)</loc>", x)


def clean_text(h: str) -> str:
    h = re.sub(r"<script.*?</script>|<style.*?</style>", "", h, flags=re.S)
    h = re.sub(r"<li[^>]*>", "\n- ", h)
    h = re.sub(r"</(p|h\d|div|blockquote|ul|ol)>", "\n\n", h)
    h = re.sub(r"<br[^>]*>", "\n", h)
    h = re.sub(r"<[^>]+>", "", h)
    h = html.unescape(h)
    h = re.sub(r"[ \t]+", " ", h)
    h = re.sub(r"\n{3,}", "\n\n", h)
    return h.strip()


def mine(url: str):
    slug = url.rstrip("/").rsplit("/", 1)[-1]
    raw = get(url)
    m = re.search(r"<h1 class=\"entry-title[^>]*>(.*?)</h1>", raw, re.S)
    title = clean_text(m.group(1)) if m else slug
    m2 = re.search(r"<div class=\"entry-content\">(.*?)</div>\s*(<footer|</article)", raw, re.S)
    body = clean_text(m2.group(1)) if m2 else ""
    imgs = re.findall(r"<img[^>]+src=\"([^\"]+)\"", raw)
    imgs = sorted({u for u in imgs if "geometryofthinking" in u or u.startswith("http")})
    sha = hashlib.sha256(raw.encode()).hexdigest()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{slug}.md").write_text(
        f"# {title}\n\nSource: {url}\n\n{body}\n", encoding="utf-8")
    prov = {"url": url, "title": title, "fetched": time.strftime("%Y-%m-%d"),
            "sha256": sha, "chars": len(body), "images": imgs}
    import json
    (OUT / f"{slug}.prov.json").write_text(json.dumps(prov, indent=1), encoding="utf-8")
    return slug, len(body), len(imgs)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    urls = [u for u in sitemap_urls()
            if u.startswith(SITE + "/20") and not any(u.endswith(s) for s in SKIP)]
    if a.list:
        print(f"{len(urls)} article urls")
        for u in urls:
            print(" ", u)
        return 0
    if a.only:
        urls = [u for u in urls if a.only in u]
    if not urls:
        print("nothing matched")
        return 1
    rows = []
    for u in urls:
        try:
            slug, n, ni = mine(u)
            rows.append((slug, n, ni, u))
            print(f"OK {slug} ({n} chars, {ni} imgs)")
        except Exception as e:
            print(f"FAIL {u} {str(e)[:80]}")
        time.sleep(1)
    lines = ["# geometryofthinking imports", "",
             f"Fetched {time.strftime('%Y-%m-%d')}, {len(rows)} articles.", "",
             "| slug | chars | imgs | url |", "|---|---|---|---|"]
    for slug, n, ni, u in sorted(rows):
        lines.append(f"| {slug} | {n} | {ni} | {u} |")
    (OUT / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {len(rows)} articles -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
