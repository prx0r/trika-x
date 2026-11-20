#!/usr/bin/env python3
"""lit_review.py — turn harvested citations into a review block the essay must engage.

Input is lit-seed.json (claims as the seed paper reports them). Output is a
grouped matrix plus a compact prompt block. Every line is attributed
"[Author Year, via seed]" because we have not read the cited work; the block
says so and the essay must repeat it.

  python3 tools/lit_review.py bridge/essay-gold/kaul-causal-reasoning-2022/lit-seed.json \
      --out bridge/essay-gold/kaul-causal-reasoning-2022/lit-review.json
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

TOPICS = {
    "causality": ["causal", "cause", "kārya", "kāraṇa", "sāmagrī", "dependent origination"],
    "buddhism": ["buddhis", "vijñāna", "mādhyamika", "nāgārjuna", "dignāga", "dharmakīrti"],
    "recognition": ["recognition", "pratyabhijñā", "utpaladeva", "īpk", "īpv", "reflexiv"],
    "history": ["sanderson", "kashmir", "siddhānta", "krama", "mālinī", "tantra"],
    "philology": ["edition", "ksts", "manuscript", "translation", "torella", "gnoli"],
}


def topic_of(rec: dict) -> str:
    blob = " ".join([rec["citation"]] + rec.get("claims", [])[:2]).lower()
    for name, keys in TOPICS.items():
        if any(k in blob for k in keys):
            return name
    return "context"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("seed")
    ap.add_argument("--out", required=True)
    ap.add_argument("--max", type=int, default=25)
    a = ap.parse_args()
    d = json.loads(Path(a.seed).read_text(encoding="utf-8"))
    seed = d.get("seed", "seed")
    rows = []
    for c in d.get("citations", []):
        if not c.get("claims"):
            continue
        claim = re.sub(r"\s+", " ", c["claims"][0]).strip()
        claim = claim[:420]
        rows.append({"citation": c["citation"], "author": c["author"],
                     "year": c["year"], "pages": c.get("pages", []),
                     "topic": topic_of(c), "claim": claim,
                     "claim_count": len(c.get("claims", []))})
    rows.sort(key=lambda r: (-r["claim_count"], r["citation"]))
    selected = rows[:a.max]
    groups = {}
    for r in selected:
        groups.setdefault(r["topic"], []).append(r)
    lines = [f"SECONDARY SCHOLARSHIP (claims as reported by {seed}; cite as "
             f"[Author Year, via {seed}]; do not invent what they say)"]
    for topic in sorted(groups):
        lines.append(f"\n[{topic}]")
        for r in groups[topic]:
            pg = f":{r['pages'][0]}" if r["pages"] else ""
            lines.append(f"- {r['author']} {r['year']}{pg} — {r['claim']}")
    prompt_block = "\n".join(lines)
    doc = {"format": "svread-lit-review/1", "seed": seed,
           "note": "Attribution is second-hand. The essay must say 'via seed'.",
           "count": len(selected), "groups": groups, "prompt_block": prompt_block}
    Path(a.out).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"lit-review -> {a.out}: {len(selected)} citations, {len(prompt_block)} chars")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
