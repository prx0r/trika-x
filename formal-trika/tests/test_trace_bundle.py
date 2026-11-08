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


def _db_ok() -> bool:
    try:
        import psycopg2
        c = psycopg2.connect(DSN, connect_timeout=3)
        c.close()
        return True
    except Exception:  # noqa: BLE001 — no DB is a skip, never a failure
        return False


DB_OK = _db_ok()


def run(*args, env=None):
    e = dict(os.environ)
    if env:
        e.update(env)
    return subprocess.run([sys.executable, str(TOOL), *args],
                          capture_output=True, text=True, env=e, timeout=120)


@unittest.skipUnless(
    (TW / "tantrasara-a08" / "passages.jsonl").is_file(),
    "needs a translation-work checkout (real chunk to compile)")
class TestTraceBundle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = os.path.join(cls.tmp.name, "tsa08-p03.json")
        args = ["--work", "tantrasara-a08", "--target", "tsa08-p03",
                "--out", cls.out]
        if not DB_OK:
            args.append("--no-db")
        r = run(*args)
        assert r.returncode == 0, r.stderr
        with open(cls.out, encoding="utf-8") as f:
            cls.bundle = json.load(f)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    @unittest.skipUnless(DB_OK, "needs the openpatala box DB for identity binding")
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
        self.assertEqual(b["formal"]["status"], "REGISTERED")
        self.assertTrue(all(t.get("run_bound") is False
                            for t in b["formal"]["theorems"]))
        self.assertEqual(b["essays"]["citing"], [])
        self.assertEqual(b["verdict"], "COMPLETE")
        self.assertTrue(any("whole-song" in c for c in b["caveats"]))
        self.assertTrue(any("BLOCKED" in c for c in b["caveats"]))
        # PR #7: assurance dimensions are separate; COMPLETE + BLOCKED gate
        # coexist without contradiction.
        a = b["assurance"]
        self.assertEqual(a["trace_links_present"], "PASS")
        self.assertEqual(a["chunk_gate"], "BLOCKED")
        self.assertEqual(a["witness"], "UNPINNED")
        self.assertEqual(a["formal_run"], "UNBOUND")
        self.assertEqual(a["publication"], "NOT_AUTHORIZED")

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

    def test_verify_removed_gaps_fails(self):
        # PR #7: a bundle with its warnings deleted must fail, not verify.
        bad = os.path.join(self.tmp.name, "nogaps.json")
        d = json.loads(json.dumps(self.bundle))
        d["gaps"] = []
        d["caveats"] = []
        d["open_problems"] = []
        with open(bad, "w", encoding="utf-8") as f:
            json.dump(d, f)
        r = run("--verify", bad)
        self.assertNotEqual(r.returncode, 0)
        self.assertTrue("gaps" in (r.stdout + r.stderr)
                        or "caveats" in (r.stdout + r.stderr))

    def test_verify_missing_proof_field_fails(self):
        # PR #7: an absent `blocking` list is UNKNOWN, never an empty list.
        bad = os.path.join(self.tmp.name, "nofield.json")
        d = json.loads(json.dumps(self.bundle))
        del d["proofs"]["song_proof"]["blocking"]
        with open(bad, "w", encoding="utf-8") as f:
            json.dump(d, f)
        r = run("--verify", bad)
        self.assertNotEqual(r.returncode, 0)

    def test_resolve_formal_rejects_cross_work_locator(self):
        # PR #7: theorem join is (work, locator), never bare locator.
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent
                               / "tools"))
        import trace_bundle as tb
        ev = {"works": {
            "w1": {"ledger": "translation-work/w1/passages.jsonl",
                   "chunks": ["x-p01"]},
            "w2": {"ledger": "translation-work/w2/passages.jsonl",
                   "chunks": ["x-p01"]}},
            "entries": {"F.lean :: t": {"kind": "KEY", "chunks": [
                {"locator": "x-p01", "via": "L2",
                 "tier": "R", "status": "X"}]}}}
        thms, probs = tb.resolve_formal(ev, "w1", "x-p01")
        self.assertEqual(thms, [])
        self.assertTrue(any("ambiguous" in p for p in probs))
        thms, probs = tb.resolve_formal(ev, "w3", "x-p01")
        self.assertEqual(thms, [])
        good = {"works": {
            "w1": {"ledger": "translation-work/w1/passages.jsonl",
                   "chunks": ["x-p01"]}},
            "entries": {"F.lean :: t": {"kind": "KEY", "chunks": [
                {"locator": "x-p01", "via": "L2",
                 "tier": "R", "status": "X"}]}}}
        thms, probs = tb.resolve_formal(good, "w1", "x-p01")
        self.assertEqual(len(thms), 1)
        self.assertEqual(probs, [])

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
