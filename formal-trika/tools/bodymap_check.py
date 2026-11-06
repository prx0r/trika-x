#!/usr/bin/env python3
"""bodymap_check.py — E6: one body-map truth source (drift check).

SH1: the syllabus compiler's body layer points at matrika_body_map.json
v2 (verse-literal TĀ 15.117–120); the deitybody map is a DERIVATIVE, and
all copies must stay byte-identical. Any drift FAILS (one source, noted
provenance, never three truths).
Usage: python3 formal-trika/tools/bodymap_check.py
"""
import hashlib
from pathlib import Path

TRUTH = Path("/root/sanskrithelp/public/memory/data/matrika_body_map.json")
MIRRORS = [Path("/root/deitybody/data/matrika_body_map.json"),
           Path("/root/deitybody/site/data/matrika_body_map.json")]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    t = sha(TRUTH)
    print(f"truth {TRUTH}: sha256:{t[:16]}")
    bad = []
    for m in MIRRORS:
        h = sha(m)
        ok = h == t
        print(f"{'MIRROR-OK' if ok else 'DRIFT'} {m}: sha256:{h[:16]}")
        if not ok:
            bad.append(str(m))
    if bad:
        print("FAIL: body-map drift — restore mirrors from truth, never edit mirrors")
        return 1
    print("body-map: ONE truth, mirrors identical")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
