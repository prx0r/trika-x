#!/usr/bin/env python3
"""test_federation_gateway.py — parent multiplexes, prefixes, routes, FailOpens.

Live: scholar (real) + bookfactory (real, from origin/master worktree).
FailOpen: one dead child is excluded, calls to it error 'Unknown tool'.
Local: openpatala__resolve/coverage + federation__guide served by the parent.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GATEWAY = Path(__file__).resolve().parent.parent / "tools" / "federation_gateway.py"


def start_gateway(config: dict):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(config, f)
        path = f.name
    env = dict(os.environ, FEDERATION_CONFIG=path)
    proc = subprocess.Popen(
        [sys.executable, str(GATEWAY)], stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        text=True, bufsize=1, env=env)
    seq = [0]

    def rpc(method, params=None):
        seq[0] += 1
        proc.stdin.write(json.dumps({"jsonrpc": "2.0", "id": seq[0],
                                     "method": method,
                                     "params": params or {}}) + "\n")
        proc.stdin.flush()
        while True:
            line = proc.stdout.readline()
            if not line:
                raise RuntimeError("gateway closed stdout")
            try:
                msg = json.loads(line)
            except ValueError:
                continue
            if msg.get("id") == seq[0]:
                return msg
    return proc, rpc, path


def live_config():
    return {"children": {
        "scholar": {"cmd": ["python3", "/root/svread/mcp/scholar_server.py"],
                    "cwd": "/root/svread/mcp"},
        "bookfactory": {"cmd": ["python3", "/tmp/bf-mcp-test/bf_mcp/server.py"],
                        "cwd": "/tmp/bf-mcp-test"},
        "deadchild": {"cmd": ["python3", "/nonexistent/child.py"],
                      "cwd": "/tmp"}}}


class TestFederationGateway(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not Path("/tmp/bf-mcp-test/bf_mcp/server.py").exists():
            raise unittest.SkipTest("bf worktree not present")
        cls.proc, rpc_fn, cls.cfg = start_gateway(live_config())
        cls.rpc = staticmethod(rpc_fn)
        init = cls.rpc("initialize")
        assert init["result"]["serverInfo"]["name"] == "openpatala-federation"

    @classmethod
    def tearDownClass(cls):
        try:
            cls.proc.kill()
        except OSError:
            pass
        os.unlink(cls.cfg)

    def test_list_aggregates_with_prefixes(self):
        tools = self.rpc("tools/list")["result"]["tools"]
        names = {t["name"] for t in tools}
        self.assertIn("openpatala__resolve", names)
        self.assertIn("openpatala__coverage", names)
        self.assertIn("federation__guide", names)
        self.assertIn("scholar__passage_evidence", names)
        self.assertIn("bookfactory__factory_overview", names)
        self.assertFalse(any(n.startswith("deadchild__") for n in names),
                         "dead child must be FailOpen-excluded")

    def test_local_identity(self):
        res = self.rpc("tools/call", {"name": "openpatala__resolve",
                                      "arguments": {"work": "tantrasara-a08"}})
        body = json.loads(res["result"]["content"][0]["text"])
        self.assertEqual(body["ledger"], "tantrasara-a08/passages.jsonl")
        res = self.rpc("tools/call", {"name": "openpatala__resolve",
                                      "arguments": {"work": "no-such-work"}})
        body = json.loads(res["result"]["content"][0]["text"])
        self.assertEqual(body["status"], "UNRESOLVED")

    def test_route_to_scholar(self):
        res = self.rpc("tools/call", {"name": "scholar__list_works",
                                      "arguments": {}})
        body = json.loads(res["result"]["content"][0]["text"])
        self.assertIn("tantrasara-a08", json.dumps(body))

    def test_route_to_bookfactory(self):
        res = self.rpc("tools/call", {"name": "bookfactory__factory_overview",
                                      "arguments": {}})
        body = json.loads(res["result"]["content"][0]["text"])
        self.assertIn("bookfactory", json.dumps(body).lower())

    def test_unknown_and_dead_are_unknown_tool(self):
        res = self.rpc("tools/call", {"name": "deadchild__whatever",
                                      "arguments": {}})
        self.assertTrue(res.get("isError"))
        res = self.rpc("tools/call", {"name": "bogus__x", "arguments": {}})
        self.assertTrue(res.get("isError"))
        res = self.rpc("tools/call", {"name": "vf_launch", "arguments": {}})
        self.assertTrue(res.get("isError"), "unprefixed must not resolve")

    def test_guide(self):
        res = self.rpc("tools/call", {"name": "federation__guide",
                                      "arguments": {}})
        text = res["result"]["content"][0]["text"]
        self.assertIn("openpatala__resolve", text)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
