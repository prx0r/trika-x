#!/usr/bin/env python3
"""mcp_bridge.py — HTTP (Streamable) front door for the trika-x federation gateway.

ChatGPT cannot reach stdio. This bridge speaks MCP Streamable HTTP on the
outside (POST /mcp JSON-RPC, GET /mcp SSE, DELETE /mcp session end) and the
existing stdio NDJSON gateway on the inside
(formal-trika/tools/federation_gateway.py). It invents nothing: tools,
descriptions and results pass through verbatim from the gateway.

Laws (EXTERNAL-STRATEGY section C, MCP-INTEGRATION section 2):
- Small read-only allowlist (the read sheaf). Everything else answers
  401/unauthorized — OAuth for the write sheaf is NOT built yet, and the
  bridge says so instead of faking acceptance.
- initialize + tools/list are public. No token in a URL, ever.
- FailOpen preserved: a dead child drops from tools/list, the parent stays.
- Limits: 60 s/call, 10 concurrent, 64 KB body. Long jobs are refused
  honestly (no job-id system yet) rather than half-implemented.
- SSE carries no fake notifications: endpoint + heartbeat only.

  python3 tools/mcp_bridge.py --port 8799        # serve on 127.0.0.1:8799
  python3 tools/mcp_bridge.py --port 0           # ephemeral; prints BRIDGE_PORT=<n>
  python3 tools/mcp_bridge.py --selftest          # local proof, exits 0/1
"""
from __future__ import annotations

import argparse
import json
import queue
import select
import subprocess
import sys
import threading
import time
import urllib.request
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
GATEWAY = REPO / "formal-trika" / "tools" / "federation_gateway.py"

PROTOCOL_LATEST = "2025-06-18"
PROTOCOL_LEGACY = "2024-11-05"
CALL_TIMEOUT = 60
MAX_CONCURRENT = 10
MAX_BODY = 64 * 1024

# Read sheaf: public without auth (MCP-INTEGRATION section 2). Everything else
# in the 112-tool catalog answers unauthorized until OAuth exists.
READ_SHEAF = {
    "openpatala__resolve", "openpatala__coverage",
    "openpatala_mcp__resolve", "openpatala_mcp__get_bundle",
    "openpatala_mcp__search", "openpatala_mcp__get_frontier",
    "openpatala_mcp__get_health",
    "scholar__passage_evidence", "scholar__search_texts",
    "scholar__wheel_harness", "scholar__wheel_level",
    "scholar__wheel_lookup", "scholar__wheel_verify",
    "scholar__wheel_certificate", "scholar__layers_index",
    "scholar__passage_layers", "scholar__translation_forks",
    "formal__trace", "formal__bridge", "formal__evidence",
    "formal__table", "formal__gaps", "formal__runs", "formal__axioms",
    "federation__guide",
}

BRIDGE_NOTE = (
    "svatantrya bridge: public read sheaf. Layers are named in plain words "
    "(draft-translation, literal-gloss, argument-map, reading-translation, "
    "essence, register-render, final-translation, song); machine keys "
    "T1/L0/ARGMAP/L2/C1/C2/L3/L4 still work. Source, review status and "
    "licence are the tool's own words (passed through verbatim). A dead "
    "child returns an explicit unavailable error; partial results never "
    "masquerade as complete. Writes need OAuth, which is not issued yet."
)


def layers_legend() -> list[dict]:
    try:
        data = json.loads((REPO / "formal-trika" / "data" /
                           "layer-names.json").read_text(encoding="utf-8"))
    except OSError:
        return []
    return [{"code": l.get("code"), "name": l.get("public"),
             "label": l.get("label"), "blurb": l.get("blurb")}
            for l in data.get("layers", [])]


class Gateway:
    """One gateway subprocess, shared by all HTTP requests in this process."""

    def __init__(self) -> None:
        self.proc = subprocess.Popen(
            [sys.executable, str(GATEWAY)], cwd=str(REPO),
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, bufsize=1)
        self._lock = threading.Lock()
        self._pending: dict[int | str, queue.Queue] = {}
        self._seq = 0
        self._sema = threading.Semaphore(MAX_CONCURRENT)
        threading.Thread(target=self._reader, daemon=True).start()

    def _reader(self) -> None:
        while True:
            line = self.proc.stdout.readline()
            if not line:
                return
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue
            mid = msg.get("id")
            with self._lock:
                q = self._pending.get(mid)
            if q is not None:
                q.put(msg)

    def call(self, method: str, params: dict, timeout: int = CALL_TIMEOUT) -> dict:
        with self._lock:
            self._seq += 1
            mid = self._seq
            q: queue.Queue = queue.Queue()
            self._pending[mid] = q
        req = {"jsonrpc": "2.0", "id": mid, "method": method,
               "params": params or {}}
        try:
            with self._lock:
                self.proc.stdin.write(json.dumps(req) + "\n")
                self.proc.stdin.flush()
            if not self._sema.acquire(timeout=timeout):
                return {"jsonrpc": "2.0", "id": mid,
                        "error": {"code": -32000,
                                  "message": "bridge busy: too many concurrent calls"}}
            try:
                return q.get(timeout=timeout)
            finally:
                self._sema.release()
        except queue.Empty:
            return {"jsonrpc": "2.0", "id": mid,
                    "error": {"code": -32000,
                              "message": f"gateway timeout after {timeout}s"}}
        finally:
            with self._lock:
                self._pending.pop(mid, None)


