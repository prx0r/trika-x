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
import os
import sys
from pathlib import Path

import bridge_resolve

HERE = Path(__file__).resolve().parent.parent
EV = json.loads((HERE / "EVIDENCE.json").read_text(encoding="utf-8"))
SOURCES = [str(f.relative_to(HERE)) for d in ("control", "recognition")
           for f in sorted((HERE / d).glob("*.lean")) if not f.name.startswith("Broken")]
TW = Path(sys.argv[sys.argv.index("--root") + 1]
          if "--root" in sys.argv else os.environ.get("TRANSLATION_WORK", HERE.parent.parent / "translation-work"))


def theorems():
    out = set()
    for f in SOURCES:
        text = (HERE / f).read_text(encoding="utf-8")
        for m in re.finditer(r"(?m)^theorem\s+([A-Za-z0-9_]+)", text):
            from os.path import basename as _bn
            key = f"{_bn(f)} :: {m.group(1)}"
            if key in out:
                raise ValueError(f"duplicate theorem: {key}")
            out.add(key)
    return out


def ledgers():
    out = {}
    for work, spec in EV["works"].items():
        rows = {}
        p = TW / spec["ledger"].split("translation-work/")[-1]
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                locator = r.get("locator")
                if not locator or locator in rows:
                    raise ValueError(f"missing or duplicate passage locator in {p}")
                rows[locator] = r
        if not rows:
            raise ValueError(f"empty passage ledger: {p}")
        out[work] = rows
    return out


WORK_OF = {"tsa08": "tsa08", "tsa07": "tsa07", "param": "param", "phr": "phr",
           "vbt": "vbt", "spanda": "spanda", "span": "spanda", "tal": "tal15",
           "tsa01": "tsa01", "tsa02": "tsa02", "tsa03": "tsa03",
           "tsa04": "tsa04", "tsa05": "tsa05", "tsa06": "tsa06",
           "tsa09": "tsa09", "tsa10": "tsa10", "tsa11": "tsa11",
           "tsa12": "tsa12", "tsa13": "tsa13", "tsa14": "tsa14",
           "tsa15": "tsa15", "tsa16": "tsa16", "tsa17": "tsa17",
           "tsa18": "tsa18", "tsa19": "tsa19", "tsa20": "tsa20",
           "tsa21": "tsa21", "tsa22": "tsa22"}


def work_of(locator):
    if locator in ("vbt",):
        return "vbt"
    for prefix, work in WORK_OF.items():
        if locator.startswith(prefix):
            return work
    return None


def main():
    snapshot = bridge_resolve.read_json(bridge_resolve.SNAPSHOT_PATH)
    bridge_resolve.inventory(snapshot, bridge_resolve.read_json(bridge_resolve.MAP_PATH), EV)
    bridge_resolve.verify_ledgers(TW, snapshot)
    thms = theorems()
    entries, exempt = EV["entries"], EV["exemptions"]
    problems = []
    for name, reason in exempt.items():
        matches = [key for key in thms if key.split(" :: ", 1)[1] == name]
        if len(matches) != 1 or not isinstance(reason, str) or not reason.strip():
            problems.append(f"exemption must identify one theorem and explain why: {name}")
    for key in sorted(thms):
        name = key.split(" :: ", 1)[1]
        if key not in entries and name not in exempt:
            problems.append(f"no evidence entry: {key}")
    for key in entries:
        if key not in thms:
            problems.append(f"evidence without theorem: {key}")
    led = ledgers()
    locator_ok, locator_bad, covered, work_refs = 0, [], set(), set()
    for key, e in entries.items():
        for c in e.get("chunks", []):
            loc = c["locator"]
            w = work_of(loc)
            if loc == "vbt":
                work_refs.add("vbt")
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
    print(f"direct registry references: {len(covered)}/{total} passage chunks "
          f"({100 * len(covered) // max(total, 1)}%)")
    print("work-level references (not passage coverage):", sorted(work_refs))
    print("Registry references are not independently verified source-to-theorem entailments.")
    print("covered:", sorted(f"{w}:{l}" for w, l in covered))
    print("gaps (Treeka formal-column seed):",
          sorted(f"{w}:{l}" for w, l in gaps))
    for p in problems:
        print("PROBLEM:", p)
    return 1 if problems else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, json.JSONDecodeError, ValueError, TypeError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
