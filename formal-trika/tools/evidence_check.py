#!/usr/bin/env python3
"""evidence_check.py — every formal claim resolves to chunks (or says why not).

Checks: (1) every `^theorem` in positive Lean files has an EVIDENCE.json entry
or a named exemption; (2) every chunk locator resolves in its work's
passages.jsonl (reports immutable_id); (3) coverage = gold chunks with >=1
formal ref, plus the gap list (Treeka formal-column seed).
Usage: python3 tools/evidence_check.py [--root translation-work-path]
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
EV = json.loads((HERE / "EVIDENCE.json").read_text(encoding="utf-8"))
SOURCES = ["control/Mala.lean", "control/Pramatr.lean", "control/Kancuka.lean",
           "control/Recognition.lean", "control/AnswerKey.lean",
           "recognition/Transitions.lean", "recognition/NonEntail.lean",
           "recognition/Conjuncts.lean", "recognition/Memory.lean",
           "recognition/Tractatus.lean", "recognition/Coords.lean",
           "recognition/KancukaCorr.lean", "recognition/Grace.lean",
           "recognition/Upaya.lean"]
TW = Path(sys.argv[sys.argv.index("--root") + 1]
          if "--root" in sys.argv else "/root/translation-work")


def theorems():
    out = {}
    for f in SOURCES:
        text = (HERE / f).read_text(encoding="utf-8")
        for m in re.finditer(r"(?m)^theorem\s+([A-Za-z0-9_]+)", text):
            from os.path import basename as _bn
            out[m.group(1)] = _bn(f)
    return out


def ledgers():
    out = {}
    for work, spec in EV["works"].items():
        rows = {}
        p = TW / spec["ledger"].split("translation-work/")[-1]
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                rows[r.get("locator")] = r
        out[work] = rows
    return out


WORK_OF = {"tsa08": "tsa08", "tsa07": "tsa07", "param": "param", "phr": "phr",
           "vbt": "vbt", "spanda": "spanda", "span": "spanda"}


def work_of(locator):
    if locator in ("vbt",):
        return "vbt"
    for prefix, work in WORK_OF.items():
        if locator.startswith(prefix):
            return work
    return None


def main():
    thms = theorems()
    entries, exempt = EV["entries"], EV["exemptions"]
    problems = []
    for name, f in sorted(thms.items()):
        key = f"{f} :: {name}"
        if key not in entries and name not in exempt:
            problems.append(f"no evidence entry: {key}")
    for key in entries:
        if key.split(" :: ")[1] not in thms:
            problems.append(f"evidence without theorem: {key}")
    led = ledgers()
    locator_ok, locator_bad, covered = 0, [], set()
    for key, e in entries.items():
        for c in e.get("chunks", []):
            loc = c["locator"]
            w = work_of(loc)
            if w is None or loc == "vbt" and w == "vbt":
                pass
            if loc == "vbt":
                covered.add(("vbt", "*work-level*"))
                locator_ok += 1
                continue
            if w is None or loc not in led.get(w, {}):
                problems.append(f"unresolvable chunk {loc} (cited by {key})")
                locator_bad.append(loc)
            else:
                locator_ok += 1
                covered.add((w, loc))
    total, all_chunks = 0, []
    for work, rows in led.items():
        for loc, r in rows.items():
            total += 1
            all_chunks.append((work, loc))
    gaps = [c for c in all_chunks if c not in covered]
    print(f"theorems: {len(thms)}, entries: {len(entries)}, "
          f"exemptions: {len(exempt)}")
    print(f"chunk refs resolve: {locator_ok}, bad: {len(locator_bad)} {locator_bad}")
    print(f"coverage: {len(covered)}/{total} gold chunks "
          f"({100 * len(covered) // max(total, 1)}%)")
    print("covered:", sorted(f"{w}:{l}" for w, l in covered))
    print("gaps (Treeka formal-column seed):",
          sorted(f"{w}:{l}" for w, l in gaps))
    for p in problems:
        print("PROBLEM:", p)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
