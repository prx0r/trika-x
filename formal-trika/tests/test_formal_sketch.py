#!/usr/bin/env python3
"""test_formal_sketch.py — the sketch gate proves itself on every pilot present.

Runs tools/formal_sketch_check.py for real: each pilot dir under
formal-trika/pilot/ that has a sketch.json must pass every mechanical gate;
a manifest-less directory must fail (fail-closed, fast path — no Lean needed
for the negative). Positive paths compile Lean + run must_fail twins, so they
are slow by design. Pilots are the machine-proposed, assessor-gated pattern:
none of these is promoted by being present.
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKER = HERE.parent / "tools" / "formal_sketch_check.py"
PILOTS = sorted(p for p in (HERE.parent / "pilot").glob("*") if (p / "sketch.json").is_file())


class TestFormalSketch(unittest.TestCase):
    def test_each_pilot_passes_all_gates(self):
        if not PILOTS:
            self.skipTest("no pilot sketches present")
        for pilot in PILOTS:
            with self.subTest(pilot=pilot.name):
                r = subprocess.run([sys.executable, str(CHECKER), str(pilot)],
                                   capture_output=True, text=True, timeout=600)
                self.assertEqual(r.returncode, 0,
                                 f"pilot {pilot.name} must pass every gate:\n{r.stdout}\n{r.stderr}")
                self.assertIn("ALL GATES PASS", r.stdout)

    def test_missing_manifest_fails_closed(self):
        with tempfile.TemporaryDirectory() as t:
            r = subprocess.run([sys.executable, str(CHECKER), t],
                               capture_output=True, text=True, timeout=60)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("FAIL", r.stdout)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
