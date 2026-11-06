#!/usr/bin/env python3
"""roundtrip.py — F5: round-trip diff signal prototype (CPU, no model).

Signal: translate Sanskrit→English→Sanskrit requires a model (not here);
this prototype measures the DETERMINISTIC half: given (source, candidate,
back-translation), the back-translation's Sanskrit token overlap with the
source is a consistency signal (low overlap = drift somewhere in the loop).
Scores are signals, never verdicts; thresholds need the F2 calibration
treatment before any gate use.
Usage: python3 formal-trika/tools/roundtrip.py --src "snskrt..." --cand "eng..." --back "snskrt2..."
   or: python3 formal-trika/tools/roundtrip.py --demo
"""
import argparse
import re


def toks(s):
    return [w for w in re.split(r"\s+", (s or "").strip().lower()) if len(w) > 1]


def roundtrip_score(source, back):
    a, b = set(toks(source)), set(toks(back))
    if not a or not b:
        return {"overlap": 0.0, "note": "empty side"}
    return {"overlap": round(len(a & b) / len(a | b), 3),
            "src_tokens": len(a), "back_tokens": len(b),
            "note": "Jaccard over Sanskrit tokens; needs F2-style calibration"}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", default="")
    ap.add_argument("--cand", default="")
    ap.add_argument("--back", default="")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        src = "yad idaṃ vibhavātmakaṃ bhuvanajātaṃ garbhīkṛtānantavicitrabhoktṛbhogyaṃ"
        back_good = "yad idaṃ vibhavātmakaṃ bhuvanajātaṃ vicitrabhoktṛbhogyaṃ"
        back_bad = "rājā vanaṃ gataḥ siṃham apaśyat nadītaṭe sthitaḥ"
        print("good-loop:", roundtrip_score(src, back_good))
        print("bad-loop: ", roundtrip_score(src, back_bad))
        return 0
    print(roundtrip_score(a.src, a.back))


if __name__ == "__main__":
    raise SystemExit(main())
