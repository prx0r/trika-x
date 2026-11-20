#!/usr/bin/env python3
"""essay_score.py — measure a draft against the gold-standard shape and list gaps.

  python3 tools/essay_score.py swarm/essay-*.md --out swarm/essay.score.json

Exit 0 always (this is a report). The gap list is what essay_revise.py consumes.
Targets are the "journal tier": ~4,000 words, 9+ body sections, 22+ unique
verses, 14+ Sanskrit quotes, 18+ objections, 20+ replies, 10+ questions,
3+ explicit author claims, 8+ secondary citations, a desideratum.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import essay_gold_analyze as A  # noqa: E402

TARGET = {
    "words": 4000, "sections": 9, "unique_verses": 22, "sanskrit_quotes": 14,
    "objection_moves": 18, "reply_moves": 20, "questions": 10,
    "author_claims": 3, "secondary_citations": 8,
}
DIACRITIC = set("āīūṛṝḷḹṃḥśṣṭḍṇñṅĀĪŪṚṜḶḸṂḤŚṢṬḌṆÑṄ")


def score(text: str) -> dict:
    secs = re.split(r"(?m)^##\s+", text)[1:]
    words = len(re.findall(r"\b[\w\u0100-\u017f'-]+\b", text))
    verses = set(re.findall(r"\b(?:tsa|tal|ipk|ipv)-[a-z0-9]+-v\d+\b", text))
    sanskrit = []
    for line in text.splitlines():
        t = line.strip()
        if not t:
            continue
        if t.startswith(">") and ("||" in t or any(c in t for c in DIACRITIC)):
            sanskrit.append(t); continue
        # bare Sanskrit quote line: diacritic-dense, long, ending in a verse marker
        if len(t) > 50 and any(c in t for c in DIACRITIC) and re.search(r"\[(?:tsa|tal|ipk|ipv)-[^\]]+\]\s*$", t):
            sanskrit.append(t)
    sec_cites = re.findall(r"\[[^\]]*\b\d{4}[a-z]?[^\]]*\]", text)
    m = {
        "words": words,
        "sections": len(secs),
        "unique_verses": len(verses),
        "sanskrit_quotes": len(sanskrit),
        "objection_moves": len(A.OBJECTION.findall(text)),
        "reply_moves": len(A.REPLY.findall(text)),
        "questions": text.count("?"),
        "author_claims": len(A.AUTHOR_CLAIM.findall(text)),
        "secondary_citations": len(sec_cites),
        "has_literature_section": bool(re.search(r"(?mi)^##\s+.*(literature|scholarship)", text)),
        "has_desideratum": bool(re.search(r"(?i)desideratum|what remains|remains unresolved", text)),
    }
    checks = {}
    for k, target in TARGET.items():
        checks[k] = {"value": m[k], "target": target, "pass": m[k] >= target}
    checks["has_literature_section"] = {"value": m["has_literature_section"],
                                        "target": True, "pass": m["has_literature_section"]}
    checks["has_desideratum"] = {"value": m["has_desideratum"],
                                 "target": True, "pass": m["has_desideratum"]}
    gaps = [k for k, v in checks.items() if not v["pass"]]
    return {"format": "essay-score/1", "metrics": m, "checks": checks,
            "gaps": gaps, "pass_count": sum(1 for v in checks.values() if v["pass"]),
            "total": len(checks)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("draft")
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    text = Path(a.draft).read_text(encoding="utf-8", errors="replace")
    doc = score(text)
    if a.out:
        Path(a.out).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    m = doc["metrics"]
    print(f"{a.draft}: {doc['pass_count']}/{doc['total']} checks pass")
    for k, v in doc["checks"].items():
        mark = "PASS" if v["pass"] else "FAIL"
        print(f"  {mark} {k:<22} {v['value']!s:>6} / {v['target']}")
    print("gaps: " + (", ".join(doc["gaps"]) or "none"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
