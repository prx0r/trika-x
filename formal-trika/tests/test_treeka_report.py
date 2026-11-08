#!/usr/bin/env python3
"""test_treeka_report.py — the gap report renders and stays in gap-list order.
"""
import subprocess
import sys
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parent.parent / "tools" / "treeka_report.py"


def run(*args):
    r = subprocess.run([sys.executable, str(TOOL), *args], capture_output=True,
                       text=True, timeout=120)
    return r.returncode, r.stdout


class TestTreekaReport(unittest.TestCase):
    def test_full_report(self):
        rc, out = run()
        self.assertEqual(rc, 0)
        self.assertIn("Treeka gap report", out)
        self.assertIn("formal_reference = registry association only", out)
        self.assertIn("AMBIGUOUS", out)

    def test_queue_order_starts_with_vbt(self):
        # phrdaya is fully referenced, so the published queue head is VBT.
        rc, out = run("--queue")
        self.assertEqual(rc, 0)
        first = [l for l in out.splitlines() if l.startswith("  ")][0]
        self.assertTrue(first.startswith("  vbt:"),
                        f"queue head must be VBT, got: {first}")

    def test_work_filter(self):
        rc, out = run("--work", "phrdaya")
        self.assertEqual(rc, 0)
        self.assertIn("phrdaya | 5 (0 unargued)", out)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
