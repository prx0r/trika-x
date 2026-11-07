#!/usr/bin/env python3
"""federation_gateway.py — openpatala as the parent MCP for all children.

One stdio endpoint an agent connects to. Aggregates every child's tools/list
as <child>__<tool>, routes tools/call by prefix, FailOpen on dead children
(a down child is excluded; calls to it error — never fatal, never leaked).
Serves local identity tools itself (openpatala__*) plus a navigation guide
(federation__guide). No account tools, no ship/publish/signoff/submit tools
anywhere in the federated surface.

Children speak NDJSON JSON-RPC over stdio (initialize / tools/list /
tools/call) — true for the custom servers (scholar, bookfactory) and the
MCP-spec stdio transport (FastMCP/SDK servers). Config: FEDERATION_CONFIG
(JSON file, same shape as formal-trika/data/federation-children.json).

Usage:
  python3 formal-trika/tools/federation_gateway.py   # stdio MCP server
"""
from __future__ import annotations

import json
import os
import queue
import subprocess
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
DATA = HERE / "data" / "federation-children.json"
SOURCE_MAP = Path("/root/svread/source-map.json")

SYS_IDENT = "federation-gateway/1 trika-x"


class Child:
    def __init__(self, name: str, cmd: list, cwd: str):
        self.name = name
        self.cmd = cmd
        self.cwd = cwd
        self.proc = None
        self.inbox: "queue.Queue[str]" = queue.Queue()
        self.tools: list = []
        self.alive = False
        self.error = ""

    def start(self, timeout: float = 12.0) -> bool:
        try:
            self.proc = subprocess.Popen(
                self.cmd, cwd=self.cwd, stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                text=True, bufsize=1)
        except (OSError, FileNotFoundError) as e:
            self.error = f"spawn failed: {e}"
            return False
        threading.Thread(target=self._pump, daemon=True).start()
        if not self._call({"jsonrpc": "2.0", "id": "init",
                           "method": "initialize",
                           "params": {"protocolVersion": "2025-06-18",
                                      "capabilities": {},
                                      "clientInfo": {"name": SYS_IDENT,
                                                     "version": "1"}}},
                          timeout):
            self.error = "initialize timeout"
            self.stop()
            return False
        resp = self._call({"jsonrpc": "2.0", "id": "list",
                           "method": "tools/list", "params": {}},
                          timeout)
        if not resp or not isinstance(resp.get("result"), dict):
            self.error = "tools/list failed"
            self.stop()
            return False
        self.tools = resp["result"].get("tools", [])
        self.alive = True
        return True

    def _pump(self):
        try:
            for line in self.proc.stdout:
                self.inbox.put(line)
        except (ValueError, OSError):
            pass

    def _call(self, req: dict, timeout: float):
        if not self.proc or self.proc.poll() is not None:
            return None
        try:
            self.proc.stdin.write(json.dumps(req) + "\n")
            self.proc.stdin.flush()
        except (BrokenPipeError, OSError):
            return None
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                line = self.inbox.get(timeout=max(0.1, deadline - time.time()))
            except queue.Empty:
                return None
            try:
                msg = json.loads(line)
            except (ValueError, TypeError):
                continue
            if str(msg.get("id")) == str(req.get("id")):
                return msg
        return None

    def call_tool(self, tool: str, args: dict, timeout: float = 120.0):
        return self._call({"jsonrpc": "2.0", "id": f"c-{time.time_ns()}",
                           "method": "tools/call",
                           "params": {"name": tool, "arguments": args or {}}},
                          timeout)

    def stop(self):
        self.alive = False
        try:
            if self.proc and self.proc.poll() is None:
                self.proc.kill()
        except OSError:
            pass


def load_config() -> dict:
    path = Path(os.environ.get("FEDERATION_CONFIG", str(DATA)))
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"children": {}}


def local_identity() -> dict:
    """openpatala__* tools: file-backed (source-map.json), no DB required."""
    try:
        sm = json.loads(SOURCE_MAP.read_text(encoding="utf-8"))
        works = sm.get("works", {})
    except (OSError, ValueError):
        works = {}

    def resolve(a: dict) -> dict:
        wid = (a.get("work") or "").strip()
        if not wid:
            raise ValueError("work required")
        ent = works.get(wid)
        if ent is None:
            return {"work": wid, "status": "UNRESOLVED",
                    "note": "not in source-map; draft-only downstream"}
        return {"work": wid, "ledger": ent.get("ledger"),
                "ledger_sha256": ent.get("ledger_sha256"),
                "openpatala_work_key": ent.get("openpatala_work_key"),
                "openpatala_work_id": ent.get("openpatala_work_id"),
                "witness": ent.get("witness", "UNPINNED"),
                "status": ent.get("status", "CANDIDATE-TODO"),
                "note": "witnesses UNPINNED box-wide; UNRESOLVED = draft-only"}

    def coverage(_a: dict) -> dict:
        total = len(works)
        bridged = sum(1 for e in works.values()
                      if e.get("openpatala_work_id") not in (None, "UNRESOLVED", ""))
        return {"ledger_works": total, "bridged": bridged,
                "todo": total - bridged,
                "witnesses": "UNPINNED box-wide",
                "note": "source-map view; box DB (544 works / 909 passages) is the live store"}

    return {"resolve": resolve, "coverage": coverage}