GATEWAY_SINGLETON: Gateway | None = None
SESSIONS: dict[str, dict] = {}
SESSIONS_LOCK = threading.Lock()


def gateway() -> Gateway:
    global GATEWAY_SINGLETON
    if GATEWAY_SINGLETON is None or GATEWAY_SINGLETON.proc.poll() is not None:
        GATEWAY_SINGLETON = Gateway()
    return GATEWAY_SINGLETON


def sheaf_filter(tools: list[dict]) -> list[dict]:
    out = []
    for t in tools:
        name = t.get("name", "")
        if name in READ_SHEAF:
            t = dict(t)
            t["description"] = t.get("description", "") + " [" + BRIDGE_NOTE + "]"
            t["annotations"] = {"sheaf": "read", "auth": "none"}
            out.append(t)
    return out


class Handler(BaseHTTPRequestHandler):
    server_version = "svatantrya-mcp-bridge/1"

    def log_message(self, *args):  # keep stdout for BRIDGE_PORT only
        pass

    def _version(self) -> str:
        v = self.headers.get("MCP-Protocol-Version", PROTOCOL_LATEST)
        return v if v in (PROTOCOL_LATEST, PROTOCOL_LEGACY) else PROTOCOL_LATEST

    def _send(self, code: int, obj: dict, version: str) -> None:
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("MCP-Protocol-Version", version)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        if self.path != "/mcp":
            return self._send(404, {"error": "only /mcp here"}, self._version())
        try:
            length = int(self.headers.get("Content-Length", 0))
        except ValueError:
            length = 0
        if length > MAX_BODY:
            return self._send(413, {"error": "body over 64 KB"}, self._version())
        try:
            req = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            return self._send(400, {"error": "bad JSON"}, self._version())
        version = self._version()
        method = req.get("method", "")
        mid = req.get("id")
        params = req.get("params") or {}

        if method == "initialize":
            sid = uuid.uuid4().hex
            with SESSIONS_LOCK:
                SESSIONS[sid] = {"created": time.time(), "version": version}
            resp = {"jsonrpc": "2.0", "id": mid,
                    "result": {"protocolVersion": version,
                               "capabilities": {"tools": {"listChanged": False}},
                               "serverInfo": {"name": "svatantrya-bridge",
                                              "version": "1"}}}
            body = json.dumps(resp).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("MCP-Protocol-Version", version)
            self.send_header("Mcp-Session-Id", sid)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            return self.wfile.write(body)

        if method in ("tools/list", "tools/list_tools"):
            gw = gateway().call("tools/list", {})
            if "error" in gw:
                return self._send(502, {"jsonrpc": "2.0", "id": mid,
                                        "error": gw["error"]}, version)
            tools = ((gw.get("result") or {}).get("tools")) or []
            served = sheaf_filter(tools)
            return self._send(200, {"jsonrpc": "2.0", "id": mid,
                                    "result": {"tools": served,
                                               "sheaf": "read",
                                               "layers": layers_legend(),
                                               "served": len(served),
                                               "withheld": len(tools) - len(served)}} , version)

        if method in ("tools/call", "tools/call_tool"):
            name = (params.get("name") or "")
            args = params.get("arguments") or {}
            if name not in READ_SHEAF:
                return self._send(200, {"jsonrpc": "2.0", "id": mid,
                                        "error": {
                                            "code": -32001,
                                            "message": ("unauthorized: '" + name +
                                                        "' is outside the public read sheaf; "
                                                        "write-sheaf OAuth is not issued yet")}},
                                  version)
            gw = gateway().call("tools/call",
                                {"name": name, "arguments": args})
            return self._send(200, gw if isinstance(gw, dict) else
                              {"jsonrpc": "2.0", "id": mid, "result": gw}, version)

        return self._send(200, {"jsonrpc": "2.0", "id": mid,
                                "error": {"code": -32601,
                                          "message": f"unknown method: {method}"}},
                           version)

    def do_GET(self) -> None:
        if self.path != "/mcp":
            return self._send(404, {"error": "only /mcp here"}, self._version())
        version = self._version()
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("MCP-Protocol-Version", version)
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        try:
            self.wfile.write(b"event: endpoint\ndata: /mcp\n\n")
            self.wfile.flush()
            for _ in range(3):
                time.sleep(10)
                self.wfile.write(b": heartbeat\n\n")
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_DELETE(self) -> None:
        if self.path != "/mcp":
            return self._send(404, {"error": "only /mcp here"}, self._version())
        sid = self.headers.get("Mcp-Session-Id", "")
        with SESSIONS_LOCK:
            SESSIONS.pop(sid, None)
        self.send_response(200 if sid else 400)
        self.send_header("MCP-Protocol-Version", self._version())
        self.end_headers()


