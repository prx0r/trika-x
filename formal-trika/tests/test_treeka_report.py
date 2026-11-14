#!/usr/bin/env python3
"""test_treeka_report.py — the gap report renders and stays in gap-list order.
"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
TOOL = HERE / "tools" / "treeka_report.py"
sys.path.insert(0, str(HERE / "tools"))


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

    def test_treeka_matches_evidence_refs(self):
        # Lead review R5: the next refresh must prove itself. Treeka's
        # formal_reference flags must equal the EVIDENCE registry refs —
        # 909 - referenced = unformalised, exactly.
        import treeka as treeka_mod
        ev = json.loads((HERE / "EVIDENCE.json").read_text(encoding="utf-8"))
        refs = treeka_mod.formal_references(ev)
        d = json.loads((HERE / "data" / "treeka.json").read_text(
            encoding="utf-8"))
        flagged = {f"{v.get('work')}:{k.split(':', 1)[1]}"
                   for k, v in d["works"].items() if v.get("formal_reference")}
        expected = {f"{w}:{loc}" for (w, loc) in refs}
        self.assertEqual(flagged, expected,
                         "treeka formal column disagrees with EVIDENCE refs")
        counts = d.get("counts", {})
        self.assertEqual(counts.get("no_formal_reference"),
                         counts.get("passages", 0) - len(expected))

    def test_work_filter(self):
        rc, out = run("--work", "phrdaya")
        self.assertEqual(rc, 0)
        self.assertIn("phrdaya | 5 (0 unargued)", out)

    def test_work_filter_scopes_every_summary_count(self):
        # External review P1: --work used to filter the table but print
        # corpus-wide gaps/counts/ambiguous in the summary lines.
        rc, out = run("--work", "phrdaya")
        self.assertEqual(rc, 0)
        lines = out.splitlines()
        header, summary = lines[0], lines[1]
        self.assertIn("'passages': 5", header)
        self.assertNotIn("909", header, "corpus count leaked into --work header")
        self.assertIn("unargued=0", summary)
        self.assertIn("essayless=5", summary)
        self.assertNotIn("578", summary, "corpus unargued leaked into --work summary")
        self.assertNotIn("ambiguous=12", summary, "corpus ambiguous leaked in")
        # and the full report still shows the real corpus numbers
        rc2, out2 = run()
        self.assertEqual(rc2, 0)
        self.assertIn("'passages': 909", out2.splitlines()[0])
        self.assertIn("unargued=578", out2.splitlines()[1])


if __name__ == "__main__":
    raise SystemExit(unittest.main())
