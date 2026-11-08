#!/usr/bin/env python3
"""essay_derive.py — the northstar gate: is every essay derivable to Sanskrit?

For each compiled essay (formal-trika/swarm/*.essay.json) the chain is:

  essay claim (verse_id + tier)
    -> chunk locator (essay.chunk)
    -> trace bundle (data/traces) : verdict, source bytes, identity
    -> EVIDENCE registry (essay.theorems)
    -> openpatala block (essay.openpatala)

Verdicts: DERIVED (chain green end to end) / PARTIAL (chain intact but a hop
is CANDIDATE/UNVERIFIED/PARTIAL) / BROKEN (a hop is missing). Nothing here
promotes: UNVERIFIED theorems, CANDIDATE mappings and PARTIAL traces stay
exactly what they are — the report just names them.

  python3 formal-trika/tools/essay_derive.py                # full report
  python3 formal-trika/tools/essay_derive.py --json          # counts + rows
  python3 formal-trika/tools/essay_derive.py --swarm DIR     # other essay dir

Rule: no essay ships a claim its chain cannot produce.
"""
from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
TRACES = HERE / "data" / "traces" / "index.json"
EVIDENCE = HERE / "EVIDENCE.json"
SWARM = HERE / "swarm"


def load_traces() -> dict:
    try:
        d = json.loads(TRACES.read_text(encoding="utf-8"))
        out = {}
        for e in d.get("entries", []):
            out[(e.get("work"), e.get("target"))] = e
        return out
    except OSError:
        return {}


def load_evidence() -> dict:
    try:
        return json.loads(EVIDENCE.read_text(encoding="utf-8")).get(
            "entries", {})
    except OSError:
        return {}


def audit_essay(path: Path, traces: dict, evidence: dict) -> dict:
    d = json.loads(path.read_text(encoding="utf-8"))
    problems: list[str] = []
    notes: list[str] = []
    chunk = d.get("chunk", "")
    work, _, target = chunk.partition(":")
    if not work or not target:
        problems.append("no chunk locator")
        return {"essay": path.stem, "chunk": chunk, "verdict": "BROKEN",
                "problems": problems, "notes": notes}

    entry = traces.get((work, target))
    if not entry:
        problems.append(f"no trace bundle for {chunk}")
    else:
        if entry.get("verdict") != "COMPLETE":
            notes.append(f"trace {entry.get('verdict')}: "
                         + "; ".join(entry.get("gaps", [])[:3]))
        bundle_p = HERE / "data" / entry.get("file", "")
        try:
            b = json.loads(bundle_p.read_text(encoding="utf-8"))
            src = b.get("source", {}) or {}
            if not src.get("bytes_present"):
                problems.append("trace has no source bytes")
            ident = b.get("identity", {}) or {}
            if ident.get("status") not in ("BOUND",):
                notes.append(f"identity {ident.get('status')}")
            wit = (b.get("source", {}) or {}).get("witness", {})
            if isinstance(wit, dict) and wit.get("status") != "VERIFIED":
                notes.append("witness UNPINNED (no primary-source claim)")
        except OSError:
            problems.append("trace bundle file unreadable")

    for cl in d.get("claims", []) or []:
        if not cl.get("verse_id"):
            problems.append(f"claim {cl.get('id')} has no verse_id")
        if cl.get("tier") not in ("R", "T", "E", "C", "H", "X"):
            problems.append(f"claim {cl.get('id')} bad tier")
        if cl.get("tier") == "T":
            notes.append(f"claim {cl.get('id')} asserts T (span-verified "
                         "bind required downstream)")

    for th in d.get("theorems", []) or []:
        name = th.get("name", "")
        if name not in evidence:
            problems.append(f"theorem {name} has no EVIDENCE entry")
        if th.get("tier") == "UNVERIFIED":
            notes.append(f"theorem {name} UNVERIFIED (registry ref only)")

    op = d.get("openpatala")
    if not isinstance(op, dict) or not op:
        problems.append("no openpatala block")
    elif not op.get("openpatala_work_id"):
        notes.append("openpatala UNMAPPED: "
                     + str(op.get("note") or "no resolvable work id"))
    elif op.get("mapping_status") != "RESOLVED":
        notes.append(f"openpatala mapping {op.get('mapping_status')}")

    verdict = "BROKEN" if problems else ("PARTIAL" if notes else "DERIVED")
    # PR #7 R3: distance-to-DERIVED — the exact hops blocking a green chain.
    blocking = (["BROKEN: " + p for p in problems]
                + ["OPEN: " + n for n in notes])
    return {"essay": path.stem, "chunk": chunk, "verdict": verdict,
            "claims": len(d.get("claims", []) or []),
            "distance_to_derived": len(blocking),
            "blocking": blocking[:10],
            "problems": problems, "notes": notes[:6]}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--swarm", default=str(SWARM))
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    traces, evidence = load_traces(), load_evidence()
    paths = sorted(glob.glob(str(Path(a.swarm) / "*.essay.json")))
    rows = [audit_essay(Path(p), traces, evidence) for p in paths]
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1

    if a.json:
        print(json.dumps({"count": len(rows), "verdicts": counts,
                          "rows": rows}, indent=1))
        return 0 if not any(r["verdict"] == "BROKEN" for r in rows) else 1

    print(f"essay_derive: {len(rows)} essays; "
          + " ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    for r in rows:
        if r["verdict"] == "DERIVED":
            continue
        print(f"  [{r['verdict']}] {r['essay']} ({r['chunk']})")
        for p in r["problems"]:
            print(f"    BROKEN: {p}")
        for n in r["notes"][:4]:
            print(f"    note: {n}")
    return 0 if counts.get("BROKEN", 0) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
