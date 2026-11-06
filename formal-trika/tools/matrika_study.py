#!/usr/bin/env python3
"""matrika_study.py — mātṛkā study cards (learn Sanskrit through the body).

Joins (read-only) deitybody phonemes.json (50 records: mātṛkā/mālinī loci,
clips, phonetic class) into study cards: phoneme × loci × clip × class.
Each card is a study record, not an instruction for bodily installation.
trika_link (tattva mapping) is LEFT NULL with needs_scholar flag — the
candidate loci and tattva-letter doctrine require source review.
Usage: python3 formal-trika/tools/matrika_study.py [--out cards.json]
"""
import argparse
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PHONEMES = Path(os.environ.get('DEITYBODY_CHECKOUT', ROOT.parent.parent / 'deitybody')) / 'site/data/phonemes.json'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--phonemes', type=Path, default=PHONEMES)
    ap.add_argument("--out", type=Path,
                    default=ROOT / 'data/matrika-study.json')
    a = ap.parse_args()
    d = json.loads(a.phonemes.read_text(encoding="utf-8"))
    if not isinstance(d.get('phonemes'), list) or not d['phonemes']:
        raise ValueError('phoneme source is missing or empty')
    cards = []
    for p in d.get("phonemes", []):
        cards.append({
            "phoneme": p.get("iast"), "dev": p.get("dev"),
            "matrika_locus": (p.get("matrika") or {}).get("locus"),
            "malini_locus": (p.get("malini") or {}).get("locus"),
            "clip": p.get("clip"),
            "audio_verified": (p.get("audio") or {}).get("verified", False),
            "class": (p.get("phonetic") or {}).get("class"),
            "study": "compare phoneme, audio and candidate loci; source review required",
            "trika_link": None,
            "needs_scholar": "loci, sequence and any tattva-letter mapping need textual and scholar review",
        })
    doc = {"format": "matrika-study/1",
           "sources": ["deitybody phonemes.json (candidate loci and clips; independent body map not checked)"],
           "cards": cards}
    a.out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    unverified = sum(1 for c in cards if not c["audio_verified"])
    print(f"cards: {len(cards)} (audio unverified: {unverified}) -> {a.out}")


if __name__ == "__main__":
    raise SystemExit(main())
