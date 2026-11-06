#!/usr/bin/env python3
"""kappa.py — inter-rater agreement for T-C2 (SOTA per LREC-2026 James guide).

Preregistered T-C2 rule (PREREGISTRATION-DECODE-RUNG.md) is RAW agreement
≥ 0.6 on the 12-clause rater sheet — that threshold is authoritative and
unchanged. This tool reports raw agreement PLUS Cohen's κ (chance
corrected, the standard for 2 raters × nominal categories; cf. Cohen
1960; Fleiss κ only if a third rater joins; weighted κ only for ordinal
scales — our upaya tags are nominal, so unweighted κ).

Usage:
  python3 tools/kappa.py rater1.json rater2.json
Files: JSON lists of 12 tags each (order = sheet order), or CSV with a
`tag` column. Prints raw agreement, κ, expected agreement, per-category
matches, and the verbatim disagreement list (disagreements are the
finding if we fail — sheet rule).

κ interpretation (report, never re-threshold): <0 none, 0–0.2 slight,
0.2–0.4 fair, 0.4–0.6 moderate, 0.6–0.8 substantial, 0.8–1 almost
perfect. With 12 items CIs are wide — report the numbers, not adjectives.
"""
import csv
import json
import sys
from collections import Counter


def load(path):
    text = open(path, encoding="utf-8").read()
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return [str(x) for x in data]
        raise ValueError("JSON must be a list of tags")
    except json.JSONDecodeError:
        pass
    with open(path, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows or "tag" not in rows[0]:
        raise ValueError("CSV needs a `tag` column")
    return [str(r["tag"]).strip() for r in rows]


def cohen_kappa(a, b):
    if len(a) != len(b) or not a:
        raise ValueError("raters need equal nonzero item counts")
    n = len(a)
    agree = sum(1 for x, y in zip(a, b) if x == y)
    po = agree / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb.get(k, 0) for k in ca) / (n * n)
    kappa = (po - pe) / (1 - pe) if pe != 1 else 1.0
    return {"n": n, "agree": agree, "raw": po,
            "expected": pe, "kappa": kappa}


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    a, b = load(sys.argv[1]), load(sys.argv[2])
    r = cohen_kappa(a, b)
    print(f"items: {r['n']}, matches: {r['agree']}")
    print(f"raw agreement: {r['raw']:.3f} (T-C2 threshold ≥ 0.600, authoritative)")
    print(f"expected (chance): {r['expected']:.3f}")
    print(f"Cohen κ: {r['kappa']:.3f} (reported alongside, never re-thresholds)")
    print(f"T-C2 verdict: {'HOLDS' if r['raw'] >= 0.6 else 'REWRITE/PARK per kill rule'}")
    cats = sorted(set(a) | set(b))
    for c in cats:
        tot = sum(1 for x, y in zip(a, b) if x == c or y == c)
        hit = sum(1 for x, y in zip(a, b) if x == c == y)
        print(f"  {c}: {hit}/{tot} agreed-when-involved")
    bad = [(i + 1, x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y]
    if bad:
        print("disagreements (verbatim finding if we fail):")
        for i, x, y in bad:
            print(f"  clause {i}: rater1={x} rater2={y}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
