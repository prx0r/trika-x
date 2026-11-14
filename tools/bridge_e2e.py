#!/usr/bin/env python3
"""bridge_e2e.py — end-to-end proof that the ChatGPT front door serves real work.

Not a unit test with fakes: starts the HTTP bridge, drives MCP over HTTP, and
asks the real federation for real passages and real Lean traces. Every check
prints PASS/FAIL with the observed value; exit 0 only if all pass.

  python3 tools/bridge_e2e.py                 # default probe set
  python3 tools/bridge_e2e.py --json          # machine-readable report
  python3 tools/bridge_e2e.py --work bodhapancadasika --target bod-p01-v01
"""
from __future__ import annotations

import argparse
import json
import sys
import threading
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(HERE))

import mcp_bridge  # noqa: E402


class Client:
    def __init__(self, base: str):
        self.base = base
        self.sid = None

    def post(self, payload: dict) -> tuple[int, dict]:
        headers = {"Content-Type": "application/json",
                   "MCP-Protocol-Version": mcp_bridge.PROTOCOL_LATEST}
        if self.sid:
            headers["Mcp-Session-Id"] = self.sid
        req = urllib.request.Request(self.base, data=json.dumps(payload).encode(),
                                     headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                hdrs = dict(r.headers)
                if hdrs.get("Mcp-Session-Id"):
                    self.sid = hdrs["Mcp-Session-Id"]
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read() or b"{}")

    def rpc(self, method: str, params: dict | None = None):
        code, body = self.post({"jsonrpc": "2.0", "id": 1, "method": method,
                                "params": params or {}})
        return body

    def call(self, name: str, args: dict | None = None):
        return self.post({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                          "params": {"name": name, "arguments": args or {}}})


def text_of(body: dict) -> str:
    try:
        return body["result"]["content"][0]["text"]
    except (KeyError, IndexError, TypeError):
        return json.dumps(body)[:400]


def is_json(s: str):
    try:
        return json.loads(s)
    except (ValueError, TypeError):
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="bodhapancadasika")
    ap.add_argument("--target", default="bod-p01-v01")
    ap.add_argument("--trace-work", default="tantrasara-a08")
    ap.add_argument("--trace-target", default="tsa08-p03")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    httpd = mcp_bridge.serve(0)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    c = Client(f"http://127.0.0.1:{port}/mcp")

    results: list[dict] = []

    def check(name: str, ok: bool, detail: str):
        results.append({"check": name, "pass": bool(ok), "detail": detail})

    # 1. initialize
    body = c.rpc("initialize", {})
    v = (body.get("result") or {}).get("protocolVersion")
    check("initialize", v == mcp_bridge.PROTOCOL_LATEST, f"version={v}")

    # 2. tools/list = read sheaf + public layers legend
    body = c.rpc("tools/list", {})
    res = body.get("result") or {}
    tools = res.get("tools") or []
    names = {t["name"] for t in tools}
    legend = {l.get("code"): l.get("name") for l in res.get("layers", [])}
    check("tools_list_is_read_sheaf", names <= mcp_bridge.READ_SHEAF and bool(names),
          f"{len(names)} tools, withheld={res.get('withheld')}")
    check("public_layer_legend", legend.get("T1") == "draft-translation"
          and legend.get("L0") == "literal-gloss"
          and legend.get("ARGMAP") == "argument-map",
          json.dumps(legend))

    # 3. openpatala resolve (identity)
    code, body = c.call("openpatala__resolve", {"work": a.work})
    txt = text_of(body)
    obj = is_json(txt) or {}
    check("identity_resolve", code == 200 and bool(obj),
          f"status={obj.get('status')} work={obj.get('work') or obj.get('openpatala_work_id')}")

    # 4. passage evidence (real Sanskrit + layers)
    code, body = c.call("scholar__passage_evidence",
                        {"work": a.work, "target": a.target})
    txt = text_of(body)
    obj = is_json(txt) or {}
    layers = obj.get("layers") or obj.get("data", {}).get("layers") or {}
    check("passage_evidence", code == 200 and ("error" not in body),
          f"{len(txt)} bytes, top keys={sorted(obj)[:6]}")

    # 5. formal trace (real Lean chain)
    code, body = c.call("formal__trace", {"work": a.trace_work,
                                          "target": a.trace_target})
    txt = text_of(body)
    obj = is_json(txt) or {}
    verdict = obj.get("verdict")
    theorems = obj.get("formal") or obj.get("theorems") or []
    check("formal_trace", code == 200 and verdict in ("COMPLETE", "PARTIAL"),
          f"verdict={verdict} theorems={len(theorems) if isinstance(theorems, list) else theorems}")

    # 6. formal gaps (coverage, honest denominator)
    code, body = c.call("formal__gaps", {})
    txt = text_of(body)
    obj = is_json(txt) or {}
    check("formal_gaps", code == 200 and bool(obj),
          f"keys={sorted(obj)[:6]}")

    # 7. write-sheaf refuses (no OAuth yet)
    code, body = c.call("video__vf_launch", {})
    check("write_refused", (body.get("error") or {}).get("code") == -32001,
          f"error={(body.get('error') or {}).get('message', '')[:60]}")

    httpd.shutdown()

    passed = sum(1 for r in results if r["pass"])
    total = len(results)
    if a.json:
        print(json.dumps({"passed": passed, "total": total,
                          "results": results}, indent=2))
    else:
        for r in results:
            print(("PASS " if r["pass"] else "FAIL ") + r["check"] + "  " + r["detail"])
        print(f"\n{passed}/{total} checks passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
