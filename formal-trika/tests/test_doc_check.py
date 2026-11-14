#!/usr/bin/env python3
"""test_doc_check.py — the documentation gate is itself gated.

Hermetic fixtures (temp dirs, no network, no box): a well-formed tree must pass;
each failure mode must fail with a message naming it. If doc_check ever stops
biting, these tests go red before a stale number ships.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKER = HERE.parent / "tools" / "doc_check.py"


def run(root: Path):
    return subprocess.run([sys.executable, str(CHECKER), "--root", str(root)],
                          capture_output=True, text=True, timeout=120)


def build(root: Path, docs, registry, geometry=None):
    (root / "formal-trika" / "data").mkdir(parents=True)
    (root / "formal-trika" / "data" / "docs.json").write_text(
        json.dumps({"format": "trika-docs-registry/1", "docs": registry}), encoding="utf-8")
    (root / "formal-trika" / "data" / "docs-geometry.json").write_text(
        json.dumps(geometry or {"format": "trika-docs-geometry/1", "nodes": [], "edges": []}),
        encoding="utf-8")
    for name, text in docs.items():
        (root / name).write_text(text, encoding="utf-8")


GOOD = "# A doc — thing (2026-11-14)\n*Status: CANONICAL. real.*\n\nlive count is 7 tools.\n"
GOOD_REG = {"A.md": {"status": "CANONICAL", "note": "x", "claims": []}}
GOOD_DOCS = {"A.md": GOOD}


class TestDocCheck(unittest.TestCase):
    def test_wellformed_tree_passes(self):
        with tempfile.TemporaryDirectory() as t:
            r = Path(t)
            build(r, GOOD_DOCS, GOOD_REG)
            res = run(r)
            self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
            self.assertIn("docs: SHARP", res.stdout)

    def test_unregistered_doc_fails(self):
        with tempfile.TemporaryDirectory() as t:
            r = Path(t)
            build(r, {"A.md": GOOD, "Stray.md": "# Stray\n*Status: REFERENCE. x.*\n"}, GOOD_REG)
            res = run(r)
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("unregistered doc: Stray.md", res.stdout)

    def test_status_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as t:
            r = Path(t)
            bad = GOOD.replace("CANONICAL", "REFERENCE")
            build(r, {"A.md": bad}, GOOD_REG)
            res = run(r)
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("header status", res.stdout)

    def test_missing_date_fails_for_canonical(self):
        with tempfile.TemporaryDirectory() as t:
            r = Path(t)
            nodate = GOOD.replace(" (2026-11-14)", "")
            build(r, {"A.md": nodate}, {"A.md": {"status": "CANONICAL", "note": "x"}})
            res = run(r)
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("requires a date", res.stdout)

    def test_claim_number_drift_fails(self):
        with tempfile.TemporaryDirectory() as t:
            r = Path(t)
            reg = {"A.md": {"status": "CANONICAL", "note": "x", "claims": [
                {"id": "n", "pattern": r"(\d+) tools",
                 "source": {"argv": [sys.executable, "-c", "print(115)"], "pattern": r"(\d+)", "timeout": 30}}]}}
            build(r, {"A.md": GOOD}, reg)  # doc says 7, live says 115
            res = run(r)
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("DRIFT", res.stdout)

    def test_matching_claim_passes(self):
        with tempfile.TemporaryDirectory() as t:
            r = Path(t)
            reg = {"A.md": {"status": "CANONICAL", "note": "x", "claims": [
                {"id": "n", "pattern": r"(\d+) tools",
                 "source": {"argv": [sys.executable, "-c", "print(7)"], "pattern": r"(\d+)", "timeout": 30}}]}}
            build(r, {"A.md": GOOD}, reg)
            res = run(r)
            self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

    def test_dead_link_fails(self):
        with tempfile.TemporaryDirectory() as t:
            r = Path(t)
            doc = GOOD + "\nsee [gone](does-not-exist.md)\n"
            build(r, {"A.md": doc}, GOOD_REG)
            res = run(r)
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("dead link", res.stdout)

    def test_dated_line_suppresses_warn(self):
        with tempfile.TemporaryDirectory() as t:
            r = Path(t)
            doc = ("# A doc — thing (2026-11-14)\n*Status: CANONICAL. real.*\n\n"
                   "2026-11-08 baseline: 157 theorems (historical snapshot).\n")
            build(r, {"A.md": doc}, GOOD_REG)
            res = run(r)
            self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
            self.assertNotIn("157 theorems", res.stdout.split("WARN:")[-1] if "WARN:" in res.stdout else "")

    def test_geometry_missing_node_fails(self):
        with tempfile.TemporaryDirectory() as t:
            r = Path(t)
            geo = {"format": "trika-docs-geometry/1",
                   "nodes": [{"id": "formal-trika/data/nope.json", "kind": "data"}], "edges": []}
            build(r, GOOD_DOCS, GOOD_REG, geo)
            res = run(r)
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("geometry: data node missing", res.stdout)

    def test_geometry_known_edge_endpoint_fails(self):
        with tempfile.TemporaryDirectory() as t:
            r = Path(t)
            geo = {"format": "trika-docs-geometry/1",
                   "nodes": [{"id": "trika-x", "kind": "repo"}],
                   "edges": [{"from": "trika-x", "to": "nowhere-repo", "kind": "cites", "note": "x"}]}
            build(r, GOOD_DOCS, GOOD_REG, geo)
            res = run(r)
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("edge endpoint unknown", res.stdout)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
