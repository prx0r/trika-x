#!/usr/bin/env python3
"""test_federation_gateway.py — parent multiplexes, prefixes, routes, FailOpens.

Live: all five children (scholar, bookfactory, translation, video,
openpatala_mcp) + local tools (openpatala__*, federation__guide,
formal__trace). FailOpen: one dead child is excluded, calls to it error
'Unknown tool'.
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

    def rpc(method, params=None, timeout=180):
        import select
        seq[0] += 1
        proc.stdin.write(json.dumps({"jsonrpc": "2.0", "id": seq[0],
                                     "method": method,
                                     "params": params or {}}) + "\n")
        proc.stdin.flush()
        while True:
            r, _, _ = select.select([proc.stdout], [], [], timeout)
            if not r:
                raise TimeoutError(f"no reply to {method}")
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
        "bookfactory": {"cmd": ["python3", "/root/bookfactory/bf_mcp/server.py"],
                        "cwd": "/root/bookfactory"},
        "translation": {"cmd": ["python3", "/root/translation-work/mcp_server.py",
                                "--serve"],
                        "cwd": "/root/translation-work"},
        "video": {"cmd": ["python3", "/root/videofactory/vf_mcp_server.py"],
                  "cwd": "/root/videofactory"},
        "openpatala_mcp": {"cmd": ["python3", "/root/openpatala/patala/mcp_server.py"],
                            "cwd": "/root/openpatala"},
        "deadchild": {"cmd": ["python3", "/nonexistent/child.py"],
                      "cwd": "/tmp"}}}


class TestFederationGateway(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
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
        self.assertIn("formal__trace", names)
        self.assertIn("scholar__passage_evidence", names)
        self.assertIn("bookfactory__factory_overview", names)
        self.assertIn("translation__status", names)
        self.assertTrue(any(n.startswith("video__") for n in names),
                        "video child live")
        self.assertTrue(any(n.startswith("openpatala_mcp__") for n in names),
                        "openpatala child live")
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

    def test_route_to_children(self):
        res = self.rpc("tools/call", {"name": "scholar__list_works",
                                      "arguments": {}})
        self.assertIn("tantrasara-a08", json.dumps(res["result"]))
        res = self.rpc("tools/call", {"name": "bookfactory__factory_overview",
                                      "arguments": {}})
        self.assertIn("bookfactory", json.dumps(res["result"]).lower())
        res = self.rpc("tools/call", {"name": "translation__status",
                                      "arguments": {"work": "tantrasara-a01"}})
        self.assertIn("tantrasara", json.dumps(res["result"]).lower())

    def test_formal_trace_end_to_end(self):
        res = self.rpc("tools/call", {"name": "formal__trace",
                                      "arguments": {"work": "tantrasara-a08",
                                                    "target": "tsa08-p03"}})
        self.assertNotIn("isError", res, str(res)[:300])
        body = json.loads(res["result"]["content"][0]["text"])
        self.assertEqual(body["verdict"], "COMPLETE")
        self.assertGreaterEqual(len(body["formal"]["theorems"]), 1)
        res = self.rpc("tools/call", {"name": "formal__trace",
                                      "arguments": {"work": "tantrasara-a08",
                                                    "target": "tsa08-p99"}})
        self.assertTrue(res.get("isError"), "unknown chunk must fail closed")

    def test_formal_tool_family(self):
        # every documented formal tool exists and answers
        cases = [
            ("formal__bridge", {"chunk": "chunk:tsa08-p03"}, "locator"),
            ("formal__evidence", {}, "counts"),
            ("formal__evidence", {"theorem": "Pramatr.lean :: seven"}, "kind"),
            ("formal__table", {}, "rows_total"),
            ("formal__gaps", {}, "coverage"),
            ("formal__runs", {}, "runs"),
            ("formal__axioms", {}, "report"),
        ]
        names = {t["name"] for t in self.rpc("tools/list")["result"]["tools"]}
        for name, _a, _k in cases:
            self.assertIn(name, names, f"{name} must be listed")
        for name, args, key in cases:
            res = self.rpc("tools/call", {"name": name, "arguments": args})
            self.assertNotIn("isError", res, f"{name}: {str(res)[:200]}")
            body = json.loads(res["result"]["content"][0]["text"])
            self.assertIn(key, body, f"{name} missing {key}")
        # bridge: witness always UNPINNED, never invented
        res = self.rpc("tools/call", {"name": "formal__bridge",
                                      "arguments": {"chunk": "chunk:tsa08-p03"}})
        body = json.loads(res["result"]["content"][0]["text"])
        self.assertEqual(body.get("witness_status"), "UNPINNED")
        # negative: bad chunk refs fail closed
        for bad in ({"chunk": "nope:xyz"}, {}):
            res = self.rpc("tools/call", {"name": "formal__bridge",
                                          "arguments": bad})
            self.assertTrue(res.get("isError"), f"must fail closed: {bad}")

    def test_tal_work_level_binding(self):
        res = self.rpc("tools/call", {"name": "formal__trace",
                                      "arguments": {"work": "tantraloka-a15",
                                                    "target": "tal-a15-p12"}},
                       timeout=180)
        self.assertNotIn("isError", res, str(res)[:200])
        body = json.loads(res["result"]["content"][0]["text"])
        self.assertEqual(body["verdict"], "PARTIAL", "TAL not gold yet")
        bound = {k for k, v in body["layers"].items()
                 if str(v.get("status", "")).startswith("BOUND")}
        self.assertIn("t1", bound, "TAL T1.md binds at work level")
        self.assertIn("l2", bound, "TAL L2.md binds at work level")
        self.assertTrue(any("layer:l0" == g for g in body["gaps"]),
                        "missing gold layers stay named gaps")

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
        self.assertIn("formal__trace", text)

    def test_guide_uses_real_prefixes(self):
        # Docs drift: the guide once said book__* while the surface is
        # bookfactory__*. Guard every family prefix that actually exists.
        init = self.rpc("initialize")
        text = init["result"]["serverInfo"]["instructions"]
        for fam in ("openpatala__", "openpatala_mcp__", "formal__",
                    "scholar__", "translation__", "bookfactory__", "video__"):
            self.assertIn(fam, text, f"guide must name {fam}*")
        self.assertNotIn("book__", text, "book__ is not a real prefix")

    def test_local_families_present(self):
        names = {t["name"] for t in self.rpc("tools/list")["result"]["tools"]}
        for name in ("openpatala__resolve", "openpatala__coverage",
                     "formal__trace", "formal__bridge", "formal__gaps",
                     "formal__axioms", "federation__guide"):
            self.assertIn(name, names)

    def test_catalog_matches_live_when_full(self):
        from collections import Counter
        catalog = Path(__file__).resolve().parent.parent / "data" / \
            "mcp-catalog.json"
        if not catalog.exists():
            self.skipTest("no catalog yet — run tools/mcp_catalog.py --write")
        names = [t["name"] for t in
                 self.rpc("tools/list")["result"]["tools"]]
        if len(names) < 100:
            self.skipTest("children not all live; catalog describes full "
                          "federation")
        recorded = json.loads(catalog.read_text())
        live = dict(sorted(Counter(n.split("__")[0] for n in names).items()))
        self.assertEqual(recorded["families"], live,
                         "catalog drift — regenerate tools/mcp_catalog.py")


if __name__ == "__main__":
    raise SystemExit(unittest.main())