def serve(port: int) -> ThreadingHTTPServer:
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    return httpd


def selftest() -> int:
    httpd = serve(0)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{port}/mcp"

    def post(payload: dict, headers: dict | None = None) -> tuple[int, dict, dict]:
        req = urllib.request.Request(
            base, data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json",
                     "MCP-Protocol-Version": PROTOCOL_LATEST,
                     **(headers or {})}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.status, json.loads(r.read()), dict(r.headers)
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read()), dict(e.headers)

    fails: list[str] = []

    # 1. initialize -> session + version
    code, body, hdrs = post({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                             "params": {}})
    sid = hdrs.get("Mcp-Session-Id", "")
    if code != 200 or not sid:
        fails.append(f"initialize: code={code} sid={bool(sid)}")
    if (body.get("result") or {}).get("protocolVersion") != PROTOCOL_LATEST:
        fails.append("initialize: version not echoed")

    # 2. legacy protocol still answers
    code, body, _ = post({"jsonrpc": "2.0", "id": 2, "method": "initialize",
                          "params": {}},
                         {"MCP-Protocol-Version": PROTOCOL_LEGACY})
    if code != 200 or (body.get("result") or {}).get("protocolVersion") != PROTOCOL_LEGACY:
        fails.append("legacy 2024-11-05 fallback broken")

    # 3. tools/list is sheaf-filtered and smaller than the full catalog
    code, body, _ = post({"jsonrpc": "2.0", "id": 3, "method": "tools/list",
                          "params": {}})
    tools = ((body.get("result") or {}).get("tools")) or []
    names = {t["name"] for t in tools}
    if not (names <= READ_SHEAF):
        fails.append(f"list leaks outside sheaf: {sorted(names - READ_SHEAF)[:5]}")
    if not names:
        fails.append("list returned empty sheaf")
    if not all((t.get("annotations") or {}).get("sheaf") == "read" for t in tools):
        fails.append("list tools missing sheaf annotation")
    legend = {(l.get("code")): l.get("name")
              for l in (body.get("result") or {}).get("layers", [])}
    if legend.get("T1") != "draft-translation" or \
            legend.get("ARGMAP") != "argument-map" or \
            legend.get("L0") != "literal-gloss":
        fails.append(f"layers legend missing public names: {legend}")

    # 4. read-sheaf call passes through verbatim
    code, body, _ = post({"jsonrpc": "2.0", "id": 4, "method": "tools/call",
                          "params": {"name": "openpatala__resolve",
                                     "arguments": {"work": "tantrasara"}}})
    if "error" in body and body.get("error", {}).get("code") == -32001:
        fails.append("read-sheaf call wrongly unauthorized")
    if code != 200:
        fails.append(f"read call code={code}")

    # 5. write-sheaf call refuses honestly (no OAuth yet)
    code, body, _ = post({"jsonrpc": "2.0", "id": 5, "method": "tools/call",
                          "params": {"name": "video__vf_launch", "arguments": {}}})
    if (body.get("error") or {}).get("code") != -32001:
        fails.append("write-sheaf call did not refuse with -32001")

    # 6. oversize body refused
    big = {"jsonrpc": "2.0", "id": 6, "method": "tools/list",
           "params": {"pad": "x" * (MAX_BODY + 1)}}
    code, _, _ = post(big)
    if code != 413:
        fails.append(f"oversize body code={code}, want 413")

    # 7. unknown method is a clean JSON-RPC error, not a crash
    code, body, _ = post({"jsonrpc": "2.0", "id": 7, "method": "nope", "params": {}})
    if (body.get("error") or {}).get("code") != -32601:
        fails.append("unknown method did not return -32601")

    # 8. DELETE ends the session
    req = urllib.request.Request(base, method="DELETE",
                                 headers={"Mcp-Session-Id": sid})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            if r.status != 200:
                fails.append(f"delete code={r.status}")
    except Exception as e:  # noqa: BLE001
        fails.append(f"delete raised {e}")

    httpd.shutdown()
    if fails:
        print("SELFTEST FAIL:")
        for f in fails:
            print(" -", f)
        return 1
    print(f"SELFTEST OK: sheaf={len(names)} tools, session+refusals+limits verified")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8799)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    httpd = serve(a.port)
    print(f"BRIDGE_PORT={httpd.server_address[1]}", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