GUIDE = """Navigate from openpatala (identity root) across the federation:

1. openpatala__resolve {work} — is this work known? ledger + witness status. UNRESOLVED = draft-only.
2. scholar__passage_evidence {work, target} — read the Sanskrit + layers (internal codes T1/L0/argmap/L2/C1/C2/L3/L4; public names in trika-x layer-names.json).
3. scholar__audit_draft / link_claims / pushback — check a draft before a human signs. Machine report, never verdict.
4. translation__status {work} (shastra) — registry state, proof, what the swarm is doing. Writes never push/signoff.
5. book__* (bookfactory) — draft previews only (quote_preview); stage/inspect are gated builds; NOTHING ships via MCP.
6. video__* (videofactory) — vf_gate/vf_triage to read state; vf_launch/vf_queue ship ONLY gated+approved renders (see videofactory#1: defaults should be explicit opt-in).
7. openpatala__coverage — how much of the corpus is bridged.

Laws: UNRESOLVED/draft-only inputs stay draft-only. No auto-sign, auto-publish, auto-ship. Human disposes; receipts are the trail.
"""


def main() -> int:
    cfg = load_config()
    children: dict[str, Child] = {}
    for name, spec in cfg.get("children", {}).items():
        cmd, cwd = spec.get("cmd"), spec.get("cwd", "/tmp")
        if not isinstance(cmd, list) or not cmd:
            continue
        children[name] = Child(name, cmd, cwd)
    for child in children.values():
        child.start()
    ident = local_identity()

    def tools_list() -> list:
        out = [
            {"name": "openpatala__resolve",
             "description": "Resolve a work to ledger + openpatala identity block (UNRESOLVED = draft-only).",
             "inputSchema": {"type": "object",
                             "properties": {"work": {"type": "string"}},
                             "required": ["work"]}},
            {"name": "openpatala__coverage",
             "description": "Source-map coverage: ledger works bridged vs todo (witnesses UNPINNED).",
             "inputSchema": {"type": "object", "properties": {}}},
            {"name": "federation__guide",
             "description": "How an agent navigates openpatala -> translation -> scholar -> factories.",
             "inputSchema": {"type": "object", "properties": {}}},
        ]
        for name, child in children.items():
            if not child.alive:
                continue
            for t in child.tools:
                tname = t.get("name", "")
                if not tname or "__" in tname:
                    continue
                out.append({"name": f"{name}__{tname}",
                            "description": f"[{name}] {t.get('description', '')}"[:400],
                            "inputSchema": t.get("inputSchema",
                                                 {"type": "object"})})
        seen, dedup = set(), []
        for t in out:
            if t["name"] not in seen:
                seen.add(t["name"])
                dedup.append(t)
        return dedup

    def out(obj: dict):
        sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")
        sys.stdout.flush()

    for line in sys.stdin:
        try:
            req = json.loads(line)
        except (ValueError, TypeError):
            continue
        if not isinstance(req, dict) or req.get("jsonrpc") != "2.0" or "id" not in req:
            continue
        mid, method, params = req["id"], req.get("method"), req.get("params") or {}
        try:
            if method == "initialize":
                out({"jsonrpc": "2.0", "id": mid,
                     "result": {"protocolVersion": "2025-06-18",
                                "capabilities": {"tools": {}},
                                "serverInfo": {"name": "openpatala-federation",
                                               "version": "1",
                                               "title": "Openpatala federated parent",
                                               "instructions": GUIDE}}})
            elif method == "ping":
                out({"jsonrpc": "2.0", "id": mid, "result": {}})
            elif method == "notifications/initialized":
                continue
            elif method == "tools/list":
                out({"jsonrpc": "2.0", "id": mid,
                     "result": {"tools": tools_list()}})
            elif method == "tools/call":
                name = params.get("name", "")
                args = params.get("arguments", {}) or {}
                if name == "federation__guide":
                    out({"jsonrpc": "2.0", "id": mid,
                         "result": {"content": [{"type": "text",
                                                 "text": GUIDE}]}})
                elif name == "openpatala__resolve":
                    try:
                        res = ident["resolve"](args)
                        out({"jsonrpc": "2.0", "id": mid,
                             "result": {"content": [{"type": "text",
                                                     "text": json.dumps(res)}]}})
                    except (ValueError, TypeError) as e:
                        out({"jsonrpc": "2.0", "id": mid, "isError": True,
                             "error": {"code": -32602, "message": str(e)}})
                elif name == "openpatala__coverage":
                    res = ident["coverage"](args)
                    out({"jsonrpc": "2.0", "id": mid,
                         "result": {"content": [{"type": "text",
                                                 "text": json.dumps(res)}]}})
                elif "__" in name:
                    child_name, tool = name.split("__", 1)
                    child = children.get(child_name)
                    if child is None or not child.alive:
                        out({"jsonrpc": "2.0", "id": mid, "isError": True,
                             "error": {"code": -32601,
                                       "message": "Unknown tool"}})
                    else:
                        resp = child.call_tool(tool, args)
                        if resp is None:
                            child.alive = False
                            out({"jsonrpc": "2.0", "id": mid, "isError": True,
                                 "error": {"code": -32603,
                                           "message": "target down"}})
                        elif "error" in resp:
                            out({"jsonrpc": "2.0", "id": mid, "isError": True,
                                 "error": {"code": -32603,
                                           "message": str(resp["error"])[:500]}})
                        else:
                            out({"jsonrpc": "2.0", "id": mid,
                                 "result": resp.get("result", {})})
                else:
                    out({"jsonrpc": "2.0", "id": mid, "isError": True,
                         "error": {"code": -32601, "message": "Unknown tool"}})
            else:
                out({"jsonrpc": "2.0", "id": mid, "isError": True,
                     "error": {"code": -32601, "message": "Unknown tool"}})
        except (BrokenPipeError, OSError):
            break
    for child in children.values():
        child.stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
