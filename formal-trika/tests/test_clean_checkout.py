#!/usr/bin/env python3
"""test_clean_checkout.py — gated tools work without sibling checkouts.

PR #7 P1: several scripts assume /root/... paths, so a clean environment
cannot run them. The fixture suite builds synthetic translation-work trees
in tmp and asserts the trace compiler, verifier, and essay derivation run
and fail closed — no /root/translation-work, no DB, no svread needed.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
TOOLS = HERE / "tools"
TRACE = TOOLS / "trace_bundle.py"


def run(*args, timeout=180):
    return subprocess.run([sys.executable, str(TRACE), *args],
                          capture_output=True, text=True, timeout=timeout)


def make_tw(tmp: Path, work="w1", target="w1-p01"):
    (tmp / work).mkdir()
    (tmp / work / "passages.jsonl").write_text(json.dumps({
        "work_id": work, "order": 1, "locator": target,
        "verses": "1-2", "sanskrit": "abc deva",
        "immutable_id": "pt:pid:test:001"}) + "\n", encoding="utf-8")
    (tmp / work / "data").mkdir()
    return work, target


class TestTraceFixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_compile_verify_synthetic(self):
        work, target = make_tw(self.root)
        out = str(self.root / "t.json")
        r = run("--work", work, "--target", target, "--tw", str(self.root),
                "--sv", str(self.root), "--no-db", "--out", out)
        self.assertEqual(r.returncode, 0, r.stderr)
        b = json.loads(Path(out).read_text(encoding="utf-8"))
        self.assertEqual(b["chunk"]["immutable_id"], "pt:pid:test:001")
        self.assertTrue(b["source"]["bytes_present"])
        self.assertEqual(b["identity"]["status"], "UNKNOWN")
        self.assertEqual(b["verdict"], "PARTIAL")
        self.assertIn("identity:db", b["gaps"])
        # Deterministic recompile without DB must verify clean.
        r2 = run("--verify", out, "--tw", str(self.root),
                 "--sv", str(self.root))
        self.assertEqual(r2.returncode, 0, r2.stdout + r2.stderr)
        self.assertIn("VERIFIED", r2.stdout)
        bad = str(self.root / "bad.json")
        d = json.loads(json.dumps(b))
        d["gaps"] = []
        Path(bad).write_text(json.dumps(d), encoding="utf-8")
        r3 = run("--verify", bad, "--tw", str(self.root),
                 "--sv", str(self.root))
        self.assertNotEqual(r3.returncode, 0)

    def test_unknown_target_fails_closed(self):
        make_tw(self.root)
        r = run("--work", "w1", "--target", "nope",
                "--tw", str(self.root), "--no-db")
        self.assertNotEqual(r.returncode, 0)


class TestDeriveFixture(unittest.TestCase):
    def test_audit_uses_supplied_maps(self):
        sys.path.insert(0, str(TOOLS))
        import essay_derive as ed
        with tempfile.TemporaryDirectory() as td:
            ej = Path(td) / "e.essay.json"
            ej.write_text(json.dumps({
                "chunk": "w1:w1-p01",
                "claims": [{"id": "CLM-1", "text": "t",
                            "verse_id": "v", "tier": "R"}],
                "theorems": [], "openpatala": {
                    "openpatala_work_id": "w1",
                    "mapping_status": "CANDIDATE"}}),
                encoding="utf-8")
            traces = {("w1", "w1-p01"): {
                "verdict": "COMPLETE", "gaps": [], "work": "w1",
                "target": "w1-p01", "file": "traces/x.json",
                "immutable_id": "i", "sha256": "s", "theorems": []}}
            row = ed.audit_essay(ej, traces, {})
            # trace bundle file itself is absent here -> unreadable problem
            self.assertEqual(row["verdict"], "BROKEN")
            self.assertTrue(any("unreadable" in p or "bytes" in p
                                for p in row["problems"]))



    def test_out_of_range_verse_is_broken(self):
        sys.path.insert(0, str(TOOLS))
        import essay_derive as ed
        with tempfile.TemporaryDirectory() as td:
            ej = Path(td) / "e.essay.json"
            ej.write_text(json.dumps({
                "chunk": "phrdaya:phr-p05",
                "claims": [{"id": "CLM-1", "text": "t",
                            "verse_id": "phr-p05-v99", "tier": "R"}],
                "theorems": [], "openpatala": {
                    "openpatala_work_id": "phrdaya",
                    "mapping_status": "CANDIDATE"}}),
                encoding="utf-8")
            tr = ed.load_traces()
            row = ed.audit_essay(ej, tr, {})
            self.assertEqual(row["verdict"], "BROKEN")
            self.assertTrue(any("outside chunk" in p for p in row["problems"]))


if __name__ == "__main__":
    raise SystemExit(unittest.main())
