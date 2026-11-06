#!/usr/bin/env python3
"""matrika_study.py — mātṛkā study cards (learn Sanskrit through the body).

Joins (read-only) deitybody phonemes.json (50 records: mātṛkā/mālinī loci,
clips, phonetic class) into study cards: phoneme × loci × clip × class.
Each card is a touch-first study unit (Night-1 rule: sound + articulation
+ touch + locus FIRST, visualization later). trika_link (tattva mapping)
is LEFT NULL with needs_scholar flag — tattva-letter doctrine is NOT
inferred here (cf. third-party comparison tables, rights-reserved).
Usage: python3 formal-trika/tools/matrika_study.py [--out cards.json]
"""
import argparse
import json
from pathlib import Path

PHONEMES = Path("/root/deitybody/site/data/phonemes.json")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path,
                    default=Path("/root/trika-x/formal-trika/data/matrika-study.json"))
    a = ap.parse_args()
    d = json.loads(PHONEMES.read_text(encoding="utf-8"))
    cards = []
    for p in d.get("phonemes", []):
        cards.append({
            "phoneme": p.get("iast"), "dev": p.get("dev"),
            "matrika_locus": (p.get("matrika") or {}).get("locus"),
            "malini_locus": (p.get("malini") or {}).get("locus"),
            "clip": p.get("clip"),
            "audio_verified": (p.get("audio") or {}).get("verified", False),
            "class": (p.get("phonetic") or {}).get("class"),
            "study": "touch-first: sound + articulation + touch + locus; glyph later",
            "trika_link": None,
            "needs_scholar": "tattva-letter mapping needs scholar review (comparison tables exist, rights-reserved)",
        })
    doc = {"format": "matrika-study/1",
           "sources": ["deitybody phonemes.json (loci+clips)", "matrika_body_map v2 (truth)"],
           "cards": cards}
    a.out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    unverified = sum(1 for c in cards if not c["audio_verified"])
    print(f"cards: {len(cards)} (audio unverified: {unverified}) -> {a.out}")


if __name__ == "__main__":
    raise SystemExit(main())
