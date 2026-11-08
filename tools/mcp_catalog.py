#!/usr/bin/env python3
"""mcp_catalog.py — probe the federation gateway and freeze its tool catalog.

Docs drift when tool names change. This tool makes the catalog executable:
it starts the gateway exactly as an agent would, asks tools/list, and writes
`formal-trika/data/mcp-catalog.json`. `--check` fails when the live catalog
no longer matches the recorded one.

  python3 tools/mcp_catalog.py --write    # capture
  python3 tools/mcp_catalog.py --check    # drift gate (exit 1)
  python3 tools/mcp_catalog.py            # print summary

A child that is down is excluded by FailOpen, so a --check against a box with
missing children reports drift by design: the catalog describes the full
5-child federation, not a degraded one.
"""
from __future__ import annotations

import argparse
import json
import os
import select
import subprocess
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
GATEWAY = REPO / "formal-trika" / "tools" / "federation_gateway.py"
CATALOG = REPO / "formal-trika" / "data" / "mcp-catalog.json"
BANNED_EXACT = {"ship", "render", "seal", "publish", "send", "spend",
                "post", "isbn", "isbn_issue", "grant_rights", "signoff",
                "submit"}
BANNED_PREFIX = tuple(b + "_" for b in BANNED_EXACT) + tuple(
    b + "-" for b in BANNED_EXACT)


def banned_hit(name: str) -> str | None:
    """Exact/prefix match on the bare tool name — never substring.

    `list_published_essays` is a read-only list and `vf_publish` is the
    factory's own gated tool; neither is the banned *action* `publish`.
    Substring scans produced false positives here before (and once flagged
    'relationships' for 'ship')."""
    base = name.split("__")[-1]
    if base in BANNED_EXACT:
        return base
    for p in BANNED_PREFIX:
        if base.startswith(p):
            return p.rstrip("_-")
    return None


def start_gateway() -> subprocess.Popen:
    return subprocess.Popen(
        [sys.executable, str(GATEWAY)], cwd=REPO, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        bufsize=1, env=dict(os.environ))


def rpc(proc, method: str, params=None, timeout: int = 120, seq=[0]):
    seq[0] += 1
    proc.stdin.write(json.dumps({"jsonrpc": "2.0", "id": seq[0],
                                 "method": method,
                                 "params": params or {}}) + "\n")
    proc.stdin.flush()
    t0 = time.time()
    while time.time() - t0 < timeout:
        r, _, _ = select.select([proc.stdout], [], [], 1)
        if not r:
            continue
        line = proc.stdout.readline()
        if not line:
            err = ""
            try:
                err = proc.stderr.read()[:400]
            except Exception:  # noqa: BLE001
                pass
            raise RuntimeError(f"gateway closed stdout: {err}")
        try:
            msg = json.loads(line)
        except ValueError:
            continue
        if msg.get("id") == seq[0]:
            return msg
    raise TimeoutError(method)


def probe() -> dict:
    proc = start_gateway()
    try:
        init = rpc(proc, "initialize")["result"]["serverInfo"]
        tools = rpc(proc, "tools/list")["result"]["tools"]
    finally:
        proc.kill()
    entries = []
    for t in sorted(tools, key=lambda x: x["name"]):
        name = t["name"]
        entries.append({
            "name": name,
            "family": name.split("__")[0],
            "description": (t.get("description") or "")[:160],
            "required": (t.get("inputSchema") or {}).get("required", []),
        })
    fam = Counter(e["family"] for e in entries)
    banned_hits = [e["name"] for e in entries if banned_hit(e["name"])]
    return {
        "format": "trika-mcp-catalog/1",
        "generated_at": datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"),
        "gateway": init,
        "count": len(entries),
        "families": dict(sorted(fam.items())),
        "banned_hits": banned_hits,
        "tools": entries,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--write", action="store_true")
    g.add_argument("--check", action="store_true")
    a = ap.parse_args()

    live = probe()

    if a.write:
        CATALOG.parent.mkdir(parents=True, exist_ok=True)
        CATALOG.write_text(json.dumps(live, indent=1) + "\n")
        print(f"mcp_catalog: wrote {CATALOG}")
        print(f"  {live['count']} tools: {live['families']}")
        if live["banned_hits"]:
            print(f"  BANNED SURFACE: {live['banned_hits']}", file=sys.stderr)
            return 1
        return 0

    if a.check:
        if not CATALOG.exists():
            print("mcp_catalog: no catalog — run --write first", file=sys.stderr)
            return 1
        old = json.loads(CATALOG.read_text())
        drift = []
        if old.get("count") != live["count"]:
            drift.append(f"count {old.get('count')} -> {live['count']}")
        if old.get("families") != live["families"]:
            drift.append(f"families {old.get('families')} -> "
                         f"{live['families']}")
        old_names = {t["name"] for t in old.get("tools", [])}
        live_names = {t["name"] for t in live["tools"]}
        added = sorted(live_names - old_names)
        removed = sorted(old_names - live_names)
        if added:
            drift.append(f"added: {added}")
        if removed:
            drift.append(f"removed: {removed}")
        if live["banned_hits"]:
            drift.append(f"banned surface: {live['banned_hits']}")
        if drift:
            print("mcp_catalog: DRIFT", file=sys.stderr)
            for d in drift:
                print("  " + d, file=sys.stderr)
            return 1
        print(f"mcp_catalog: SHARP ({live['count']} tools, "
              f"{len(live['families'])} families)")
        return 0

    print(json.dumps({"count": live["count"],
                      "families": live["families"],
                      "banned_hits": live["banned_hits"]}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
