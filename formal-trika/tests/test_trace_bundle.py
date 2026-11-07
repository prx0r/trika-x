#!/usr/bin/env python3
"""test_trace_bundle.py — trika-trace/1 compiler + verifier, incl. negatives."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parent.parent / "tools" / "trace_bundle.py"
TW = Path(os.environ.get("TRANSLATION_WORK", "/root/translation-work"))
SV = Path(os.environ.get("SVREAD_CHECKOUT", "/root/svread"))
DSN = os.environ.get("OPENPATALA_DSN",
                     "postgresql://patala:patala@localhost:5432/openpatala")


def run(*args, env=None):
    e = dict(os.environ)
    if env:
        e.update(env)
    return subprocess.run([sys.executable, str(TOOL), *args],
                          capture_output=True, text=True, env=e, timeout=120)


class TestTraceBundle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = os.path.join(cls.tmp.name, "tsa08-p03.json")
        r = run("--work", "tantrasara-a08", "--target", "tsa08-p03",
                "--out", cls.out)
        assert r.returncode == 0, r.stderr
        with open(cls.out, encoding="utf-8") as f:
            cls.bundle = json.load(f)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_end_to_end_slice(self):
        b = self.bundle
        self.assertEqual(b["format"], "trika-trace/1")
        self.assertEqual(b["chunk"]["immutable_id"], "pt:pid:ts:a08:7f9e4b3307f2")
        self.assertTrue(b["source"]["bytes_present"])
        self.assertEqual(b["identity"]["status"], "BOUND")
        self.assertEqual(b["identity"]["rows"]["passage"]["work_id"],
                         "tantrasara-a08")
        self.assertEqual(b["layers"]["t1"]["status"], "BOUND-WHOLE-SONG")
        self.assertEqual(b["layers"]["c2"]["status"], "NOT-APPLICABLE")
        self.assertEqual(b["proofs"]["chunk_gate"]["deterministic_gate"], "BLOCKED")
        self.assertEqual(b["proofs"]["song_proof"]["status"], "PASS")
        self.assertGreaterEqual(len(b["formal"]["theorems"]), 1)
        self.assertEqual(b["formal"]["status"], "MODEL_CHECKED")
        self.assertEqual(b["essays"]["citing"], [])
        self.assertEqual(b["verdict"], "COMPLETE")
        self.assertTrue(any("whole-song" in c for c in b["caveats"]))
        self.assertTrue(any("BLOCKED" in c for c in b["caveats"]))

    def test_verify_clean(self):
        r = run("--verify", self.out)
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
        self.assertIn("VERIFIED", r.stdout)

    def test_verify_tampered_fails_and_names_hop(self):
        bad = os.path.join(self.tmp.name, "tampered.json")
        d = json.loads(json.dumps(self.bundle))
        d["layers"]["t1"]["sha256"] = "0" * 64
        with open(bad, "w", encoding="utf-8") as f:
            json.dump(d, f)
        r = run("--verify", bad)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("layers", (r.stdout + r.stderr))

    def test_unknown_chunk_fails_closed(self):
        r = run("--work", "tantrasara-a08", "--target", "tsa08-p99")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("exact matches", r.stderr)

    def test_unknown_work_fails_closed(self):
        r = run("--work", "no-such-work", "--target", "x-p01")
        self.assertNotEqual(r.returncode, 0)

    def test_flat_layout_binds_exact(self):
        out = os.path.join(self.tmp.name, "param-p04.json")
        r = run("--work", "paramarthasara", "--target", "param-p04",
                "--out", out)
        self.assertEqual(r.returncode, 0, r.stderr)
        with open(out, encoding="utf-8") as f:
            b = json.load(f)
        self.assertEqual(b["layers"]["t1"]["status"], "BOUND")
        self.assertEqual(b["layers"]["argmap"]["status"], "BOUND")
        self.assertGreaterEqual(len(b["formal"]["theorems"]), 1)
        r2 = run("--verify", out)
        self.assertEqual(r2.returncode, 0, r2.stderr + r2.stdout)

    def test_no_db_mode_marks_unknown(self):
        out = os.path.join(self.tmp.name, "nodb.json")
        r = run("--work", "tantrasara-a08", "--target", "tsa08-p03",
                "--out", out, "--no-db")
        self.assertEqual(r.returncode, 0, r.stderr)
        with open(out, encoding="utf-8") as f:
            b = json.load(f)
        self.assertEqual(b["identity"]["status"], "UNKNOWN")
        self.assertEqual(b["verdict"], "PARTIAL")
        self.assertIn("identity:db", b["gaps"])


if __name__ == "__main__":
    raise SystemExit(unittest.main())
