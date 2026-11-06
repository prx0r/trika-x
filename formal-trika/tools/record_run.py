#!/usr/bin/env python3
"""record_run.py — append one machine-written line per harness to runs/runs.jsonl.

Captures: time, git rev, Lean version, per-harness pass/fail. The runs ledger
(INDEX.md) stays hand-written verdicts; this file is the machine receipt the
verdicts cite. Nothing here judges — it records.
Usage: python3 tools/record_run.py [--rev REV] (defaults to git HEAD)
"""
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "runs" / "runs.jsonl"


def sh(*args, cwd=None):
    r = subprocess.run(args, cwd=str(cwd or ROOT), capture_output=True,
                       text=True, timeout=600)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def main():
    rev = sys.argv[sys.argv.index("--rev") + 1] if "--rev" in sys.argv else None
    if not rev:
        code, out = sh("git", "rev-parse", "--short", "HEAD")
        rev = out.strip() if code == 0 else "unknown"
    code, out = sh("lean", "--version")
    lean = out.strip().split("\n")[0] if code == 0 else "missing"
    harnesses = {}
    for d in ("control", "recognition"):
        script = ROOT / d / "run.sh"
        code, out = sh("bash", str(script), cwd=ROOT / d)
        tail = [l for l in out.splitlines()
                if l.startswith("==") or l.startswith("PASS") or l.startswith("FAIL")]
        harnesses[d] = {"exit": code, "tail": tail[-8:]}
    code, out = sh("python3", str(ROOT / "tools" / "tc1_cooccurrence.py"))
    harnesses["tc1"] = {"exit": code,
                        "tail": [l for l in out.splitlines() if l][-2:]}
    rec = {"at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "rev": rev, "lean": lean, "harnesses": harnesses}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    bad = [k for k, v in harnesses.items() if v["exit"] != 0]
    print(f"recorded {rev} ({'FAIL: ' + ','.join(bad) if bad else 'all green'})")
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
