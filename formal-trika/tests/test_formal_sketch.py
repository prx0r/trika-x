#!/usr/bin/env python3
"""test_formal_sketch.py — the sketch gate proves itself on the DSP pilot.

Runs tools/formal_sketch_check.py for real: the pilot must pass every
mechanical gate, and a manifest-less directory must fail (fail-closed, fast
path — no Lean needed for the negative). The positive path compiles Lean +
runs four must_fail twins, so it is slow (~1-2 min); that is the point.
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKER = HERE.parent / "tools" / "formal_sketch_check.py"
PILOT = HERE.parent / "pilot" / "dsp-a18"


class TestFormalSketch(unittest.TestCase):
    def test_pilot_passes_all_gates(self):
        r = subprocess.run([sys.executable, str(CHECKER), str(PILOT)],
                           capture_output=True, text=True, timeout=600)
        self.assertEqual(r.returncode, 0,
                         f"pilot must pass every gate:\n{r.stdout}\n{r.stderr}")
        self.assertIn("ALL GATES PASS", r.stdout)

    def test_missing_manifest_fails_closed(self):
        with tempfile.TemporaryDirectory() as t:
            r = subprocess.run([sys.executable, str(CHECKER), t],
                               capture_output=True, text=True, timeout=60)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("FAIL", r.stdout)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
