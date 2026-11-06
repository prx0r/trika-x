#!/usr/bin/env python3
"""bodymap_check.py — compare body-map copies with a reference (drift check).

Byte identity establishes copy consistency, not that the reference correctly
represents any Sanskrit source or is appropriate for teaching.
Usage: python3 formal-trika/tools/bodymap_check.py
"""
import hashlib
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2].parent
SAN = Path(os.environ.get('SANSKRITHELP_CHECKOUT', ROOT / 'sanskrithelp'))
DB = Path(os.environ.get('DEITYBODY_CHECKOUT', ROOT / 'deitybody'))
TRUTH = SAN / 'public/memory/data/matrika_body_map.json'
MIRRORS = [DB / 'data/matrika_body_map.json', DB / 'site/data/matrika_body_map.json']


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    t = sha(TRUTH)
    print(f"reference {TRUTH}: sha256:{t[:16]}")
    bad = []
    for m in MIRRORS:
        h = sha(m)
        ok = h == t
        print(f"{'MIRROR-OK' if ok else 'DRIFT'} {m}: sha256:{h[:16]}")
        if not ok:
            bad.append(str(m))
    if bad:
        print("FAIL: body-map copies differ from the reference")
        return 1
    print("body-map: reference and mirrors identical; textual accuracy not checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
