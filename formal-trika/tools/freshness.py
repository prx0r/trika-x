#!/usr/bin/env python3
"""freshness.py — one ledger of every canonical number + how to reproduce it.

The rule this enforces: a number without a source hash and a command is not
evidence. Every metric here records value + the command that produced it +
the sha256 of the file it came from where one exists.

  python3 formal-trika/tools/freshness.py            # print live state
  python3 formal-trika/tools/freshness.py --write    # capture into ledger
  python3 formal-trika/tools/freshness.py --check    # drift gate (exit 1)

The ledger is `formal-trika/data/freshness.json`. `--check` compares live
metric values against the recorded ones (git rev/dirty and measured_at are
excluded — they are context, not claims). A drifted metric is a stale number,
and stale numbers are exactly what this project refuses to publish.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent            # formal-trika/tools
REPO = HERE.parent.parent                          # trika-x
SVREAD = Path(os.environ.get("SVREAD_CHECKOUT", "/root/svread"))
OPENPATALA = Path(os.environ.get("OPENPATALA_CHECKOUT", "/root/openpatala"))
TW = Path(os.environ.get("TW_CHECKOUT", "/root/translation-work"))
LEDGER = REPO / "formal-trika" / "data" / "freshness.json"
DSN = os.environ.get(
    "OPENPATALA_DSN",
    "dbname=openpatala user=patala password=patala host=127.0.0.1",
)


def sha256_file(p: Path) -> str | None:
    try:
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return None


def git(*args: str, cwd: Path = REPO) -> str:
    try:
        return subprocess.run(["git", *args], cwd=cwd, capture_output=True,
                              text=True, timeout=30).stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return ""


def run(argv: list[str], cwd: Path = REPO) -> str:
    try:
        return subprocess.run(argv, cwd=cwd, capture_output=True, text=True,
                              timeout=300,
                              env={**os.environ, "PYTHONPATH": str(cwd)}
                              ).stdout + subprocess.run(
            argv, cwd=cwd, capture_output=True, text=True, timeout=300,
            env={**os.environ, "PYTHONPATH": str(cwd)}).stderr
    except (OSError, subprocess.TimeoutExpired) as e:
        return f"ERROR {e}"


def metric(value, command: str, source_sha256: str | None = None):
    m = {"value": value, "command": command}
    if source_sha256:
        m["source_sha256"] = source_sha256
    return m


def openpatala_db() -> dict:
    cmd = ("psql -d openpatala -t -c 'SELECT count(*) FROM works/passages/"
           "editions/etexts/assertions/translations/people/witnesses'")
    try:
        import psycopg2  # type: ignore
        c = psycopg2.connect(DSN, connect_timeout=5)
        cur = c.cursor()
        tables = ["works", "passages", "editions", "etexts", "assertions",
                  "translations", "people", "witnesses"]
        counts = {}
        for t in tables:
            cur.execute(f"SELECT count(*) FROM {t}")
            counts[t] = cur.fetchone()[0]
        c.close()
        fp = hashlib.sha256(
            json.dumps(counts, sort_keys=True).encode()).hexdigest()
        return metric(counts, cmd, fp)
    except Exception as e:  # noqa: BLE001 — BLOCKED, never faked
        return metric({"status": "BLOCKED", "reason": str(e)[:120]}, cmd)


def parse_evidence() -> dict:
    out = run([sys.executable, "formal-trika/tools/evidence_check.py"])
    vals = {}
    for key, pat in {
        "theorems": r"theorems:\s*(\d+)",
        "entries": r"entries:\s*(\d+)",
        "exemptions": r"exemptions:\s*(\d+)",
        "chunk_refs_resolve": r"chunk refs resolve:\s*(\d+)",
        "chunk_refs_bad": r"bad:\s*(\d+)",
        "direct_refs": r"direct registry references:\s*(\d+)",
        "total_chunks": r"direct registry references:\s*\d+/(\d+)",
    }.items():
        m = re.search(pat, out)
        if m:
            vals[key] = int(m.group(1))
    vals["status"] = "MEASURED" if "theorems:" in out else "BLOCKED"
    return vals


def parse_bridge() -> dict:
    out = run([sys.executable, "formal-trika/tools/bridge_resolve.py",
               "--check", "--tw", str(TW)])
    vals = {"status": "MEASURED"}
    m = re.search(r"(\d+) works,\s*(\d+) passage IDs", out)
    if m:
        vals["works"] = int(m.group(1))
        vals["passage_ids"] = int(m.group(2))
    else:
        vals["status"] = "BLOCKED"
    vals["witnesses"] = "UNPINNED" if "UNPINNED" in out else "UNKNOWN"
    return vals


def svread_traces() -> dict:
    idx = SVREAD / "data" / "traces" / "index.json"
    try:
        d = json.load(open(idx))
        entries = d.get("entries", d if isinstance(d, list) else [])
        return metric(len(entries),
                      "cat /root/svread/data/traces/index.json",
                      sha256_file(idx))
    except Exception as e:  # noqa: BLE001
        return metric({"status": "BLOCKED", "reason": str(e)[:120]},
                      "cat /root/svread/data/traces/index.json")


def trika_traces() -> dict:
    idx = REPO / "formal-trika" / "data" / "traces" / "index.json"
    try:
        d = json.load(open(idx))
        return metric({"count": d.get("count"),
                       "verdicts": d.get("verdicts", {}),
                       "errors": len(d.get("errors", []))},
                      "python3 formal-trika/tools/trace_all.py --index-only",
                      sha256_file(idx))
    except Exception as e:  # noqa: BLE001
        return metric({"status": "BLOCKED", "reason": str(e)[:120]},
                      "python3 formal-trika/tools/trace_all.py --index-only")


def trika_essays() -> dict:
    import subprocess
    cmd = [__import__("sys").executable,
           str(HERE / "formal-trika" / "tools" / "essay_derive.py"), "--json"]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True,
                             timeout=120, cwd=REPO).stdout
        d = json.loads(out)
        return metric({"count": d.get("count"),
                       "verdicts": d.get("verdicts", {})},
                      "python3 formal-trika/tools/essay_derive.py --json")
    except Exception as e:  # noqa: BLE001
        return metric({"status": "BLOCKED", "reason": str(e)[:120]},
                      "python3 formal-trika/tools/essay_derive.py --json")


def svread_source_map() -> dict:
    p = SVREAD / "source-map.json"
    try:
        d = json.load(open(p))
        works = d.get("works", {})
        bridged = [k for k, v in works.items()
                   if v.get("openpatala_work_id") not in ("UNRESOLVED", None)]
        val = {"total": len(works), "bridged": len(bridged),
               "todo": len(works) - len(bridged)}
        return metric(val, "cat /root/svread/source-map.json", sha256_file(p))
    except Exception as e:  # noqa: BLE001
        return metric({"status": "BLOCKED", "reason": str(e)[:120]},
                      "cat /root/svread/source-map.json")


def svread_surface() -> dict:
    proj = len(list((SVREAD / "data" / "scholar").glob("*.json")))
    man = SVREAD / "data" / "release-manifest.json"
    assets = None
    try:
        d = json.load(open(man))
        assets = len(d.get("assets", d)) if isinstance(d, (dict, list)) else None
    except Exception:  # noqa: BLE001
        pass
    return metric(
        {"scholar_projections": proj, "manifest_assets": assets},
        "ls /root/svread/data/scholar/*.json; jq assets "
        "/root/svread/data/release-manifest.json",
        sha256_file(man),
    )


def disk() -> dict:
    try:
        u = shutil.disk_usage("/")
        return metric({"free_gb": round(u.free / 1e9, 2),
                       "used_pct": round(100 * u.used / u.total, 1)},
                      "df -h /")
    except OSError as e:  # noqa: BLE001
        return metric({"status": "BLOCKED", "reason": str(e)[:120]}, "df -h /")


def gather() -> dict:
    def git_state(p: Path):
        return {
            "rev": git("rev-parse", "--short", "HEAD", cwd=p),
            "branch": git("rev-parse", "--abbrev-ref", "HEAD", cwd=p),
            "dirty": len([l for l in git("status", "--porcelain",
                                         cwd=p).splitlines() if l.strip()]),
        }

    return {
        "measured_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "git": {"trika-x": git_state(REPO),
                "openpatala": git_state(OPENPATALA),
                "svread": git_state(SVREAD)},
        "disk": disk(),
        "openpatala_db": openpatala_db(),
        "formal_evidence": metric(
            parse_evidence(),
            "python3 formal-trika/tools/evidence_check.py"),
        "bridge": metric(parse_bridge(),
                         "python3 formal-trika/tools/bridge_resolve.py --check "
                         f"--tw {TW}"),
        "trika_traces": trika_traces(),
        "trika_essays": trika_essays(),
        "svread_traces": svread_traces(),
        "svread_source_map": svread_source_map(),
        "svread_surface": svread_surface(),
    }


def stable(d: dict) -> dict:
    """Metric values only — context (timestamps, revs, dirt, free disk) is not
    a claim. Disk is environment, not data; it is reported but never gates."""
    skip = {"measured_at", "git", "disk"}
    out = {}
    for k, v in d.items():
        if k in skip:
            continue
        out[k] = v["value"] if isinstance(v, dict) and "value" in v else v
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--write", action="store_true", help="capture ledger")
    g.add_argument("--check", action="store_true", help="fail on drift")
    a = ap.parse_args()

    live = gather()

    if a.write:
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        LEDGER.write_text(json.dumps(live, indent=1) + "\n")
        print(f"freshness: wrote {LEDGER}")
        print(json.dumps(stable(live), indent=1))
        return 0

    if a.check:
        if not LEDGER.exists():
            print("freshness: no ledger — run --write first", file=sys.stderr)
            return 1
        old = json.loads(LEDGER.read_text())
        before, after = stable(old), stable(live)
        drift = [k for k in sorted(set(before) | set(after))
                 if before.get(k) != after.get(k)]
        if drift:
            print("freshness: DRIFT", file=sys.stderr)
            for k in drift:
                print(f"  {k}:\n    was: {before.get(k)}\n    now: "
                      f"{after.get(k)}", file=sys.stderr)
            return 1
        print("freshness: SHARP (all recorded numbers reproduce)")
        return 0

    print(json.dumps(live, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
