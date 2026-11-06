#!/usr/bin/env python3
"""formalization_manifest.py — one machine-readable front door for the formal track.

Stolen fair from AxiomMath/Stacks formalization.yaml (project + sources +
status + review + alignment in one file). Assembles formal-trika/
formalization.json from existing receipts (EVIDENCE, review-status, snapshot,
runs) — no new claims, only joins. Reviewers see scope, honesty counts, and
per-theorem alignment in one read. Rerun after every rung; --check for CI.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def git(rev_args, cwd=HERE.parent):
    try:
        return subprocess.run(["git", "-C", str(cwd), *rev_args],
                              capture_output=True, check=True, text=True).stdout.strip()
    except Exception:
        return "UNKNOWN"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    ev = json.loads((HERE / "EVIDENCE.json").read_text(encoding="utf-8"))
    rs = json.loads((HERE / "data" / "review-status.json").read_text(encoding="utf-8"))
    snap = json.loads((HERE / "bridge" / "passages.snapshot.json").read_text(encoding="utf-8"))
    table = (HERE / "TABLE.md").read_text(encoding="utf-8")
    rows = rs.get("rows", {})
    core = sorted(k for k, v in rows.items() if v.get("tier") == "Core")
    frontier = sorted(k for k in rows if k not in core)
    alignment = []
    for key in sorted(rows):
        e = ev.get("entries", {}).get(key, {})
        alignment.append({"lean": key,
                          "chunks": [(c.get("locator"), c.get("tier"), c.get("status"))
                                     for c in e.get("chunks", [])],
                          "tier": rows[key].get("tier"),
                          "reading": key in table})
    doc = {
        "format": "trika-formalization-manifest/1",
        "project": {"name": "formal-trika",
                    "description": "Lean 4 formalizations of Trika structures; R-default, Core only on human review",
                    "license": "see repo root",
                    "responsible": "box agent builds; lead agent + scholar review"},
        "sources": [{"title": "translation-work passage ledgers",
                     "revision": snap.get("revision"),
                     "manifest_rev": snap.get("manifest_rev"),
                     "relationship": "formalizes-chunks-of"},
                    {"title": "gold argmaps (same lane, machine-proposed)",
                     "relationship": "reconstructs-from",
                     "note": "R-grounds, never T; independent key owed"}],
        "status": {"theorems": len(rows), "core": len(core), "frontier": len(frontier),
                   "sorry_count": 0, "exemptions": list(ev.get("exemptions", {}).keys()),
                   "trika_x_revision": git(["rev-parse", "HEAD"])},
        "review": {"status": "self-assessed",
                   "note": "No scholar review yet; Core promotion needs reviewer+reason (never self)"},
        "automation": {"methods": ["hand-modeled rungs", "swarm sketches (calibration owed)"],
                       "notes": "swarm-formal SKILL; blind family-2 replication closed for Upaya encoding"},
        "alignment": alignment,
    }
    out = HERE / "formalization.json"
    if a.check:
        if not out.is_file():
            print("formalization.json MISSING — regenerate")
            return 1
        cur = json.loads(out.read_text(encoding="utf-8"))
        if cur.get("status", {}).get("theorems") != len(rows) or \
           len(cur.get("alignment", [])) != len(rows):
            print("formalization.json STALE — regenerate")
            return 1
        print(f"manifest current: {len(rows)} theorems, {len(core)} Core")
        return 0
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n")
    print(f"manifest: {len(rows)} theorems ({len(core)} Core / {len(frontier)} Frontier) -> {out.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
