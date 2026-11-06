#!/usr/bin/env python3
"""bridge_resolve.py — chunk:WORK-LOCATOR -> openpatala work record + edition.

Read-only. Resolves our chunk ids (tsa08-p03 etc.) to the mapped openpatala
work key/id and our pinned edition/source record. Witness-level IDs are
UNPINNED until their resolver runs — the output says so, never a blank.
Usage: python3 tools/bridge_resolve.py chunk:tsa08-p03 | --check
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
MAP = json.loads((HERE / "bridge" / "openpatala-map.json").read_text(encoding="utf-8"))

PREFIX = {"tsa08": "tsa08", "tsa07": "tsa07", "param": "param", "phr": "phr",
          "vbt": "vbt", "span": "spanda"}


def work_of(locator):
    for prefix, work in PREFIX.items():
        if locator == "vbt" or locator.startswith(prefix):
            return work
    return None


def resolve(chunk_ref):
    loc = chunk_ref.split(":", 1)[1] if ":" in chunk_ref else chunk_ref
    if loc == "vbt":
        return {"locator": loc, "work": "vbt",
                "record": MAP["works"]["vbt"], "note": "work-level ref"}
    w = work_of(loc)
    if w is None or w not in MAP["works"]:
        return {"error": f"unknown locator {loc!r}"}
    return {"locator": loc, "work": w, "record": MAP["works"][w]}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--check" in sys.argv:
        bad = 0
        for work, spec in MAP["works"].items():
            for field in ("ours", "openpatala_work_key", "edition", "status"):
                if not spec.get(field):
                    print(f"PROBLEM: {work} missing {field}")
                    bad += 1
        unw = [w for w, s in MAP["works"].items()
               if s.get("witness", "UNPINNED") != "UNPINNED"]
        print(f"works mapped: {len(MAP['works'])}, "
              f"witness-resolved: {len(unw)} (rest UNPINNED by design)")
        return 1 if bad else 0
    if not args:
        print(__doc__)
        return 1
    print(json.dumps(resolve(args[0]), ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
